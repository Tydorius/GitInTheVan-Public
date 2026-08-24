# Overthink Writing Pipeline

A Map that splits creative writing into separate model calls — **Plan → Draft →
Critique → Polish** — so a small instruct-tuned model spends its reasoning budget
somewhere the reader never sees, and writes prose somewhere it does.

An HTML version of this guide is available at
[`Overthink_Writing_Pipeline_README.html`](Overthink_Writing_Pipeline_README.html).

## What problem this solves

Recent small models follow instructions well, hold long contexts, and write flat.
That flatness is an alignment artefact: the model has been trained toward the
statistical middle of human-approved text, so it reaches for *tapestry*,
*testament*, *delve*, and endings that tie off neatly.

Extended reasoning helps — but only if the reasoning and the prose happen in
**separate calls**. Ask one call to think hard and then write, and the analytical
register bleeds into the prose: you get a well-planned scene written like a book
report. Splitting the stages is the whole trick.

The three levers this map pulls, in order of how much they matter:

1. **A style anchor.** Small models are stylistic chameleons. Roughly a thousand
   words of prose you actually like, injected near the end of context, shifts
   vocabulary and rhythm more than any instruction will. This is the setting to
   change first if the output still reads flat.
2. **Separated planning.** A dedicated call that outputs *only* a brief, never a
   sentence of the scene.
3. **Named refusals over banned words.** Telling a model "do not write *delve*"
   makes prose stilted, because it spends attention dodging a word. The planning
   stage instead names three clichés *specific to this scene* and says what it
   will do instead — a constraint with somewhere to go.

## Files

| File | Purpose |
|------|---------|
| `maps/overthink_writing_pipeline.json` | The four-stage map. Requires `max_map_stages` ≥ 4. |
| `maps/overthink_writing_pipeline_3stage.json` | Three-stage variant that runs at the stock cap. |
| `skills/scene_planning_discipline.json` | Planning rules (skill) |
| `skills/prose_execution_rules.json` | Drafting rules (skill) |
| `skills/anti_llmism_checklist.json` | Line-editing checklist (skill) |
| `skills/style_anchor_sample.json` | Style anchor (**sample** — placeholder, replace it) |

The map files are **self-contained**: importing one creates the map *and* the
skills and samples it needs. The standalone `skills/` files are the same content,
published separately so you can attach them to an endpoint or another map without
importing a whole pipeline.

## Setup

### 1. Install or import the map

Either route works:

- **Pack Browser** — add this repo as a content pack and install
  *Overthink Writing Pipeline*. The map and its four skills are created for you.
  Like every pack resource it installs **disabled**, so activate it on the Maps
  page afterwards.
- **Maps → Import JSON → Load from File** — pick the map file directly. Use this
  route when you want to choose how duplicate resources are handled:
  - **Keep Both** (default) — always makes fresh copies of the skills. Safe.
  - **Reuse** — links to your existing same-named skills. Pick this if you have
    already replaced the Style Anchor and are re-importing.
  - **Overwrite** — updates your same-named skills in place. This *will* replace
    a Style Anchor you have customised.

### 2. Raise the stage cap (four-stage variant only)

**Admin → Global Caps → Max Map Stages → 4.**

`max_map_stages` defaults to 3. A map with more stages than the cap is silently
truncated at request time — the extra stages just never run, and the only sign is
a line in the log. If you would rather not touch admin settings, import the
three-stage variant instead.

### 3. Tag your endpoints

Each stage routes by **endpoint tag**, not by a pinned endpoint:

| Stage | Tag | Wants |
|-------|-----|-------|
| Architect | `planner` | A reasoning model. This is where the deliberation goes. |
| Prose | `drafter` | Whatever writes best. Reasoning is not required here. |
| Line Editor | `critic` | Instruction-following matters more than prose ability. |
| Final Pass | `drafter` | Same model as the drafter, by design. |

Set the tag in **Endpoints → (endpoint) → Role Tag**. Pointing all three tags at
one endpoint is fine and is the right way to start.

This indirection is the point of the design. When you swap Qwen 3.8 for whatever
lands next quarter, you re-point a tag — the map, the skills, and the anchor are
untouched. Multiple endpoints sharing a tag also give you failover for free.

