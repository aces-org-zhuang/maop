---
name: image-drawing-skill
description: 画图辅助技能。当用户需要生成图片、创建图像、绘制图表时使用。功能包括：(1) 分析参考图片风格；(2) 根据用户需求生成画图提示词；(3) 调用 Gemini Banana Pro API 生成图片；(4) 支持交互式确认、分辨率选择和迭代优化。
notes: 本技能仅支持 Gemini Banana Pro API。脚本位于 ~/.cursor/skills/image-drawing-skill/scripts/generate_image_banana.py。
---

# Image Drawing Skill

## 重要说明

**参考图片的使用方式：**
- 只参考：整体风格、色调、线形、流程逻辑、图标样式
- **必须严格按照用户提供的实际文本内容**生成画图提示词
- 不要复制参考图中的具体文字内容

**提示词参考资料**：
- `references/prompt-templates.md` - 详细提示词模板和构建技巧（**必读**当用户没有明确提示词时）
- `references/gemini-banana-pro-api.md` - Gemini Banana Pro API 参考文档

## 工作流程

### 1. 分析参考图片（仅当有图片时）

**条件执行**：只有当用户提供了参考图片时，才执行此步骤。如果用户只提供文字提示词，则直接跳过此步骤。

**第一步：使用 MiniMax 工具分析图片**

如果用户提供了参考图片，使用 MiniMax MCP 工具分析其视觉特征：

```markdown
调用 CallMcpTool:
- server: "user-MiniMax"
- toolName: "understand_image"
- arguments:
  - prompt: "请详细分析这张图片的：1) 整体风格和色调 2) 布局结构 3) 元素组成 4) 文字样式 5) 视觉层次 6) 颜色代码（如能识别）"
  - image_source: "<图片路径>"
```

**第二步：根据图片类型决定提示词构建方式**

根据 MiniMax 的分析结果，判断图片类型并选择合适的提示词构建策略：

| 图片类型 | 识别特征 | 提示词构建方式 |
|----------|----------|----------------|
| **架构图/流程图** | 多层堆叠、层级清晰、有明确的数据流向 | 使用 ASCII 布局图展示结构，详细描述层级和箭头关系 |
| **手绘插画风** | 手绘线条、装饰元素（星星/云朵）、温暖色调、低饱和度 | 重点描述风格元素（背景色、线条色、装饰物），使用"hand-drawn sketchnote style" |
| **技术示意图** | 精确的图形、标注、公式、连接线 | 强调"technical diagram"、"precise annotations"、"clean vector style" |
| **信息图/数据可视化** | 图表元素、统计数据展示、色彩编码 | 强调"infographic style"、"data visualization"、"clean charts" |
| **实物/场景图** | 真实物体、人物、场景、光照效果 | 描述主体、场景、光线、视角 |

**第三步：提取关键风格元素**

根据分析结果，提取以下元素用于提示词构建：

```
## 图片风格提取结果

**风格类型**: [架构图/手绘风/技术图/信息图/其他]
**背景色**: [#FDFCF0 或类似色值]
**主色调**: [蓝色系/粉色系/绿色系/等]
**线条色**: [#424242 石墨灰/纯黑/其他]
**布局特点**: [多层垂直/横向流程/中心辐射/网格/自由布局]
**装饰元素**: [有/无 - 星星/云朵/图标/边框]
**字体风格**: [手写体/无衬线/衬线/等]
```

### 2. 分析用户需求

理解用户想要画什么，包括：
- 图片主题和内容（**这是实际要画的内容**）
- 目标尺寸和用途
- 特殊风格要求（参考图等）
- 层级结构（如有）
- **提示词文件路径**（用户指定，默认为 `assets/drawing_prompt.txt`）

### 2.1 当用户没有提供参考图片且没有明确提示词时的引导流程

**触发条件**：用户没有提供明确的提示词，或者只是模糊地说"画个图"、"帮我生成一个架构图"等。

**引导步骤**：

#### Step 1: 询问图片用途和类型

