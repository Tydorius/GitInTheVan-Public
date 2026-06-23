# GitInTheVan Cantrip Templates

A collection of Cantrip templates for GitInTheVan's enhanced lorebook system. Each template addresses a different use case. Pick the one that fits your scenario, or combine ideas from several. Note that these are converted from my JAI Script templates. Some of their features (Persistent memory, context management, etc) may not be necessary within GitInTheVan due to native context control I'm building into the platform.

## Templates

### [Complex Lorebook](Complex_Lorebook_Template.js) | [README](Complex_Lorebook_Template_README.md) | [GitInTheVan Link](https://gitinthevan.com/characters/addf68e5-4809-4c15-b81e-06e5cbc9ac93_character-complex-lorebook-template)

Full-featured dynamic cantrip with cascading activation, timeline events, stat-based reactions, priority ordering, and smart filtering. Best for worldbuilding-heavy scenarios with many lore entries that need to interact with each other.

### [Adaptive Lorebook](Adaptive_Lorebook_Template.js) | [README](Adaptive_Lorebook_Template_README.md)| [GitInTheVan Link](https://gitinthevan.com/characters/1411c045-6bc2-434e-b8f6-42998e8c74fc_character-token-count-conscious-lorebook-template)

Token-aware cantrip that automatically scales detail between full, summary, and bullet versions based on mention frequency and token budget. Best for scenarios with lots of lore entries where context window space is the primary concern.

### [Progressive Sentence](Progressive_Sentence_Lorebook_Template.js) | [README](Progressive_Sentence_Lorebook_Template_README.md)| [GitInTheVan Link](https://gitinthevan.com/characters/97aeaa58-0a42-49ce-94e9-fd1df396ff18_character-token-count-aware-variant-lorebook-template)

Sentence-level context builder with priority tiers, configurable history scope per subject, and round-robin allocation within tier budgets. Best when you need fine-grained control over exactly which sentences appear and in what order.

### [TimeDelay Cantrip](TimeDelay_Cantrip_Template.js) | [README](TimeDelay_Cantrip_Template_README.md)| [GitInTheVan Link](https://gitinthevan.com/characters/6387ad41-7000-4734-bc66-e57abdf41b27_character-time-delay-Cantrip-template-investigations-delayed-clues-etc)

Progressive disclosure through message count thresholds, hour-based timeline progression, canon count tracking, hidden clue embedding, and conditional story branching. Best for investigation scenarios with time-based pacing.

### [Persistent Memory Flags](Persistent_Flags_Lorebook_Template.js) | [README](Persistent_Flags_Lorebook_Template_README.md)| [GitInTheVan Link](https://gitinthevan.com/characters/e10c6c40-e665-44fe-99c8-e0f1e98abefb_character-persistent-memory-Cantrip-template)

Hex-based flag string system for tracking discrete story states across sessions. Includes anti-cheat validation, save system support for cross-character continuity, and dynamic instruction generation. Best for scenarios that need state tracking without continuous numerical values.

### [Hidden Persistent Memory](Hidden_Persistent_Memory_Template.js) | [README](Hidden_Persistent_Memory_Template_README.md) | [GitInTheVan Link](https://gitinthevan.com/characters/34ce8756-6ab5-4870-9f75-0ae91045041a_character-hidden-persistent-memory-lorebook-template)

Zero-width unicode character encoding for invisible state persistence between Cantrip instances. Tracks weather, location (with scene shift detection), emotional state (16-bit bitmask), inventory (bitfield), schedule/day counter, and character presence. Each component is independently toggleable. Best for scenarios that need persistent state tracking without visible artifacts in the chat.

### [Anti-Omniscience Investigation](Anti_Omniscience_Investigation_Template.js) | [README](Anti_Omniscience_Investigation_Template_README.md)|[ GitInTheVan Link](https://gitinthevan.com/characters/6b680acf-165e-4584-b9be-ce05badcc2ba_character-anti-omniscience-investigation-lorebook-template)

Flag-gated content system that prevents LLM omniscience by locking information behind hex flag requirements, injecting explicit anti-omniscience behavioral instructions, and eliminating meta-labels and foreshadowing. Best for mystery and investigation scenarios where spoilers ruin the experience.

### [Multiple Character](Multiple_Character_Template.js)| [README](Multiple_Character_Template_README.md) | [GitInTheVan Link](https://gitinthevan.com/characters/596dc3a1-6b62-4774-98db-6d3e9c05d7e2_character-multiple-character-drop-in-drop-out-lorebook-template)

Drop-in/drop-out character management that dynamically includes or excludes character context based on who is mentioned in recent messages. Best for group scenarios with several characters who take turns being active.

### [Context Aware Multiple Character](Context_Aware_Multiple_Character_Template.js)| [README](Context_Aware_Multiple_Character_Template_README.md) | [GitInTheVan Link](https://gitinthevan.com/characters/ccff2be4-8cad-4b03-a9de-8ea7d5d58f73_character-context-aware-multiple-character-lorebook-template)

Combines drop-in/drop-out character management with adaptive detail levels. Each character category (personality, appearance, dialog) scales between full, limited, and summary versions based on per-category token budgets. Includes support for progressive sentence categories with round-robin allocation. Best for scenarios with multiple characters where context window space needs careful management.

## [General Debug Reference](PropertyExploration.js) | [README](PropertyExploration_README.md) | [GitInTheVan Link](https://gitinthevan.com/characters/7d0fda82-058a-4dfc-830c-9e8998d633a6_character-general-debug-lorebook-template)

Utility Cantrip that logs available properties on the `context` object. Useful for debugging and discovering what the Cantrips API exposes.

## Copy Directly on GitInTheVan

All templates are available on my GitInTheVan profile, ready to copy into your own Cantrips.


[@Tydorius](https://gitinthevan.com/profiles/0f618e4a-4d83-49da-969b-aba188761259_profile-of-tydorius)

## Support

If these templates are useful to you, consider buying me a coffee:
[https://ko-fi.com/tydorius](https://ko-fi.com/tydorius)
