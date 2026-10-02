# IoTides Recruiter Console: Design Specification

This document describes the design used in `iotides-console.html`, plus one sidebar variant, the **grain gradient**, implemented in `iotides-console-gradient-sidebar.html` (see 2.9). Every value listed here is taken directly from those files' CSS and JavaScript. If they ever disagree with this document, the HTML files are the source of truth and this document should be updated.

The two files are identical except for the variant's page title and one added CSS block (the grain gradient and its sidebar text colors). Everything outside section 2.9 and the notes marked "grain gradient" applies to both.

Scope: the four hiring pages (Jobs, Candidates, Schedules, Reports), the app shell (sidebar, mobile bar), and all shared components, overlays and interaction rules. Overview, Users, Plan & usage, Profile and User manual exist only as placeholder routes.

### Revision history

| Revision | Changes |
|---|---|
| 7 | Focus on a text field is now one thin line: the field's own 1px border turns `--brand`. The extra 2px outline and the 3px `--brand-soft` halo around inputs are gone (buttons and links keep the keyboard outline). Insight notes size to their sentence and share rows instead of one full-width bar each. Dialog bodies scroll inside the card, so the scrollbar stays within it. Transcripts use chat bubbles with a corner tail and the time in the bubble (4.24). |
| 6 | The page header is now a full-width bar with a 1px `--line` rule along its bottom edge, separating it from the page content. The rule runs the full width of the content area, from the sidebar's edge to the window's edge. |
| 5 | KPI cards are now read-only summary boxes showing workspace totals (no hover, selection or filtering). Status filtering moved to a "Status" chip in the toolbar, like the original screens' Filter dropdown. Spacing increased: header → KPI cards 14 → 24px, KPI cards → toolbar 14 → 20px. |
| 4 | Replaced the status switcher with four KPI cards (label, tinted icon, count) that also act as the status filter; "Invites sent" became the fourth card on Schedules and Reports. Header compacted to a single 36px row (title 22 → 18px, description on the same line, 34px actions) and moved up (page top padding 20 → 12px), aligned with the sidebar logo. |
| 3 | Added the grain-gradient sidebar surface (variant file): a blurred brand-blue glow on a cool grey base with a film-grain overlay, sidebar-scoped text tokens (`--side-*`) that keep 4.5:1 contrast over the glow, and a matching dark version. |
| 2 | Shorter page header (title 28 → 22px, less padding). Smaller status rail (segments 46 → 34px). Sorting moved into the column headers with up/down indicators; the desktop sort chip was removed (kept on mobile, where headers are hidden). Pagination rebuilt: rows per page (10/25/50), first/previous/next/last, windowed page numbers, "Page X of Y" on mobile. Removed the connector line between the Hiring nav items. Collapsed sidebar no longer shows a separate expand button; hovering the logo swaps it for the expand button. Added a `?demo=N` testing aid. |
| 1 | Initial redesign. |

---

## 1. Design principles

**Calm by default.** The interface is neutral and quiet, in the spirit of ChatGPT and Claude style product UIs. Color is used for meaning: status tones on badges and KPI icons, and brand blue for active filters, the active nav icon and primary actions.

**Brand lives in the sidebar, not the workspace (grain gradient).** In the variant, the sidebar carries the brand as a soft, grainy blue glow. The content area stays plain white so data remains the focus. The glow uses the same hue as the brand blue on buttons and links, so the page has one blue, not two.

**Summary first, filters in one place.** Each page opens with four KPI boxes that summarize the whole workspace at a glance. They are read-only. Every way to narrow the table (status, job, date, search) lives in the toolbar directly above it, so there's one place to look for filters.

**Sort where the data is.** Each sortable column header is its own sort control with a visible up/down indicator, so the order of the table is always explained by the table itself. A separate sort dropdown exists only on mobile, where the headers are hidden.

**Compact chrome, roomy data.** The page header is a single short row and the KPI boxes are compact, so the table starts high on the screen. Spacing is spent inside the table, not above it.

**Tactile, rounded, not glassy.** Controls are pill-shaped, surfaces use soft radii, and buttons compress slightly when pressed with a spring easing. There is no backdrop blur, see-through panel or glassmorphism; the grain gradient is an opaque painted surface. This is an interpretation of a modern Android skin feel (the brief referenced Realme UI); it is not based on any official Realme design specification.

**Apply instantly, explain emptiness.** Filters apply as the user types or picks; there is no Apply button. Every empty result explains why it is empty and offers the one action that fixes it.

**Sentence case everywhere.** No all-caps labels, no tracked-out eyebrows, no decorative dividers.

---

## 2. Foundations

### 2.1 Color

The theme is controlled by `data-theme="light" | "dark"` on `<html>`. On load it follows `prefers-color-scheme`; the sun/moon button toggles it for the session (not persisted).

#### Brand

| Token | Light | Dark | Use |
|---|---|---|---|
| `--brand` | `#2563EB` | `#3D7BF7` | Primary buttons, active icons, selected counts, focus ring, checked checkboxes |
| `--brand-hover` | `#1F57D6` | `#5A8FF8` | Primary button hover |
| `--brand-soft` | `#EEF3FE` | `rgba(61,123,247,.15)` | Active filter chip, selected row, bulk bar, current page, soft button |
| `--brand-line` | `#CFDCFB` | `rgba(61,123,247,.4)` | Borders on brand-soft surfaces |
| `--on-brand` | `#FFFFFF` | `#FFFFFF` | Text/icons on `--brand` |

#### Surfaces

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#FFFFFF` | `#1A1B1E` | Page background, mobile bar |
| `--rail` | `#F6F7F9` | `#141517` | Sidebar background |
| `--surface` | `#FFFFFF` | `#1A1B1E` | Table panel, inputs, chips, secondary buttons |
| `--pop` | `#FFFFFF` | `#222327` | Menus, popovers, dialogs, sheets |
| `--sunk` | `#F1F2F5` | `#232428` | Mini chips, empty-state icon tile, read-only fields, link box |
| `--hover` | `#F5F6F8` | `#212226` | Hover on content-area controls and table rows |
| `--press` | `#EBEDF0` | `#2A2B30` | Hover on sidebar items (darker, because the rail is already tinted); dark-mode menu item hover |
| `--thumb` | `#FFFFFF` | `#34353B` | Raised pill: active sidebar item |

#### Text and lines

| Token | Light | Dark | Use |
|---|---|---|---|
| `--text` | `#16181D` | `#ECEDEF` | Primary text, names, values |
| `--text-2` | `#555B66` | `#A9ADB6` | Secondary text, descriptions, default icon color, table cell text |
| `--text-3` | `#8A909B` | `#747985` | Tertiary: table headers, page description, meta, placeholders |
| `--line` | `#E8EAEE` | `#2A2C31` | Panel borders, row dividers, sidebar border |
| `--line-2` | `#D9DCE2` | `#393B41` | Input, chip and rows-per-page borders, checkbox border |

#### Semantic tones

Each tone has a strong color and a soft background. Components never read these directly; they use a tone class (`.t-ok`, `.t-warn`, `.t-info`, `.t-violet`, `.t-teal`, `.t-rose`, `.t-amber`, `.t-danger`, `.t-neutral`, and `.t-blue` as an alias of info), which sets `--tone` and `--tone-soft`. `.t-amber` maps to the warn pair.

| Tone | Light strong | Light soft | Dark strong | Dark soft |
|---|---|---|---|---|
| ok | `#11824B` | `#E8F6EF` | `#4CC38A` | `rgba(76,195,138,.13)` |
| warn | `#A45A00` | `#FDF3E2` | `#E5A845` | `rgba(229,168,69,.13)` |
| info | `#2563EB` | `#EEF3FE` | `#6E9DF9` | `rgba(110,157,249,.14)` |
| violet | `#6A41D8` | `#F2EDFD` | `#A98BFA` | `rgba(169,139,250,.14)` |
| teal | `#0E7C86` | `#E3F4F5` | `#4FC8D1` | `rgba(79,200,209,.13)` |
| rose | `#B8386A` | `#FCEBF2` | `#F07FAA` | `rgba(240,127,170,.13)` |
| danger | `#C42F3B` | `#FDEDEF` | `#F0707A` | `rgba(240,112,122,.14)` |
| neutral | `#5B616C` | `#F1F2F4` | `#A9ADB6` | `#26272B` |

#### Inverse (tooltip and toast)

