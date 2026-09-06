# CLI Command Spec Template

状态：运行时产物模板，供目标项目实现 CLI 前复制或引用。

```text
Bin name: <resolved from package/build config>
Entity: projects | habits | members | deliverables | teams | <custom>
Source of truth: <file/db/service/store path>
Schema version: <version>

Commands:
  <bin> <entity> list --format json|table --project <id>
  <bin> <entity> get <id> --format json
  <bin> <entity> create --input <json-file|-> --dry-run
  <bin> <entity> update <id> --input <json-file|-> --dry-run
  <bin> <entity> delete <id> --dry-run --yes
  <bin> <entity> export --output <path> --format json
  <bin> <entity> import --input <path> --dry-run --conflict skip|overwrite|merge|rename
  <bin> doctor --json

Exit codes:
  0 success
  1 validation or user input error
  2 partial failure
  3 environment/configuration error
  4 data consistency error

Verification:
  Source smoke: <command>
  Build: <command>
  Installed/package smoke: <command>
```
