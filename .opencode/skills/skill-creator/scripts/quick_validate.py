#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    lines = content.splitlines()
    has_sop_router = any((skill_path / "references").glob("sop-*.md"))
    if has_sop_router and len(lines) > 300:
        return False, f"SKILL.md is too long ({len(lines)} lines). Maximum is 300 for SOP-routed skills."

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    # For execution-model skills, require SOP routing instead of single-file drafts.
    references_dir = skill_path / "references"
    sop_files = sorted(references_dir.glob("sop-[0-9][0-9]-*.md")) if references_dir.exists() else []
    has_execution_router = all(section in content for section in ["执行模型", "核心契约", "资源索引"])
    if has_execution_router and not sop_files:
        return False, "Execution-model skills must include numbered SOP files under references/"

    # For SOP-routed skills, require contiguous numbering and real relative markdown references.
    if sop_files:
        sop_numbers = []
        for sop_file in sop_files:
            match = re.match(r"^sop-(\d+)-", sop_file.name)
            if not match:
                continue
            sop_numbers.append(int(match.group(1)))
        sop_numbers.sort()
        expected = list(range(sop_numbers[0], sop_numbers[0] + len(sop_numbers)))
        if sop_numbers != expected:
            return False, f"SOP numbering must be contiguous: found {sop_numbers}, expected {expected}"

    # Require the router shape for SOP-routed skills.
    if sop_files:
        required_sections = ["执行模型", "核心契约", "资源索引"]
        for section in required_sections:
            if section not in content:
                return False, f"Missing required section in SKILL.md: {section}"
        required_contract_markers = ["todo/status", "SOP", "round", "loop", "dialectical"]
        for marker in required_contract_markers:
            if marker not in content:
                return False, f"Missing required execution-model marker in SKILL.md: {marker}"
        if len(sop_files) < 2:
            return False, "SOP-routed skills must have at least two numbered SOP files"
        if not ("派发" in content and "代理" in content and "SOP" in content):
            return False, "Missing explicit agent-dispatch instruction in SKILL.md"
        if "按需派发代理执行" in content:
            return False, "Avoid vague delegation wording; use explicit conditions or explicit delegation nodes"
        if "sop-0" not in content:
            return False, "Missing explicit SOP node references in SKILL.md execution model"
        if not re.search(r"sop-0\d-", content):
            return False, "Missing concrete numbered SOP node reference in SKILL.md"
        if content.count("任务依赖树") > 1 and "choose 1..n" not in content:
            return False, "Execution model should select among base models, not flatten them into one undifferentiated block"

    # Check for obvious relative markdown references inside SKILL.md.
    relative_refs = set(re.findall(r"`([^`]+\.md)`", content))
    for ref in sorted(relative_refs):
        if "<" in ref or ">" in ref:
            continue
        if ref.startswith(("http://", "https://")):
            continue
        ref_path = (skill_path / ref).resolve()
        try:
            ref_path.relative_to(skill_path.resolve())
        except ValueError:
            continue
        if not ref_path.exists():
            return False, f"Referenced markdown file does not exist: {ref}"

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