| Token | Light | Dark |
|---|---|---|
| `--toast-bg` | `#1C1E23` | `#ECEDEF` |
| `--toast-ink` | `#FFFFFF` | `#16181D` |
| `--toast-ico` | `#6EE7A8` | `#11824B` |

The inverse pair flips with the theme, so toasts and tooltips always contrast with the page.

### 2.2 Typography

**Family:** `"Geist", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`, loaded from Google Fonts at weights 400, 500, 600 and 700. If Google Fonts is unreachable, the system UI font is used. One family is used for everything; there is no display or monospace face.

**Base:** 14px / 1.5, weight 400, antialiased.

| Role | Size | Weight | Line height | Letter spacing | Color |
|---|---|---|---|---|---|
| Page title | 18px (17px ≤720px) | 600 | 1.3 | −0.018em | `--text` |
| KPI count | 26px (22px ≤720px) | 600 | 1.05 | −0.025em | `--text` |
| Dialog / sheet title | 18px | 600 | inherit | −0.015em | `--text` |
| Brand name | 16.5px | 600 | inherit | −0.015em | `--text` |
| Empty-state title | 15.5px | 600 | inherit | 0 | `--text` |
| Page description | 13px | 400 | 1.4 | 0 | `--text-3`, max 62ch, on the same line as the title |
| Person name | 14.5px | 500 | 1.35 | 0 | `--text` |
| Body / buttons / menu items | 14px | 500 (controls), 400 (text) | 1.5 | 0 | varies |
| KPI label | 13px | 500 | inherit | 0 | `--text-2` |
| Chips, small buttons, header primary button | 13.5px | 500 | inherit | 0 | varies |
| Emails, form labels, footer text, rows-per-page button | 13px | 400–500 | inherit | 0 | varies |
| Table headers (incl. sort buttons), badges, nav counts, time under dates | 12.5px | 500 (400 for time) | inherit | 0 | `--text-3`; sorted header `--text` |
| Tags, mini chips, source line | 12px | 500 (400 for source) | inherit | 0 | varies |
| Keyboard hint | 11.5px | 500 | 1 | 0 | `--text-3` |

**Numbers:** every count, table number, pager and footer uses `font-variant-numeric: tabular-nums` so values don't shift width.

**Casing:** sentence case for all labels, headers, buttons and menu items. Table headers are not uppercased. Person names are shown in title case even if the source data is uppercase.

### 2.3 Spacing and layout

There is no formal spacing scale; values cluster around a 2/4px rhythm. The ones that define the layout:

| Item | Value |
|---|---|
| Page max width | 1280px, centered |
| Header bar padding (desktop) | 12px top and bottom, 40px sides (content stays within the same 1280px column as the page) |
| Header bar padding (≤960px) | 14px top and bottom, 16px sides |
| Page padding (desktop) | 24px top (below the header rule), 40px sides, 56px bottom |
| Page padding (≤960px) | 20px top (18px ≤720px), 16px sides, 48px bottom |
| Title → description | 12px, same row, baseline-aligned (wraps below on narrow screens) |
| Page header height | 60px bar (36px row + 12px padding top and bottom), vertically centered with the sidebar logo row |
| Header rule → KPI boxes | 24px (20px ≤960px, 18px ≤720px) |
| Between KPI boxes | 12px (8px ≤720px) |
| KPI boxes → toolbar | 20px |
| Toolbar → table panel | 14px |
| Toolbar gaps | 10px between search and tools; 8px between chips |
| Header actions gap | 2px (+8px extra before the primary button) |
| Table cell padding | 14px vertical, 16px horizontal; first column 22px left |
| Sidebar padding | 12px; 20px between nav groups; 2px between items |
| Dialog body | 16px 24px 6px, 16px between fields |
| Sheet key/value rows | 13px vertical, 128px label column |

### 2.4 Radius

Radius follows hierarchy: the larger or more "container" the element, the larger the radius. Anything the user presses as a single control is a full pill.

| Radius | Elements |
|---|---|
| 999px (pill) | Buttons, filter chips, search field, status badges, job status select, icon buttons (`lg` size), rows-per-page button, toasts, date presets, search clear button |
| 24px | Dialog card |
| 20px | Table panel |
| 17px | Empty-state icon tile (52px) |
| 16px | KPI boxes (14px ≤720px) |
| 16px | Menus and popovers |
| 14px | Account button |
| 13px | Avatar (38px); 11px for the small 34px avatar |
| 12px | Sidebar items, collapsed-sidebar expand button, form inputs, date inputs, read-only field, link box |
| 10px | KPI icon tile (30px; 9px at 26px on mobile), icon buttons (34px), menu items, pager buttons, logo mark (on a 32-unit viewBox) |
| 8px | Tooltip, mini chips, sortable column header buttons |
| 7px | Tags |
| 6px | Checkbox, keyboard hint |

### 2.5 Elevation

Borders do most of the separation work. Shadows are used only for things that are raised or floating.

| Token | Light | Dark | Used on |
|---|---|---|---|
| `--shadow-raise` | `0 1px 2px rgba(17,24,39,.06), 0 1px 6px -1px rgba(17,24,39,.09)` | `0 1px 2px rgba(0,0,0,.45), 0 0 0 1px rgba(255,255,255,.04)` | Active sidebar item |
| `--shadow-pop` | `0 18px 44px -14px rgba(17,24,39,.24), 0 2px 6px rgba(17,24,39,.06)` | `0 18px 44px -14px rgba(0,0,0,.65), 0 0 0 1px rgba(255,255,255,.06)` | Menus, popovers, dialogs, toasts, open mobile drawer |
| `--scrim` | `rgba(17,20,26,.34)` | `rgba(0,0,0,.55)` | Dialog/sheet backdrop, mobile drawer scrim |

In dark mode, shadows add a 1px white hairline at 4–6% opacity, because dark shadows alone don't separate dark surfaces.

**Stacking order:** mobile bar 30, drawer scrim 35, sidebar 40, menus/popovers 80, tooltip 100, toasts 120. Dialogs and sheets use the native `<dialog>` top layer. The tooltip and toast container are `popover="manual"` elements that are re-shown whenever they update, so they always sit above an open dialog or sheet.

### 2.6 Motion

| Token | Value | Character |
|---|---|---|
| `--ease` | `cubic-bezier(.2,.8,.2,1)` | Quick out, soft landing. Used for color, background, fades, slides. |
| `--spring` | `cubic-bezier(.32,1.3,.52,1)` | Slight overshoot. Used for anything that moves or scales in response to a press. |

| Motion | Duration | Easing | Trigger |
|---|---|---|---|
| Press compression: buttons, chips `scale(.97)`, icon buttons `scale(.9)`, status select `scale(.96)` | 250ms | spring | `:active` |
| Hover color/background | 150ms | ease | Hover |
| Table row hover | 120ms | ease | Hover |
| Sidebar collapse (grid column width) | 280ms | ease | Collapse / expand button |
| Logo ↔ expand button swap (opacity) | 150ms | ease | Hovering the logo while collapsed |
| Sort indicator opacity (40% → 80% on hover) | 150ms | ease | Hovering a sortable header |
| Mobile drawer slide | 340ms | ease | Menu button |
| Menu / popover in (fade, −4px, scale .98) | 180ms | ease | Open |
| Dialog in (fade, +10px, scale .97) / out | 340ms spring / 160ms ease | — | Open / close |
| Sheet in (from +32px, opacity .4) / out | 360ms / 180ms | ease | Open / close |
| Toast in (from +14px, scale .95) / out | 450ms spring / 200ms ease | — | Show / after 2.8s |
| Tooltip fade + 3px rise | 120ms | ease | Hover / keyboard focus |
| Backdrop fade | 200ms | ease | Dialog/sheet open |

There is no motion on page load and no hover animation on cards or rows beyond a background tint. Everything that moves does so because the user did something. `prefers-reduced-motion: reduce` collapses all animations and transitions to ~0ms.

### 2.7 Iconography

Icons are an inline SVG sprite (`<symbol id="i-*">`) on a 24×24 grid, stroke only: `stroke-width: 1.75`, round caps and joins, `fill: none`, `stroke: currentColor`. Most paths follow the Lucide icon style; a few (contact card, sparkle, calendar-clock, file-chart) are custom drawings in the same style. Icons are always `aria-hidden`; the control carries the label.

