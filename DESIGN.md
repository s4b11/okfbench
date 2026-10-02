# design specification

This document describes the design implemented in the current source, including the homepage, all five project case studies, and the 404 page. Values are CSS values, not estimates from screenshots. Rem-based pixel equivalents assume the browser's default 16px root size; the site does not set a custom root font size.

## Source of truth

| Source | Responsibility |
| --- | --- |
| [assets/index.html](assets/index.html) | Homepage markup, inline custom CSS, animations, navigation, carousel, and interaction scripts |
| [assets/css/case.css](assets/css/case.css) | Shared project case-study design |
| [assets/projects/](assets/projects/) | AI interview, IVR agent, analytics dashboard, WMS, and Infant Guard pages; content and entrance delays |
| [assets/fonts/fonts.css](assets/fonts/fonts.css) | Self-hosted font faces and available weights |
| [tailwind.config.js](tailwind.config.js) | Matching palette and font utility configuration |
| [assets/css/tailwind.css](assets/css/tailwind.css) | Compiled Tailwind reset and utilities, loaded before custom styling |
| [assets/js/icons.js](assets/js/icons.js), [assets/icons/](assets/icons/) | Local outline interface icons and technology logos |
| [src/lib.rs](src/lib.rs) | Minimal themed 404 page |

## Visual language

The has an editorial, typography-led layout: parchment backgrounds, brown text, oversized tightly spaced display headings, small uppercase monospace labels, numbered sections, generous vertical spacing, and thin ruled grids. Cards, badges, buttons, and icon frames have square corners. Circular marks are reserved for status and brand dots; the favicon is a rounded square.

There is one fixed warm theme. The dark contact section and marquee invert the same paper/brown palette; there is no theme switch or separate dark-mode palette. Technology logos keep their own SVG brand colors. There are no photographic hero images, project thumbnails, or background gradients. Depth comes from subtle grain, translucent navigation, and a project-card hover shadow.

## Color theme

The homepage `:root`, case-study `:root`, and Tailwind configuration share these exact colors:

| CSS token / Tailwind name | Hex | Use |
| --- | --- | --- |
| `--paper` / `paper` | `#F3E4C9` | Main background; card surfaces; text on brown surfaces |
| `--bone` / `bone` | `#F8EFD9` | Stack and projects section backgrounds; hover surfaces; case badges, statistics, code, and repository callouts |
| `--ink` / `ink` | `#8A5F41` | Main text, display headings, filled buttons, marquee, contact section, footer |
| `--mute` / `mute` | `#A77F60` | Secondary copy, labels, button hover fill, subtle icon accents |
| `--line` / `line` | `#D8C49E` | Borders, dividers, grid seams, scrollbar thumb |
| `--clay` / `clay` | `#8A5F41` | Semantic accent: numbers, dots, arrows, progress, animated underlines |
| `--clay-tint` / `clay-tint` | `#EAD8BB` | Defined theme token; not used by the current custom page styles or markup |

`ink` and `clay` intentionally resolve to the same brown in the current implementation. Accent classes do not introduce a second hue.

Additional treatments:

- Text selection: `#8A5F41` background, `#F3E4C9` text.
- Scrolled homepage nav: `rgba(243,228,201,0.88)` with `blur(14px) saturate(1.2)`.
- Case-study nav: `rgba(243,228,201,0.9)` with `blur(12px) saturate(1.2)`.
- Project hover shadow: `0 22px 50px -20px rgba(138,95,65,0.22)`.
- Contact/footer use `rgba(243,228,201,alpha)`: `0.85` link text, `0.7` supporting text/back-to-top, `0.55` contact kicker, `0.4` labels/footer text, `0.2` icon borders, `0.15` grid divider, `0.12` link dividers, `0.1` footer divider. Primary headings and email use solid paper.

## Typography

All fonts are local WOFF2 files with `font-display: swap` and normal-style declarations. Display/body font faces declare a variable weight range of `100 900`; IBM Plex Mono has separate `400`, `500`, and `600` files. Italic headings/quotes request CSS italic, without a dedicated italic font file.

| Role | Family and fallback | Usage |
| --- | --- | --- |
| Display / `font-display` | `'Bricolage Grotesque', sans-serif` | Name, section headings, card titles, large numbers, quotes, email, mobile menu |
| Body / `font-sans` | `'Hanken Grotesk', system-ui, sans-serif` | Paragraphs, descriptions, metadata values, technology names |
| Mono / `font-mono` | `'IBM Plex Mono', monospace` | Navigation, kickers, dates, categories, badges, button labels, inline code |

