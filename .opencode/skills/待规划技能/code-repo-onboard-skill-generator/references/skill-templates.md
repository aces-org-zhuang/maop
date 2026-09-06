# 技能模板参考

## 技能结构模板

### 基础技能模板
```
skill-name/
├── SKILL.md
├── references/
│   ├── project-overview.md
│   ├── setup-guide.md
│   ├── development.md
│   └── deployment.md
├── scripts/
│   ├── setup.py
│   ├── setup-environment.sh
│   └── run-tests.sh
└── assets/
    ├── config-templates/
    └── example-files/
```

### SKILL.md 模板

```markdown
---
name: [技能名称]
description: [技能描述，包含触发条件]
---

# [项目名称] Onboard Skill

## 概述

[项目简要介绍，包括用途、技术栈、主要功能]

## 快速开始

### 环境要求
- [编程语言和版本]
- [数据库和版本]
- [其他依赖]

### 安装步骤
1. [克隆仓库]
2. [安装依赖]
3. [配置环境]
4. [启动应用]

## 开发指南

### 项目结构
```
[项目目录结构说明]
```

### 代码规范
- [代码风格指南]
- [提交规范]
- [测试要求]

### 常用命令
```bash
# 开发命令
[开发相关命令]

# 测试命令
[测试相关命令]

# 构建命令
[构建相关命令]
```

## 部署指南

### 环境配置
- [生产环境要求]
- [环境变量配置]
- [数据库配置]

### 部署步骤
1. [构建应用]
2. [配置服务器]
3. [启动服务]
4. [监控和维护]

## 贡献指南

### 如何贡献
1. [Fork仓库]
2. [创建分支]
3. [提交更改]
4. [创建Pull Request]

### 代码审查
- [审查标准]
- [测试要求]
- [文档要求]

## 故障排除

### 常见问题
1. [问题1：描述和解决方案]
2. [问题2：描述和解决方案]
3. [问题3：描述和解决方案]

### 获取帮助
- [文档链接]
- [社区支持]
- [问题跟踪]

## 检查清单

- [ ] 环境配置完成
- [ ] 依赖安装完成
- [ ] 数据库配置完成
- [ ] 应用启动成功
- [ ] 测试通过
- [ ] 部署验证完成
```

## 项目类型特定模板

### Web应用模板

**SKILL.md 特定部分：**
```markdown
## 前端开发
- 框架: [React/Vue/Angular等]
- 构建工具: [Webpack/Vite等]
- 样式: [CSS/Sass/Tailwind等]

## 后端开发
- 框架: [Django/Spring/Express等]
- API设计: [REST/GraphQL等]
- 认证授权: [JWT/OAuth等]

## 数据库
- 类型: [关系型/非关系型]
- 迁移工具: [Alembic/Flyway等]
- 数据模型: [模型定义]
```

### 库/包模板

**SKILL.md 特定部分：**
```markdown
## 安装
```bash
# 从PyPI安装
pip install [package-name]

# 从源码安装
pip install -e .
```

## 使用示例
```python
import [package-name]

# 基本用法示例
```

## API文档
- [主要类和函数]
- [参数说明]
- [返回值说明]

## 开发
- 版本管理: [语义化版本]
- 发布流程: [打包和发布]
- 文档生成: [Sphinx/JSDoc等]
```

### 命令行工具模板

**SKILL.md 特定部分：**
```markdown
## 安装
```bash
# 全局安装
pip install [tool-name]

# 或使用源码
python setup.py install
```

## 使用
```bash
# 基本命令
[tool-name] [command] [options]

# 查看帮助
[tool-name] --help
```

## 命令参考
- `[command1]`: [功能描述]
- `[command2]`: [功能描述]
- `[command3]`: [功能描述]

## 配置
- 配置文件位置: [~/.config/tool-name/config.yaml]
- 环境变量: [TOOL_NAME_API_KEY等]
- 命令行选项: [所有可用选项]
```

## 内容生成规则

### 1. 项目概述生成
- 从README.md提取项目描述
- 从package.json/pom.xml提取项目信息
- 识别技术栈和框架

### 2. 环境配置生成
- 分析依赖文件（requirements.txt, package.json等）
- 提取版本要求
- 生成安装命令