```
为了帮您生成合适的图片，请告诉我：

1. **图片用途**（必填）
   - [ ] 学术论文插图
   - [ ] 技术文档/架构图
   - [ ] 演示文稿（PPT）
   - [ ] 博客/文章配图
   - [ ] 其他：__________

2. **图片类型**（必填）
   - [ ] 流程图 (Flowchart)
   - [ ] 架构图 (Architecture Diagram)
   - [ ] 示意图 (Schematic)
   - [ ] 信息图 (Infographic)
   - [ ] 时间线 (Timeline)
   - [ ] 决策树 (Decision Tree)
   - [ ] 其他：__________

3. **主要内容**（必填）
   请描述您希望在图中展示的核心内容，例如：
   - 系统名称/主题
   - 主要组件或步骤
   - 组件之间的关系或流程顺序
```

#### Step 2: 根据类型提供布局建议

根据用户选择的图片类型，推荐合适的布局结构：

| 图片类型 | 推荐布局 | 说明 |
|----------|----------|------|
| 流程图 | Linear Pipeline | 线性流程，左→右或上→下 |
| 架构图 | Hierarchical Stack | 层级堆叠，适合系统架构 |
| 决策树 | Tree Structure | 树形分支，适合条件判断 |
| 时间线 | Horizontal Timeline | 水平时间轴，适合项目计划 |
| 循环流程 | Cyclic/Iterative | 中心循环，适合迭代算法 |
| 多角色流程 | Swimlane | 分泳道，适合跨部门流程 |

#### Step 3: 收集关键信息

根据图片类型，引导用户提供：

**对于架构图：**
```
请提供以下信息：

1. **系统/框架名称**：__________
2. **主要层次/组件**（列出）：
   - 层次1：__________
   - 层次2：__________
   - 层次3：__________
   - （可添加更多）
3. **组件之间的关系**（简要描述）：
   - 如何连接：单向/双向/循环
   - 数据流向：__________
4. **特殊要求**（可选）：
   - 配色偏好：__________
   - 风格要求：__________
   - 参考图片：__________
```

**对于流程图：**
```
请提供以下信息：

1. **流程名称**：__________
2. **开始步骤**：__________
3. **主要步骤**（按顺序列出）：
   - 步骤1：__________
   - 步骤2：__________
   - 步骤3：__________
   - （可添加更多）
4. **决策点**（如有条件分支）：
   - 条件：__________
   - 是/否 分支：__________
5. **结束步骤**：__________
```

#### Step 4: 生成提示词初稿

根据收集的信息，生成提示词初稿：

**提示词生成原则：**
1. 使用简洁、直接的描述（Gemini 3 偏好短句）
2. 明确指定布局结构
3. 使用标准符号（矩形=过程，菱形=决策，椭圆=开始/结束）
4. 指定配色方案和风格
5. 添加质量修饰词

**生成后，展示 ASCII 布局预览供用户确认：**

```markdown
## 提示词初稿已生成

### 布局结构
```
[ASCII 布局图]
```

### 提示词预览
```
[生成的提示词内容]
```

---
请确认：
1. 布局结构是否符合预期？
2. 内容是否完整？
3. 是否需要修改或添加内容？

回复选项：
- **确认**：内容正确，开始生成图片
- **修改**：描述需要修改的部分
- **补充**：提供更多内容细节
```

### 3. 检查/读取提示词文件

**重要**：每次操作时，首先尝试读取用户指定的提示词文件（如已存在），在此基础上进行修改。

```python
def read_prompt_file(file_path):
    """读取现有提示词文件"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

prompt_file = "用户指定的路径或默认路径"
existing_prompt = read_prompt_file(prompt_file)
```

### 4. 检查 API Key

**第一步：从 .env 文件加载环境变量**

```python
def load_env():
    env_path = ".env"  # 相对于当前工作目录
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value

load_env()
```

**第二步：检查 Banana API Key**

```python
banana_key = os.environ.get("BANANA_API_KEY", "").strip()

if not banana_key:
    # 需要询问用户获取 API Key
```

**如果缺少 API Key，询问用户提供：**

```
未检测到有效的 Banana API Key。

请提供您的 Gemini Banana Pro API Key。
获取地址：https://console.cloud.google.com/apis/credentials?project=_
（需要 Google 账号，免费注册）
```

收到 API Key 后，保存到 .env 文件：

```python
def save_api_key(key_name, key_value, env_path):
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key_name}="):
            new_lines.append(f"{key_name}={key_value}\n")
        else:
            new_lines.append(line)

    if not any(line.strip().startswith(f"{key_name}=") for line in lines):
        new_lines.append(f"{key_name}={key_value}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)
```

### 5. 生成/修改画图提示词

**重要**：在现有提示词文件基础上修改，不要覆盖整个文件。

