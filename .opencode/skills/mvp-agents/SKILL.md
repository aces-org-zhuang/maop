---
name: mvp-agents
description: Innovation Master multi-agent system for rapid MVP development. Coordinates product analysis, competitor research, innovation analysis, PRD writing, UX design, and prototype building.
tools: [call_mvp_agent, start_mvp, background_output, find_similar_project]
---

# Innovation Master System

Innovation Master 是一个基于 OpenCode 插件的多 Agent 系统，通过主编排 Agent 协调 6 个专业子 Agent 完成 MVP 开发。

## 可用工具

| 工具 | 说明 |
|------|------|
| `start_mvp` | 启动完整的 MVP 开发工作流 |
| `call_mvp_agent` | 调用特定的 MVP 子代理 |
| `background_output` | 查询后台任务输出 |
| `find_similar_project` | 查找可复用的相似项目 |

## 子代理

| Agent | 职责 |
|-------|------|
| `product-analyzer` | 产品分析 - 需求解析、价值主张、关键词、**核心功能×适用场景×痛点**（无执行摘要） |
| `competitor-researcher` | 竞品研究 - 竞品调研、市场分析、机会识别 |
| `innovation-analyst` | 创新分析 - 差异化论证、**技术点+架构图(Mermaid)+壁垒/可绕过性+价值**；禁止路线图/实施路径；**禁止**以合规认证、客户信任、「企业级」、**生态构建**作创新/壁垒主线 |
| `prd-writer` | PRD撰写 - **不含任何 UX/界面占位**；功能与非功能需求、验收；界面与交互由 `ux-designer` 阶段单独产出 |
| `ux-designer` | UX设计 - 用户流程设计、信息架构、技术栈建议 |
| `prototype-builder` | 原型构建 - HTML/CSS/JS可交互原型生成 |
| `reviewer` | 阶段评审 - 打分与改进建议（每阶段子 Agent 之后必须调用） |

## 工作流程

### Step 0: 项目复用检查（必须）

**在开始工作前，必须先使用 `find_similar_project` 查找相似项目：**

```
find_similar_project({ description: "<用户需求描述>" })
```

- **有候选且可能相关**：`find_similar_project` 只展示至多 **3** 个最相关项目；用 `question` **询问用户**是否复用、复用哪一个或是否新建；**用户明确答复前**不得调用子代理或新建目录（用户已指定路径的除外）；勿向用户罗列更多项目，除非用户明确要求
- **用户确认复用**：读取参考内容，在子代理 prompt 中加入复用建议
- **用户选择新建或未找到项目**：注明「无参考项目，从零开始」或「用户选择不复用」，再创建新项目目录

### Step 1-6: 按顺序调用子代理

1. **product-analyzer** - 产品分析
2. **competitor-researcher** - 竞品研究
3. **innovation-analyst** - 创新分析
4. **prd-writer** - PRD 文档
5. **ux-designer** - UX 设计
6. **prototype-builder** - 原型构建

每完成一个子代理的落盘后，**必须先**用 **reviewer** 评审（`review/*.md` 与 `*.json`）；score ≥ 70 后才可用 question 征求用户意见；未通过则带评审建议重呼同一子代理，**最多 3 轮**评审循环。

## 文件保存规则

所有路径均在 `projects/<项目名>/` 下：`structured/` 存各阶段 JSON，`reports/` 存各阶段 Markdown，原型在 `prototype/`：

| 阶段 | 结构化产物（`structured/`，JSON） | 阶段报告（`reports/`，Markdown） |
|------|----------------|-------------------|
| 产品分析 | 01-product-analysis.json | 01-product-analysis.md |
| 竞品研究 | 02-competitor-research.json | 02-competitor-research.md |
| 创新分析 | 03-innovation-analysis.json | 03-innovation-analysis.md |
| PRD | 04-product-document.json | 04-product-document.md |
| UX | 05-ux-design.json | 05-ux-design.md |
| 原型 | - | - |

**原型（`prototype/`）**：`prototype/index.html`、`prototype/styles.css`、`prototype/app.js`

**评审（`review/`）**：各阶段 `*-review.md` 与可选 `*-review.json`

## 调用示例

```
call_mvp_agent({
  description: "产品分析：在线教育平台",
  prompt: "项目路径：projects/online-edu-platform/\n【参考项目】xxx（如有）\n\n可选 Skill 参考：mvp-agents\n\n分析以下 MVP 需求...",
  subagent_type: "product-analyzer",
  run_in_background: true
})
```
