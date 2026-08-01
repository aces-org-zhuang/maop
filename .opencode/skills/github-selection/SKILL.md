---
name: github-selection
description: GitHub开源项目选型评估。用于搜索、评估和选择合适的开源项目。触发条件：用户要求GitHub项目选型、技术选型、开源项目评估、项目对比分析。支持四阶段评估：(1)候选清单和推荐 (2)安全扫描和暴露面分析 (3)功能版图分析 (4)部署流程图和方案。
---

# github-selection

GitHub开源项目选型评估工具，帮助快速评估和选择合适的开源项目。

## 使用方法

### 输入参数

- search_keyword: 搜索关键词（必填）
- language: 编程语言过滤（可选）
- min_stars: 最小star数（默认100）
- max_results: 最大结果数（默认10）

### 执行流程

分四个阶段执行，每个阶段完成后等待用户确认：

**阶段一：候选清单和推荐**
1. 收集用户需求并保存配置
2. 使用web_search搜索GitHub项目
3. 使用[skill: github]获取项目详情
4. 评估活跃度、成熟度、社区健康度
5. 生成综合评分和推荐清单
6. 分析项目依赖关系
7. 使用[skill: gh-issues]创建评估issues跟踪进度

**阶段二：安全扫描和暴露面分析**
1. License合规性分析（类型、感染性、业界应用）
2. 安全漏洞扫描（CVE、依赖漏洞）
3. 暴露面分析（浅克隆项目，扫描配置风险）

**阶段三：功能版图分析**
1. 功能模块梳理（从README/docs/examples提取）
2. 用EARS句法生成功能版图

**阶段四：部署流程图和方案**
1. 使用[skill: ipd-uml]生成部署流程图（Mermaid格式）
2. 编写部署方案文档（环境要求、依赖安装、配置步骤、启动命令）
3. 不生成可执行脚本，仅提供部署指南

### 输出文件

```
.aces/projects/github-selection/<选型标题>
├── config.txt
├── data/
│   ├── projects.csv
│   ├── project-details.csv
│   ├── security-scan.csv
│   └── usecases.csv
├── temp/
│   ├── activity-scores.csv
│   ├── maturity-scores.csv
│   ├── community-scores.csv
│   └── repos/  # 浅克隆的代码仓
├── outputs/
│   ├── licenses.csv
│   ├── phase1-candidates.md
│   ├── dependencies.md
│   ├── phase2-security.md
│   ├── phase3-features.md
│   └── phase4-deployment.md  # 部署流程图和方案
```

## 评分标准

### 活跃度得分（0-10分，权重40%）
- 最近commit时间
- 近3个月commit数
- issue响应速度

### 成熟度得分（0-10分，权重30%）
- 项目年龄
- release版本数
- 文档完整性
- 测试覆盖率

### 社区健康度得分（0-10分，权重30%）
- 贡献者数量
- issue关闭率
- PR合并率
- 讨论活跃度

## EARS句法格式

```
WHEN <触发条件> IF <前置条件> THEN <系统行为>
```

按场景分类：核心场景、扩展场景、边缘场景

## 验收 Checklist

- [ ] 生成候选清单报告（outputs/phase1-candidates.md），包含综合评分和推荐理由
- [ ] 完成 License 合规性分析（outputs/licenses.csv），标注感染性
- [ ] 生成功能版图（outputs/phase3-features.md），使用 EARS 句法描述场景
- [ ] 生成部署流程图和方案（outputs/phase4-deployment.md），包含 Mermaid 流程图和部署指南
- [ ] 创建GitHub issues跟踪选型进度（使用gh-issues技能）

## 注意事项

- 每个阶段完成后必须等待用户确认
- 浅克隆使用 depth=1 减少下载量
- License分析包含感染性评估
- 暴露面分析检查默认配置风险
- 依赖关系图使用ASCII格式
