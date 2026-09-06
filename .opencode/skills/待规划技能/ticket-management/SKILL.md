---
name: ticket-management
description: 工单管理系统 - 提供工单模板创建、验证、进度查看、归档和清理功能。支持九种工单类型（6标准+3自定义），包含五级安全确认和智能备份机制。
---

# 工单管理系统

## 输出
- 工单创建成功消息
- 验证结果（通过/失败）
- 进度报告（完成率、任务列表）
- 归档/清理操作结果
- 操作日志（增强格式或基本格式）

## 检查清单
- [ ] 所有脚本提供 `-h` 或 `--help` 帮助功能
- [ ] Windows环境优先使用Python CLI
- [ ] 脚本支持热加载（setup.py配置）
- [ ] 文件管理采用Git版本控制
- [ ] 日志系统可操作
- [ ] 软件安装至.aces/目录
- [ ] 版本管理使用Git
- [ ] 国内源优先策略
- [ ] 注释限制：单文件注释不超过500字
- [ ] 文件操作优先使用Git命令
- [ ] 日志提示具备可操作性

## 核心功能
- 创建工单：`ticket-cli add <标题> --template <模板类型>`
- 验证工单：`ticket-cli validate <工单路径>`
- 查看进度：`ticket-cli progress <工单路径>`
- 归档工单：`ticket-cli archive <工单路径> [--auto-cleanup]`
- 查看日志：`ticket-cli logs [--enhanced]`

## 使用场景
- 工单结构验证：验证工单目录结构是否符合规范
- 工单归档管理：归档已完成工单到指定目录
- 工单进度查看：查看工单任务完成情况
- 工单自动清理：安全删除已归档的工单原目录
- 操作日志查看：追溯归档和清理操作历史
- 工单模板使用：使用9个工单模板创建工单

## 模板位置
所有模板文件位于：`templates/` 目录

## 何时读取参考文件
当需要了解以下内容时，应读取对应的参考文件：
- 工单流转关系：`references/ticket_flow_relations.md`
- 工单类型规格：`references/ticket_type_specs.md` 
- 源码构建示例：`references/software_build_example.md`

## 注意事项
1. **验证功能**：仅验证工单结构，不验证内容正确性
2. **归档功能**：支持基本归档和自动清理两种模式
3. **安全清理**：自动清理功能包含五级确认机制防止误删
4. **日志记录**：所有操作都会记录到增强日志文件
5. **强制验证**：创建任何工单后必须立即使用 `ticket-cli validate` 验证结构

## 版本信息
- 版本：v3.10.0
- Python包：ticket-management-cli
- 模板版本：v3.0
- 功能：validate、progress、archive、cleanup、logs
- 设计原则：简单、可靠、专注、与模板同步

## Ticket Types

- **ipo** - IPO工单类型：首次公开募股流程管理