### 4. Replace the Style Anchor

**Skills → Style Anchor → Edit.** Replace the placeholder with 800–1500 words of
prose whose texture you want.

This is not optional. It ships as a placeholder because an anchor written by a
language model would anchor the pipeline to exactly the register it exists to
escape. Notes on choosing one are in the placeholder text itself.

### 5. Optional — add a Forbidden Words list

**Forbidden Words** → enable, then add the phrases you never want to see:
*delve, tapestry, testament, a symphony of, the air was thick with*. Regex is
supported.

The list is not shown to the writing stages. GitInTheVan scans each stage's
output and hands the hits to the next stage, so the editor fixes them and the
drafter never writes around them. See *Things worth knowing* below.

### 6. Activate

Either set the map as your default (**Settings → Default Map**) or give it a tag
on the Maps page and use that tag in your persona or first message.

## How it runs

```
User message
  │
  ├─ Stage 1  Architect     [planner]  → THE PLAN
  │             names 3 clichés to refuse, maps subtext,
  │             sensory register, shape, what stays unresolved
  │
  ├─ Stage 2  Prose         [drafter]  → THE DRAFT
  │             + <writing_sample> style anchor
  │             prose only, no analysis
  │
  ├─ Stage 3  Line Editor   [critic]   → NUMBERED EDITS
  │             quotes offending text, gives replacements
  │
  └─ Stage 4  Final Pass    [drafter]  → FINAL PROSE  ← the reader sees only this
                applies the edits, keeps the ending where it was
```

Stages 1–3 use `output_mode: sanitize`, which hands each output to the next stage
wrapped as `[STAGE N OUTPUT: name] … [/STAGE OUTPUT]` — labelled, so the final
stage can tell the plan from the draft from the critique. Nothing before stage 4
reaches the client.

## Things worth knowing

**It costs four calls.** Latency is roughly four times a single turn, and tokens
scale similarly. This is a deliberate trade of throughput for quality; it is not
a good fit for fast back-and-forth roleplay.

**Forbidden Words are flagged per stage, not enforced up front.** Add your list
under **Forbidden Words** and enable it. Each stage's output is scanned, and any
hits are handed to the *next* stage as a
`[FORBIDDEN WORDS FLAGGED IN STAGE N OUTPUT]` block naming the exact phrases.

The Architect and the Drafter never see the list. That is deliberate: a writer
spending attention dodging banned words produces stilted prose, which is a worse
failure than the one you were fixing. The Line Editor stage is told to take
flagged phrases first, and the Final Pass is told they are non-negotiable.

The consequence is that a word introduced by the *last* stage has nothing after
it to catch the fix — GitInTheVan logs a warning when that happens. If it matters
to you, keep the editing stage last.

**Reasoning output.** `reasoning_content` from a stage is dropped before the next
stage — only the message content carries forward, which is what you want. If your
planner emits inline `<think>` tags in its content instead, and you do not want
them reaching the client, set **Settings → Preserve Thinking → off**.

**Verification is off on every stage.** Under Maps, a failing stage verification
logs a warning and continues rather than regenerating, so it buys little here. The
Line Editor stage *is* the quality gate, and unlike a verifier it can act.

## Tuning

Change one thing at a time, in this order:

1. **The Style Anchor.** Everything else is a rounding error next to this.
2. **The planner model.** This is the stage that most rewards a reasoning model.
   Point `planner` somewhere else and re-run the same prompt.
3. **The Architect's refusal count.** Three is a starting point. More refusals
   push harder but start constraining the scene into a corner.
4. **The checklist.** Your LLMisms are not everyone's. Edit
   `skills/anti_llmism_checklist.json` — or the imported Skill — to name the tics
   your model actually produces.

If the prose comes out stilted rather than flat, you have over-constrained it:
trim the checklist before you add to it.

## Three-stage variant

`overthink_writing_pipeline_3stage.json` merges the Line Editor and Final Pass
into one *Editor & Polish* stage that critiques silently and emits only the
revised scene. It runs at the stock cap of 3 with no admin change.

It is genuinely weaker. A model that judges and applies in the same breath tends
to under-cut — it finds problems it then declines to fix. Use it to try the
pipeline out, and move to the four-stage version if it earns its keep.
