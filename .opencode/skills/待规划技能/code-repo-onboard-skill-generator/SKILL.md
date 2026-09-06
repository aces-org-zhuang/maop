---
name: code-repo-onboard-skill-generator
description: 为指定代码仓生成onboard skill的技能。当需要为GitHub/GitLab代码仓创建快速上手指南、环境配置、开发流程说明等onboarding文档时使用此技能。支持分析代码仓结构、提取关键信息、生成标准化的onboard skill模板。
---

# Code Repo Onboard Skill Generator

## 概述

本技能用于为指定代码仓生成完整的onboard skill，帮助新用户快速上手项目。生成的onboard skill包含项目介绍、环境配置、开发流程、贡献指南等关键信息。

## 输出

生成的onboard skill包含以下文件：
1. `SKILL.md` - 技能主文件，包含项目概述和使用指南
2. `references/` - 参考文档目录
3. `scripts/` - 自动化脚本目录
4. `assets/` - 项目资源目录

## 使用流程

### 1. 分析代码仓
- 克隆或分析目标代码仓
- 提取项目结构、依赖关系、配置文件
- 识别关键文件和目录

### 2. 生成onboard skill模板
- 创建标准化的技能目录结构
- 生成基础SKILL.md模板
- 添加项目特定信息

### 3. 填充内容
- 项目概述和背景
- 环境配置指南
- 开发流程说明
- 测试和部署指南
- 贡献规范

### 4. 验证和优化
- 检查技能完整性
- 验证链接和路径
- 优化文档结构

## 检查清单

- [ ] 代码仓URL或路径已提供
- [ ] 项目类型已识别（Web应用、库、工具等）
- [ ] 主要技术栈已分析
- [ ] 依赖管理方式已确定
- [ ] 构建和测试流程已了解
- [ ] 部署方式已明确
- [ ] 贡献指南已包含
- [ ] 常见问题已收集
- [ ] 技能结构完整
- [ ] 所有链接有效

## 参考文件

- [references/code-analysis.md](references/code-analysis.md) - 代码仓分析指南
- [references/skill-templates.md](references/skill-templates.md) - 技能模板参考
- [references/project-types.md](references/project-types.md) - 项目类型分类

## 脚本

- `scripts/analyze-repo.py` - 代码仓分析脚本
- `scripts/generate-skill.py` - 技能生成脚本
- `scripts/validate-skill.py` - 技能验证脚本
