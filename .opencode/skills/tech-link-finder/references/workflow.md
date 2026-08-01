# Tech Link Finder Workflow

## 基本信息

**工作流名称**: tech-link-finder-discovery
**工作流类型**: aitools-skills-discovery
**项目目录**: .aces/tech-link-finder
**创建时间**: 2026-04-05
**工作流文件路径**: skills/tech-link-finder/references/workflow.md
**本工作流是否有效**: false

### 执行前验证工作流
执行以下命令
```bash
workflow-creator validate .aces/tech-link-finder/references/workflow.md
```

## 执行步骤

### Stage 1: 准备阶段
[ ] Task: 准备搜索环境
    操作(必选)：
        Step1: 确定搜索关键词和参数
        Step2: 配置搜索模式和过滤条件
        Step3: 验证技术源可用性

### Stage 2: 探索阶段
[ ] Task: 执行广域关键词搜索
    操作(必选)：
        Step1: 使用web_search搜索技术文章
        Step2: 使用github搜索开源项目
        Step3: 收集初步搜索结果

### Stage 3: 分析阶段
[ ] Task: 执行时间序列趋势分析
    操作(必选)：
        Step1: 分析关键词热度变化趋势
        Step2: 计算增长率和排名变化
        Step3: 识别技术生命周期阶段

### Stage 4: 收集阶段
[ ] Task: 精准收集高质量内容
    操作(必选)：
        Step1: 基于热度加权筛选内容
        Step2: 从多源收集技术文章和项目
        Step3: 提取丰富元数据信息

### Stage 5: 整理阶段
[ ] Task: 智能整理和分类
    操作(必选)：
        Step1: 按技术栈和热度分类
        Step2: 去重和优化链接集合
        Step3: 生成最终报告

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | 网络搜索失败 | 检查网络连接，重试搜索，如失败则切换搜索源 | AI代理 |
| ERROR:002 | GitHub API限制 | 等待API恢复，或使用缓存数据 | AI代理 |
| ERROR:003 | 数据解析失败 | 验证数据格式，重新解析或跳过无效数据 | AI代理 |
| ERROR:004 | 输出文件写入失败 | 检查文件权限和路径，重试写入 | AI代理 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 多个技术源结果冲突 | THEN: **权衡权威性**：<br>① 优先选择企业级技术博客<br>② 平衡中文和国际技术源 | 结果权威性最高，覆盖面最广 | 锁定至单一可靠技术源 |
| WHEN: 热度趋势数据不完整 | THEN: **权衡完整性**：<br>① 使用可用数据进行趋势推断<br>② 标注数据不完整警告 | 趋势分析基本准确，有明确标注 | 使用简化分析模式，忽略趋势数据 |
| WHEN: 搜索关键词过于宽泛 | THEN: **权衡精确性**：<br>① 自动扩展相关关键词<br>② 优先搜索热门相关技术 | 搜索结果覆盖面广，相关性高 | 缩小搜索范围，聚焦核心关键词 |
| WHEN: 发现重复或相似内容 | THEN: **权衡独特性**：<br>① 保留质量最高或最新内容<br>② 合并相似内容的元数据 | 内容集合精简，无重复信息 | 保留所有内容，但明确标注重复 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS_POINT: 搜索结果数量 | OBS_METHOD: 统计返回结果数 | 结果数 >= 最小预期数 | 扩大搜索范围，调整关键词 |
| OBS_POINT: 内容质量评分 | OBS_METHOD: 计算平均质量评分 | 平均质量 >= 质量阈值 | 降低质量要求，或更换搜索源 |
| OBS_POINT: 热度指数分布 | OBS_METHOD: 分析热度指数分布 | 热度分布合理，有梯度 | 检查热度计算逻辑，重新分析 |
| OBS_POINT: 链接有效性 | OBS_METHOD: 验证链接可访问性 | 有效链接比例 >= 90% | 清理无效链接，增加验证步骤 |

## 交付物

**主要交付物**:
- 技术链接集合 (JSON/CSV/Markdown格式)
- 趋势分析报告
- 热度排行榜
- 学习路径建议
- 技术雷达图

## 目录结构

```markdown
.aces/flows/aitools-skills-discovery/tech-link-finder/
├── output/                  # 输出文件目录
│   ├── links.json           # 技术链接集合
│   ├── trends.md            # 趋势分析报告
│   ├── rankings.csv         # 热度排行榜
│   ├── learning-path.md     # 学习路径建议
│   └── tech-radar.md        # 技术雷达图
├── logs/                    # 执行日志
├── temp/                    # 临时文件
└── trace.md                 # 执行跟踪文件
```

## 占位符号变量清单

| 变量 | 来源 |
|--------|----------|
| {search_query} | 用户输入的搜索关键词 |
| {search_mode} | 用户选择的搜索模式 |
| {trend_period} | 趋势分析时间周期 |
| {output_format} | 用户选择的输出格式 |
| {min_quality} | 最小质量阈值，默认为3 |
| {max_results} | 最大结果数，默认为10 |

## 子工作流清单

| 子工作流名称 | 验证是否通过 |
|--------|----------|
| 无子工作流 | 不适用 |

## AI能力增强

| 类型 | 名称 | 预期使用 |
|--------|----------|----------|
| mcp | web_search | WHEN 需要搜索技术文章 THEN 使用web_search工具搜索指定关键词 |
| skill | github-selection | WHEN 需要搜索开源项目 THEN 使用github-selection技能发现相关项目 |
| slashcommand | /search | WHEN 需要快速搜索 THEN 使用/search命令获取技术信息 |
| skill | ipd-uml | WHEN 需要可视化趋势 THEN 使用ipd-uml技能生成趋势图表 |

## 注意事项

### 核心原则

#### 1. 精简高效原则
- **信息压缩**：优先使用Markdown Table和IPD图表
- **聚焦做什么** When-How 的结构化表达
- **即刻标记**: 完成即刻对任务进行标注[x]

#### 2. 质量保证原则
- **多源验证**：从多个技术源验证信息准确性
- **热度加权**：基于时间序列热度进行智能排序
- **时效性**：优先推荐最新高质量内容

#### 3. 渐进式披露原则
- **分层展示**：从概括到详细的分层信息展示
- **按需加载**：仅在需要时加载详细信息
- **智能推荐**：基于分析结果提供个性化推荐

### 工作流命名标准

| 领域 | 类型 | 说明 | 示例 |
|------|------|------|------|
| user | softinstall/setup | 个人用户场景 | user-softinstall-vscode |
| ipd | coding/review/ops/data/sec | 集成产品开发 | ipd-coding-webui |
| aigc | ppt/xlsx/doc | AIGC内容生成 | aigc-ppt-report |
| aitools | skills/agent | AI能力增强 | aitools-skills-creator |

### Markdown文档规范

- **表格展示**：结构化数据使用Markdown表格
- **图形化展示**：使用技能ipd-uml绘制IPD图表，精简表达
- **引用链接**：避免重复内容，使用相对路径引用
- **文件大小**：单文件控制合理大小，必要时拆分
- **目录索引**：超过500行的文档必须包含目录
- **引用标注**：所有参考资料必须标注来源