# 提示词模板与构建技巧

## Gemini 3 Pro 提示词核心原则

### 关键发现：简洁直接

**重要变化**：Gemini 3 相比 2.x 版本，对简短、直接的指令响应更好。如果你的提示词是为 2.x 编写的，可以简化它们——以前"安全"的长提示词现在可能显得过度。

### 快速检查清单

1. **保持任务一句话**：核心请求应简洁明了
2. **指定输出格式**：明确说明期望的输出类型
3. **移除重复约束**：删除旧版提示词中的重复内容
4. **按需添加细节**：如果输出质量下降，再添加细节
5. **测试两种模式**：先用纯文本，再用多模态输入测试

---

## 一、基础提示词结构

### 核心公式

```
[主体] + [构图] + [动作] + [位置] + [风格] + [编辑指令]
```

### 六要素模板

| 要素 | 说明 | 示例 |
|------|------|------|
| **Subject (主体)** | 谁或什么是图片内容？要具体 | `a stoic robot barista with glowing blue optics` |
| **Composition (构图)** | 镜头如何取景？ | `extreme close-up`, `wide shot`, `low angle shot` |
| **Action (动作)** | 正在发生什么？ | `brewing a cup of coffee`, `casting a magical spell` |
| **Location (位置)** | 场景在哪里？ | `a futuristic cafe on Mars`, `a sun-drenched meadow` |
| **Style (风格)** | 整体美学是什么？ | `3D animation`, `film noir`, `watercolor`, `photorealistic` |
| **Editing (编辑)** | 修改现有图片时的具体指令 | `change the man's tie to green` |

---

## 二、学术论文图表两阶段生成法

### 概述

将复杂的学术图表创建任务分解为两个独立阶段：
1. **The Architect（架构师）** - 用 LLM 生成视觉蓝图
2. **The Renderer（渲染器）** - 用图像生成模型渲染

### 第一阶段：The Architect（视觉蓝图生成）

#### 提示词模板

```
# Role
You are a **Visual Architect** for a top-tier academic conference like CVPR or NeurIPS. Your core competency is translating abstract research logic into **concrete, structured, geometry-level visual instructions**.

# Objective
Read the paper content I provide and output a **[VISUAL SCHEMA]**. This schema will be fed directly to an AI image generation model, so it must use **concrete physical descriptions**.

# Phase 1: Layout Strategy Selector (Critical Step: Layout Decision)
Before generating the schema, first analyze the paper's logic and select the most appropriate **layout archetype** (or a combination) from the following options:

1. **Linear Pipeline**: A left-to-right flow, ideal for Data Processing or Encoder-Decoder architectures.
2. **Cyclic/Iterative**: Features a central loop with arrows, perfect for Optimization, Reinforcement Learning, or Feedback Loops.
3. **Hierarchical Stack**: A top-to-bottom or bottom-to-top arrangement, suitable for Multiscale Features or Tree Structures.
4. **Parallel/Dual-Stream**: A side-by-side structure, great for Multi-modal Fusion or Contrastive Learning.
5. **Central Hub**: A central element connecting surrounding components, used for Agent-Environment interactions or Knowledge Graphs.

# Phase 2: Schema Generation Rules
1. **Dynamic Zoning**: Based on the selected layout, define 2-5 distinct physical zones. Do not feel constrained to just three.
2. **Internal Visualization**: You must define the "objects" (e.g., Icons, Grids, Trees) inside each zone. Avoid abstract concepts.
3. **Explicit Connections**: For a cyclic process, you must describe it explicitly, e.g., "A curved arrow loops back from Zone X to Zone Y".

# Output Format (Required Schema)
Please strictly adhere to the following Markdown structure for the output:
---BEGIN PROMPT---
[Style & Meta-Instructions]
High-fidelity scientific schematic, technical vector illustration, clean white background, distinct boundaries, academic textbook style. High resolution 4k, strictly 2D flat design with subtle isometric elements.

[LAYOUT CONFIGURATION]
* **Selected Layout**: [e.g., Cyclic Iterative Process with 3 Nodes]
* **Composition Logic**: [e.g., A central triangular feedback loop surrounded by input/output panels]
* **Color Palette**: Professional Pastel (Azure Blue, Slate Grey, Coral Orange, Mint Green).

[ZONE 1: LOCATION - LABEL]
* **Container**: [Shape description, e.g., Top-Left Panel]
* **Visual Structure**: [Specific description, e.g., A stack of documents]
* **Key Text Labels**: "[Text 1]"

[ZONE 2: LOCATION - LABEL]
* **Container**: [Shape description, e.g., Central Circular Engine]
* **Visual Structure**: [Specific description, e.g., A clockwise loop connecting 3 internal modules: A (Gear), B (Graph), C (Filter)]
* **Key Text Labels**: "[Text 2]", "[Text 3]"

[ZONE 3: LOCATION - LABEL]
... (Add Zone 4/5 if necessary based on layout)

[CONNECTIONS]
1. [Describe connection, e.g., A curved dotted arrow looping from Zone 2 back to Zone 1 labeled "Feedback"]
2. [Describe connection, e.g., A wide flow arrow from Zone 2 to Zone 3]
---END PROMPT---

# Input Data
[Paste your paper's content here]
```