**Sizes:** 18px default; 17px inside buttons, search and menu items; 16px in chips, KPI icon tiles, pager and select arrows; 15px in "with-icon" table cells and search clear; 14px in badges, status select, sort indicators (stroke 2) and the rows-per-page chevron; 13px in tags, mini chips and ok-notes; 22px in empty-state tiles. Primary buttons use stroke 2.1; badges and tags use 2.

| Icon | Meaning in the UI |
|---|---|
| `grid` | Overview |
| `briefcase` | Jobs; job filter chip |
| `filter` | Status filter chip |
| `contact` | Candidates |
| `cal-clock` | Schedules; "See schedules" |
| `file-chart` | Reports; "View report" |
| `users` | Users |
| `card` | Plan & usage |
| `user` | Profile |
| `user-check` | "Profile ready" stage |
| `help` | User manual |
| `bell` | Notifications |
| `logout` | Log out |
| `search` | Search field; empty results |
| `plus` | Primary "add/create" buttons |
| `chev-down` | Dropdowns, rows-per-page button |
| `chev-left` / `chev-right` | Previous / next page |
| `chev-first` / `chev-last` | First / last page |
| `chevs` | Unsorted sortable column; account switcher |
| `arrow-up` / `arrow-down` | Column sorted ascending / descending |
| `calendar` | Date range chip |
| `cal-plus` | Schedule interview |
| `sort` | Mobile sort chip; the page's default order in the sort menu |
| `pencil` | Edit |
| `eye` | View details / profile |
| `upload` | Publish job |
| `download` | Export CSV |
| `ext` | View schedule |
| `copy` | Copy interview link |
| `mail` | Send invite; "Email linked" |
| `send` | Invites sent KPI box |
| `x-circle` | Cancel schedule; "Cancelled" status |
| `x` | Close; clear search |
| `check-circle` | "Completed" status; success toast |
| `check` | Menu selection tick; "Published", "Invite sent", "Included" |
| `clock` | "Scheduled" status; interview window |
| `video` | Recording |
| `sparkle` | Analysis |
| `sun` / `moon` | Theme toggle |
| `menu` | Open mobile navigation |
| `panel` | Collapse sidebar (expanded); expand sidebar (shown in place of the logo on hover when collapsed) |
| `pin` | Location |
| `info` | Informational toast |
| `layers` | Placeholder pages |
| `link` | Defined in the sprite, currently unused |

### 2.8 Logo mark

A 32×32 app-icon squircle: a `#2563EB` rounded rect (rx 10), a white almond eye shape, a teal iris `#14B8A6` (r 4.3) and a deep blue pupil `#0B3B8C` (r 1.9). Displayed at 30×30 next to the "IoTides" wordmark. These colors are hardcoded and do not change in dark mode.

---

### 2.9 Grain gradient (sidebar surface)

Implemented in `iotides-console-gradient-sidebar.html`. It replaces the flat `--rail` sidebar background with a blurred brand-blue glow and a fine film grain. It started from a supplied reference gradient (grey base, blue glow, pale corner, grain), which was turned vertical to suit a tall sidebar and then shifted from sky blue to the brand blue.

#### Composition

Read top to bottom, the sidebar goes: quiet grey behind the logo, the strongest blue glow behind the Hiring menu, a soft haze fading down the left side, neutral grey through the middle, and a lighter blue glow in the bottom-right corner behind the account button. The glow is centered slightly right of middle (58%), so the menu labels on the left sit on the lighter edge of it.

```
┌──────────────┐
│ ░░ grey ░░░░ │  logo
│   ▒▒▓▓▓▓▓▒   │  ← main glow (29% down)
│  ▒▒▓▓██▓▓▒▒  │  Hiring menu
│ ▒▒▒▓▓▓▓▒▒    │  ← side haze (39% down, left)
│ ░░ grey ░░░░ │  Workspace menu, empty space
│ ░░░░░░░░░░░░ │
│        ▒▒▓▓▓ │  ← corner glow (bottom right)
└──────────────┘  account
```

#### Layers, light theme

Painted as CSS background layers on `.side`, top layer first. Radial sizes and positions are percentages of the sidebar box, so the same gradient stretches to the collapsed rail (72px) and the mobile drawer (284px).

| # | Layer | Definition |
|---|---|---|
| 1 | Grain | `var(--grain)`, 200×200px tile, repeated, `background-blend-mode: overlay` (see Grain below) |
| 2 | Main glow | `radial-gradient(ellipse 150% 23% at 58% 29%, …)` with stops `rgba(37,99,235,.5)` 0%, `rgba(52,112,238,.42)` 28%, `rgba(96,140,242,.26)` 55%, `rgba(160,184,238,.1)` 80%, transparent 100% |
| 3 | Side haze | `radial-gradient(ellipse 120% 34% at 30% 39%, …)` with stops `rgba(80,130,242,.25)` 0%, `rgba(110,152,242,.12)` 55%, transparent 100% |
| 4 | Corner glow | `radial-gradient(ellipse 95% 28% at 96% 100%, …)` with stops `rgba(96,150,244,.55)` 0%, `rgba(130,170,242,.36)` 40%, `rgba(180,200,238,.13)` 72%, transparent 100% |
| 5 | Base | `linear-gradient(to bottom, #E8E9EC 0%, #E5E7EB 45%, #E3E6EB 65%, #DCE2EE 100%)` over `background-color: #E8E9EC` |

All blue stops are in the brand hue family: the main glow's center is `#2563EB` itself at 50% strength. On screen, the brightest point of the glow renders at about `#7DA0EC`.

#### Layers, dark theme

Same geometry and layer order, on a near-black base, using the dark-theme brand blue `#3D7BF7` (`rgb(61,123,247)`).

| # | Layer | Stops |
|---|---|---|
| 1 | Grain | Same tile, 0.5 opacity |
| 2 | Main glow | `rgba(61,123,247,.5)` 0%, `rgba(50,110,235,.34)` 30%, `rgba(40,90,200,.14)` 60%, transparent 100% |
| 3 | Side haze | `rgba(61,123,247,.18)` 0%, transparent 100% |
| 4 | Corner glow | `rgba(70,130,245,.34)` 0%, `rgba(55,105,220,.15)` 45%, transparent 100% |
| 5 | Base | `linear-gradient(to bottom, #15171C 0%, #13151A 60%, #12151B 100%)` over `#121419` |

The brightest point renders at about `#294B8F`.

#### Grain

The grain is an inline SVG image (no external file), tiled every 200px and blended over the gradient with `overlay`, which lightens light areas and darkens dark ones without shifting their average color.

| Property | Value |
|---|---|
| Noise | `feTurbulence type="fractalNoise" baseFrequency="1.15" numOctaves="3" stitchTiles="stitch"` (fine, even grain that tiles without seams) |
| Color | Converted to grey with `feColorMatrix` (each channel = 0.33 R + 0.33 G + 0.33 B, alpha forced to 1) |
| Contrast | `feComponentTransfer`, linear `slope 1.6`, `intercept −0.3` on R, G and B (boosts contrast while keeping mid-grey at mid-grey) |
| Strength | Rect opacity 0.55 in light theme, 0.5 in dark theme |
| Color space | `color-interpolation-filters="sRGB"` on the filter. **Required.** Without it, the browser computes the noise in linear light and the grain brightens the whole gradient (about 17 levels out of 255 in testing) |
| Measured strength | Standard deviation of about 5.7 levels (light) and 4.0 levels (dark) on a 0–255 scale, measured on the rendered sidebar |

A stronger setting (opacity 0.9, slope 2, frequency 0.9) was tried and rejected: it read as TV static and speckled the blue.

#### Sidebar text tokens

The glow is darker than the flat `--rail` gray, so the sidebar uses its own text and line tokens, scoped to `.side`:

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--side-ink` | `#0F1724` | `#F3F5F8` | Wordmark, account name, hovered items |
| `--side-ink-2` | `#1F2A3A` | `#D2D8E1` | Menu item labels and icons, sidebar icon buttons |
| `--side-ink-3` | `#2A3444` | `#B9C1CD` | Group labels ("Hiring", "Workspace"), counts, "Workspace" subtitle, account chevrons |
| `--side-hover` | `rgba(255,255,255,.55)` | `rgba(255,255,255,.09)` | Hover on items, account button, icon buttons, the collapsed-sidebar expand button |
| `--side-line` | `rgba(25,50,110,.12)` | `rgba(255,255,255,.07)` | Sidebar right border, footer divider, collapsed group dividers |

