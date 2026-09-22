---
feature: full-github-upgrade
status: designed
updated: 2026-09-22
branch: feat/full-github-upgrade
commits: # filled at delivery
---

# Full GitHub Upgrade (shadrackb1)

## Report

## [S1] Problem

shadrackb1’s GitHub account (~98 public repos) no longer reads as one engineer’s body of work.

- The profile README is widget-heavy (trophies, streak, snake, typing SVG, multiple analytics cards) and does not match a credible hiring/client surface.
- Flagship products (RIS, Juriscore, KSAS, USSD Attendance, FieldOps, EFK) are real systems, but most other repos share a 14-line stub README and look unfinished or interchangeable.
- Clear duplicate/version sprawl (KSAS×5, RAWLINE×5, Mingle×4, OBOMOCARE×4, UniHub×4, KABU AI×3, justice/foundation pairs) buries the work that matters.
- Repo descriptions and topics are thin or empty across most of the account.
- `research-in-a-stick` (named as the core product) has no README.

Goal: a full account upgrade — redesigned profile, consistent READMEs across public repos, metadata pass, and reversible archive of duplicates.

## [S2] Design

### Decisions (settled)

| Axis | Choice |
| --- | --- |
| Scope | Full account hygiene: profile + public READMEs + metadata + archive dups |
| Profile look | Full redesign (new visual system, not a polish) |
| Cleanup | Archive duplicates/abandoned experiments; document the rest; never delete |
| Delivery | Short-lived branches, verify locally, push to each repo’s default branch |

### Profile visual system (full redesign — generative)

Style anchor: **mission-control generative art** — Refik Anadol-class data sculpture meets Kenyan field telemetry. The profile is a living instrument panel made of mathematics, not a résumé frame. Ordinary hand-drawn headers are out of scope; every signature asset is procedurally generated at human-impossible density (thousands of paths, coordinated SMIL motion, projected 3D).

Palette (dual light/dark SVG pairs via `<picture>`):

| Token | Hex | Use |
| --- | --- | --- |
| Ink | `#0F172A` | Primary text on light |
| Paper | `#F8FAFC` | Light canvas |
| Night | `#0B1220` | Dark canvas |
| Teal | `#0D9488` / `#2DD4BF` | Signal traces, attractors |
| Amber | `#D97706` / `#FBBF24` | Constraint nodes, pulses |
| Mute | `#64748B` | Captions |

Typography: system UI for README prose; monospace for telemetry labels inside SVGs.

Signature assets (Python-generated SMIL SVG, light+dark):

1. **`hero-attractor.svg`** — Lorenz/Thomas strange-attractor ribbon field with 3D-projected product nodes orbiting on an icosahedral cage. Name set in the dead space of the attractor. Continuous SMIL rotation + node pulse. **Glass nameplate** (frosted blur panel) over the field; **physics**: node springs (critically damped keySplines), packet gravity bounces on the cage edges.
2. **`signal-grid.svg`** — PCB / mission-bus traces with 80+ animated pulse dots traveling constraint→product paths. **Glass docks** at each end (blur + translucent fill + inner highlight). **Physics**: packets ease with accelerating gravity then settle (keySplines mimicking g and restitution).
3. **`constellation.svg`** — 47 county points on a sphere wireframe, Kenyan products as brighter stations, slow global rotation. **Glass HUD chip** for the legend. **Physics**: station beacons spring-scale with overshoot; orbital rings use elliptical Kepler-ish phase offsets.

Material language: **glassmorphism** on every UI chrome layer (nameplates, docks, chips): `feGaussianBlur` backdrop approx, translucent fill (`rgba` equivalents via fill-opacity), 1px light-edge stroke, no drop shadows that read as bevel. **Physics-based motion** on every moving agent: spring (overshoot+settle), gravity (ease-in then bounce with restitution ~0.55), orbital (constant angular velocity with perspective scale). No linear cartoon loops.

Drop all third-party badge widgets. README sections stay scannable but sit *under* the generative stack like captions under a gallery piece.

### README tiers

| Tier | Repos | README bar |
| --- | --- | --- |
| A Flagship | research-in-a-stick, juriscore, KSAS, ussd-attendance, foursons-fieldops, efk-battles, shadrack-portfolio, playground, know-your-rights, knowyourrightske | Full dossier README: header SVG, problem, constraint, how it works, stack, run, links. Match profile brand tokens. |
| B Product | careconnect1, law-beyond, mingle-app, obomocare-live, shopledger, KABU-AI, UniHUbKe, class-connect, Campuseats, haki-chatbot, PAWA, JUA-KAZI-KE, Stk-push | Structured README: title, one-liner, what it does, stack, run, links. |
| C Client/demo | remaining public non-archived repos | Short consistent README: title, one-liner, status, stack or “static demo”, link if live. |
| D Archive candidates | duplicates + abandoned version snapshots | Canonical repo gets Tier A/B; non-canonical is archived with a one-line pointer in description. No content rewrite required after archive. |

