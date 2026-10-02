# Security and Quality Expectations

Sensitive infant data needs authentication, role checks, validation, and HTTPS on public deployments. Staff should review permissions when people change roles.

Quality checks in a serious build would cover unit tests for risk scoring and nutrition drafting, integration tests for alert delivery after plan approval, and basic usability passes on each role's home view. This repository focuses on retrieval comparison, so those tests are described as expectations rather than a full suite.