**提示词参考资料**：详细提示词模板和构建技巧请参考 `references/prompt-templates.md`。

**提示词生成原则：**
- 参考图的风格、配色、图标样式作为指导（仅当有参考图时）
- **实际内容必须使用用户提供的确切文本**
- 使用清晰的结构化描述
- 包含分辨率和质量要求
- Gemini 3 偏好简洁、直接的指令，避免过度冗长

**根据图片类型选择提示词构建方式：**

#### A. 有参考图片时 - 基于风格重建

**手绘插画风格**（来自 MiniMax 分析）：

```
Create a hand-drawn sketchnote-style [主题描述].

Style specifications:
- Hand-drawn / Sketchnote aesthetic (warm, approachable)
- Background: [背景色 如 #FDFCF0]
- Soft pastel/macaron colors with low saturation
- Stroke color: [线条色 如 #424242]
- Rounded shapes, organic curves
- Decorative elements: [装饰元素描述]
- Text style: [字体风格描述]

Layout structure:
[根据实际布局描述]
```

**扁平学术架构图风格**（来自 MiniMax 分析）：

```
Create a clean academic-style systems architecture diagram showing [主题描述].

Style specifications:
- Flat 2D academic diagram
- White background
- [主色调描述]
- Thin gray borders, light shadows
- Clean box layouts, readable fonts

Layout structure:
[详细的层级和组件描述]
- Arrow directions: [箭头方向说明]
- Color scheme: [配色方案]
```

**技术示意图风格**：

```
Create a technical diagram illustrating [主题描述].

Style specifications:
- Technical/precision style
- Clean vector graphics
- [线条和边框描述]
- Professional illustration style
- Include annotations and labels

Layout structure:
[详细的组件和连接描述]
```

#### B. 无参考图片时 - 使用标准模板

根据 `references/prompt-templates.md` 中的模板选择合适的结构：

| 图片类型 | 模板选择 |
|----------|----------|
| 流程图 | 基础流程图模板、循环流程图模板 |
| 架构图 | 层级堆叠布局、五种架构图模板 |
| 决策树 | 决策树模板 |
| 时间线 | 时间线模板 |
| 跨职能流程 | Swimlane 模板 |

**学术图表两阶段生成法**（适用于复杂论文架构图）：

**第一阶段 - 生成视觉蓝图**：
使用 LLM 根据论文内容生成 [VISUAL SCHEMA]，包含布局策略、区域划分、连接关系。

**第二阶段 - 渲染图像**：
将视觉蓝图作为提示词，使用 Gemini Banana Pro 生成最终图像。

详细步骤和模板见 `references/prompt-templates.md` 第 2 节。

根据用户需求和参考图风格（如有），修改提示词。

**提示词文件管理**：
```python
def save_prompt_to_file(file_path, prompt_content):
    """保存提示词到文件（在现有内容基础上修改）"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(prompt_content)

prompt_file = "用户指定的提示词文件路径"
```

**ASCII 布局图文件管理**：
```python
def save_ascii_to_file(file_path, ascii_content):
    """保存 ASCII 布局图到单独文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ascii_content)

ascii_file = "用户指定的ASCII文件路径（默认为 assets/drawing_ascii.txt）"
```

### 6. 展示预览和确认

**根据图片类型决定预览方式：**

| 图片类型 | 预览方式 | 说明 |
|----------|----------|------|
| 架构图/流程图 | ASCII 布局图 | 清晰展示层级和组件关系 |
| 手绘插画风 | 风格描述 + 文字预览 | 重点展示风格元素和配色 |
| 技术示意图 | 组件列表 + 连接关系 | 强调技术细节和标注 |
| 通用/其他 | 文字描述 | 按实际情况灵活处理 |

**架构图/流程图 - 展示 ASCII 布局图：**

使用类似以下的 ASCII 图形展示布局结构：

```
┌─────────────────────────────────────────────────────────────┐
│                   层级名称 (Layer Name)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   模块A     │  │   模块B     │  │   模块C     │        │
│  │  (Module A) │  │  (Module B) │  │  (Module C) │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
```

**展示给用户确认：**