Other sidebar adjustments in the variant: the account avatar sits on `rgba(255,255,255,.72)` (dark: `rgba(255,255,255,.08)`) so it doesn't merge with the corner glow. Hover is suppressed on the active item, so it keeps its solid raised pill (`--thumb` + `--shadow-raise`), which stands out clearly on the glow.

**Measured contrast** (worst case across the menu area, against the gradient averaged under the text): `--side-ink-2` 5.6:1 light and 5.9:1 dark; `--side-ink-3` 4.9:1 light and 4.6:1 dark. All pass WCAG AA 4.5:1 for small text. Grain makes individual pixels vary slightly around these averages.

#### Usage rules

- Use the grain gradient only on the sidebar. The content area, table panel, dialogs and menus stay flat so data is always on a clean surface.
- Keep blue stops in the brand hue family (`#2563EB` light, `#3D7BF7` dark). The earlier sky-blue version (`#5EC1F9`) was dropped because it clashed with the brand blue on buttons.
- If you move or strengthen the glow, re-check the `--side-ink-3` contrast; it is the first token to drop below 4.5:1.
- Don't place text directly on the strongest part of the glow without a surface under it (the active item's white pill is the model).

## 3. App shell

### 3.1 Structure

```
┌──────────────┬─────────────────────────────────────────────────┐
│ Sidebar      │ Page (max 1280px, centered)                     │
│ 264px        │  Title  Description           [◐][🔔][+ Action]  │
│              ├─────────────────────────────────────────────────┤
│ (72px        │  ┌────────┐┌────────┐┌────────┐┌────────┐        │
│  collapsed)  │  │Total ▣ ││Status ▣││Status ▣││Status ▣│ (read- │
│              │  │ 2      ││ 1      ││ 1      ││ 0      │        │
│              │  └────────┘└────────┘└────────┘└────────┘  only) │
│              │  [🔍 Search…     /]    [Status▾][Job▾][Date▾]    │
│              │  ┌───────────────────────────────────────────┐  │
│              │  │ Name ↑ │ Role ⇅ │ Job ⇅ │ Updated ⇅ │     │  │
│              │  │ rows…                                      │  │
│              │  │ Rows per page [10▾]  1–10 of 62  « ‹ 1 2 › »│  │
│              │  └───────────────────────────────────────────┘  │
└──────────────┴─────────────────────────────────────────────────┘
```

Content is left-aligned throughout. The app is a CSS grid: `var(--side-w) minmax(0, 1fr)`, full dynamic viewport height.

### 3.2 Sidebar

| Part | Spec |
|---|---|
| Container | Sticky, full height, `--rail` background, 1px `--line` right border, 12px padding, scrollbar hidden. **Grain gradient:** gradient background (2.9), `--side-line` border |
| Header | 36px row: logo mark + "IoTides" wordmark; collapse icon button (`panel`) on the right, tooltip "Collapse sidebar". Its center lines up with the page header row |
| Groups | Overview (no label) → "Hiring" (Jobs, Candidates, Schedules, Reports) → "Workspace" (Users, Plan & usage) |
| Group label | 12.5px, 500, `--text-3`, sentence case |
| Item | 40px tall, 12px radius, 12px gap between icon and label, `--text-2`, weight 500 |
| Item hover | `--press` background, `--text` color. **Grain gradient:** `--side-hover` / `--side-ink`, not applied to the active item |
| Active item | Raised pill: `--thumb` background + `--shadow-raise`, `--text` color, icon turns `--brand`. Set via `aria-current="page"` |
| Count | Right-aligned, 12.5px `--text-3`, tabular. Shows total rows for Jobs, Candidates, Schedules, Reports and updates live |
| Footer | Top border `--line`, "User manual" link, then the account button |
| Account button | 34px avatar "IT" (blue tint), "IoTides" / "Workspace", up-down chevrons. Opens a menu: Profile, Plan & usage, separator, Log out (danger) |

The Hiring items are a plain group: there is no connecting line between them.

**Collapsed (desktop only):** width 72px. Labels, counts, wordmark and account text are hidden; group labels become 1px dividers; items center their icon. The collapse button is removed, so the header contains only the logo mark, centered.

**Expanding from collapsed:** a 40×40 expand button (12px radius, `panel` icon) sits exactly over the logo mark at 0% opacity. Hovering the logo area fades the mark out and the expand button in (`--press` background, `--text` icon, 150ms), with the tooltip "Expand sidebar" to the right. Clicking anywhere on the logo area expands the sidebar, so it also works on devices without hover. For keyboard users, the logo link is removed from the tab order while collapsed (`tabindex="-1"`), and the expand button becomes visible when it has `:focus-visible`. After collapsing, focus moves to the expand button; after expanding, it moves back to the collapse button.

In the collapsed state, sidebar items show tooltips to the right of the icon. When expanded, sidebar items never show tooltips.

**≤960px:** the sidebar becomes a 284px off-canvas drawer that slides in over a scrim. Collapse and expand buttons are hidden, and the collapsed state is cleared on resize. Choosing a route, tapping the scrim or pressing Escape closes it.

### 3.3 Mobile bar (≤960px)

Sticky, 56px tall (+ top safe-area inset), `--bg` with a bottom `--line` border. Contains: menu button (40px round icon button), logo + wordmark, then theme toggle and notifications pushed to the right. The theme and notification buttons in the page header are hidden at this width, since they live here instead. Below the mobile bar comes the page header bar (title, description, primary button) with its own bottom rule.

---

## 4. Components

### 4.1 Button

Pill-shaped, 40px tall, 18px horizontal padding, 8px gap, 14px / 500. Presses to `scale(.97)`.

| Variant | Background | Text | Border | Hover | Use |
|---|---|---|---|---|---|
| `primary` | `--brand` | `--on-brand` | none | `--brand-hover` | The page's main action; dialog confirm |
| `secondary` | `--surface` | `--text` | `--line-2` | `--hover` | Supporting actions, dialog cancel, empty-state recovery |
| `soft` | `--brand-soft` | `--brand` | none | border `--brand-line` | Per-row actions that would be too heavy as primary ("Open report") |
| `ghost` | transparent | `--text-2` | none | `--hover`, `--text` | Low-emphasis inline actions ("Clear filters", "Clear selection") |
| `danger` | `--danger` | white | none | brightness 1.06 | Destructive confirmation ("Cancel schedule" in the confirm dialog) |
| `danger-ghost` | transparent | `--danger` | none | `--danger-soft` | Destructive action placed next to a primary action (sheet footer) |

Size `sm`: 34px tall, 14px padding, 13.5px text. Icons in buttons are 17px and always come before the label. Button text is never followed by an arrow.

### 4.2 Icon button

34×34, 10px radius, transparent, `--text-2` icon. Hover: `--press` in the sidebar, `--hover` in the content area. Press: `scale(.9)`. Size `lg`: 40×40 and fully round (mobile bar). In the page header, `lg` icon buttons are reduced to 34×34 to keep the header short. Variant `danger`: hover turns `--danger-soft` / `--danger`.

**Disabled** uses `aria-disabled="true"` rather than the `disabled` attribute, so the tooltip can still explain why (for example "Already scheduled"). Visual: 32% opacity, `not-allowed` cursor, no hover or press feedback. The global click handler ignores these buttons.

Every icon button has both `aria-label` and a `data-tip` tooltip with the same text.

### 4.3 Checkbox

18×18, 6px radius, 1.5px `--line-2` border on `--surface`. Hover border `--text-3`. Checked and indeterminate: `--brand` fill with a white tick (9×5 rotated L) or dash (8×2). Native `appearance: none` input, so it stays keyboard and screen-reader accessible.

### 4.4 Page header

A full-width bar at the top of the content area, separated from the page by a 1px `--line` rule along its bottom edge. The rule spans the whole content area (from the sidebar's right edge to the window's right edge), while the header's contents stay aligned with the 1280px page column below. Inside: a single row, 36px minimum height, with 12px padding above and below (60px bar). Left: title (h1, 18px / 600) followed on the same line by the description (13px, `--text-3`), baseline-aligned with a 12px gap; the description wraps under the title when space runs out. Right, vertically centered: theme toggle and notifications (34×34 round icon buttons, 2px apart), then the page's primary button at 34px tall, 14px padding, 13.5px text, 8px extra left margin. The page content starts 24px below the rule (18px at ≤720px). The row's center lines up with the sidebar's logo row. Reports has no primary button.

The header is rendered into its own element (`#topbar`) above the page content (`#page`), so the rule can run full width even when the page column is narrower than the window.

