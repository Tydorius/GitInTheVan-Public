"""Convert GitInTheVan-Public repo from raw .js files to content pack format.

- Converts each .js cantrip to .json with metadata
- Removes JanitorAI references from all files
- Creates descriptions.json manifest
- Updates docs and skills references
"""

import json
import re
from pathlib import Path

REPO = Path(r"E:\github\GitInTheVan-Public")

CANTRIP_META = {
    "Dice_Controller.js": {
        "name": "Dice Controller",
        "description": "Intercepts /roll commands and dice requests. Supports polyhedral dice, exploding dice, Savage Worlds Aces/Wild Die. Injects formatted results into scenario.",
        "llm_instructions": "Call this tool to roll dice. Args: dice (e.g. '2d6+3', '1d20', '4d6!'). Example: <call:dice_controller dice=\"2d6+3\">",
        "version": "1.0.0",
        "tags": ["utility", "dice", "gaming"],
    },
    "Context_Control_Template.js": {
        "name": "Context Control Template",
        "description": "Master context management script. Provides /maxtokens command for selecting context window size, then calculates and injects per-script token budgets for all active content scripts.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["utility", "context", "budget"],
    },
    "Context_Control_Awareness_Template.js": {
        "name": "Context Control Awareness Template",
        "description": "Companion script that reads token budgets injected by the Context Control Template. Adapts lore detail levels (full/summary/bullets) to stay within the per-script allocation.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["utility", "context", "budget"],
    },
    "Adaptive_Lorebook_Template.js": {
        "name": "Adaptive Lorebook Template",
        "description": "Manages token usage by dynamically adjusting lore detail level (full/summary/bullet) based on keyword mention count and relevance.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["lorebook", "adaptive", "tokens"],
    },
    "Complex_Lorebook_Template.js": {
        "name": "Complex Lorebook Template",
        "description": "Complex dynamic lorebook foundation with cascading keyword triggers, timeline events, stat parsing, and priority-based lore ordering.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["lorebook", "complex", "dynamic"],
    },
    "Multiple_Character_Template.js": {
        "name": "Multiple Character Template",
        "description": "Basic drop-in/drop-out character management. Characters included dynamically based on recent context mentions via regex matching.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["character", "multi-character"],
    },
    "Context_Aware_Multiple_Character_Template.js": {
        "name": "Context Aware Multiple Character Template",
        "description": "Advanced drop-in/drop-out character management with adaptive detail levels (full/limited/summary) that scale to the available token budget.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["character", "multi-character", "adaptive"],
    },
    "Advanced_Faction_Management_Template.js": {
        "name": "Advanced Faction Management Template",
        "description": "Two-mode faction governance system (roleplay + management interface). Tracks diplomacy, resources, projects, and population with persistent state.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["faction", "governance", "persistent"],
    },
    "Hidden_Persistent_Memory_Template.js": {
        "name": "Hidden Persistent Memory Template",
        "description": "Modular persistent state system using zero-width unicode for invisible data transmission. Tracks weather, location, and emotional state across messages.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["memory", "persistent", "state"],
    },
    "Persistent_Flags_Lorebook_Template.js": {
        "name": "Persistent Flags Lorebook Template",
        "description": "Hex-based flag system for tracking persistent state across sessions. Includes anti-cheat validation and dynamic lore activation based on flag state.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["memory", "flags", "persistent"],
    },
    "Progressive_Sentence_Lorebook_Template.js": {
        "name": "Progressive Sentence Lorebook Template",
        "description": "Builds context sentence-by-sentence by priority tiers (HIGH/MEDIUM/LOW) instead of switching between full/summary/bullet versions.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["lorebook", "progressive", "adaptive"],
    },
    "Anti_Omniscience_Investigation_Template.js": {
        "name": "Anti-Omniscience Investigation Template",
        "description": "Progressive disclosure system preventing the LLM from knowing things it shouldn't. Uses flag-gated content unlocking with strict information isolation.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["lorebook", "investigation", "progressive"],
    },
    "TimeDelay_Script_Template.js": {
        "name": "Time Delay Script Template",
        "description": "Progressive disclosure via message-count thresholds. Tracks hours, canon count, and timeline events. Embeds hidden clues that unlock at specific story beats.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["lorebook", "timeline", "progressive"],
    },
    "PropertyExploration.js": {
        "name": "Property Exploration",
        "description": "Debug and utility script that inspects context.character and context.chat object properties and types. Outputs to console.log for debugging.",
        "llm_instructions": "",
        "version": "1.0.0",
        "tags": ["utility", "debug"],
    },
}