### 第二阶段：The Renderer（图像生成）

#### 提示词模板

```
**Style Reference & Execution Instructions:**
1. **Art Style (Visio/Illustrator Aesthetic):**
   Generate a **professional academic architecture diagram** suitable for a top-tier computer science paper (CVPR/NeurIPS).
   * **Visuals:** Flat vector graphics, distinct geometric shapes, clean thin outlines, and soft pastel fills (Azure Blue, Slate Grey, Coral Orange).
   * **Layout:** Strictly follow the spatial arrangement defined in the schema below.
   * **Aesthetic:** Technical, precise, clean white background. This should NOT be hand-drawn, photorealistic, a 3D render, or have any shadows/shading.

2. **CRITICAL TEXT CONSTRAINTS (Read Carefully):**
   * **DO NOT render meta-labels:** Do not write words like "ZONE 1", "LAYOUT CONFIGURATION", "Input", "Output", or "Container" on the image. These are structural instructions for YOU, not text to be displayed.
   * **ONLY render "Key Text Labels":** The only text that should appear in the diagram is the text inside double quotes (e.g., "[Text]") listed under "Key Text Labels".
   * **Font:** Use a clean, bold Sans-Serif font (like Roboto or Helvetica) for all labels.

3. **Visual Schema Execution:**
   Translate the following structural blueprint into the final image:
   [Directly paste the content generated in Step 1 from ---BEGIN PROMPT--- to ---END PROMPT--- here]
```

---

## 三、流程图/架构图专用模板

### 通用模板

```
[图表类型], showing [主题描述], clean modern design, [配色方案],
with [布局描述], professional business style, white background,
high detail, [分辨率修饰]
```

### 流程图模板（Nano Banana Pro）

```
Create a [流程名] flowchart:

Process Description:
1. [步骤1描述]
2. [步骤2描述]
3. [步骤3描述]
...

Design Requirements:
- Use standard flowchart symbols
- Start/End: Rounded rectangles
- Process steps: Rectangles
- Decisions: Diamonds
- Connections: Arrows with direction labels
- Layout: Top to bottom OR Left to right
- Color scheme: Professional [颜色]
- Background: White
- Font: Clear and readable

Output Format: High-resolution flowchart, suitable for documents and presentations
```

### 架构图模板

```
Design a [ASPECT RATIO] diagram topic: [TOPIC]
central focus: [MAIN IDEA]
layout: [FLOW / CYCLE / STEPS / HIERARCHY]
style: clean and instructional
background: white
text must be clear, legible, and accurate
```

---

## 四、五种流程图类型

### 1. 基础流程图 (Basic Flowchart)

**适用场景**：用户操作流程、系统处理流程、算法逻辑

```
Create a user login flowchart:

Process Description:
1. User opens login page (Start)
2. Enter username and password (Input)
3. Click login button (Action)
4. System validates username and password (Process)
5. Judge validation result (Decision)
   - If validation fails: Display error message, return to step 2
   - If validation succeeds: Redirect to user homepage
6. Login complete (End)

Design Requirements:
- Use standard flowchart symbols
- Start/End: Rounded rectangles
- Process steps: Rectangles
- Decisions: Diamonds
- Connections: Arrows with direction labels
- Layout: Top to bottom
- Color scheme: Professional blue (#1f2937, #3b82f6)
- Background: White
```

### 2. 跨职能流程图 (Cross-Functional / Swimlane)

**适用场景**：跨部门审批流程、多角色协作

```
Create an order approval cross-functional flowchart:

Participating Roles:
1. Customer
2. Salesperson
3. Finance Department
4. Warehouse

Process Description:
[Customer]
- Submit order (Start)
- Receive order confirmation

[Salesperson]
- Receive customer order
- Review order information
- Decision: Is order valid?
  - Invalid: Notify customer to modify
  - Valid: Submit to finance for review

[Finance Department]
- Review order amount and credit limit
- Decision: Finance approval passed?
  - Not passed: Return to sales
  - Passed: Notify warehouse to ship

[Warehouse]
- Receive shipping notification
- Prepare goods and ship (End)

Design Requirements:
- Use Swimlane layout
- 4 horizontal swimlanes (Customer, Sales, Finance, Warehouse)
- Swimlanes distinguished by different light background colors
- Cross-swimlane connections use dashed lines
```

