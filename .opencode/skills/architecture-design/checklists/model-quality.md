# 模型质量检查清单

交付前逐项确认。任何一项为否时，先修复再交付；无法修复时必须向用户说明残余风险。

## 语言友好

- [ ] 元素显示名、视图标题、描述、关系标签、部署节点名均为中文
- [ ] 标识符（元素 id、视图 id）为英文，未因汉化改动
- [ ] 技术专有名词保留原文（RAGFlow、LLM Wiki、Node.js、HTTP、JSON、API、文件路径、端口）
- [ ] 已用 grep 自检无遗漏英文：

```bash
grep -hoE "(title|description) '[^']*'" src/**/*.c4 | grep -oE "'[^']*'" \
  | grep -E "[A-Za-z]{4,}" | grep -vE "RAGFlow|LLM|Node|HTTP|HTTPS|JSON|API|src/|localhost"
```

  有输出即逐条处理；技术专有名词误报时加入排除列表再确认。

## 图类型路由

- [ ] 已执行 `references/00-diagram-routing.md`，确定目标图类型与轨道
- [ ] 已确认所用 LikeC4 版本（记录在交付说明中）
- [ ] 未用 LikeC4 硬凑类图、状态机图或严格 UML 用例图
- [ ] 未写入当前版本不支持的语法（1.58.0：`opt` `loop` `break` `alt` `try`、视图文件夹分组）
- [ ] 走轨道二/三的部分已向用户说明原因
- [ ] 未把 Mermaid/PlantUML 产物当作架构真源

## 语法正确性（1.58.0 实测坑位）

- [ ] `shape` 只用了合法值（`rectangle` `component` `storage` `cylinder` `browser` `mobile` `person` `queue` `bucket` `document`），未误用 `database` / `cloud`
- [ ] `color` 只用了合法值，未误用 `teal` / `d2`
- [ ] 关系上未挂 `style { }` 块
- [ ] 部署视图语法正确：使用 `instanceOf`（非 `instance of`）
- [ ] 部署节点类型已在 specification 中用 `deploymentNode` 声明
- [ ] 视图名全局唯一，无 `Duplicate view`

## 模型正确性

- [ ] `likec4 validate` 通过（输出 `✓ Valid`，退出码 0）
- [ ] `likec4 format --check` 通过（输出 `All N file(s) are formatted`）
- [ ] 跨文件引用全部使用 FQN，无 short name 越界
- [ ] 视图属性（title / description / tags / link）写在 predicate 之前
- [ ] 被 `navigateTo` 引用的视图均已具名
- [ ] 模型事实定义在 `model/`，未藏在 `views/`

## 视图质量

- [ ] 视图已具名（导出文件名与 URL 依赖它）
- [ ] `view of <element>` 的作用域被正确利用
- [ ] 元素有意义的 `description`
- [ ] 存在导航入口（`index` 或明确的顶层视图）

## Dynamic View 专项

- [ ] sequence 变体只连接叶子元素
- [ ] `parallel` / `par` 未嵌套（1.58.0 实测禁止）
- [ ] 条件分支/循环/异常需求已确认当前版本是否支持；不支持时改走 Mermaid flowchart
- [ ] 步骤元素若不在 model 中，已在视图内 `include`

## 工程集成

- [ ] 已确认验证路径（MCP / CLI / npx / 只读降级），未因环境缺 likec4 而停止交付
- [ ] Node 版本满足锁定版本的 engines 下限（仅影响 CLI，不影响 MCP）
- [ ] `package.json` 中 likec4 使用精确版本号而非 `^`
- [ ] CI 中 `actions/setup-node` 显式指定满足要求的版本
- [ ] submodule 场景下 CI 已开 `submodules: recursive`
- [ ] PNG/JPG 导出未放入主 CI 路径（依赖 Playwright）
- [ ] MCP 配置已就绪，且已提醒用户重启 opencode
- [ ] 已确认改动后同步可见（serve 热更新，或 MCP 查询确认）

## 资产归属

- [ ] 已执行 `references/05-design-repo-layout.md` 确定归属层级
- [ ] 未把多个项目设计放进同一个被 submodule 引用的仓
- [ ] 需与代码同 PR 的内容未被放进设计仓
- [ ] 项目层设计仓已在主仓 `submodules-index.md` 登记，`build_entry` 为 `none`
- [ ] 全局聚合层未被任何项目 submodule 引用

## 架构交接（进入实现阶段时）

- [ ] 已读取 `references/06-architecture-handoff.md` 并按模板产出交接规格
- [ ] 规格含五部分：组件边界、依赖约束、流程锚点、部署要求、验收锚点
- [ ] 每条规格内容都有模型依据（元素 id 或 view id），写不出的已标 `待补充`
- [ ] 依赖方向与模型一致（模型 `a -> b` 未被写成反向）
- [ ] 流程锚点的 view id 在模型中真实存在，可被 `read-view` 读取
- [ ] 验收锚点均为可观察或有明确查询方式的信号，无「符合设计文档」这类表述
- [ ] 关键结论置信度已标注，低于 90% 的项已列出缺口与补证动作
- [ ] 已明确说明接口契约、数据结构、业务规则由 `technical-design` 补齐
- [ ] 未声称「架构即开发」或暗示可从模型直接生成代码
- [ ] 交接路径判断已给出（直接实现 / 先技术设计 / 先完成建模）
- [ ] 架构有变更时，已提醒设计仓发版与主仓指针更新

## 诚实性

- [ ] 无法运行的校验已说明原因、降级证据和残余风险
- [ ] 只读降级交付时已明确标注「未经 `likec4 validate` 校验」
- [ ] 环境故障（EBADENGINE / MODULE_NOT_FOUND / 网络）未被误报为模型语法错误
- [ ] LikeC4 不支持的图类型已如实说明，未伪造交付
- [ ] 升级版本的建议已给出（若用户需要当前版本不支持的特性）
