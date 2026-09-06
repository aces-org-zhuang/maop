# 代码仓Onboard技能生成器脚本

## 概述

这个Python包包含用于为指定代码仓生成onboard skill的脚本工具集。

## 安装

### 开发模式安装（支持热加载）
```bash
pip install -e .
```

### 全局安装
```bash
pip install .
```

## 使用

### 1. 分析代码仓
```bash
# 分析本地代码仓
analyze-repo /path/to/repo --output analysis.json

# 分析GitHub仓库（需要先克隆）
analyze-repo https://github.com/user/repo --clone --output analysis.json
```

### 2. 生成onboard skill
```bash
# 根据分析结果生成技能
generate-skill analysis.json --output my-project-skill --template web-app

# 使用特定模板
generate-skill analysis.json --output my-project-skill --template python-package
```

### 3. 验证技能
```bash
# 验证生成的技能
validate-skill my-project-skill --verbose

# 验证并自动修复问题
validate-skill my-project-skill --fix

# 生成验证报告
validate-skill my-project-skill --output validation-report.json
```

## 命令行参数

### analyze-repo
```
usage: analyze-repo [-h] [--output OUTPUT] [--clone] [--verbose] target

分析代码仓结构和技术栈

positional arguments:
  target                代码仓路径或URL

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        输出文件路径 (默认: repo-analysis.json)
  --clone               如果是URL，则克隆代码仓
  --verbose, -v         显示详细输出
```

### generate-skill
```
usage: generate-skill [-h] [--output OUTPUT] [--template {web-app,python-package,cli-tool,data-science,mobile-app,generic}] [--verbose] [--overwrite] analysis_file

根据代码仓分析结果生成onboard skill

positional arguments:
  analysis_file         代码仓分析结果JSON文件

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        输出技能目录路径
  --template {web-app,python-package,cli-tool,data-science,mobile-app,generic}
                        技能模板类型 (默认: generic)
  --verbose, -v         显示详细输出
  --overwrite           覆盖已存在的目录
```

### validate-skill
```
usage: validate-skill [-h] [--output OUTPUT] [--verbose] [--fix] skill_dir

验证onboard skill的完整性和正确性

positional arguments:
  skill_dir             技能目录路径

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        验证报告输出文件路径
  --verbose, -v         显示详细输出
  --fix                 自动修复发现的问题
```

## 项目结构

```
code-repo-onboard-skill-generator/
├── __init__.py
├── analyze_repo.py      # 代码仓分析脚本
├── generate_skill.py    # 技能生成脚本
├── validate_skill.py    # 技能验证脚本
└── templates/           # 技能模板
    ├── web-app.md
    ├── python-package.md
    └── generic.md
```

## 开发

### 设置开发环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# 安装开发依赖
pip install -e .[dev]
```

### 运行测试
```bash
# 运行单元测试
pytest tests/

# 运行代码检查
flake8 code_repo_onboard/

# 运行类型检查
mypy code_repo_onboard/
```

## 许可证

MIT License