The homepage preloads Bricolage, Hanken, and Plex Mono 400; case studies preload Bricolage and Hanken. Homepage hero animations wait for the display font readiness check, with a 1500ms safety timeout.

### Main type scale

| Element / selector | Size | Weight | Line height | Letter spacing |
| --- | --- | --- | --- | --- |
| Body | Browser base size | Default 400 | Homepage `1.5`; case studies `1.6` | Default |
| Hero name `.hero-name` | `clamp(4rem, 17vw, 15rem)` | 800 | `0.82` | `-0.04em` |
| Section heading `.h-sec` | `clamp(2.6rem, 7vw, 5.5rem)` | 700 | `0.94` | `-0.025em` |
| Section italic `.h-sec .it` | Inherits | 500 italic | Inherits | Inherits |
| Contact heading `.ct-head` | `clamp(2.6rem, 9vw, 7rem)` | 700; italic span 500 | `0.94` | `-0.03em` |
| Lead `.lead` | `clamp(1rem, 1.4vw, 1.15rem)` | Default | `1.7` | Default |
| Hero bio | `clamp(0.98rem, 1.3vw, 1.12rem)` | Default | `1.72` | Default |
| About paragraph | `clamp(1.05rem, 1.6vw, 1.3rem)` | 400 | `1.65` | Default |
| About quote | `clamp(1.3rem, 2.4vw, 1.9rem)` | 500 italic | `1.3` | `-0.01em` |
| Expertise title | `1.35rem` | 600 | `1.2` | `-0.02em` |
| Project title | `1.4rem` | 600 | `1.18` | `-0.02em` |
| Experience role / education degree | `clamp(1.5rem, 2.6vw, 2.1rem)` | 600 | Inherited | `-0.02em` |
| Hero statistic | `clamp(2rem, 4vw, 3.2rem)` | 700 | `1` | `-0.03em` |
| Contact email | `clamp(1.4rem, 4vw, 2.6rem)` | 500 | Inherited | `-0.02em` |
| `.mono` label | `0.7rem` | 500 | Inherited | `0.14em`, uppercase |
| `.kicker` | `0.72rem` | 600 | Inherited | `0.16em`, uppercase |
| Main button `.btn` | `0.74rem` | Default | Inherited | `0.12em`, uppercase |
| Project badge | `0.62rem` | Default | Inherited | `0.06em`, uppercase |

Typical secondary copy: expertise descriptions `0.93rem/1.7`, project descriptions `0.9rem/1.68`, experience bullets `0.97rem/1.65`, education note `0.95rem/1.65`. Technology names use `0.88rem`, weight 600; category labels use `0.56rem`, `0.12em` tracking. The shared lead width is `46ch`, hero bio `42ch`, education note `52ch`, and experience list `60ch`.

## Layout and spacing

- Global reset: border-box sizing, zero margins/padding on all elements and pseudo-elements. Links inherit color and remove text decoration. Body uses antialiased font smoothing and `overflow-x: hidden`.
- Both page families use `--gut: clamp(1.5rem, 6vw, 6rem)`, applied by `.wrap` to horizontal padding: 24px minimum and 96px maximum at the default root size.
- Homepage `.maxw`: `1320px`, centered. Case-study `.maxw`: `900px`, centered. These widths sit inside the outer gutters.
- Homepage content sections use `padding-block: clamp(5rem, 11vw, 9rem)`; contact retains that top padding and uses `clamp(3rem, 6vw, 5rem)` at the bottom.
- Section kickers generally have `1.4rem` bottom margin. Many section grids/lists begin `3.5rem` below the heading area. Grid gaps and padding are component-specific rather than a universal spacing token scale.
- Borders are predominantly `1px solid var(--line)`; buttons/nav CTA use selected `1.5px` borders. Quotes use a `3px` left accent border and `1.4rem` left padding.

### Homepage sections

The content order is Home → marquee → About (01) → Expertise (02) → Stack (03) → Experience (04) → Projects (05) → Education (06) → Contact (07) → footer.