### 4.5 KPI boxes

Four read-only summary boxes in a row between the page header and the toolbar. They show workspace totals and are not interactive: no hover, no press, no selection, and clicking them does nothing.

| Part | Spec |
|---|---|
| Grid | 4 equal columns, 12px gap (8px at ≤720px). 2 columns at ≤640px, where four boxes would truncate their labels |
| Box | 16px radius, 1px `--line` border, `--surface` background, padding 13px 14px 14px 16px. Content stacks with an 8px gap: a top row (label left, icon tile right), then the count |
| Label | 13px / 500, `--text-2`, truncates with an ellipsis |
| Icon tile | 30×30, 10px radius, `--tone-soft` background, 16px icon in `--tone` (tone per box, see below) |
| Count | 26px / 600, tabular, −0.025em, `--text` |
| Mobile (≤720px) | Padding 11px 12px 12px, 6px gap, 14px radius, 26×26 icon tile (9px radius), 22px count |

**Counts are workspace totals.** They are not affected by search, the status filter, the job filter or the date range, so they always describe the whole page's data. They update when data changes (adding a job, creating or cancelling a schedule, changing a job's status, sending an invite).

**Box tones and icons**

| Page | Box 1 | Box 2 | Box 3 | Box 4 |
|---|---|---|---|---|
| Jobs | Jobs, `briefcase`, neutral | Open, `check-circle`, ok | On hold, `clock`, warn | Closed, `x-circle`, neutral |
| Candidates | Profiles, `contact`, neutral | Unscheduled, `user-check`, violet | Scheduled, `clock`, info | Completed, `check-circle`, ok |
| Schedules | Schedules, `cal-clock`, neutral | Active, `clock`, info | Completed, `check-circle`, ok | Invites sent, `send`, teal |
| Reports | Reports, `file-chart`, neutral | With analysis, `sparkle`, violet | With recording, `video`, rose | Invites sent, `send`, teal |

Status boxes use the same tone as the matching status badge in the table. Total boxes are neutral so the status colors stand out.

**Accessibility:** the row is a `<section>` labelled "{Page} summary". Each box is plain text read as label then count (e.g. "Open 1"); icons are decorative.

**Insight notes** (the tinted one-line facts under the KPI boxes on Overview and insight pages: "1 interview is live right now", "Analysis completes for 100% of interviews") are as wide as their sentence and flow into rows with an 8px gap, several to a row. A long note wraps inside its own box at full width. They never stack as one full-width bar per note.

### 4.6 Status filter chip

The first chip in the toolbar, before the job and date chips. It replaces the original screens' "Filter" dropdown and is the only way to filter by status.

| Part | Spec |
|---|---|
| Chip | Standard filter chip (see 4.8) with the `filter` (funnel) icon |
| Default label | Jobs and Schedules "All statuses", Candidates "All stages", Reports "All reports" |
| Menu | The default option, a separator, then each status with its tone dot: Jobs: Open, On hold, Closed. Candidates: Unscheduled, Scheduled, Completed. Schedules: Active, Completed. Reports: With analysis, With recording. The current option shows a tick |
| Active | When a status is chosen, the chip shows its name and the brand-tinted active state, and "Clear filters" appears |

Choosing a status resets to page 1. "Clear filters" also resets the status to the default.

### 4.7 Search field

Pill, 40px tall, flexes from 260px up to 400px (full width ≤720px). Search icon at 14px from the left; 40px horizontal padding. Focus: the 1px border turns `--brand` (no outline, no halo; see 4.22).

The field shows a "/" keyboard hint on the right when it is empty and unfocused (hidden on touch devices). Once it has text, a round clear button replaces the hint. Filtering is live on every keystroke and resets to page 1.

### 4.8 Filter chip

Pill, 40px tall, 280px max width (220px ≤720px), 1px `--line-2` border, `--surface` background, 13.5px / 500, `--text-2`. Layout: leading icon (16px), label (truncates with ellipsis), trailing chevron (15px, 70% opacity).

| State | Visual |
|---|---|
| Default | As above; label shows the default ("All statuses", "All jobs", "Any date") |
| Hover | `--hover` background, `--text` |
| Open (`aria-expanded="true"`) | Border `--text-3`, `--text` |
| Active filter (`.on`) | `--brand-soft` background, `--brand-line` border, `--brand` text. Label shows the chosen value |
| Pressed | `scale(.97)` |

Chips sit in a right-aligned group after the search field.

**Sort chip (≤720px only).** Hidden on desktop, where column headers handle sorting. On mobile its label is "{Column}: {direction}" (e.g. "Updated: newest first"), or the default order's name when that order isn't a visible column (e.g. "Recently updated" on Jobs). Its menu lists the default order (if hidden) and every sortable column; the active one shows an up/down arrow and a tick, inactive ones show the `chevs` icon. Choosing the active column flips its direction; choosing another column applies its first direction. The sort chip never shows the brand-tinted active state. A ghost "Clear filters" button is added at the end only while a search, status, job filter or date range is set.

### 4.9 Table panel

| Part | Spec |
|---|---|
| Panel | `--surface`, 1px `--line` border, 20px radius, clips its content |
| Scroll | Horizontal scroll wrapper; table min-width 900px on desktop |
| Header row | 46px, 12.5px / 500, `--text-3`, left-aligned, no uppercase, 1px bottom border. Sortable headers contain a sort button (see 4.9.1) |
| Body cells | 14px 16px padding, `--text-2`, vertically centered, 1px `--line` divider (none on the last row) |
| First column | 22px left padding (aligns with the footer text) |
| Row hover | `--hover` background (120ms) |
| Selected row | `--brand-soft` background |
| Numeric columns | Right-aligned, tabular (`.c-num`) |
| Actions column | Shrinks to fit, right-aligned, no wrap. Header text is visually hidden ("Actions" for screen readers). Icon buttons 2px apart |
| Checkbox column | 52px wide (Reports only) |

#### 4.9.1 Sortable column header

Each sortable header holds a `<button class="th-sort">`: label then indicator, 5px gap, 28px tall, 8px radius, 8px horizontal padding offset by −8px margins so the label stays aligned with the cell text. In numeric (right-aligned) columns the indicator sits before the label (`row-reverse`) so the label stays flush right.

| State | Indicator | Label | Background |
|---|---|---|---|
| Unsorted | `chevs` (up-down), 14px, stroke 2, 40% opacity | `--text-3` | none |
| Unsorted, hover | `chevs` at 80% opacity | `--text` | `--hover` |
| Sorted ascending | `arrow-up`, 100%, `--brand` | `--text` | none |
| Sorted descending | `arrow-down`, 100%, `--brand` | `--text` | none |

**Click cycle:** an unsorted column applies its first direction; clicking again reverses it; a third click returns to the page's default order. First direction depends on the data: text and status columns start ascending (A to Z, or earliest stage first); date and number columns start descending (newest or highest first). When the page's default order is itself a visible column (Candidates "Updated", Reports "Completed"), that column shows as sorted on load and toggles between its two directions.

**Ordering rules:** text compares case-insensitively with natural number order ("3 yrs" before "10 yrs"). Status columns sort by workflow rank, not alphabetically. Empty values always go last in either direction. Ties fall back to the page's default order, then to row ID, so the order is stable.

Only one header is sorted at a time; its `<th>` carries `aria-sort="ascending"` or `"descending"`. Changing the sort resets to page 1. Header buttons update in place, so keyboard focus stays on the header after sorting.

Not sortable: Actions, Report, the Reports Status column (always "Completed"), Includes, Focus.

#### Cell patterns

| Pattern | Spec |
|---|---|
| Person | Avatar + stacked name (14.5px / 500, `--text`) and email (13px, `--text-3`, truncates at 260px with a `title` tooltip). Optional third line for source (12px, `--text-3`) |
| Avatar | 38×38, 13px radius, initials (up to 2, uppercase, 13px / 600). The tint comes from the name: sum of character codes mod 5 picks blue, violet, teal, amber or rose. The same name always gets the same color |
| Title cell | Title (name style) with a tag underneath, 6px gap |
| Emphasis | Primary facts like company or current role use `--text`; supporting facts use the default `--text-2` |
| With icon | 15px `--text-3` icon + text, 7px gap, no wrap (location, window, focus) |
| Date | Date in `--text` (no wrap) above time in 12.5px `--text-3` |
| Empty value | Em dash in `--text-3` with `aria-label="Not added"` |
| Zero count | Rendered in `--text-3` instead of `--text` |
| Ok note | 12.5px / 500 `--ok` with a 13px check, e.g. "Invite sent" |
| Mini chip | 24px, 8px radius, `--sunk`, 12px / 500, 13px icon, e.g. "Analysis", "Recording" |

