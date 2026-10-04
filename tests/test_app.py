import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient
from openai import APIConnectionError

TEMP = tempfile.TemporaryDirectory()
os.environ['DATABASE_URL'] = 'sqlite:///' + (Path(TEMP.name) / 'test.db').as_posix()
os.environ['LLM_STUB'] = 'true'

from app.config import Settings
from app.main import app
from app.db import engine
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.okf import OKFRetriever
from app.services.llm import LLMResult, generate_answer


def tearDownModule():
    engine.dispose()
    TEMP.cleanup()


class RetrievalTests(unittest.TestCase):
    def test_bundle_links_and_source_limits(self):
        okf, bm25 = OKFRetriever(), BM25Retriever()
        self.assertEqual(len(okf.concepts), 24)
        self.assertEqual(sum(len(c.links) for c in okf.concepts.values()), 98)
        for concept in okf.concepts.values():
            self.assertTrue(set(concept.links) <= okf.concepts.keys())
        question = 'How does an approved nutrition plan reach parents?'
        hits = okf.retrieve(question)
        self.assertEqual(hits[0].id, 'nutrition-plan-module')
        self.assertIn(('alerts-notifications', 1), [(s.id, s.hops) for s in hits])
        for retriever in [okf, bm25, HybridRetriever(okf, bm25)]:
            sources = retriever.retrieve(question, top_k=5)
            self.assertEqual(len(sources), 5)
            context = retriever.context_block(sources)
            for source in sources:
                self.assertIn('[' + source.id + ']', context)
            self.assertEqual(retriever.retrieve('zzzxxyyqq'), [])
        hybrid = HybridRetriever(okf, bm25).retrieve(question)
        self.assertEqual([s.kind for s in hybrid[:2]], ['concept', 'doc'])

    def test_local_links_depth_cycles_and_reserved_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'nested').mkdir()
            (root / 'nested/start.md').write_text('---\ntype: Concept\ntitle: Quasar\n---\n[Next](../next.md)\n[Web](https://example.com/no.md)\n[Missing](/missing.md)')
            (root / 'next.md').write_text('---\ntype: Concept\n---\n[End](/end.md)\n[Start](nested/start.md#heading)')
            (root / 'end.md').write_text('---\ntype: Concept\n---\n[Next](next.md)')
            (root / 'index.md').write_text('# Index')
            retriever = OKFRetriever(root)
            with patch('app.retrieval.okf.get_settings', return_value=Settings(_env_file=None, top_k=5, okf_hop_depth=2)):
                sources = retriever.retrieve('quasar')
            self.assertEqual([(s.id, s.hops) for s in sources], [('nested/start', 0), ('next', 1), ('end', 2)])
            (root / 'invalid.md').write_text('---\ntitle: Missing type\n---\nBody')
            with self.assertRaisesRegex(ValueError, 'needs a type'):
                OKFRetriever(root)

    def test_bm25_ranking(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'a.md').write_text('# Orchard\napple apple pear')
            (root / 'b.md').write_text('# Workshop\nmetal wood tools')
            retriever = BM25Retriever(root)
            self.assertEqual([s.id for s in retriever.retrieve('apple')], ['a'])


class ProviderTests(unittest.TestCase):
    def test_provider_model_defaults(self):
        for keys, expected in [({'groq_api_key': 'test', 'openai_api_key': ''}, 'openai/gpt-oss-20b'), ({'groq_api_key': '', 'openai_api_key': 'test'}, 'gpt-4o-mini')]:
            settings = Settings(_env_file=None, llm_stub=False, llm_model='', **keys)
            with patch('app.services.llm.get_settings', return_value=settings), patch('app.services.llm._chat_openai_compatible', return_value=LLMResult('answer')) as request:
                generate_answer('question', 'context', 'okf')
                self.assertEqual(request.call_args.kwargs['model'], expected)

    def test_no_sources_skips_provider(self):
        with patch('app.services.llm._chat_openai_compatible') as request:
            result = generate_answer('zzzxxyyqq', '', 'okf')
            self.assertEqual(result.provider, 'none')
            request.assert_not_called()

    def test_render_database_url(self):
        for scheme in ['postgres://', 'postgresql://']:
            settings = Settings(_env_file=None, database_url=scheme + 'user:pass@host/db')
            self.assertEqual(settings.database_url, 'postgresql+psycopg://user:pass@host/db')


class APITests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)

    def test_modes_and_session_history(self):
        ids = []
        for mode in ['okf', 'bm25', 'hybrid']:
            response = self.client.post('/api/chat', json={'question': 'nutrition approval', 'mode': mode})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            ids.append(data['session_id'])
            self.assertEqual(data['mode'], mode)
            self.assertLessEqual(data['metrics']['source_count'], 5)
            self.assertEqual(data['metrics']['prompt_tokens'], 0)
            self.assertTrue(all(not Path(s['path']).is_absolute() for s in data['sources']))
        runs = self.client.get('/api/runs', params={'session_id': ids[0]}).json()['runs']
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]['session_id'], ids[0])
        self.assertEqual(self.client.get('/api/runs').status_code, 422)

    def test_validation_and_provider_error(self):
        self.assertEqual(self.client.post('/api/chat', json={'question': '   '}).status_code, 400)
        self.assertEqual(self.client.post('/api/chat', json={'question': 'test', 'session_id': 'bad'}).status_code, 422)
        self.assertEqual(self.client.post('/api/chat', json={'question': 'test', 'mode': 'vector'}).status_code, 422)
        self.assertEqual(self.client.post('/api/reload-knowledge').status_code, 404)
        error = APIConnectionError(request=httpx.Request('POST', 'https://example.com'))
        with patch('app.routers.chat.generate_answer', side_effect=error):
            response = self.client.post('/api/chat', json={'question': 'nutrition'})
        self.assertEqual(response.status_code, 502)
        self.assertIn('unavailable', response.json()['detail'])


if __name__ == '__main__':
    unittest.main()
