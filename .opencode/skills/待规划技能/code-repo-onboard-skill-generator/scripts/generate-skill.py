#!/usr/bin/env python3
"""
技能生成脚本
根据代码仓分析结果生成onboard skill
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='根据代码仓分析结果生成onboard skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s analysis.json --output my-project-skill
  %(prog)s analysis.json --output my-project-skill --template web-app
        '''
    )
    
    parser.add_argument(
        'analysis_file',
        help='代码仓分析结果JSON文件'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='输出技能目录路径'
    )
    
    parser.add_argument(
        '--template',
        choices=['web-app', 'python-package', 'cli-tool', 'data-science', 'mobile-app', 'generic'],
        default='generic',
        help='技能模板类型 (默认: generic)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='覆盖已存在的目录'
    )
    
    return parser.parse_args()

def load_analysis(analysis_file: Path) -> Dict[str, Any]:
    """加载分析结果"""
    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"错误: 无法加载分析文件: {e}")
        sys.exit(1)

def create_skill_structure(output_dir: Path, overwrite: bool = False):
    """创建技能目录结构"""
    if output_dir.exists():
        if overwrite:
            import shutil
            shutil.rmtree(output_dir)
            print(f"已删除现有目录: {output_dir}")
        else:
            print(f"错误: 目录已存在: {output_dir}")
            print("使用 --overwrite 参数覆盖现有目录")
            sys.exit(1)
    
    # 创建目录结构
    directories = [
        output_dir,
        output_dir / 'references',
        output_dir / 'scripts',
        output_dir / 'assets'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        if args.verbose:
            print(f"创建目录: {directory}")
    
    return output_dir

def generate_skill_md_content(analysis: Dict[str, Any], template: str) -> str:
    """生成SKILL.md内容"""
    repo_info = analysis.get('repo_info', {})
    structure = analysis.get('structure', {})
    config_analysis = analysis.get('config_analysis', {})
    project_type = analysis.get('project_type', 'unknown')
    
    # 提取项目信息
    project_name = repo_info.get('name', 'Unknown Project')
    
    # 从package.json提取描述
    description = ''
    if 'package.json' in config_analysis:
        pkg_config = config_analysis['package.json']
        if isinstance(pkg_config, dict) and 'description' in pkg_config:
            description = pkg_config['description']
    
    # 提取技术栈
    languages = structure.get('languages', [])
    
    # 生成技能描述
    skill_description = f"为{project_name}项目生成的onboard skill。"
    if description:
        skill_description += f" {description}"
    skill_description += " 包含项目概述、环境配置、开发流程、部署指南和贡献规范。"
    
    # 生成触发条件
    trigger_conditions = [
        f"当需要了解{project_name}项目时",
        f"当需要配置{project_name}开发环境时",
        f"当需要参与{project_name}开发时",
        f"当需要部署{project_name}时"
    ]
    
    # 根据项目类型选择模板
    if template == 'generic':
        template = project_type
    
    # 生成SKILL.md内容
    content = f"""---
name: {project_name.lower().replace(' ', '-')}-onboard
description: {skill_description} 使用场景: {'; '.join(trigger_conditions)}。
---

# {project_name} Onboard Skill

## 概述

{description if description else f'{project_name}是一个软件项目。'}

### 技术栈
- **编程语言**: {', '.join(languages) if languages else '未识别'}
- **项目类型**: {project_type}

### 关键特性
- [特性1]
- [特性2]
- [特性3]

## 快速开始

### 环境要求
- [操作系统要求]
- [编程语言版本]
- [数据库要求]
- [其他依赖]

### 安装步骤
1. 克隆仓库
```bash
git clone [仓库URL]
cd {project_name}
```

2. 安装依赖
```bash
[安装命令]
```

3. 配置环境
```bash
[配置命令]
```

4. 启动应用
```bash
[启动命令]
```

## 开发指南

### 项目结构
```
[项目目录结构说明]
```

### 代码规范
- 代码风格: [代码风格指南]
- 提交规范: [Git提交规范]
- 测试要求: [测试覆盖率要求]

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
- 生产环境要求
- 环境变量配置
- 数据库配置

### 部署步骤
1. 构建应用
2. 配置服务器
3. 启动服务
4. 监控和维护

## 贡献指南

### 如何贡献
1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 代码审查
- 审查标准
- 测试要求
- 文档要求

## 故障排除

### 常见问题
1. **问题1**: 描述和解决方案
2. **问题2**: 描述和解决方案
3. **问题3**: 描述和解决方案

### 获取帮助
- 项目文档
- 问题跟踪
- 社区支持