### 4.10 Status badge

Pill, 26px tall, padding 9px left / 11px right, 6px gap, 12.5px / 500, `--tone-soft` background and `--tone` text, 14px icon at stroke 2. If a status has no icon, a 7px dot is shown instead. Every status uses color plus an icon plus a word, so it never relies on color alone.

### 4.11 Tag

22px, 7px radius, 12px / 500. Default: `--neutral-soft` / `--neutral` ("Not published"). `.t-ok`: `--ok-soft` / `--ok` with a check ("Published").

### 4.12 Job status select

An inline badge that is also a menu button. Pill, 30px, 1px transparent border, `--tone-soft` / `--tone`, 13px / 500: dot, label, 14px chevron. Hover: border becomes `--tone`. Press: `scale(.96)`. Opens a menu of Open / On hold / Closed, each with its tone dot and a tick on the current value. Changing it updates the row, the KPI box counts and shows a toast.

### 4.13 Bulk selection bar (Reports)

Appears at the top of the panel when at least one row is selected (fades in over 200ms). `--brand-soft` background, `--brand-line` bottom border, `--brand` text at 500. Left: "N report(s) selected". Right: secondary small "Export CSV" and ghost small "Clear selection".

The header checkbox selects or clears all rows on the current page and shows the indeterminate state for partial selection. Selection is pruned whenever filters change, so hidden rows can't be exported by accident.

### 4.14 Footer and pagination

Footer: 56px min height, 1px top border, 13px tabular text, wraps when narrow.

| Part | Spec |
|---|---|
| Rows per page | "Rows per page" label (`--text-3`) + a 30px pill button (1px `--line-2`, `--surface`, 13px / 500 `--text`, 14px chevron). Opens a menu: "10 per page", "25 per page", "50 per page" (default 10). Open state: border `--text-3` |
| Range | "1–10 of 62" in `--text-2` (en dash), 20px after the rows-per-page control. "No {jobs} to show" when empty |
| Pager | Right-aligned, 2px gaps: First (`chev-first`), Previous (`chev-left`), page numbers, Next (`chev-right`), Last (`chev-last`) |

**Pager buttons:** 34×34 minimum, 10px radius, transparent, `--text-2` / 500, tabular. Hover: `--hover` / `--text`. Current page: `--brand-soft` / `--brand` with `aria-current="page"`. First/Previous are disabled (32% opacity) on page 1; Next/Last on the last page. All have `aria-label`s ("First page", "Page 3", etc.).

**Page numbers** use at most 7 slots. With 7 or fewer pages, all are shown. Otherwise: near the start `1 2 3 4 5 … N`; near the end `1 … N−4 N−3 N−2 N−1 N`; in the middle `1 … p−1 p p+1 … N`. Ellipses are `aria-hidden`.

**Changing rows per page** keeps the first visible row on screen: the new page is `floor(firstRowIndex / newSize) + 1`. Changing page scrolls the table panel into view if needed. Filters, search, status and sort changes reset to page 1.

**≤720px:** the "Rows per page" label and the page numbers are hidden; "Page X of Y" (`--text-2`) appears between Previous and Next, and the pager wraps below the range.

### 4.15 Empty states

Centered, max 380px wide: a 52px `--sunk` tile with a 22px `--text-3` icon (17px radius), a 15.5px / 600 title, a `--text-2` line of guidance, then one action. Inside the table it spans all columns with 64px vertical padding.

| Situation | Title | Guidance | Action |
|---|---|---|---|
| No data at all | "No {jobs} yet" | "Your {jobs} will show up here once you add them." (Reports: "Completed interviews will show up here.") | Page primary button (none on Reports) |
| Filters exclude everything (including a status with no rows) | "No {candidates} match these filters" | "Try a different status, search or date range." | Secondary "Clear filters" |
| Placeholder page | "Not part of this prototype" (or "This page doesn't exist") | Explains which pages the redesign covers | Secondary "Go to Jobs" |

### 4.16 Menu

Fixed-position, `--pop`, 1px `--line` border, 16px radius, `--shadow-pop`, 6px padding, 210px min width, 340px max width. Items: 38px min height, 10px radius, 14px `--text`, optional 17px `--text-2` icon or tone dot, label truncates, tick on the right for the selected option (`menuitemradio` + `aria-checked`). Hover/focus: `--hover` (`--press` in dark mode). Danger items are `--danger` for both text and icon. Separator: 1px `--line` with 6px/4px margins.

**Placement:** below the anchor with a 6px gap, aligned to its start (or end, for the sort chip and notifications). It is clamped 12px from the viewport edges and flips above the anchor when there isn't room below. It repositions on scroll and closes on resize.

**Behaviour:** clicking the same anchor again closes it; clicking outside closes it. On open, focus goes to the selected item (or the first item). Up/Down arrows move focus, Escape closes and returns focus to the anchor, Tab closes.

### 4.17 Date range popover

Same shell as the menu but 312px wide with 16px padding. Contents: title "{Updated / Created / Completed} between" (14px / 600), preset pills ("Last 7 days", "Last 30 days", "Any time": 32px, 13px / 500, `.on` state matches the filter chip), then From / To native date inputs in two columns (40px, 12px radius, 12.5px `--text-3` labels). Changes apply immediately. If From is later than To, the two are swapped when filtering. Presets are calculated from the viewer's current date, inclusive of today.

### 4.18 Notifications popover

Same shell, right-aligned to the bell. Title "Notifications" and an empty state: bell tile plus "No notifications yet." The bell has no unread dot because there is no notification data.

### 4.19 Tooltip

