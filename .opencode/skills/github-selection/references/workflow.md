# GitHub Selection - 详细执行步骤

## 阶段一：候选清单和推荐

### 任务1：收集用户需求
- 询问搜索关键词（必填）
- 询问编程语言偏好（可选）
- 询问最小star数要求（默认100）
- 询问需要评估的项目数量（默认10）
- 保存配置到 config.txt

### 任务2：搜索GitHub项目
- 使用 web_search 搜索 GitHub 项目
- 按 star 数排序
- 过滤符合条件的项目
- 提取项目基本信息（名称、URL、star、描述）
- 保存到 data/projects.csv

### 任务3：获取项目详细信息
- 遍历候选项目列表
- 使用 [skill: github] 获取项目详情
- 提取关键指标：star数、fork数、issue数、最后更新时间、贡献者数
- 检查 README 质量
- 保存到 data/project-details.csv

### 任务4：评估项目活跃度
- 检查最近 commit 时间
- 统计近3个月的 commit 数
- 检查 issue 响应速度
- 计算活跃度得分（0-10分）
- 保存到 temp/activity-scores.csv

### 任务5：评估项目成熟度
- 检查项目年龄
- 检查 release 版本数
- 检查文档完整性
- 检查测试覆盖率（如果可获取）
- 计算成熟度得分（0-10分）
- 保存到 temp/maturity-scores.csv

### 任务6：评估社区健康度
- 统计贡献者数量
- 检查 issue 关闭率
- 检查 PR 合并率
- 检查讨论活跃度
- 计算社区得分（0-10分）
- 保存到 temp/community-scores.csv

### 任务7：生成综合评分和推荐
- 合并所有评分数据
- 计算加权总分（活跃度40%、成熟度30%、社区30%）
- 按总分排序
- 为每个项目生成推荐理由
- 标注推荐权重（高/中/低）
- 生成备选清单报告
- 等待用户确认
- 输出：outputs/phase1-candidates.md

### 任务8：分析项目依赖关系
- 检查项目间是否存在直接依赖
- 分析技术栈重叠
- 识别互补关系
- 标注依赖层级（基础设施层/应用层）
- 生成依赖关系图（ASCII）
- 保存到 outputs/dependencies.md

## 阶段二：安全扫描和暴露面分析

### 任务9：License合规性分析
- 识别项目 License 类型（MIT/Apache/GPL/BSD等）
- 分析 License 感染性（强感染/弱感染/无感染）
- 统计代码行数（使用 cloc 或 tokei）
- 评估代码仓活跃度（commit频率、贡献者数）
- 评估成熟度（项目年龄、版本数）
- 搜索业界应用案例（知名公司使用情况）
- 分析受众类型（企业级/个人开发者/学术研究）
- 保存到 .aces/licenses/projects.csv
- 列：代码仓名称、链接、License类型、感染分析、活跃度、行数、成熟度、业界应用、受众类型

### 任务10：安全漏洞扫描
- 使用 [skill: github] 检查 Security Advisories
- 检查依赖项漏洞
- 查看 CVE 记录
- 统计漏洞数量和严重程度
- 保存到 data/security-scan.csv

### 任务11：暴露面分析
- 浅克隆项目到 temp/repos/ 目录（depth=1）
- 扫描配置文件中的网络监听设置（如端口、host配置）
- 检查默认配置的暴露风险（如0.0.0.0监听、默认密码）
- 分析 README 和 docs 中的部署说明
- 检查环境变量要求和敏感配置
- 统计第三方依赖数量和风险等级
- 生成暴露面报告
- 等待用户确认
- 输出：outputs/phase2-security.md

## 阶段三：功能版图分析

### 任务12：功能模块梳理
- 使用已克隆的代码（temp/repos/）
- 扫描 README.md 提取使用场景和示例
- 检查 docs/ 目录获取教程和用例
- 读取 examples/ 或 demo/ 目录的示例代码
- 提取 issue 和 discussion 中的高频使用场景
- 识别主要功能入口和 API
- 保存到 data/usecases.csv

### 任务13：生成功能版图
- 基于 usecases.csv 整理使用场景
- 用 EARS 句法表述（WHEN <触发条件> IF <前置条件> THEN <系统行为>）
- 按场景分类（核心场景、扩展场景、边缘场景）
- 对比不同项目的场景覆盖度
- 绘制场景关系图（ASCII）
- 生成功能版图报告
- 等待用户确认
- 输出：outputs/phase3-features.md

## 阶段四：集成建议

### 任务14：生成集成建议
- 需要真实集成、安装、验证或交付时，转入 `implementation-delivery`。
- 只需要方案表达、部署流程图或演示材料时，转入 `expression-delivery`。
- 输出：outputs/phase4-deploy.md