| Area | Implemented structure |
| --- | --- |
| Hero | `min-height: 100svh`; vertically centered flex column; `6.5rem` top and `2rem` bottom padding. Top availability/location row wraps; thin horizontal rule; main grid `1.55fr 1fr`, gap `clamp(1.5rem, 4vw, 4rem)`, aligned to the bottom. Two masked name lines, typed role, bio, wrapping CTA row. |
| Hero stats | Three equal columns with top rule and vertical cell dividers; top margin `clamp(2rem, 5vw, 4rem)`. Large numbers above small mono labels. |
| Marquee | Full-width brown band with brown top/bottom borders and `1.1rem` vertical padding. Paper display text `clamp(1.1rem, 2vw, 1.7rem)`, muted star separators. |
| About | Grid `0.85fr 1.15fr`, gap `clamp(2rem, 6vw, 6rem)`. Heading sticky at `top: 110px`; narrative, italic quote, and two-column ruled metadata grid. |
| Expertise | Three-column grid with `1px` gaps, line-colored backing, and outer border. Paper cards padded `clamp(1.8rem, 3vw, 2.6rem)`; number, square icon frame, title, description. |
| Stack | Bone background and section borders. Auto-fill grid `repeat(auto-fill, minmax(146px, 1fr))`, gap `0.6rem`. Paper tiles centered vertically, padding `1.7rem 1rem 1.5rem`; logo `34px` square, name, category. |
| Experience | Ruled list, ink outer rules and line interior rules. Each row uses `0.7fr 2.3fr`, gap `clamp(1rem, 4vw, 4rem)`, padding `clamp(2rem, 4vw, 3.2rem) 0`. Date/year left; role/company/arrow bullets right; bracketed status absolutely positioned top-right. |
| Projects | Bone background and section borders. Heading/lead/arrows use a wrapping flex header. Five paper cards form a horizontal scroll-snap carousel, not a visible grid. |
| Education | Ink-bordered card, top margin `3.5rem`, grid `auto 1fr`; year column separated by a line border. Both cells padded `clamp(2rem, 4vw, 3rem)`. |
| Contact | Brown background; large paper heading and email. Ruled grid `1.5fr 1fr`, gap `3rem`, aligned bottom; social/contact rows left, availability copy and paper CTA right. |
| Footer | Brown background, `1.6rem` vertical gutter padding; wrapping flex row with copyright and back-to-top link, gap `0.8rem`. |

## Components and interaction states

### Navigation

Homepage navigation is fixed at the top, z-index `200`, with `1.1rem var(--gut)` padding. After `scrollY > 40`, `.solid` adds the translucent blurred paper background, bottom line border, and `0.85rem` vertical padding. The transition is `0.35s`.

Brand: Plex Mono 600, `0.82rem`, `0.08em` tracking; 8px round brown dot. Desktop links: `0.72rem` uppercase mono, muted, `1.5rem` list gap; brown `0.6rem` numerical prefixes. Hover/active links become ink. The Contact CTA uses a `1.5px` ink border, `0.5rem 0.95rem` padding, and inverts to ink/paper on hover.

Mobile navigation uses a three-line burger (`26px × 2px` lines, `5px` gaps) at z-index `210`. The first/third lines translate ±7px and rotate ±45°; the middle fades out. The full-screen paper overlay is z-index `190`, starts at `translateY(-100%)`, and slides down over `0.55s cubic-bezier(.7,0,.2,1)`. Menu links use display font 600, `clamp(1.7rem, 7vw, 3rem)`, numerical mono prefixes, and `0.3rem` vertical padding. Opening locks body scrolling; selecting a link closes the menu and restores it.

The desktop section rail is fixed `right: 2rem`, vertically centered, z-index `150`, with `0.85rem` gaps. Ticks widen from 18px to 34px on hover/active and turn brown; hidden labels fade in and move from `translateX(6px)` to zero. Active navigation/rail selection uses an IntersectionObserver threshold of `0.45`.

### Buttons and cards

