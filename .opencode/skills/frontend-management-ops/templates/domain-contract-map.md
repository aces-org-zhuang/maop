# Domain Contract Map Template

状态：运行时产物模板，用于把管理实体映射到现有代码和验证入口。

| Entity | UI path | preload/API | IPC channel | main service/store | shared type/schema | persistence | CLI command | tests | RED |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| projects | `<path>` | `<path>` | `<channel>` | `<path>` | `<path>` | `<path>` | `<bin> projects ...` | `<path>` | `<none/gap>` |
| habits | `<path>` | `<path>` | `<channel>` | `<path>` | `<path>` | `<path>` | `<bin> habits ...` | `<path>` | `<none/gap>` |
| members | `<path>` | `<path>` | `<channel>` | `<path>` | `<path>` | `<path>` | `<bin> members ...` | `<path>` | `<none/gap>` |
| deliverables | `<path>` | `<path>` | `<channel>` | `<path>` | `<path>` | `<path>` | `<bin> deliverables ...` | `<path>` | `<none/gap>` |
| teams | `<path>` | `<path>` | `<channel>` | `<path>` | `<path>` | `<path>` | `<bin> teams ...` | `<path>` | `<none/gap>` |

Notes:

- Mark missing source paths as `missing`, not inferred.
- Keep UI and CLI on the same shared type/schema.
- Add i18n namespace and locale file paths for every user-visible string.