JANITORAI_PATTERNS = [
    (r"\bJanitorAI\b", "GitInTheVan"),
    (r"\bJANITOR AI\b", "GITINTHEVAN"),
    (r"\bJanitor AI\b", "GitInTheVan"),
    (r"\bjanitorai\b", "gitinthevan"),
    (r"\bNine API v1\b", "GitInTheVan API v1"),
    (r"\bNine API\b", "GitInTheVan API"),
    (r"\bJLLM\b", "LLM"),
]


def remove_janitorai_refs(text: str) -> str:
    for pattern, replacement in JANITORAI_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text


def convert_js_to_json(js_path: Path, meta: dict) -> dict:
    code = js_path.read_text(encoding="utf-8")
    code = remove_janitorai_refs(code)
    return {
        "name": meta["name"],
        "description": meta["description"],
        "llm_instructions": meta["llm_instructions"],
        "code": code,
        "version": meta["version"],
        "tags": meta.get("tags", []),
        "is_active": False,
        "run_pre_driver": True,
    }


def main():
    cantrips_dir = REPO / "cantrips"
    files_manifest = []

    for js_file in sorted(cantrips_dir.glob("*.js")):
        stem = js_file.name
        meta = CANTRIP_META.get(stem, {
            "name": js_file.stem.replace("_", " "),
            "description": "",
            "llm_instructions": "",
            "version": "1.0.0",
            "tags": [],
        })

        cantrip_data = convert_js_to_json(js_file, meta)

        json_name = js_file.stem + ".json"
        json_path = cantrips_dir / json_name
        json_path.write_text(json.dumps(cantrip_data, indent=2), encoding="utf-8")

        files_manifest.append({
            "path": f"cantrips/{json_name}",
            "type": "cantrip",
            "name": meta["name"],
            "description": meta["description"],
            "author": "Tydorius",
            "version": meta["version"],
            "updated": "2026-06-22T00:00:00Z",
            "tags": meta.get("tags", []),
            "min_gitv_version": "0.5.0",
        })
        print(f"  Converted: {stem} -> {json_name}")

    for js_file in cantrips_dir.glob("*.js"):
        js_file.unlink()
        print(f"  Removed: {js_file.name}")

    for doc_file in REPO.rglob("*.md"):
        content = doc_file.read_text(encoding="utf-8")
        cleaned = remove_janitorai_refs(content)
        if cleaned != content:
            doc_file.write_text(cleaned, encoding="utf-8")
            print(f"  Cleaned refs: {doc_file.relative_to(REPO)}")

    for doc_file in REPO.rglob("*.html"):
        content = doc_file.read_text(encoding="utf-8")
        cleaned = remove_janitorai_refs(content)
        if cleaned != content:
            doc_file.write_text(cleaned, encoding="utf-8")
            print(f"  Cleaned refs: {doc_file.relative_to(REPO)}")

    skills_dir = REPO / "skills"
    old_skill = skills_dir / "janitorai_scripts.md"
    new_skill = skills_dir / "cantrip_authoring_guide.md"
    if old_skill.exists():
        content = remove_janitorai_refs(old_skill.read_text(encoding="utf-8"))
        new_skill.write_text(content, encoding="utf-8")
        old_skill.unlink()
        print("  Renamed skill: janitorai_scripts.md -> cantrip_authoring_guide.md")

    manifest = {
        "pack_name": "GitInTheVan Public Cantrips",
        "pack_author": "Tydorius",
        "pack_version": "1.0.0",
        "pack_description": "A collection of cantrips for roleplay and creative writing with GitInTheVan. Includes dice rolling, context management, adaptive lorebooks, multi-character support, faction management, persistent memory, and progressive disclosure systems.",
        "pack_url": "",
        "files": files_manifest,
    }

    manifest_path = REPO / "descriptions.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n  Created: descriptions.json ({len(files_manifest)} files)")

    print("\nDone.")


if __name__ == "__main__":
    main()