- Main buttons: `0.95rem 1.5rem` padding, `0.55rem` icon gap. Filled brown/paper buttons hover to mute; outlined line/ink buttons hover to ink/paper. Paper contact buttons hover to mute/paper. Typical color transitions are `0.25s`, transform `0.15s`.
- Magnetic movement is applied only to elements with `data-mag` (View Work and Say Hello): cursor offset from center × `0.18` horizontally and × `0.28` vertically, reset on mouseleave.
- Expertise hover: paper → bone; 46px square icon frame becomes brown with paper glyph, over `0.3s`.
- Stack hover: bone surface, mute border, 2px bottom accent expands to full width over `0.45s cubic-bezier(.7,0,.2,1)`; logo scales `1.12` and moves up 2px.
- Project cards: `2.2rem` padding, line border. Hover lifts 4px, changes border to mute, adds the brown shadow, fills the 42px icon frame brown/paper, draws a 3px bottom accent, and shifts the link arrow `(3px, -3px)`.
- Project badges are square outlined mono labels, padding `0.28rem 0.6rem`; tag rows wrap with `0.4rem` gap. Source links use mute and become ink on hover.
- Email hover draws a 2px paper underline from the left over `0.4s cubic-bezier(.7,0,.2,1)`.
- Contact rows have 34px square icon frames; hover adds `0.6rem` left padding and inverts the frame to paper/ink over `0.25s`. Long email/contact values use `overflow-wrap: anywhere`.

### Project carousel

`.pj-track` is flex with `1.4rem` gap, horizontal overflow, `scroll-snap-type: x mandatory`, smooth scrolling, and `10px 2px 34px` padding. Its scrollbar is hidden. Each card is `flex: 0 0 clamp(280px, 80vw, 360px)` with start snap alignment; card width remains responsive at every viewport.

The previous/next buttons are 46px squares with 17px outline arrows and `0.6rem` gap. Hover inverts paper/ink. Disabled controls have opacity `0.28` and default cursor. Each click scrolls one measured card width plus the computed gap; disabled edge states update on scroll and resize with a 4px tolerance. Touch swipe uses native scrolling.

The CSS still defines `.pj-grid` with 360px minimum columns and a 600px single-column override, but current markup uses `.pj-carousel` / `.pj-track`. That grid rule does not describe the displayed projects layout. `.wipe` is likewise defined as an entrance helper but unused in current homepage markup.

## Texture, icons, and layering

- Grain is a fixed full-viewport, pointer-transparent SVG noise overlay: 180px tile, `feTurbulence` fractal noise, frequency `0.85`, three octaves, stitched tiles. Opacity `0.04`, blend mode `multiply`, z-index `9998`.
- Scroll progress is a fixed 2px brown bar at top-left, z-index `9999`; scroll position updates its width as a percentage of the scrollable document height.
- WebKit page scrollbar: 9px wide, paper track, line thumb with a 3px paper border. Homepage thumb hover becomes mute. The case stylesheet does not define that hover state.
- Interface glyphs are local Lucide-style SVG outlines: 24×24 viewBox, no fill, `currentColor`, 2px strokes, round caps/joins. Inline styles set individual glyphs to roughly 12–18px; carousel arrows are 17px. The local renderer replaces `data-lucide` placeholders and preserves their style/class.
- Technology tiles use local multicolor SVG logos fitted into 34×34px boxes with `object-fit: contain`.
- Favicon: 32×32 SVG, brown rectangle with radius 7 and a centered paper-colored Georgia `S`, font size 17.

## Motion

| Effect | Exact behavior |
| --- | --- |
| Scroll reveal `.rise` | Opacity 0 and `translateY(38px)` → visible/untransformed; `0.8s cubic-bezier(.16,.7,.2,1)` |
| Rule draw `.draw` | `scaleX(0)` → 1, left origin; `0.9s cubic-bezier(.7,0,.2,1)` |
| Hero masked lines | `translateY(110%)` → 0 inside overflow-hidden masks; `1s cubic-bezier(.16,.8,.2,1)`, forwards |
| Hero fade-up | Opacity 0 / `translateY(22px)` → visible/untransformed; `0.9s cubic-bezier(.16,.8,.2,1)`, forwards |
| Status pulse | `1.8s` infinite; at midpoint opacity `0.4`, scale `0.7`; endpoints opacity/scale 1 |
| Typing caret | 2px wide, height `1.05em`; `0.9s step-end` blink, invisible at 50% |
| Scroll hint line | 40×1px; `1.8s ease-in-out` infinite; scaleX `0.4` / opacity `0.4` → scaleX 1 / opacity 1 → repeat |
| Marquee | Two identical generated content sets; `34s linear infinite` translation to `-50%`; paused on hover |
| Counters | `1500ms`, requestAnimationFrame, cubic ease-out `1 - (1-p)^3`; starts once stats intersect at threshold `0.4` |
| Case entrance `.up` | Opacity 0 / `translateY(20px)` → visible/untransformed; `0.8s cubic-bezier(.16,.8,.2,1)`, forwards |

