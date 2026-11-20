# MUD World Engine

A portable, GitInTheVan `0.42.1`-idiomatic spatial world engine using the **Static Base Lorebook + Sparse `chat_data` Delta Overlay** pattern.

An HTML version of this guide is available at [`MUD_World_Engine_README.html`](MUD_World_Engine_README.html).

## Architecture

- **Static Base Lorebook (`lorebooks/MUD_World_Example.json`)** — Stores immutable room definitions as compact JSON entries (`overworld:a1`..`c2`, plus interior sub-grid `tavern_f1:a1`..`a2`). Imported **inactive** so GitInTheVan does not keyword-dump the whole map into context.
- **Sparse `chat_data` Delta Overlay (`cantrips/MUD_World_Engine.json`)** — Tracks only what changed in the current chat:
  - Global state: `mud_loc`, `mud_prev_loc`, `mud_time`, `mud_weather`, `mud_last_img`, `mud_images_enabled`
  - Per-cell deltas (`cell:<loc>`): `events`, `npcs` (status/notes), `objects` (description overrides), and `flags`

At **Pre-Driver**, the engine reads the current cell from the linked Lorebook, merges any `cell:<loc>` delta, generates a deterministic **ASCII mini-map** (`[@]` = you, `[.]` = connected room), and injects `[WORLD STATE]` into the scenario. Dead or departed NPCs are moved into `[NO LONGER HERE (DO NOT REVIVE)]` so the model never hallucinates them back.

## Setup

1. **Import the Base Lorebook (Inactive)**
   - In GitInTheVan, go to **Lorebooks → Import JSON** and import `lorebooks/MUD_World_Example.json`.
   - Keep it **inactive** (`is_active: false`). The cantrip reads it directly via `lorebook_reads`.
2. **Import & Activate the Cantrip**
   - Import `cantrips/MUD_World_Engine.json` (or install both from the Pack Browser).
   - Verify **Lorebook Reads** includes `MUD World Example`.
   - Verify **Pre-Driver**, **Driver-Callable**, and **Post-Navigator** hooks are enabled, and **Response Tags** lists `mud_move`, `mud_delta`, `mud_time`.
   - Activate the cantrip.

## Features

- **Swipe / Regenerate Safety**: Uses `context.request.is_regenerate` to restore `mud_prev_loc` before re-running, preventing double-movement on swipes.
- **Driver-Callable Mid-Turn Tools**: The LLM can call `<call:mud_world_engine action="move" dir="E" />` or `<call:mud_world_engine action="look" target="fountain" />` to resolve movement or inspection within the same turn.
- **Post-Navigator Response Tags**: Hidden tags emitted by the model (`<mud_move>`, `<mud_time>`, `<mud_delta>`) are stripped before reaching the user and applied to `context.chat_data` on the same turn.
- **Optional Location Images**: Set `mud_images_enabled` to `true` in `chat_data` and populate `images.day` / `images.night` (or `day_rain`, etc.) in your Lorebook cells. When the resolved URL changes, the engine prepends `![Location Name](url)` to the response.

## Creating Custom Worlds

Use [`MUD_World_Generator_Prompt.md`](MUD_World_Generator_Prompt.md) to generate your own grid worlds and interior sub-grids with any LLM in GITV Lorebook import format. If you name your custom Lorebook something other than `MUD World Example`, update `BOOK_NAME` in the cantrip's code and its `lorebook_reads` list.