## 检查清单

### 环境配置
- [ ] 操作系统符合要求
- [ ] 编程语言版本正确
- [ ] 依赖安装完成
- [ ] 环境变量配置完成

### 开发准备
- [ ] 代码仓库克隆完成
- [ ] 开发环境配置完成
- [ ] 测试环境准备就绪
- [ ] 构建工具安装完成

### 部署验证
- [ ] 构建过程成功
- [ ] 测试全部通过
- [ ] 部署脚本验证
- [ ] 监控配置完成

## 参考文件

- [references/project-overview.md](references/project-overview.md) - 项目详细概述
- [references/setup-guide.md](references/setup-guide.md) - 完整环境配置指南
- [references/development.md](references/development.md) - 详细开发指南
- [references/deployment.md](references/deployment.md) - 完整部署指南

## 脚本

- `scripts/setup-environment.sh` - 环境设置脚本
- `scripts/run-tests.sh` - 测试运行脚本
- `scripts/build-and-deploy.sh` - 构建部署脚本

---

*最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*基于代码仓分析生成*
"""
    
    return content

def generate_reference_files(skill_dir: Path, analysis: Dict[str, Any]):
    """生成参考文件"""
    
    # 项目概述文件
    project_overview = """# 项目概述

## 项目背景
[项目背景和目的说明]

## 功能特性
- 特性1: [描述]
- 特性2: [描述]
- 特性3: [描述]

## 技术架构
### 系统架构
[系统架构图描述]

### 数据流
[数据流程图描述]

### 组件说明
- 组件1: [功能说明]
- 组件2: [功能说明]
- 组件3: [功能说明]

## 版本历史
| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | YYYY-MM-DD | 初始版本 |
| v1.1 | YYYY-MM-DD | 功能增强 |

## 相关资源
- [官方文档链接]
- [API文档链接]
- [社区论坛链接]
"""
    
    with open(skill_dir / 'references' / 'project-overview.md', 'w', encoding='utf-8') as f:
        f.write(project_overview)
    
    # 环境配置指南
    setup_guide = """# 环境配置指南

## 系统要求
### 最低配置
- 操作系统: [要求]
- 内存: [要求]
- 存储: [要求]
- 网络: [要求]

### 推荐配置
- 操作系统: [推荐]
- 内存: [推荐]
- 存储: [推荐]
- 网络: [推荐]

## 安装步骤
### 1. 基础环境
```bash
# 安装编程语言
[安装命令]

# 验证安装
[验证命令]
```

### 2. 依赖安装
```bash
# 安装系统依赖
[系统依赖安装命令]

# 安装项目依赖
[项目依赖安装命令]
```

### 3. 数据库配置
```bash
# 安装数据库
[数据库安装命令]

# 配置数据库
[数据库配置命令]

# 初始化数据库
[数据库初始化命令]
```

### 4. 服务配置
```bash
# 配置服务
[服务配置命令]

# 启动服务
[服务启动命令]

# 验证服务
[服务验证命令]
```

## 环境变量
### 必需变量
```bash
export DATABASE_URL="[数据库连接字符串]"
export API_KEY="[API密钥]"
export DEBUG="[调试模式]"
```

### 可选变量
```bash
export LOG_LEVEL="[日志级别]"
export CACHE_SIZE="[缓存大小]"
export TIMEOUT="[超时时间]"
```

## 配置文件
### 主要配置文件
1. `config.json` - 应用配置
2. `.env` - 环境变量
3. `database.yml` - 数据库配置

### 配置示例
```json
{
  "server": {
    "port": 3000,
    "host": "localhost"
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "app_db"
  }
}
```

## 故障排除
### 常见问题
1. **依赖安装失败**
   - 检查网络连接
   - 验证版本兼容性
   - 查看错误日志

2. **服务启动失败**
   - 检查端口占用
   - 验证配置文件
   - 查看服务日志

3. **数据库连接失败**
   - 检查数据库状态
   - 验证连接字符串
   - 检查防火墙设置

### 获取帮助
- 查看日志文件: `logs/app.log`
- 查阅文档: [文档链接]
- 提交问题: [问题跟踪链接]
"""
    
    with open(skill_dir / 'references' / 'setup-guide.md', 'w', encoding='utf-8') as f:
        f.write(setup_guide)
    
    # 开发指南
    development_guide = """# 开发指南

## 开发环境
### 编辑器配置
- VS Code配置
- IntelliJ IDEA配置
- 其他编辑器配置

### 开发工具
- 调试工具
- 测试工具
- 构建工具

