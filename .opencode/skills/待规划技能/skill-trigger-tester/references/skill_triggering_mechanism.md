# Opencode Skill Triggering Mechanism

This document explains how opencode determines when to trigger a skill based on user input.

## How Skill Triggering Works

Opencode uses the skill's description field in the YAML frontmatter of SKILL.md as the primary mechanism for determining when to trigger the skill. The description should clearly state:

1. What the skill does
2. Specific contexts or trigger phrases for when to use it

## Best Practices for Skill Descriptions

To ensure reliable triggering:

1. **Include concrete examples**: Mention specific phrases users might say
2. **Be comprehensive**: List all common trigger variations
3. **Use natural language**: Write as users would actually speak
4. **Include action verbs**: Start descriptions with what the skill enables users to do

## Testing Approach

When testing skill triggers, consider:

1. **Direct matches**: Exact phrases from the skill description
2. **Variations**: Different wording that means the same thing
3. **Edge cases**: Phrases that might accidentally trigger the skill
4. **Negative cases**: Phrases that should NOT trigger the skill

## Example

For a docx skill, a good description might be:
```
description: Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Codex needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks
```

This description would trigger for phrases like:
- "Help me edit this Word document"
- "I need to create a new docx file"
- "Can you add comments to this document?"
- "Please turn on track changes"

But would NOT trigger for:
- "How do I format text in HTML?"
- "Create a markdown heading"
- "What's the difference between PDF and DOC?"