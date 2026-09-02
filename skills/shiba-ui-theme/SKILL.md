---
name: shiba-ui-theme
description: Design or restyle a UI so its visual language comes from what the project is actually about, instead of defaulting to generic style -- vivid and expressive for an anime project, pitch-toned and kinetic for a football one, and so on. Use before or during any UI/visual design work (artifacts, apps, dashboards, decks) on a project with a distinctive subject, genre, or fandom.
---

# UI Theme Fit

Generic style is the default failure: a football tracker and a tax form rendered in the same neutral blue-and-white read as the same product. This skill is the step that happens *before* layout — pull a theme profile out of the project's actual subject, then let that profile drive every visual decision that follows.

## 1. Find the subject signal

Don't guess the theme from the skill name or the framework — read what the project is actually *about*: its README, its content, its data, sample entries, or the user's own description of it. A "tracker" app could be for anime episodes, football fixtures, or invoices; each deserves a completely different look.

If the subject is genuinely generic (an internal admin tool, a CRUD form with no fandom or domain flavor) — don't force a theme onto it. Fall back to the neutral baseline in the `dataviz`/`artifact-design` skills and stop here.

## 2. Build the theme profile

For the subject found in step 1, work out, in this order:

- **Mood** — 2-3 adjectives a fan of the subject would use to describe it (e.g. anime: vivid, expressive, energetic; football: kinetic, competitive, pitch-side).
- **Palette cues** — colors the subject is *known for*, not just "colors that go with the mood." Football pulls pitch green, chalk white, kit colors; anime pulls saturated primaries and high-contrast accent pops; a noir detective project pulls desaturated ambers and deep shadow.
- **Motifs** — concrete visual objects from the domain worth echoing structurally, not just decoratively: a scoreboard/stat-card treatment and pitch-line dividers for football; speed lines, halftone dots, or panel-gutter framing for anime; not a mascot slapped in a corner.
- **Type** — a pairing that matches the domain's own printed material (bold condensed sports-broadcast numerals; playful rounded or display faces for anime; a slab serif for a noir project) over a generic system-UI font stack.
- **Voice** — do labels/copy read like the domain talks (match scores and "FT", episode/season labels, chapter numbers) or like generic app chrome ("Item 1", "Submit")?

Write this profile down explicitly before touching layout — it's the thing every subsequent design decision gets checked against.

## 3. Apply it, then guard it

Translate the profile into concrete tokens (hex values, a type stack, spacing/motif rules) and apply them consistently across the surface, the way `dataviz`'s palette formula or `artifact-design`'s fundamentals expect a token set to arrive. Two guardrails hold regardless of theme:

- **Readability survives the theme.** Contrast, hierarchy, and legibility are non-negotiable — a themed palette that fails contrast gets adjusted within the theme's hue family, never abandoned for generic colors.
- **Reference over cliché.** One well-placed motif that a fan of the subject would recognize beats five generic ones (jersey stripes, not a random soccer-ball emoji; a manga panel gutter, not a random anime character sticker).

## 4. Hand off to the builder

Once the profile and tokens exist, build with whichever skill matches the output: `design` for a canvas mockup, `dataviz` for charts/dashboards (its palette validator still applies — swap its placeholder values for the theme palette from step 2), or `artifact-design` for a general Artifact page. This skill decides *what* the visual language is; those decide *how* to build it correctly.