## 代码结构
### 目录说明
```
project/
├── src/           # 源代码
├── tests/         # 测试代码
├── docs/          # 文档
├── config/        # 配置文件
└── scripts/       # 脚本文件
```

### 模块说明
- `module1/`: [模块1功能]
- `module2/`: [模块2功能]
- `module3/`: [模块3功能]

## 开发流程
### 1. 获取代码
```bash
git clone [仓库URL]
cd [项目目录]
git checkout -b feature/your-feature
```

### 2. 开发准备
```bash
# 安装开发依赖
[开发依赖安装命令]

# 启动开发服务器
[开发服务器启动命令]
```

### 3. 编写代码
- 遵循代码规范
- 编写单元测试
- 更新文档

### 4. 测试验证
```bash
# 运行测试
[测试命令]

# 代码检查
[代码检查命令]

# 构建验证
[构建验证命令]
```

## 代码规范
### 命名规范
- 变量命名: [规范]
- 函数命名: [规范]
- 类命名: [规范]

### 代码风格
- 缩进: [规范]
- 空格: [规范]
- 注释: [规范]

### 提交规范
- 提交消息格式
- 分支命名规范
- 代码审查流程

## 测试指南
### 单元测试
```python
# 测试示例
def test_function():
    assert function(input) == expected_output
```

### 集成测试
```python
# 集成测试示例
def test_integration():
    # 测试多个组件集成
    pass
```

### 性能测试
```python
# 性能测试示例
def test_performance():
    # 测试性能指标
    pass
```

## 调试技巧
### 日志调试
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug('调试信息')
```

### 断点调试
```python
# 设置断点
import pdb
pdb.set_trace()
```

### 性能分析
```python
# 性能分析
import cProfile
cProfile.run('your_function()')
```

## 最佳实践
### 代码质量
- 保持代码简洁
- 避免重复代码
- 及时重构

### 安全性
- 输入验证
- 输出编码
- 权限控制

### 性能优化
- 缓存策略
- 数据库优化
- 代码优化
"""
    
    with open(skill_dir / 'references' / 'development.md', 'w', encoding='utf-8') as f:
        f.write(development_guide)
    
    # 部署指南
    deployment_guide = """# 部署指南

## 部署环境
### 生产环境要求
- 操作系统: [要求]
- 硬件配置: [要求]
- 网络要求: [要求]

### 环境准备
```bash
# 系统更新
sudo apt update && sudo apt upgrade -y

# 安装基础软件
sudo apt install -y [所需软件]

# 配置防火墙
sudo ufw allow [端口]
sudo ufw enable
```

## 部署流程
### 1. 代码准备
```bash
# 获取代码
git clone [仓库URL] --branch [分支] --depth 1

# 进入目录
cd [项目目录]
```

### 2. 环境配置
```bash
# 安装依赖
[依赖安装命令]

# 配置环境变量
echo "export KEY=value" >> ~/.bashrc
source ~/.bashrc
```

### 3. 数据库部署
```bash
# 安装数据库
[数据库安装命令]

# 配置数据库
[数据库配置命令]

# 导入数据
[数据导入命令]
```

### 4. 应用部署
```bash
# 构建应用
[构建命令]

# 配置服务
[服务配置命令]

# 启动应用
[启动命令]
```

## 配置管理
### 配置文件
1. `production.env` - 生产环境变量
2. `nginx.conf` - Web服务器配置
3. `supervisor.conf` - 进程管理配置

### 配置示例
```nginx
# nginx配置示例
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 监控和维护
### 监控指标
- CPU使用率
- 内存使用率
- 磁盘空间
- 网络流量
- 应用性能

### 日志管理
```bash
# 查看应用日志
tail -f /var/log/app.log

# 查看系统日志
tail -f /var/log/syslog

# 日志轮转配置
[日志轮转配置]
```

### 备份策略
```bash
# 数据库备份
pg_dump [数据库名] > backup.sql

# 文件备份
tar -czf backup.tar.gz [目录]

# 备份上传
scp backup.tar.gz [备份服务器]:[路径]
```

## 故障恢复
### 常见问题
1. **服务宕机**
   ```bash
   # 检查服务状态
   systemctl status [服务名]
   
   # 重启服务
   systemctl restart [服务名]
   
   # 查看日志
   journalctl -u [服务名] -f
   ```

2. **数据库问题**
   ```bash
   # 检查数据库状态
   systemctl status [数据库服务]
   
   # 修复数据库
   [数据库修复命令]
   
   # 从备份恢复
   [备份恢复命令]
   ```