Inverse colors (`--toast-bg` / `--toast-ink`), 5px 9px padding, 8px radius, 12.5px / 500, no wrap. Fades in with a 3px rise over 120ms. Positioned 8px above the element (below it if there's no room), or 10px to the right for sidebar elements, clamped 8px from the viewport edges.

Shown on mouse hover and on keyboard focus (`:focus-visible` only). Never shown for touch input. Hidden on pointer down, blur and scroll. Text comes from `data-tip`.

### 4.20 Toast

Bottom-center, 24px above the bottom safe area, stacked with 8px gaps. Pill with inverse colors, 11px 20px 11px 14px padding, 14px / 500, `--shadow-pop`, max width = viewport − 32px. The icon is `check-circle` in `--toast-ico` for success, or `info` at 70% opacity for informational messages. It springs in, stays 2.8 seconds, then fades out. The container has `aria-live="polite"`.

### 4.21 Dialog

Native `<dialog>` opened with `showModal()`, max 480px wide (viewport − 32px on small screens). The card has a 24px radius, `--pop`, `--shadow-pop`, over a `--scrim` backdrop.

| Part | Spec |
|---|---|
| Header | Title (18px / 600) and optional description (`--text-2`); close icon button on the right |
| Body | Grid of fields, 16px apart |
| Footer | Right-aligned: secondary cancel, then primary (or danger) confirm, 8px apart |

**Scrolling:** a dialog taller than the viewport scrolls its body only. The header (and footer) stay put, and the slim scrollbar sits inside the card, inset from its rounded corners, never along the card's outer edge.

**Closing:** the close button, the cancel button, clicking the backdrop, and Escape all play the 160ms exit animation first. On open, focus goes to the first input or select, or to the confirm button if there are no fields.

**Validation** runs on submit. Invalid fields get a `--danger` border (kept while focused, with no halo), `aria-invalid`, and a 12.5px `--danger` message linked with `aria-describedby`. Focus moves to the first invalid field.

### 4.22 Form fields

| Part | Spec |
|---|---|
| Label | 13px / 500 `--text`. Optional fields add "Optional" in 400 `--text-3`. Required fields and selects show no marker |
| Input / select | 42px, 12px padding, 12px radius, 1px `--line-2`, `--surface`. Focus: the same 1px border turns `--brand`. Nothing else: no outline, no halo, no second ring |
| Select | Native select with appearance removed and a 16px `--text-3` chevron on the right |
| Read-only value | 42px, 12px radius, `--sunk` background, `--text-2`, with a 16px leading icon (used for "Rolling 24h") |
| Checkbox row | Checkbox and label with a 10px gap, whole row clickable |

### 4.23 Details sheet

Native `<dialog>` pinned to the right edge: `min(440px, 100vw)` wide, full height, over a scrim. Card: `--pop`, 1px `--line` left border, slides in from 32px over 360ms.

| Part | Spec |
|---|---|
| Header | Title (18px / 600) + subtitle (`--text-2`), close button, bottom border |
| Body | Key/value list: 128px label column (13.5px `--text-3`), values in `--text` that can wrap long strings. 13px row padding with dividers. Stacks to one column at ≤720px |
| Footer | Right-aligned actions, wrapping, top border, bottom safe-area padding |
| Link box | 40px `--sunk` pill-ish field (12px radius) with the truncated URL and a copy icon button |

---

### 4.24 Transcript bubbles

Used by the report page and the public report. A chat layout: interviewer turns on the left, candidate turns on the right.

| Part | Spec |
|---|---|
| Bubble | Max 85% of the row (720px), padding 8px 12px 6px, 12px radius except the corner nearest the speaker's side, which is square and carries the tail. Faint 1px shadow |
| Colors | Interviewer `--sunk`, candidate `--brand-soft` (unchanged) |
| Tail | 8×13px triangle in the bubble's color at its top outer corner (left for the interviewer, right for the candidate) |
| Speaker row | Icon (`sparkle` interviewer, `user` candidate) and label, 12.5px / 500; candidate in `--brand` |
| Text | 14px, 1.55 line height, wraps anywhere, keeps line breaks |
| Time | Bottom-right inside the bubble, 11px `--text-3`, clock time only ("2:05 pm"); omitted when the turn has none |
| Runs | Consecutive turns by the same speaker sit 4px apart, and only the first keeps the tail (the others get a fully rounded corner) |

## 5. Status mappings

### Jobs

| Value | Label | Tone | Visual |
|---|---|---|---|
| `open` | Open | ok | Dot |
| `hold` | On hold | warn | Dot |
| `closed` | Closed | neutral | Dot |
| `published: false` | Not published | neutral tag | — |
| `published: true` | Published | ok tag | Check icon |

### Candidate stage

| Value | Label | Tone | Icon |
|---|---|---|---|
| `ready` | Profile ready | violet | `user-check` |
| `scheduled` | Scheduled | info | `clock` |
| `completed` | Completed | ok | `check-circle` |

The Candidates KPI box and status filter label `ready` as "Unscheduled" because it describes what's missing, while the badge describes the current state.

### Schedule status

| Value | Label | Tone | Icon |
|---|---|---|---|
| `scheduled` | Scheduled | info | `clock` |
| `completed` | Completed | ok | `check-circle` |
| `cancelled` | Cancelled | danger | `x-circle` |

"Scheduled" deliberately uses the info (blue) tone and a clock. The previous design used an orange warning triangle, which suggested a problem when nothing was wrong.

---

## 6. Page specifications

### 6.1 Jobs (`#/jobs`, default route)

| Item | Value |
|---|---|
| Description | "Job descriptions for the roles you're hiring for." |
| Primary action | "Add job" (plus icon) |
| KPI boxes | Jobs, Open, On hold, Closed |
| Search | Placeholder "Search by title or company"; matches title, company, location |
| Filters | Status ("All statuses"), date |
| Date field | Updated |
| Default order | Recently updated (hidden field, no column shows as sorted) |
| Sortable columns | Job, Company, Location, Questions, Skills, Status (Open → On hold → Closed) |
| Columns | Job (title + publish tag), Company, Location (pin), Questions (numeric), Skills (numeric), Status (status select), Actions |
| Row actions | Edit job (`pencil`), View details (`eye`), Publish job (`upload`; disabled with "Already published" once published) |
| Details sheet | Company, Location, Status, Publishing, Questions, Skills, Candidates (count linked to this job). Footer: "Edit job", plus "Publish job" if unpublished |
| Add/Edit dialog | Job title (required), Company (required), Location (optional). Confirm: "Add job" / "Save changes" |

### 6.2 Candidates (`#/candidates`)

| Item | Value |
|---|---|
| Description | "Everyone you've added, and where each person is in the interview process." |
| Primary action | "Add candidate" |
| KPI boxes | Profiles, Unscheduled, Scheduled, Completed |
| Search | "Search name, email or role"; matches name, email, role, job title |
| Filters | Status ("All stages"), job ("All jobs"), date |
| Date field | Updated |
| Default order | Updated, newest first (the Updated header shows as sorted) |
| Sortable columns | Candidate, Current role, Job, Experience, Stage (Profile ready → Scheduled → Completed), Updated |
| Columns | Candidate (person + source line), Current role, Job, Experience, Stage (badge), Updated (date/time), Actions |
| Row actions | View profile (`eye`); Schedule interview (`cal-plus`), disabled with "Already scheduled" or "Interview completed" unless the stage is Profile ready |
| Details sheet | Current role, Job, Experience, Stage, Source, Updated. Footer: "See schedules" (if any; opens Schedules pre-searched by name), "Schedule interview" (if eligible) |
| Add dialog | Full name (required), Email (required, format-checked, must be unique), Current role (optional), Job (select). New candidates start at "Profile ready" with source "Added manually" |

### 6.3 Schedules (`#/schedules`)

| Item | Value |
|---|---|
| Description | "Interview windows, links and invites for each candidate." |
| Primary action | "Create schedule" |
| KPI boxes | Schedules, Active (scheduled), Completed, Invites sent |
| Search | "Search candidate or job"; matches candidate name, email, job title |
| Filters | Status ("All statuses"), job ("All jobs"), date |
| Date field | Created |
| Default order | Latest window (hidden created time, no column shows as sorted) |
| Sortable columns | Candidate, Job, Window, Status (Scheduled → Completed → Cancelled) |
| Columns | Candidate (person), Job, Window (clock), Status (badge), Focus (mail + "Invite sent" note once sent), Actions |
| Row actions, scheduled | View schedule (`ext`), Copy interview link (`copy`), Send invite / Resend invite (`mail`), Cancel schedule (`x-circle`, danger hover) |
| Row actions, completed | View schedule, View report (`file-chart`) |
| Row actions, cancelled | View schedule |
| Details sheet | Status, Window, Focus, Invites sent, Interview link (link box with copy). Footer when scheduled: danger-ghost "Cancel schedule" + primary "Send invite" / "Resend invite". When completed: primary "View report" |
| Create dialog | Candidate (only "Profile ready" candidates), Job, Window (read-only "Rolling 24h"), "Email the invite now" (checked by default). Creating moves the candidate to Scheduled. If no one is eligible, the dialog says so and offers "Add candidate" |
| Cancel confirm | Title "Cancel this schedule?", description "{Name}'s interview window for {Job} will be marked as cancelled.", buttons "Keep schedule" / "Cancel schedule" (danger). If the candidate has no other active schedule, they return to Profile ready |

### 6.4 Reports (`#/reports`)

| Item | Value |
|---|---|
| Description | "Results from completed interviews." |
| Primary action | None |
| KPI boxes | Reports, With analysis, With recording (the last two overlap; they are not exclusive states), Invites sent |
| Search | "Search candidate or job" |
| Filters | Status ("All reports": With analysis, With recording), job ("All job descriptions"), date |
| Date field | Completed |
| Default order | Completed, newest first (the Completed header shows as sorted) |
| Sortable columns | Candidate, Job, Completed |
| Columns | Select checkbox, Candidate, Job, Status (always Completed), Completed (date/time), Includes (Analysis / Recording mini chips), Report ("Open report" soft small button) |
| Bulk actions | Export CSV, Clear selection |
| Details sheet | Title is the candidate name, subtitle "Interview report". Rows: Candidate, Job, Status, Completed, Analysis, Recording ("Included" / "Not available"). Footer: "Export CSV" |
| CSV export | Columns: Candidate, Email, Job, Status, Completed, Analysis, Recording. File name `iotides-reports-YYYY-MM-DD.csv` |

### 6.5 Placeholder routes

`#/overview`, `#/users`, `#/plan`, `#/profile`, `#/manual` render the page header (title only, plus theme and notifications) and the "Not part of this prototype" empty panel. Unknown routes show "Page not found" / "This page doesn't exist".

---

## 7. Interaction rules

**Routing** is hash-based (`#/jobs`, etc.). Each route re-renders the page shell and resets scroll. Filter, sort, status, page and selection state is kept per page for the session, so returning to a page restores its view. The document title is "{Page} | IoTides".

**Re-rendering:** after the first render, filter and data changes only update the table body, counts, chip labels, header sort indicators, KPI counts and footer. The search field, chips and header buttons are not replaced, so focus and the cursor position survive typing and sorting.

**Filtering order:** search → job filter → date range → status filter → sort → paginate. KPI counts are computed from all rows, before any of this. Any filter or sort change resets to page 1. Rows-per-page changes keep the first visible row (see 4.14).

**View state per page:** status, search, job filter, date range, sort key and direction, page, rows per page and (Reports) selection.

**Keyboard:**

| Key | Effect |
|---|---|
| `/` | Focus the page search (ignored while typing or when a dialog/sheet is open) |
| Escape | Close the open menu/popover (focus returns to its anchor); otherwise close the mobile drawer; inside a dialog or sheet, close it |
| ↑ ↓ | Move within a menu |

**Focus ring:** 2px `--brand` outline with a 2px offset on `:focus-visible` for buttons, links and other controls. Text-entry controls (inputs, selects, textareas, the custom select, the search field, passcode boxes, link boxes) never get it: their focus is the 1px border turning `--brand` (4.22). One thin line, not a border inside a thick ring.

---

## 8. Content and copy

**Voice:** plain verbs, sentence case, no filler, no exclamation marks, no apologies. Buttons say exactly what happens, and the toast reuses the same verb.

**Date and time:** dates are `D Mon YYYY` using fixed English month abbreviations (e.g. "21 Sep 2026"), so they don't vary by browser locale. Times are `h:mm AM/PM` (e.g. "1:03 PM"). Date-range chips use `D Mon – D Mon`, "From D Mon", "Until D Mon" or "Any date". The footer range reads "X–Y of Z" with an en dash; mobile pagination reads "Page X of Y"; the rows-per-page menu reads "10 per page".

**Sort direction labels** (mobile sort chip and menu): text "A to Z" / "Z to A"; dates "newest first" / "oldest first"; numbers "high to low" / "low to high"; status columns name the first state ("Open first" / "Closed first", "Profile ready first" / "Completed first", "Scheduled first" / "Cancelled first").

**Action → confirmation vocabulary:**

| Action label | Toast |
|---|---|
| Add job | "Job added" |
| Save changes | "Changes saved" |
| Publish job | "Published {job title}" |
| (Status menu) | "Status changed to {status}" |
| Add candidate | "Candidate added" |
| Create schedule | "Schedule created and invite sent to {email}" or "Schedule created" |
| Copy interview link | "Interview link copied" (on failure: "Couldn't copy. Open the schedule to select the link.") |
| Send invite / Resend invite | "Invite sent to {email}" |
| Cancel schedule | "Schedule cancelled" |
| Export CSV | "Exported {n} report(s)" |

**Informational toasts:** "Log out isn't connected in this prototype", "Add a job first, then add candidates to it", "No report found for this schedule".

**Validation messages:** "Enter a job title.", "Enter the company name.", "Enter the candidate's name.", "Enter an email address.", "Enter an email like name@example.com.", "This email is already in your candidates."

**Tooltips:** Edit job, View details, Publish job, Already published, View profile, Schedule interview, Already scheduled, Interview completed, View schedule, Copy interview link, Copy link, Send invite, Resend invite, Cancel schedule, View report, Collapse sidebar, Expand sidebar, Light mode, Dark mode, Notifications, Account.

**Avoid:** all-caps labels, eyebrow labels above headings, strings joined with middle dots, arrows appended to button text, and warning icons for states that aren't problems.

---

## 9. Responsive behaviour

| Breakpoint | Changes |
|---|---|
| > 960px | Full layout. Sidebar 264px, collapsible to 72px (expand via the logo) |
| ≤ 960px | Sidebar becomes a 284px drawer with a scrim; mobile bar appears; header bar padding 14/16 and page padding 20/16/48; theme and notifications move to the mobile bar; collapse/expand buttons hidden |
| ≤ 720px | Page title 17px, page content 18px below the header rule; the description wraps under the title. Primary button wraps under the header text. KPI boxes shrink (see 4.5). Search goes full width with chips wrapping below; the sort chip appears. Footer shows the compact pager ("Page X of Y") without the "Rows per page" label. **Table rows become cards**: header hidden, each row is a two-column grid (18px padding, 14px/16px gaps), the main cell spans both columns, other cells get a 12px `--text-3` label from `data-label`, and actions sit right-aligned below a dashed divider. The Reports checkbox is pinned to the card's top-right corner. Sheet key/value rows stack |
| ≤ 640px | KPI boxes go to 2 columns |
| `hover: none` | The "/" search hint is hidden |
| `prefers-reduced-motion` | Animations and transitions are effectively disabled |

Safe-area insets are respected on the mobile bar (top), toasts (bottom) and sheet footer (bottom).

---

## 10. Accessibility

- Semantic landmarks: `aside` for navigation, `main`, a `section` for the table panel, `nav` for pagination.
- Every icon-only control has an `aria-label`; icons are `aria-hidden`.
- Status is never shown by color alone: badges combine color, icon and word.
- Menus use `role="menu"` with `menuitem` / `menuitemradio` and `aria-checked`; anchors set `aria-haspopup` and `aria-expanded`.
- KPI boxes are static text in a labelled `<section>`, not controls, so they're skipped when tabbing. The status filter is a standard menu button in the toolbar.
- Sortable headers are real buttons inside `<th scope="col">`; the sorted header exposes `aria-sort`. Sort indicators are decorative (`aria-hidden`).
- Pagination is a `<nav aria-label="Pagination">`; every pager button has an `aria-label`, and the current page has `aria-current="page"`.
- The collapsed-sidebar expand button is keyboard reachable and becomes visible on focus; the hidden logo link is removed from the tab order while collapsed.
- Dialogs and sheets use native modal `<dialog>`, which provides the focus trap and inert background. Close buttons are labelled.
- Form errors are announced (`aria-live="polite"`) and linked to their inputs.
- Toasts are announced through an `aria-live="polite"` region.
- Row checkboxes are labelled "Select {name}"; the header checkbox is "Select all reports on this page".
- Contrast (grain gradient sidebar): measured, and passes 4.5:1 for all sidebar text; see 2.9.
- Contrast (everything else): the text tokens were chosen to be readable on their surfaces, but they **have not been formally measured against WCAG**. `--text-3` (`#8A909B` on white) in particular is likely below 4.5:1 and is only used for tertiary metadata; run a contrast check before relying on it for essential text.

---

## 11. Data and placeholders

The prototype's data comes from the four original screenshots. Some values were not visible there and are placeholders, marked `/* placeholder */` in the code:

- The job's `updated` timestamp (used for Jobs sorting and date filtering; not displayed in the table).
- The schedules' `created` timestamps (used for Schedules sorting and date filtering; not displayed).
- The interview link URL `https://interview.example.com/s/{id}`.

**Testing aid:** open the file with `?demo=N` (for example `iotides-console.html?demo=60`, max 200) to add clearly labelled sample rows ("Sample Candidate 01", "Sample Job 01", source "Demo data", `@example.com` emails) across all four pages. This exists only to exercise sorting and pagination; it is off by default and adds nothing when the parameter is absent.

These things are demo-only and not connected to a backend: logging out, the notification feed, and the report detail (the sheet shows a summary instead of a full report page). All data resets when the page is reloaded.

The meaning of the "Focus" column on Schedules was kept exactly as in the original ("Email linked"), since its intent wasn't clear from the screenshots.

---

## 12. Known inconsistencies

These are hardcoded values in the current file that aren't tokens yet:

- The white check and dash inside the checked checkbox, and the white text on the danger button, use `#fff` instead of `--on-brand` (or a dedicated `--on-danger`).
- The logo mark colors (`#2563EB`, `#14B8A6`, `#0B3B8C`, `#fff`) are inline and don't follow the dark-mode brand shift.
- Grain gradient: the gradient stops are literal `rgba()` values, not tokens, and the grain SVG is written out twice (light and dark differ only in opacity). The variant is a separate copy of the whole file, so any change to the main file has to be copied into it by hand. Folding it into the main file as a theme option (for example a `data-sidebar="grain"` attribute) would remove the duplication.
- The page header's 36px icon buttons and primary button are local overrides (`.head-actions …`) rather than a named size variant (e.g. `md`).
- Radii and spacing are literal pixel values rather than a named scale. If this design moves into a component library, extracting `--radius-*` and `--space-*` tokens would be the first cleanup.