```markdown
## 画图提示词预览

- 提示词文件：`assets/drawing_prompt.txt`
- ASCII 布局文件：`assets/drawing_ascii.txt`
- 默认输出目录：`assets/`（相对于当前工作目录）

### 文本框布局示意图
```
[ASCII 布局图]
```

---
请确认：
1. 布局结构是否符合预期？
2. 文字内容是否正确？
3. 是否需要调整？

回复选项：
- **确认生成**：按提示词文件中的内容画图
- **修改布局**：描述需要的调整
- **修改内容**：提供新的文字内容
```

**注意**：ASCII 布局图也会同步保存到单独的文件中。

### 7. 保存 ASCII 布局图

将 ASCII 布局图保存到单独的文件中：

```python
ascii_content = """
┌─────────────────────────────────────────────────────────────┐
│                   层级名称 (Layer Name)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   模块A     │  │   模块B     │  │   模块C     │        │
│  │  (Module A) │  │  (Module B) │  │  (Module C) │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
"""

ascii_file = "assets/drawing_ascii.txt"
save_ascii_to_file(ascii_file, ascii_content)
```

### 8. 询问分辨率

用户确认后，询问分辨率：

```markdown
请选择图片分辨率：

| 分辨率 | 适用场景 | 生成时间 |
|--------|----------|----------|
| 1K | 快速预览、草稿 | 约 30s |
| 2K | 标准输出、论文使用 | 约 60s |
| 4K | 高清打印、海报 | 约 90s |

推荐选择 **2K**，适合大多数学术论文使用。
```

### 9. 生成图片（严格读取文件内容）

**重要**：从提示词文件读取内容，严格使用文件中的提示词，不要重新生成。

```python
def read_prompt_from_file(file_path):
    """从文件读取提示词"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 严格读取文件内容
prompt_file = "assets/drawing_prompt.txt"
prompt = read_prompt_from_file(prompt_file)

# 生成图片（默认输出到 assets/ 目录）
result = generate_image(
    prompt=prompt,  # 使用文件中的提示词
    resolution="2K",  # 用户选择的分辨率
    aspect_ratio="16:9",
    output_path="assets/output.png"
)
```

或在终端运行：

```bash
# 首先读取文件内容
PROMPT=$(cat assets/drawing_prompt.txt)

# 使用文件内容生成图片（默认输出到 assets/ 目录）
python ~/.cursor/skills/image-drawing-skill/scripts/generate_image_banana.py \
    -p "$PROMPT" \
    -r 2K
# 或指定输出路径
python ~/.cursor/skills/image-drawing-skill/scripts/generate_image_banana.py \
    -p "$PROMPT" \
    -r 2K \
    -o assets/output.png
```

### 10. 询问优化意见

图片生成后，询问用户是否需要优化：

```markdown
## 图片已生成！

保存路径：`assets/framework_v8.png`

---

**是否需要优化或重新生成？**

可选操作：
- **重新生成**：用相同提示词重新生成一张
- **调整分辨率**：升级到更高分辨率（如 2K → 4K）
- **修改提示词**：描述需要调整的内容（会更新到提示词文件）
- **调整布局**：提供新的布局说明（会更新到提示词文件）
- **完成**：对当前结果满意，结束流程
```

**持续迭代直到用户满意。**

---

## Gemini Banana Pro 图片生成

### 快速参考

- **端点**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={API_KEY}`
- **分辨率**: 1K, 2K, 4K
- **宽高比**: 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5
- **超时**: 1K=180s, 2K=300s, 4K=360s
- **认证**: API Key 通过 URL 参数传递 `?key={API_KEY}`

### 提示词技巧

#### 核心公式

```
[图表类型], showing [主题描述], [设计风格], [配色方案],
with [布局描述], professional [应用场景] style, white background,
high detail, [分辨率修饰]
```

#### 六要素模板

| 要素 | 说明 | 示例 |
|------|------|------|
| **Subject** | 谁或什么是图片内容？要具体 | `a stoic robot barista with glowing blue optics` |
| **Composition** | 镜头如何取景？ | `extreme close-up`, `wide shot`, `low angle shot` |
| **Action** | 正在发生什么？ | `brewing a cup of coffee`, `casting a magical spell` |
| **Location** | 场景在哪里？ | `a futuristic cafe on Mars`, `a sun-drenched meadow` |
| **Style** | 整体美学是什么？ | `3D animation`, `film noir`, `watercolor`, `photorealistic` |
| **Editing** | 修改现有图片时的具体指令 | `change the man's tie to green` |

#### 架构图提示词模板

