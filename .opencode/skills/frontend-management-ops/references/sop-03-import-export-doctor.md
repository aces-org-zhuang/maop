# SOP-03 Import Export Doctor

## Goal and scope

实现或补齐管理数据的导入、导出和 doctor 诊断能力，让用户可在安装后的 CLI 中迁移、备份、检查和定位管理域问题。

## Pre-read

1. 读取 `sop-01-domain-contract-map.md` 和 `sop-02-crud-cli-implementation.md` 的实体、schema、CLI 入口和验证状态。
2. 若要触碰真实数据路径，确认备份、dry-run 和写入授权。

## Import/export steps

1. 定义文件格式：`json` 为默认格式；可选 `csv` 只用于扁平实体，复杂关系仍以 JSON 为准。
2. 在导出中写入 `schemaVersion`、`exportedAt`、`appVersion`、`entities`、`warnings`。
3. 导入默认 `--dry-run` 先校验：schema 版本、必填字段、外键/关联、重复 id、冲突策略、未知字段。
4. 支持冲突策略：`skip`、`overwrite`、`merge`、`rename`；默认 `skip` 或 blocked，不能静默覆盖。
5. 输出导入报告：created、updated、skipped、failed、warnings、backup path、exit code。
6. 大批量导入必须分批处理并保留部分失败可追踪结果。

## Doctor steps

1. `doctor` 默认只读，不修改数据；修复动作必须显式 `doctor fix` 或 `--apply`。
2. 检查 CLI 可执行文件、版本、Node/Electron 运行时、配置路径、数据路径权限和平台路径抽象。
3. 检查每个实体 schema、重复 id、缺失关联、孤儿引用、更新时间合法性和软删除一致性。
4. 检查 IPC/preload/shared types 是否有对应契约，前端 i18n 是否三语言齐全。
5. 检查导入导出 roundtrip 样例能否通过 dry-run。
6. 输出机器可读 JSON 和简洁人类可读 summary；失败项必须给出 remediation hint。

## Write boundary

导入导出和 doctor 可以新增 CLI 子命令、schema validator、测试 fixture 和文档。默认不修改用户真实数据；自动修复必须经过 dry-run 报告和显式授权。

## Validation

验证导出文件可重新 dry-run 导入；验证 doctor 在健康样例和损坏样例上分别返回正确退出码；构建安装后运行 `doctor`、`export`、`import --dry-run`。

## RED

- 没有 schemaVersion 的导出文件。
- 导入默认覆盖数据。
- doctor 混合只读诊断和写入修复，用户无法预判副作用。
- 诊断只输出文本，无法被自动化验证消费。
