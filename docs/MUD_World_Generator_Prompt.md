# MUD World Generator Prompt

Copy and paste the prompt below into ChatGPT, Claude, or Gemini to generate a custom spatial world directly in **GitInTheVan Lorebook import format**, ready to import and run with `MUD_World_Engine.json`.

---

## Copy-Paste Prompt

```text
You are generating a spatial MUD world in GitInTheVan Lorebook JSON import format.

Output ONLY valid JSON (no markdown commentary outside the JSON) matching this exact top-level structure:
{
  "name": "<World Name>",
  "description": "<Short description of the world>",
  "is_active": false,
  "entries": [ ... ]
}

Each item in "entries" represents ONE room/cell and must follow this exact structure:
{
  "name": "<cell_id>",
  "keys": ["<cell_id>", "<Location Name>"],
  "secondary_keys": [],
  "content": "<ESCAPED COMPACT JSON STRING>",
  "position": "before_last_message",
  "insertion_order": 10,
  "is_constant": false,
  "is_selective": false,
  "is_disabled": false,
  "character_limit": 0
}

The "content" field MUST be a single-line escaped JSON string representing this exact flat schema (keep each cell's content between 300 and 500 characters):
{
  "id": "<map>:<col><row>",
  "map": "<map_id>",
  "x": 0,
  "y": 0,
  "name": "<Location Name>",
  "desc": {
    "day": "<1-2 concise atmospheric sentences for daytime>",
    "night": "<1-2 concise atmospheric sentences for nighttime>"
  },
  "exits": {
    "E": "<target_cell_id>"
  },
  "objects": {
    "<object_id>": "<short description>"
  },
  "npcs": {
    "<npc_id>": {
      "name": "<Name>",
      "role": "<Role>",
      "desc": "<short appearance/behavior>"
    }
  },
  "images": {
    "day": "",
    "night": ""
  }
}

Strict rules:
1. Coordinate convention: x increases East (a=0, b=1, c=2...), y increases South (1=0, 2=1, 3=2...). Example: (0,0) = "overworld:a1", (1,0) = "overworld:b1", (0,1) = "overworld:a2".
2. Interior sub-grids: use a separate map id (e.g., "inn_f1:a1", "crypt_b1:a1") and connect them to the overworld with "IN" and "OUT" exits.
3. 100% symmetric exits:
   - If A has "E": B, then B MUST have "W": A.
   - If A has "N": B, then B MUST have "S": A.
   - If A has "IN": B, then B MUST have "OUT": A.
   - Every exit target MUST exist as an entry in "entries".
4. Valid JSON: ensure all quotes inside "content" are properly escaped so the outer JSON parses cleanly.

Now generate a world with the following setting and size:
- Setting: [DESCRIBE YOUR SETTING HERE, e.g., "A foggy coastal fishing town with a lighthouse, docks, and an underground smugglers' cave"]
- Overworld grid: [e.g., 3x2 = 6 cells]
- Interior sub-grids: [e.g., 1 interior with 2 cells connected via IN/OUT]
```
