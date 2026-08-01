# Development

This directory records development rules, commands, testing policy, directory governance, and submodule handling for maop's OpenCode capability surface.

## Commands

| Task | Command | Source |
| --- | --- | --- |
| Install OpenCode capability dependencies | `npm install --prefix .opencode` | `.opencode/package.json` |
| Validate project OpenCode JSON | `node -e "JSON.parse(require('fs').readFileSync('.opencode/opencode.json','utf8')); console.log('ok')"` | `.opencode/opencode.json` |
| List skills | `Get-ChildItem -Recurse -Filter SKILL.md .opencode/skills` | `.opencode/skills/` |
| Run automated tests | `待补充` | No confirmed test script yet. |

## Index

- `submodules-index.md`: Long-lived submodule registry and boundary notes.
