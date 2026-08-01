# Weixin Article Extraction Workflow

## 基本信息

**工作流名称**: knowledge-discovery-wechat-extraction
**工作流类型**: aitools
**项目目录**: `{workflow_artifact_root}/knowledge-discovery-wechat-extraction/`
**创建时间**: 2026-04-05
**工作流文件路径**: `{workflow_artifact_root}/knowledge-discovery-wechat-extraction/trace.md`
**本工作流是否有效**: true

### 执行前验证工作流
```bash
workflow-creator validate {workflow_artifact_root}/knowledge-discovery-wechat-extraction/trace.md
```

## 执行步骤

### Stage 1: URL验证
[x] Task: 验证URL格式
    操作(必选)：
        Step1: 检查URL是否包含mp.weixin.qq.com
        Step2: 验证URL格式为https://mp.weixin.qq.com/s/[article_id]
        Step3: 记录验证结果

### Stage 2: 环境准备
[x] Task: 准备执行环境
    操作(必选)：
        Step1: 确认Python 3.7+已安装
        Step2: 确认playwright已安装
        Step3: 确认chromium浏览器已安装(playwright install chromium)

### Stage 3: 内容提取
[ ] Task: 提取文章内容
    操作(必选)：
        Step1: 启动Playwright浏览器(配置反爬虫参数)
        Step2: 打开URL并等待networkidle
        Step3: 执行滚动加载完整内容
        Step4: 提取标题和正文
        Step5: 关闭浏览器释放资源

### Stage 4: 内容处理
[ ] Task: 处理提取内容
    操作(必选)：
        Step1: 生成结构化摘要(100-150字)
        Step2: 提取关键要点(3-5条)
        Step3: 识别技术内容并生成可视化图表
        Step4: 保存结果到指定格式

### Stage 5: 输出交付
[ ] Task: 交付处理结果
    操作(必选)：
        Step1: 按用户要求格式输出(text/json/summary)
        Step2: 保存到指定文件(如有)
        Step3: 验证输出完整性

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | URL格式无效 | 检查URL是否包含mp.weixin.qq.com，提示用户重新输入 | 用户 |
| ERROR:002 | 浏览器启动失败 | 检查playwright安装状态，执行playwright install chromium | 开发人员 |
| ERROR:003 | 页面加载超时 | 增加timeout参数，检查网络连接 | 开发人员 |
| ERROR:004 | 内容提取为空 | 检查页面结构变化，更新选择器 | 开发人员 |
| ERROR:005 | 反爬虫拦截 | 调整User-Agent，增加随机延迟 | 开发人员 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 文章包含技术内容 | THEN: 自动生成架构图/流程图 | 提供可视化辅助理解 | 仅输出文本摘要 |
| WHEN: 文章过长(>5000字) | THEN: 分段提取并合并 | 完整内容不丢失 | 仅提取前2000字 |
| WHEN: 用户要求详细分析 | THEN: 输出完整报告格式 | 包含所有技术细节 | 输出标准摘要 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS_POINT: URL验证 | OBS_METHOD: knowledge-discovery --validate-wechat <url> | 返回VALID | 检查URL格式 |
| OBS_POINT: 环境检查 | OBS_METHOD: python -c "import playwright" | 无错误 | 安装playwright |
| OBS_POINT: 浏览器启动 | OBS_METHOD: playwright install chromium | 安装成功 | 检查网络/代理 |
| OBS_POINT: 内容提取 | OBS_METHOD: 检查提取结果非空 | 标题和正文存在 | 更新选择器 |

## 交付物

1. 提取的文章内容(标题+正文)
2. 结构化摘要(100-150字)
3. 关键要点列表(3-5条)
4. 可视化图表(如适用)
5. 完整报告(可选)

## 目录结构
```markdown
{knowledge_artifact_root}/wechat-extraction/
├── output/                  # 输出文件目录
│   ├── articles/            # 提取的文章
│   ├── summaries/           # 摘要文件
│   └── visualizations/      # 可视化图表
└── trace.md                 # 执行跟踪文件
```

## 占位符号变量清单

| 变量 | 来源 |
|------|------|
| {{ARTICLE_URL}} | 用户输入 |
| {{OUTPUT_FORMAT}} | 用户选择(text/json/summary) |
| {{OUTPUT_DIR}} | 环境变量或默认值 |

## 子工作流清单

| 子工作流名称 | 验证是否通过 |
|--------|----------|
| 无 | N/A |

## AI能力增强

| 类型 | 名称 | 预期使用 |
|--------|----------|----------|
| skill | knowledge-discovery | WHEN 用户提供微信文章URL THEN 触发内容提取 |
| skill | expression-delivery | WHEN 文章包含技术架构 THEN 生成可视化图表 |
| skill | workflow-creator | WHEN 文章包含操作流程 THEN 生成工作流文件 |
| mcp | browser | WHEN 需要访问网页 THEN 使用Playwright浏览器 |

### Markdown文档规范

表格展示：结构化数据使用Markdown表格
图形化展示: 使用 `expression-delivery` 绘制图表
引用链接：避免重复内容，使用相对路径引用
文件大小：单文件控制合理大小，必要时拆分
目录索引：超过500行的文档必须包含目录
引用标注：所有参考资料必须标注来源

## 注意事项

### 核心原则

#### 1. 精简高效原则
- **信息压缩**：优先使用Markdown Table和IPD图表
- **聚焦做什么** When-How 的结构化表达
- **即刻标记**: 完成即刻对任务进行标注[x]

### 工作流命名标准

| 领域 | 类型 | 说明 | 示例 |
|------|------|------|------|
| aitools | skills/agent | AI能力增强 | aitools-knowledge-discovery-wechat |