Homepage hero delays: availability `0.1s`, location `0.2s`, name lines `0.25s` / `0.4s`, role `0.6s`, bio `0.7s`, CTAs `0.8s`, stats `0.95s`, scroll hint `1.1s`. The rule has a `0.2s` transition delay. Below-fold `.rise` / `.draw` elements reveal once with threshold `0.12` and root margin `0px 0px -50px 0px`; individual inline transition delays stagger content.

Role typing cycles Software Developer, AI Agent Engineer, Voice AI Developer, Backend & Microservices, and R&D Engineer. Timing: 85ms to type a character, 40ms to delete, 2000ms at the full phrase, 320ms before the next role.

`html` has smooth scroll behavior. With `prefers-reduced-motion: reduce`, both custom stylesheets disable CSS animations and transitions globally and restore visibility/transforms for their entrance helpers. The homepage's JavaScript typing, counters, magnetic movement, smooth carousel calls, and CSS smooth scroll are not disabled by that media query; it is a CSS motion reduction rather than a complete static interaction mode.

## Responsiveness

Both page families include `width=device-width, initial-scale=1.0` viewport metadata and `-webkit-text-size-adjust: 100%`. Fluid `clamp()` typography, gutters, spacing, wrapping flex rows, and intrinsic grid sizing operate between breakpoints. The max-width queries below are inclusive and cumulative.

### Homepage breakpoints

| Query | Applied changes |
| --- | --- |
| `max-width: 1100px` | Hide the right section rail. |
| `max-width: 1024px` | Hide desktop nav links and Contact CTA; show burger. |
| `max-width: 900px` | Hero becomes one column, aligned start, with no hero-sub bottom padding. About becomes one column with `2.5rem` gap and static heading. Expertise becomes two columns. Experience becomes one column with `1rem` gap and hidden status tags. Education stacks, replacing the year right border with a bottom border. Contact becomes one column with `2.5rem` gap. |
| `max-width: 600px` | Hero stats become two columns; second cell loses right border, first two gain bottom borders. About metadata and expertise become one column. Stack becomes exactly two columns. Project card padding reduces to `1.7rem`; the carousel remains horizontal. The unused `.pj-grid` becomes one column. |

The third hero statistic wraps onto a second row at 600px and below; it is not stretched into a full-width row by a separate rule. Stack tiles above 600px use auto-fill columns, so their count depends on available width. Hero buttons, heading/lead groups, badges, and footer wrap naturally rather than using dedicated phone breakpoints. There is no separate portrait/landscape query or safe-area inset rule.

### Case-study breakpoints and intrinsic grids

| Rule | Behavior |
| --- | --- |
| Metadata default | `repeat(auto-fit, minmax(150px, 1fr))`; zero gap, top/bottom rules, right dividers |
| Highlight cards default | `repeat(auto-fit, minmax(230px, 1fr))`; 1px line-backed seams |
| Outcome statistics default | `repeat(auto-fit, minmax(170px, 1fr))`; 1px line-backed seams |
| `max-width: 600px` | Metadata becomes two equal columns; every even cell loses its right border. |
| `max-width: 560px` | Statistics become one column; repository callout stacks vertically, aligns left, reduces padding to `1.3rem`, and gives its button full width with centered content. |

## Case-study page design

All five project pages use the same shared case stylesheet and theme. Their layout is a narrower reading column with a sticky top bar, project hero, summary, badges, metadata strip, numbered/labelled narrative sections, and a ruled contact footer. Metrics/highlight cards and repository callouts appear where supplied by each page's content.

