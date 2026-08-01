# SOP 01: Repo Foundation

## 目标

建立最小可靠代码仓基础，让项目从第一天具备 Git、README、忽略规则、环境样例和基础验证入口。

## 前置读取

- `sop-00-intake.md` 的结论。
- 已有 `README.md`、`.gitignore`、`.env.example`、`.gitmodules`。

## 执行步骤

1. 如果目标目录不是 Git 仓库，执行或建议执行 `git init`。
2. 创建或合并 `README.md`，内容只做项目入口、目录导航、常用命令占位和研究区入口，不放长设计。
3. 创建或合并 `.gitignore`。按技术栈补充常见忽略项；未知技术栈时至少包含环境文件、日志、缓存、构建产物和系统文件。
4. 创建 `.env.example` 或等价环境变量样例文件；不要创建真实 `.env`。
5. 如果项目需要 secret 扫描或安全忽略，创建 `.secretsignore.example`。
6. 如果用户明确要求许可证，创建 `LICENSE`；否则不猜测许可证类型。
7. 在 README 或 `docs/02-development/README.md` 中记录安装、构建、测试、运行命令。未知命令写 `待补充`。

## 生成或修改的文件

- `README.md`
- `.gitignore`
- `.env.example` 或技术栈等价文件
- `.secretsignore.example`，可选
- `LICENSE`，可选

## 验证方式

- `git status --short`
- 检查 README 是否指向 `docs/README.md`、研究区入口和常用命令。
- 检查 `.gitignore` 是否避免提交真实密钥、缓存、构建产物和日志。

## 常见 RED 点

- 不要把真实凭据写入任何模板。
- 不要在技术栈未知时伪造 `npm run build`、`pytest` 等命令。
- 不要覆盖已有 README 的用户内容；追加初始化治理段落即可。