3. **性能问题**
   ```bash
   # 监控系统资源
   top
   htop
   
   # 分析性能瓶颈
   [性能分析工具]
   
   # 优化配置
   [优化命令]
   ```

### 应急预案
1. **数据丢失**
   - 立即停止写入
   - 从备份恢复
   - 验证数据完整性

2. **安全漏洞**
   - 隔离受影响系统
   - 应用安全补丁
   - 审计日志记录

3. **灾难恢复**
   - 切换到备用系统
   - 恢复关键服务
   - 逐步恢复全部功能

## 更新和升级
### 版本更新
```bash
# 获取最新代码
git pull origin [分支]

# 更新依赖
[依赖更新命令]

# 重启服务
systemctl restart [服务名]
```

### 数据库迁移
```bash
# 备份当前数据
[备份命令]

# 执行迁移
[迁移命令]

# 验证迁移
[验证命令]
```

### 回滚流程
```bash
# 停止服务
systemctl stop [服务名]

# 回滚代码
git revert [提交]  # 或 git reset --hard [旧提交]

# 恢复数据库
[数据库恢复命令]

# 重启服务
systemctl start [服务名]
```

## 安全最佳实践
### 访问控制
- 最小权限原则
- 定期审计权限
- 多因素认证

### 网络安全
- 防火墙配置
- SSL/TLS加密
- 入侵检测

### 数据安全
- 数据加密
- 定期备份
- 安全删除
"""
    
    with open(skill_dir / 'references' / 'deployment.md', 'w', encoding='utf-8') as f:
        f.write(deployment_guide)

def generate_script_files(skill_dir: Path, analysis: Dict[str, Any]):
    """生成脚本文件"""
    
    # 环境设置脚本
    setup_script = """#!/bin/bash
# 环境设置脚本
# 用于设置开发环境

set -e  # 遇到错误时退出

echo "开始设置开发环境..."

# 检查操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到Linux系统"
    # Linux特定设置
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到macOS系统"
    # macOS特定设置
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "检测到Windows系统"
    # Windows特定设置
else
    echo "未知操作系统: $OSTYPE"
    exit 1
fi

# 检查必要工具
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "错误: $1 未安装"
        echo "请先安装 $1"
        exit 1
    fi
    echo "✓ $1 已安装"
}

echo "检查必要工具..."
check_command git
check_command python3
check_command pip3

# 创建虚拟环境
echo "创建Python虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
fi

# 安装依赖
echo "安装Python依赖..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    pip install -e .
else
    echo "警告: 未找到依赖文件"
fi

# 如果是Node.js项目
if [ -f "package.json" ]; then
    check_command node
    check_command npm
    echo "安装Node.js依赖..."
    npm install
fi

# 数据库设置
if command -v docker &> /dev/null; then
    echo "检测到Docker，尝试启动数据库..."
    if [ -f "docker-compose.yml" ]; then
        docker-compose up -d db
        echo "等待数据库启动..."
        sleep 10
    fi
fi

echo "环境设置完成!"
echo ""
echo "下一步:"
echo "1. 配置环境变量: cp .env.example .env"
echo "2. 运行数据库迁移: [迁移命令]"
echo "3. 启动开发服务器: [启动命令]"
"""
    
    with open(skill_dir / 'scripts' / 'setup-environment.sh', 'w', encoding='utf-8') as f:
        f.write(setup_script)
    
    # 使脚本可执行
    os.chmod(skill_dir / 'scripts' / 'setup-environment.sh', 0o755)
    
    # 测试运行脚本
    test_script = """#!/bin/bash
# 测试运行脚本
# 用于运行项目测试

set -e  # 遇到错误时退出

echo "开始运行测试..."

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    fi
fi

# 运行Python测试
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "运行Python测试..."
    
    # 检查测试框架
    if pip list | grep -q pytest; then
        python -m pytest tests/ -v --cov=.
    elif [ -f "setup.py" ]; then
        python setup.py test
    else
        echo "警告: 未找到Python测试框架"
    fi
fi

# 运行Node.js测试
if [ -f "package.json" ]; then
    echo "运行Node.js测试..."
    
    # 检查package.json中的测试脚本
    if grep -q '"test"' package.json; then
        npm test
    else
        echo "警告: package.json中未定义测试脚本"
    fi
fi

# 运行其他测试
if [ -f "Makefile" ]; then
    echo "运行Makefile测试..."
    make test
fi

echo "测试完成!"
"""
    
    with open(skill_dir / 'scripts' / 'run-tests.sh', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    # 使脚本可执行
    os.chmod(skill_dir / 'scripts' / 'run-tests.sh', 0o755)
    
    # 构建部署脚本
    build_script = """#!/bin/bash