- Sticky `.cs-nav`: top 0, z-index 100, `1rem var(--gut)` padding, blurred translucent paper, line bottom border. The All Projects link uses uppercase `0.72rem` mono, `0.1em` tracking; hover changes mute → ink and shifts the arrow left 3px over `0.25s`.
- Hero padding: `clamp(3.5rem, 9vw, 7rem)` top and `clamp(2rem, 5vw, 3.5rem)` bottom. Title: display 700, `clamp(2.4rem, 6vw, 4.4rem)`, line-height `0.98`, tracking `-0.03em`; italic spans use 500/clay.
- Summary: `clamp(1.05rem, 1.8vw, 1.35rem)`, line-height `1.6`, mute, max-width `60ch`, top margin `1.5rem`. Badges wrap with `0.45rem` gap and `1.75rem` top margin; `0.64rem` mono, bone fill, line border, `0.3rem 0.65rem` padding.
- Metadata top margin `2.5rem`; cells padded `1.1rem 1.2rem 1.1rem 0`; keys `0.6rem` uppercase mono / `0.12em`, values `0.92rem` / 500.
- Body bottom padding `clamp(4rem, 9vw, 7rem)`; section top padding `clamp(2.5rem, 5vw, 3.5rem)`. Eyebrow: `0.68rem` mono / 600 / `0.14em`. H2: display 600, `clamp(1.5rem, 3vw, 2.1rem)`, line-height `1.15`, tracking `-0.02em`.
- Body paragraphs: `1.02rem/1.75`, mute, `68ch` maximum, `1.1rem` bottom margin. Strong text becomes ink/600. Lists are unbulleted with brown mono arrow pseudo-elements; `1rem/1.7`, `1.6rem` left inset, `0.6rem` item spacing. Quotes use display 500 italic, `clamp(1.3rem, 2.6vw, 1.9rem)`, line-height `1.35`, max-width `60ch`.
- Highlight cards: paper, `1.6rem` padding; mono eyebrow `0.64rem`, display title `1.1rem/1.2` at 600, body `0.9rem/1.6`.
- Outcome statistics: bone cells, `1.45rem 1.25rem` padding; display number 700, `clamp(1.5rem, 3.2vw, 2.1rem)`, line-height `1.05`, tracking `-0.03em`; muted italic comparison value at 500; label `0.6rem` mono / `0.12em`.
- Inline code: Plex Mono, `0.85em`, bone background, line border, `0.1em 0.36em` padding.
- Repository callout: wrapping flex row, bone fill, line border, `1.5rem 1.6rem` padding, `1.2rem` gap. Name wraps anywhere. Outlined button uses `0.72rem` uppercase mono, `0.8rem 1.25rem` padding; hover inverts ink/paper and lifts 2px.
- Footer stays on paper. Padding `clamp(3rem, 6vw, 4.5rem)` top / `clamp(2rem, 4vw, 3rem)` bottom. Display invitation: 700, `clamp(1.8rem, 4vw, 3rem)`, line-height `1.05`, tracking `-0.02em`, 500 italic accent. CTA: brown/paper, `0.85rem 1.5rem` padding, `0.74rem` mono; hover lifts 2px and arrow shifts `(3px, -3px)`. Its hover fill changes ink → clay, which are currently the same color.
- Hero entrance stagger: kicker starts immediately; title `0.05s`, summary `0.1s`, badges `0.15s`, metadata `0.2s`. Body content is not wired to the homepage scroll-reveal observer. Each case page includes the scroll-progress script.

## Existing accessibility and fallback behavior

The implementation uses semantic headings, sections/articles, links, real buttons, alt text on technology images, and accessible labels for menu and carousel controls. The decorative marquee and side rail are marked `aria-hidden="true"`. Reduced-motion CSS exists as described above. Custom hover styles are specified, but there is no matching custom focus-visible design or scripted menu focus management / `aria-expanded` state. These are implementation facts, not claims of an accessibility audit.

The 404 response uses paper `#F3E4C9`, ink `#8A5F41`, and system-ui sans-serif rather than the hosted font stack. Full-height body uses `display: grid; place-items: center`; its inner content is text-centered. The `404` heading is `5rem`, weight 800, followed by a short message and brown Return home link. It has viewport metadata but no grain, navigation, progress bar, or entrance animation.

## Maintaining design fidelity

Keep the tokens synchronized across homepage `:root`, `case.css`, and `tailwind.config.js`. Preserve the three font roles, large display/small mono contrast, square components, thin borders, warm alternating surfaces, and the listed breakpoint behavior when extending the design. Inspect the served markup before treating older helper styles as active patterns.

Custom design changes belong in homepage inline CSS or `case.css`. Rebuild `assets/css/tailwind.css` from `tailwind-input.css` and the theme configuration when changing utility usage. Fonts, icons, and styles are locally served; source assets are embedded into the Rust WASM service at build time. This document records source-defined behavior; it does not claim a browser-rendered visual or accessibility audit.