```
[图表类型], showing [主题描述], [设计风格], [配色方案],
with [布局描述], professional [应用场景] style, white background,
high detail, [分辨率修饰]
```

**详细提示词模板和构建技巧**：请参考 `references/prompt-templates.md`，包含：
- 学术论文图表两阶段生成法
- 五种流程图类型模板（基础、跨职能、时间线、决策树、循环）
- 视觉风格配置和配色方案
- 问题修复和迭代优化策略

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `BANANA_API_KEY` | Gemini Banana Pro API 密钥（必需） |

---

## API Key 获取指南

### 首次使用流程

**Step 1: 检查 API Key**

脚本会自动检查以下位置获取 API Key（按优先级）：

1. **环境变量** `BANANA_API_KEY`
2. **当前目录**的 `.env` 文件
3. **脚本所在目录**的 `.env` 文件
4. **用户主目录**的 `.env` 文件
5. **交互式输入**（如果以上都没有）

**Step 2: 获取 API Key**

如果未找到 API Key，脚本会显示获取指南：

```
============================================
  Gemini Banana Pro API Key 获取指南
============================================

需要 API Key 才能使用图片生成功能。

获取步骤:
1. 访问 Google Cloud Console:
   https://console.cloud.google.com/apis/credentials?project=_

2. 使用 Google 账号登录（如没有，需要注册，免费）

3. 点击 "Create Credentials" > "API Key"

4. 复制生成的 API Key

5. 选择以下方式之一配置:
   
   方式 A - 保存到 .env 文件:
     echo 'BANANA_API_KEY="您的API Key"' >> .env
   
   方式 B - 设置环境变量:
     export BANANA_API_KEY="您的API Key"
   
   方式 C - 直接在下方输入:
     输入您的 API Key 并按回车

============================================
```

**Step 3: 保存并使用**

- 如果选择方式 A（CUI 输入），脚本会自动保存到 `.env` 文件
- 保存后下次运行无需再次输入

### 手动配置 API Key

**方式 1: 环境变量（推荐临时使用）**

```bash
export BANANA_API_KEY="YOUR_GEMINI_API_KEY"
```

**方式 2: .env 文件（推荐长期使用）**

在项目根目录创建或编辑 `.env` 文件：

```bash
# 在项目根目录执行
echo 'BANANA_API_KEY="您的API Key"' >> .env
```

**方式 3: 全局 .env 文件**

在用户主目录创建：

```bash
echo 'BANANA_API_KEY="您的API Key"' >> ~/.env
```

### 注意事项

- **API Key 是免费的**：Google Gemini API 有免费配额
- **不要泄露**：不要将 API Key 提交到公开的代码仓库
- **使用 .gitignore**：如果使用 .env 文件，确保将其加入 .gitignore

---

## 文本框示意图模板

### 单层横向布局
```
┌─────────────────────────────────────────────────────────────┐
│                     层级名称 (Layer Name)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  模块A   │  │  模块B   │  │  模块C   │  │  模块D   │  │
│  │          │  │          │  │          │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 单层竖向堆叠
```
┌─────────────────────────────┐
│         模块 A (Module A)    │
├─────────────────────────────┤
│         模块 B (Module B)    │
├─────────────────────────────┤
│         模块 C (Module C)    │
└─────────────────────────────┘
```

### 上下层级连接
```
┌─────────────────────────────────────────────┐
│              上层 (Upper Layer)             │
└─────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────┐
│              下层 (Lower Layer)              │
└─────────────────────────────────────────────┘
```

### 四层完整架构图
```
┌─────────────────────────────────────────────────────────────┐
│                    第一层：用户界面层                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  命令行  │  │  Web界面  │  │ 集成开发 │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    第二层：协调控制层                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   工作流引擎                          │  │
│  │  • 智能体调度  • 状态管理  • 错误处理  • 进度跟踪     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    第三层：智能体服务层                       │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │产品分│ │竞品调│ │创新分│ │UX设  │ │文档编│ │原型构│   │
│  │析智能│ │研智能│ │析智能│ │计智能│ │写智能│ │建智能│   │
│  │  体  │ │  体  │ │  体  │ │  体  │ │  体  │ │  体  │   │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    第四层：基础设施层                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  消息队列 │ │  数据存储 │ │ 外部API  │ │  工具库  │      │
│  │ (Redis) │ │(SQLite) │ │   集成   │ │(NLP,AI) │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
```