# 构建部署脚本
# 用于构建和部署项目

set -e  # 遇到错误时退出

# 配置
BUILD_DIR="dist"
DEPLOY_ENV=${1:-"staging"}  # 默认部署到staging环境

echo "开始构建和部署到 $DEPLOY_ENV 环境..."

# 清理构建目录
echo "清理构建目录..."
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    fi
fi

# Python项目构建
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "构建Python项目..."
    
    # 安装依赖
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # 如果是包，进行构建
    if [ -f "setup.py" ]; then
        python setup.py sdist bdist_wheel
        cp -r dist/* $BUILD_DIR/
    fi
    
    # 复制必要文件
    cp -r src/ $BUILD_DIR/ 2>/dev/null || true
    cp -r config/ $BUILD_DIR/ 2>/dev/null || true
    cp *.py $BUILD_DIR/ 2>/dev/null || true
fi

# Node.js项目构建
if [ -f "package.json" ]; then
    echo "构建Node.js项目..."
    
    # 安装依赖
    npm ci --only=production
    
    # 运行构建脚本
    if grep -q '"build"' package.json; then
        npm run build
        cp -r build/ $BUILD_DIR/ 2>/dev/null || true
        cp -r public/ $BUILD_DIR/ 2>/dev/null || true
    fi
    
    # 复制必要文件
    cp package.json $BUILD_DIR/
    cp package-lock.json $BUILD_DIR/ 2>/dev/null || true
    cp yarn.lock $BUILD_DIR/ 2>/dev/null || true
fi

# 复制配置文件
echo "复制配置文件..."
cp .env.example $BUILD_DIR/.env 2>/dev/null || true
cp docker-compose.yml $BUILD_DIR/ 2>/dev/null || true
cp Dockerfile $BUILD_DIR/ 2>/dev/null || true

# 创建部署包
echo "创建部署包..."
DEPLOY_PACKAGE="deploy-$DEPLOY_ENV-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf $DEPLOY_PACKAGE -C $BUILD_DIR .

echo "构建完成! 部署包: $DEPLOY_PACKAGE"
echo ""
echo "部署命令示例:"
echo "  scp $DEPLOY_PACKAGE user@server:/path/to/deploy/"
echo "  ssh user@server 'tar -xzf /path/to/deploy/$DEPLOY_PACKAGE -C /path/to/app/'"
echo "  ssh user@server 'cd /path/to/app && docker-compose up -d'"
"""
    
    with open(skill_dir / 'scripts' / 'build-and-deploy.sh', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # 使脚本可执行
    os.chmod(skill_dir / 'scripts' / 'build-and-deploy.sh', 0o755)

def main():
    """主函数"""
    global args
    args = parse_arguments()
    
    # 加载分析结果
    analysis_file = Path(args.analysis_file)
    if not analysis_file.exists():
        print(f"错误: 分析文件不存在: {analysis_file}")
        sys.exit(1)
    
    analysis = load_analysis(analysis_file)
    
    # 创建技能目录结构
    output_dir = Path(args.output)
    skill_dir = create_skill_structure(output_dir, args.overwrite)
    
    # 生成SKILL.md
    print("生成SKILL.md...")
    skill_md_content = generate_skill_md_content(analysis, args.template)
    with open(skill_dir / 'SKILL.md', 'w', encoding='utf-8') as f:
        f.write(skill_md_content)
    
    # 生成参考文件
    print("生成参考文件...")
    generate_reference_files(skill_dir, analysis)
    
    # 生成脚本文件
    print("生成脚本文件...")
    generate_script_files(skill_dir, analysis)
    
    # 生成资产文件占位符
    print("生成资产文件...")
    with open(skill_dir / 'assets' / 'README.md', 'w', encoding='utf-8') as f:
        f.write("# 资产文件\n\n此目录包含项目相关的资产文件，如图片、模板、配置文件等。\n")
    
    print(f"\n技能生成完成! 技能目录: {skill_dir}")
    print("\n生成的文件:")
    print(f"  ✓ {skill_dir}/SKILL.md")
    print(f"  ✓ {skill_dir}/references/ (4个参考文件)")
    print(f"  ✓ {skill_dir}/scripts/ (3个脚本文件)")
    print(f"  ✓ {skill_dir}/assets/ (占位符文件)")
    
    print("\n下一步:")
    print("1. 检查生成的技能内容")
    print("2. 根据实际项目信息更新占位符")
    print("3. 测试脚本功能")
    print("4. 验证技能完整性")

if __name__ == '__main__':
    main()