### 3. 时间线流程图 (Timeline)

**适用场景**：项目计划、产品开发流程

```
Create a product launch timeline flowchart:

Project Duration: 12 weeks

Timeline Process:
Weeks 1-2: Requirements Research Phase
- Market research, User interviews
- Output: Requirements document

Weeks 3-4: Product Design Phase
- Prototype design, UI/UX design
- Output: Design mockups

Weeks 5-8: Development & Testing Phase
- Frontend/Backend development
- Output: Beta version

Weeks 9-10: Internal Testing
- Bug fixes, Feature optimization
- Output: RC version

Weeks 11-12: Launch Phase
- Marketing preparation
- Official release

Design Requirements:
- Horizontal timeline, left to right
- Timeline clearly labeled with week numbers
- Each phase represented by colored cards
- Key milestones highlighted with star markers
```

### 4. 决策树流程图 (Decision Tree)

**适用场景**：故障排除、风险评估、分类策略

```
Create a customer service issue diagnosis decision tree:

Decision Process:
[Root] Customer reports issue
│
├─[Decision 1] What is the issue type?
│  │
│  ├─ Login Issue → [Decision 2] Forgot password?
│  │              ├─ Yes → Send reset link (End)
│  │              └─ No → Check account status (End)
│  │
│  ├─ Function Error → [Decision 3] Known bug?
│  │              ├─ Yes → Inform fix timeline (End)
│  │              └─ No → Submit to tech team (End)
│  │
│  └─ Payment Issue → Query order status (End)

Design Requirements:
- Tree structure, expanding top to bottom
- Decision nodes: Diamonds
- End nodes highlighted in green
- Color scheme: Professional blue-gray tones
```

### 5. 循环流程图 (Loop Flowchart)

**适用场景**：数据处理循环、自动化脚本

```
Create a data batch processing loop flowchart:

Process Description:
1. Start batch processing task
2. Initialize: Set counter i = 0, total N = 1000
3. Loop condition: i < N?
   - No → Batch processing complete (End)
   - Yes → Continue execution
4. Read data item i
5. Data preprocessing
6. Data validation: Is it valid?
   - Invalid → Log error, i = i + 1, return to step 3
   - Valid → Continue execution
7. Data transformation
8. Write to target database
9. i = i + 1, return to step 3

Design Requirements:
- Clearly label loop paths (thick arrows or different colors)
- Loop condition judgment: Diamond
- Counter operations: Rectangle
- Loop return: Curved arrow
- Exception exit: Red path
```

---

## 五、视觉风格配置

### 学术论文配色方案

#### 推荐色板

