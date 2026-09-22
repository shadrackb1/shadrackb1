---
feature: full-github-upgrade
status: delivered
updated: 2026-09-22
branch: main
commits: 70811bb..7dad292
---

# Full GitHub Upgrade (shadrackb1)

## Report

**What was built** — The shadrackb1 account now reads as one person: Shadrack Baraka Mwahanga, constraint-first engineer and LLB student. The profile is a hand-inked field notebook (ink wobble, tape, red pen, coffee ring, FIELD COPY stamp, SBM monogram) instead of neon AI attractors. Shadrack Lab on GitHub Pages hosts six cursor-driven biomes people can stay in. Flagship, product, and client repos have tiered READMEs and metadata. Twenty-six duplicate/abandoned repos are archived with pointers; nothing was deleted.

**Verification** — `lab.html` live 200 with brand strings and `o.wob` fix (`PASS`). Profile README contains “Constraint is the brief”, field-notebook hero, case index (`PASS`). 26 archives match cleanup report (`PASS`). Tier A 9 READMEs live (`PASS`). Public actives have README + description (`PASS`); RIS topics filled (`PASS`); Fuliza README rewritten (`PASS`). Soft-bodies `wob` scope crash fixed (`PASS`).

**Journey log**
- Ordinary capability-dossier headers were too easy; user asked for work no human would do, then for physics/glass, then for interaction, then to stop looking AI-generated. Final form is craft (hand ink) + real interaction (lab), not more math widgets.
- Metrics bot (`chore: refresh metrics calendar` / snake / 3d) races every push to profile `main`. Rebase or merge around it; deleting its assets conflicts until you `git rm` the modify/delete side.
- `putImageData` ignores `setTransform`; any DPR pixel loop must blit at identity or use an offscreen canvas.
- `gh repo edit` has no `--archived` here; use `gh api -X PATCH ... -f archived=true`. PowerShell `Set-Content -Encoding utf8` BOM breaks `gh api --input`.
- knowyourrightske and know-your-rights are different stacks, not duplicates. Jewellery-website (Aurora) and Jewellery-shop (AURUM) stay active.

## [S1] Problem

shadrackb1’s GitHub account (~98 public repos) no longer reads as one engineer’s body of work.

- Profile was widget-heavy and, after a first redesign, still looked AI-generated (attractors, Fourier roses, glass neon).
- Flagships were real; most other repos looked unfinished.
- Duplicate/version sprawl buried the work that matters.
- `research-in-a-stick` had no README.

Goal: full account upgrade — human-branded profile, interactive lab that holds attention, consistent READMEs, metadata, reversible archive of duplicates.

## [S2] Design

### Decisions (settled)

| Axis | Choice |
| --- | --- |
| Scope | Full account hygiene: profile + public READMEs + metadata + archive dups |
| Profile look | Full redesign, then de-AI: hand-inked field notebook |
| Interaction | GitHub Pages lab with cursor-driven biomes (not README JS) |
| Cleanup | Archive duplicates/abandoned experiments; document the rest; never delete |
| Delivery | Short-lived branches, verify locally, push to each repo’s default branch |

### Profile visual system (field notebook)

Style anchor: **field notebook + case file** — legal pad, typewriter labels, red pen, rubber stamp. Human craft over math flex.

| Token | Hex | Use |
| --- | --- | --- |
| Paper | `#F3EDE2` / night `#1A1712` | Page ground |
| Ink | `#1C1917` / `#F0E6D2` | Diagrams, titles |
| Pencil | `#5C5346` | Secondary notes |
| Red | `#C23B22` | Margin rule, stamps, annotations |
| Rule | `#D9D0C0` | Faint pad lines |

Signature assets (`scripts/forge_svg.py`, light+dark):

1. **`hero-attractor-*.svg`** (filename kept) — wobbly constraint→response diagram, tape, coffee ring, FIELD COPY stamp, pen-draw connectors.
2. **`case-index-*.svg`** — shipped systems as an open case index.
3. **`sketch-coverage-*.svg`** — hand globe sketch, 47 county ticks, slow pen path.
4. **`glyph-*.svg`** — rough SBM stamp.

Motion language: progressive pen strokes (`stroke-dasharray` draw), stamp opacity, county-dot pulse. No attractors, metaballs, Fourier epicycles, or glass neon.

### Shadrack Lab (interactive)

`https://shadrackb1.github.io/playground/lab.html` — full-viewport canvas, glass HUD only for chrome.

Biomes: flow field (curl noise + cursor vortex), particle life (4 species), attractor (Thomas / Lorenz on hold), Chladni sand, Julia (`c` on cursor), soft bodies. Keys `1`–`6`. Idle auto-drift. `prefers-reduced-motion` lowers work.

### README tiers

| Tier | Bar |
| --- | --- |
| A Flagship | Dossier: problem, hard constraint, flow, stack, run, links |
| B Product | Title, one-liner, what it does, stack, run |
| C Client/demo | Title, one-liner, status, stack |
| D Archive | Point description at canonical; no content rewrite required |

Canonical map: KSAS←KSASV1.x/ksas-archive; juriscore←Juslriscore; mingle-app←MingleKe*; obomocare-live←obomocare-site/app/v1; UniHUbKe←Unihub/KabuHostels; KABU-AI←KABU-AI-V2/kabu-ai-v1; RAWLINE←RAWLINE-* / rawline-dots; Receipt-2.0←receipt-; Mati-Foundation←maty-foundation-; Friendsforjustice←Friends-for-justice; bar-kitchen←generalis-; primegatesinsurancecompany←primegates-*; live←live-b. Jewellery pair left active (different brands).

### Metadata contract

Non-empty description on every public repo; 3–8 controlled topics; homepage when a live URL is known.

### Testing boundary

Live lab 200 + brand; profile README strings; archive count 26; sample Tier A/B remote match; no bare `wob` in lab soft-bodies.

## [S3] Out of Scope

- Deleting any repository.
- Renaming repositories (recommendations only).
- Application code changes beyond README/docs/assets for the dossier.
- Expanding private repos’ public exposure.
- Contribution-graph gaming.

## Tasks

- [x] T1: Rebuild profile visual assets in field-notebook palette — acceptance: wobbly ink diagram, stamp, no trophy widgets (covers: S2)
- [x] T2: Rewrite profile README to constraint-first brand + lab CTA — acceptance: brand line, lab table, flagship/index sections (covers: S2; depends: T1)
- [x] T3: Tier A READMEs including research-in-a-stick — acceptance: dossier README on each flagship (covers: S2)
- [x] T4: Tier B/C READMEs across remaining public repos — acceptance: every non-archived public repo has README (covers: S2)
- [x] T5: Metadata pass — acceptance: non-empty descriptions; key topics (covers: S2)
- [x] T6: Archive duplicates per map — acceptance: 26 archived; canonicals active (covers: S2)
- [x] T7: Cleanup report — acceptance: reports/cleanup-report.md lists archives and renames (covers: S2; depends: T6)
- [x] T8: Live verification — acceptance: lab + profile + sample repos match claims (covers: S2; depends: T2, T3, T4)
- [x] T9: Interactive lab with six cursor biomes — acceptance: lab.html 200, six systems, keyboard switch (covers: S2)
- [x] T10: De-AI animations after review/user feedback — acceptance: no neon attractor/Fourier/metaball chrome on profile (covers: S2)
- [x] T11: Fix lab soft-bodies crash + Julia DPR — acceptance: `o.wob` on blob; no bare `wob` ref (covers: S2)