Canonical map (archive the rest):

| Canonical | Archive |
| --- | --- |
| KSAS | KSASV1.2, KSASV1.0, KSASV1, ksas-archive |
| juriscore | Juslriscore |
| mingle-app | MingleKe, MingleKe-Elite, MingleKeElite |
| foursons-fieldops | (none) |
| obomocare-live | obomocare-site, obomocare-app, obomocarev1 |
| knowyourrightske | know-your-rights (after cross-link if both ship different surfaces; else archive the thinner one) |
| UniHUbKe | Unihub, KabuHostels, unihub-landing-experience (private — leave private, document only) |
| KABU-AI | KABU-AI-V2, kabu-ai-v1 |
| RAWLINE | RAWLINE-ORIGINAL-BRAND, RAWLINE-SHOPP, RAWLINE-Shop, rawline-dots |
| Receipt-2.0 | receipt- |
| Mati-Foundation | maty-foundation- |
| Friendsforjustice | Friends-for-justice |
| bar-kitchen | generalis- |
| primegatesinsurancecompany | primegates-quick-draft, Prime-gates-insurance-company- |
| research-in-a-stick | (none) |
| shadrack-portfolio | (none) |
| playground | (none) |
| live | live-b (document; archive only if content is subset) |

Jewellery-website vs Jewellery-shop are different brands (Aurora vs AURUM) — do **not** auto-archive; both get Tier C and a note in the cleanup report.

### Metadata contract

For every non-archived public repo:

- `description`: one sentence, product + audience/constraint, no trailing period required, ≤ 120 chars preferred.
- `homepage`: set when a live URL is known (GitHub Pages, Vercel, etc.); clear stale URLs.
- `topics`: 3–8 lowercase kebab topics from a controlled set (`kenya`, `legal-tech`, `offline-first`, `mpesa`, `ussd`, `attendance`, `education`, `field-ops`, `react`, `nextjs`, `python`, `fastapi`, `supabase`, `postgres`, `portfolio`, `demo`, `game`…).

Profile repo topics: keep `github-profile`, `profile`, `kenya`, `offline-ai`, `legal-tech`; drop unused language tags if they do not describe the profile content.

### Error / edge behavior

- Missing README → create Tier C (or A/B per map).
- Base64/API read failures → retry via raw.githubusercontent.com before concluding absence.
- Private repos (efk-battles, KABU-AI, Kabarak EVIS, unihub-landing-experience, uber, etc.) → description/metadata OK with push access; skip public README marketing if content is confidential.
- Archive is reversible via `gh repo edit --archived=false`.
- Never `gh repo delete`.

### Testing boundary

- Markdown renders (structure, links resolve to 200 or known Pages URLs).
- SVG assets load in README (paths relative and present).
- After push, profile page and ≥1 Tier A repo README verified live via `gh api` / webfetch.
- Archive flags verified via `gh repo list --json isArchived`.

## [S3] Out of Scope

- Deleting any repository.
- Renaming repositories (breaks links); renames listed as recommendations only.
- Application code changes inside product repos (except README/docs/assets required for the dossier).
- Private client data, secrets, or expanding private repos’ public exposure.
- Contribution-graph gaming, fake commits, or bot-driven activity.

## Tasks

- [ ] T1: Rebuild profile visual assets (header, systems map, flagship cards) in the new dossier palette — acceptance: SVGs present, labeled, match S2 tokens, no trophy widgets (covers: S2)
- [ ] T2: Rewrite profile README to S2 section order and voice — acceptance: sections 1–7 present, external widget spam removed, links to flagship repos work (covers: S2; depends: T1)
- [ ] T3: Author Tier A READMEs for flagships including missing research-in-a-stick — acceptance: each flagship has dossier README with problem/constraint/run/links (covers: S2; depends: T1)
- [ ] T4: Author Tier B/C READMEs across remaining public repos — acceptance: every non-archived public repo has a non-stub README matching its tier (covers: S2)
- [ ] T5: Metadata pass (description, homepage, topics) on non-archived public repos — acceptance: `gh repo list` shows a non-empty description for each (covers: S2)
- [ ] T6: Archive duplicate/abandoned repos per canonical map — acceptance: listed non-canonical repos have `isArchived: true`; canonical remain active (covers: S2)
- [ ] T7: Publish cleanup report (what was archived, renames recommended, Jewellery pair left active) — acceptance: report file lists every archive and why (covers: S2; depends: T6)
- [ ] T8: Live verification of profile + sample Tier A/B after push — acceptance: profile README content matches local head; ≥1 Tier A and ≥1 Tier B match (covers: S2; depends: T2, T3, T4)