| 风格 | 颜色 |
|------|------|
| **Professional Pastel** | Azure Blue (#4299e1), Slate Grey (#718096), Coral Orange (#fc8181), Mint Green (#68d391) |
| **Clean Academic** | Navy (#2c5282), Light Blue (#ebf8ff), Gray (#e2e8f0) |
| **Modern Tech** | Blue (#3182ce), Cyan (#00b5d8), Purple (#805ad5) |

#### 不推荐

- 渐变过度（gradients）
- 阴影（shadows）
- 3D 效果
- 手绘风格

### 字体要求

- **推荐**：Roboto, Helvetica, Arial (Sans-Serif)
- **避免**：Times New Roman（除非期刊要求）
- **中文**：Noto Sans SC, Source Han Sans

---

## 六、常见问题修复

### 问题 1：整体布局正确，但细节/风格不对

**解决方案**：使用自然语言编辑

```
- Modify Icons: "Change the 'Gear' icon in the center to a 'Neural Network' icon"
- Adjust Colors: "Make the background of the left panel pure white instead of light blue"
- Unify Style: "Make all lines thinner and cleaner"
- Correct Text: "Correct the text 'ZONNE' to 'ZONE'"
```

### 问题 2：布局根本性错误

**解决方案**：回到第一阶段修改视觉蓝图

- 是否选择了正确的布局类型？
- Zone 的描述是否太模糊？
- 连接关系是否清晰？

### 问题 3：文字渲染错误

**解决方案**：
1. 让 AI 移除所有文字（"Remove all text labels"）
2. 手动在 PowerPoint/Figma 中添加文字
3. 或使用矢量编辑器（如 Illustrator）后处理

### 问题 4：图片有水印

**解决方案**：
1. 在提示词末尾添加："Add a line of placeholder text at the very bottom of the image"
2. 生成后裁剪底部（水印和占位符一起被裁掉）

---

## 七、迭代优化策略

### 何时重新生成 vs 何时编辑

| 情况 | 推荐方法 |
|------|----------|
| 布局结构错误 | 回到第一阶段修改蓝图 |
| 颜色/图标风格不对 | 直接用自然语言编辑 |
| 文字拼写错误 | 后处理编辑 |
| 80%满意 | 自然语言微调 |

### 迭代检查清单

1. **核心逻辑是否正确？** → 检查箭头方向、连接关系
2. **文字标签是否准确？** → 逐一核对每个文本
3. **风格是否符合期刊要求？** → 检查配色、字体、背景
4. **视觉层次是否清晰？** → 确保最重要的元素最突出

---

## 八、重要限制与注意事项

### 不适合 AI 生成的图表

- ❌ **数据图表**：散点图、柱状图、折线图等实验数据图
- ❌ **真实人物照片**：AI 无法准确渲染真实人物
- ❌ **精确地图/建筑图纸**：需要专业工具

### 适合 AI 生成的图表

- ✅ **概念图/架构图**：系统架构、流程图
- ✅ **示意图**：算法原理、技术原理
- ✅ **学术插图**：论文中的概念说明图

### 学术诚信提醒

> **重要**：AI 辅助生成的图表必须经过人工审核。AI 可能会：
> - 画错箭头方向
> - 简化或错误表示逻辑关系
> - 放置错误位置的标签
>
> **绝对禁止**：用 AI 生成或修改实验数据图表（这构成学术造假）

---

## 九、实用示例

### 示例 1：多智能体系统架构图

```
Create a multi-agent system architecture diagram for cloud-native RCA:

Layout: Hierarchical Stack (4 layers, top to bottom)

[Layer 1 - User Interface]
- Components: Query Input Box, Intent Interpreter, Data Sources Panel
- Style: Flat boxes with rounded corners, light pastel fills

[Layer 2 - Orchestration]
- Components: Orchestration Agent (center), Skill Templates (right side)
- Knowledge Constraints flow from left to center

[Layer 3 - Specialized Agents]
- Components: 4 agents in parallel (Metric, Log, Trace, Root Cause)
- Bidirectional arrows between Orchestration and each agent

[Layer 4 - Output]
- Root Cause Report box spanning full width

Connections:
- Intent Interpreter → Data Sources (downward arrow)
- Data Sources → Orchestration Agent (downward arrow)
- Skill Templates → Orchestration Agent (left to right)
- Orchestration Agent ↔ each Specialized Agent (bidirectional)

Color Palette: Professional Pastel (Azure Blue for main components, Mint Green for output)
Background: Pure white
Style: 2D flat vector, clean lines, no shadows
```

### 示例 2：算法流程图

```
Create a machine learning training pipeline flowchart:

Process:
1. Data Loading (Start)
2. Data Preprocessing
   - Missing value handling
   - Feature normalization
3. Train/Val/Test Split
4. Model Training Loop
   - Forward pass
   - Loss calculation
   - Backpropagation
   - Optimizer step
5. Validation
   - Decision: Performance OK?
     - No → Return to Model Training
     - Yes → Continue
6. Test Evaluation
7. Model Deployment (End)

Design:
- Layout: Top to bottom with decision diamonds
- Color: Blue (#1e40af) for processes, Orange (#f59e0b) for decisions
- Green (#10b981) for positive path, Gray (#6b7280) for negative path
- Loop arrow: Curved arrow from Validation back to Model Training
```

---

## 十、快速参考卡

### 提示词关键词速查

| 类型 | 关键词 |
|------|--------|
| **风格** | flat design, vector illustration, clean, minimal, professional |
| **背景** | white background, pure white, light gray |
| **线条** | thin lines, clean outlines, no shadows |
| **字体** | sans-serif, Helvetica, Roboto, clear typography |
| **布局** | top-down, left-to-right, hierarchical, centered |
| **连接** | arrows, flow lines, dashed lines for handoffs |

### 布局选择速查

| 逻辑结构 | 推荐布局 |
|----------|----------|
| 线性流程 | Linear Pipeline (左→右 或 上→下) |
| 循环迭代 | Cyclic/Iterative (中心循环) |
| 层级关系 | Hierarchical Stack (垂直堆叠) |
| 双路对比 | Parallel/Dual-Stream (并排) |
| 中心辐射 | Central Hub (中心+周围) |