### 3. 开发流程生成
- 分析构建脚本（Makefile, package.json scripts）
- 识别测试框架和命令
- 提取代码规范配置

### 4. 部署指南生成
- 分析部署配置（Dockerfile, docker-compose.yml）
- 识别CI/CD配置
- 提取环境变量要求

### 5. 贡献指南生成
- 从CONTRIBUTING.md提取贡献规范
- 分析.gitignore文件
- 识别代码审查流程

## 自动化生成脚本

### Python生成脚本示例
```python
import os
import json
from jinja2 import Template

def generate_skill_md(repo_analysis, template_path):
    """生成SKILL.md文件"""
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # 准备模板数据
    data = {
        'project_name': repo_analysis.get('name', 'Unknown Project'),
        'description': repo_analysis.get('description', ''),
        'tech_stack': repo_analysis.get('tech_stack', {}),
        'dependencies': repo_analysis.get('dependencies', {}),
        'structure': repo_analysis.get('structure', {}),
        'commands': repo_analysis.get('commands', [])
    }
    
    # 渲染模板
    skill_md_content = template.render(**data)
    
    return skill_md_content

def create_skill_structure(skill_dir, repo_analysis):
    """创建技能目录结构"""
    os.makedirs(os.path.join(skill_dir, 'references'), exist_ok=True)
    os.makedirs(os.path.join(skill_dir, 'scripts'), exist_ok=True)
    os.makedirs(os.path.join(skill_dir, 'assets'), exist_ok=True)
    
    # 生成SKILL.md
    skill_md = generate_skill_md(repo_analysis, 'templates/skill.md.j2')
    with open(os.path.join(skill_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
        f.write(skill_md)
    
    # 生成参考文件
    generate_reference_files(skill_dir, repo_analysis)
    
    # 生成脚本文件
    generate_script_files(skill_dir, repo_analysis)
```

### 模板数据示例
```python
repo_analysis = {
    'name': 'my-awesome-project',
    'description': '一个用于演示的Web应用项目',
    'tech_stack': {
        'frontend': ['React', 'TypeScript', 'Tailwind CSS'],
        'backend': ['Python', 'FastAPI', 'SQLAlchemy'],
        'database': ['PostgreSQL', 'Redis'],
        'infrastructure': ['Docker', 'GitHub Actions']
    },
    'dependencies': {
        'python': ['fastapi>=0.95.0', 'sqlalchemy>=2.0.0'],
        'node': ['react>=18.0.0', 'typescript>=5.0.0']
    },
    'structure': {
        'src_dirs': ['src/', 'frontend/'],
        'test_dirs': ['tests/', 'frontend/__tests__'],
        'config_dirs': ['config/', 'docker/']
    },
    'commands': [
        {'name': 'dev', 'command': 'python -m uvicorn main:app --reload', 'description': '启动开发服务器'},
        {'name': 'test', 'command': 'pytest', 'description': '运行测试'},
        {'name': 'build', 'command': 'docker build -t my-app .', 'description': '构建Docker镜像'}
    ]
}
```

## 验证规则

### 内容完整性检查
1. **必需部分检查**：
   - 项目概述 ✓
   - 环境配置 ✓
   - 开发指南 ✓
   - 部署指南 ✓
   - 贡献指南 ✓

2. **链接有效性检查**：
   - 所有内部链接有效 ✓
   - 外部链接可访问 ✓
   - 文件路径存在 ✓

3. **命令可执行性检查**：
   - 安装命令正确 ✓
   - 构建命令有效 ✓
   - 测试命令可运行 ✓

### 格式规范检查
1. **Markdown格式**：
   - 标题层级正确 ✓
   - 代码块语法正确 ✓
   - 列表格式一致 ✓

2. **代码规范**：
   - 代码示例语法正确 ✓
   - 命令格式规范 ✓
   - 变量命名一致 ✓

### 最佳实践检查
1. **用户体验**：
   - 步骤清晰明确 ✓
   - 错误处理说明 ✓
   - 故障排除指南 ✓

2. **维护性**：
   - 文档结构清晰 ✓
   - 内容易于更新 ✓
   - 版本信息明确 ✓