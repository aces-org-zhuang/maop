# 代码仓分析指南

## 分析步骤

### 1. 基本信息收集
- **仓库URL**: GitHub/GitLab/Bitbucket等
- **项目名称**: 从README或package.json等文件提取
- **项目描述**: 简要说明项目用途
- **许可证**: LICENSE文件内容
- **主要维护者**: 从CONTRIBUTORS或git历史中提取

### 2. 技术栈分析
- **编程语言**: 通过文件扩展名分析
- **框架和库**: 通过配置文件分析（package.json, requirements.txt, pom.xml等）
- **构建工具**: Makefile, CMakeLists.txt, build.gradle等
- **测试框架**: Jest, pytest, JUnit等
- **数据库**: 配置文件中的数据库连接信息

### 3. 项目结构分析
- **源代码目录**: src/, lib/, app/等
- **配置文件目录**: config/, conf/等
- **测试目录**: tests/, spec/, __tests__等
- **文档目录**: docs/, documentation/等
- **构建输出目录**: dist/, build/, target/等

### 4. 依赖分析
- **运行时依赖**: 项目运行所需的依赖
- **开发依赖**: 开发、测试、构建所需的依赖
- **工具依赖**: 代码格式化、linting等工具

### 5. 开发流程分析
- **代码规范**: .editorconfig, .eslintrc, .prettierrc等
- **Git工作流**: .gitignore, git hooks
- **CI/CD配置**: .github/workflows/, .gitlab-ci.yml等
- **部署配置**: Dockerfile, docker-compose.yml, k8s配置

## 关键文件识别

### 必须检查的文件
1. **README.md** - 项目说明文档
2. **package.json** / **requirements.txt** / **pom.xml** - 依赖管理
3. **.gitignore** - Git忽略规则
4. **LICENSE** - 许可证信息
5. **CONTRIBUTING.md** - 贡献指南
6. **CHANGELOG.md** - 变更日志

### 配置文件
1. **配置文件**: .env, config.json, settings.py等
2. **构建配置**: Makefile, CMakeLists.txt, build.gradle等
3. **测试配置**: jest.config.js, pytest.ini, .travis.yml等
4. **部署配置**: Dockerfile, docker-compose.yml, serverless.yml等

## 自动化分析工具

### Python脚本示例
```python
import os
import json
import yaml

def analyze_repo_structure(repo_path):
    """分析代码仓结构"""
    structure = {
        'languages': set(),
        'files': {},
        'dependencies': [],
        'config_files': []
    }
    
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)
            
            # 识别文件类型
            if file.endswith('.py'):
                structure['languages'].add('Python')
            elif file.endswith('.js') or file.endswith('.ts'):
                structure['languages'].add('JavaScript/TypeScript')
            elif file.endswith('.java'):
                structure['languages'].add('Java')
            
            # 识别配置文件
            if file in ['package.json', 'requirements.txt', 'pom.xml', 
                       'build.gradle', 'Cargo.toml', 'go.mod']:
                structure['config_files'].append(rel_path)
    
    return structure
```

### 分析报告格式
```json
{
  "repo_info": {
    "name": "项目名称",
    "description": "项目描述",
    "license": "许可证类型",
    "url": "仓库URL"
  },
  "tech_stack": {
    "languages": ["Python", "JavaScript"],
    "frameworks": ["Django", "React"],
    "databases": ["PostgreSQL", "Redis"],
    "tools": ["Docker", "GitHub Actions"]
  },
  "project_structure": {
    "src_dirs": ["src/", "app/"],
    "test_dirs": ["tests/", "spec/"],
    "config_dirs": ["config/", "conf/"],
    "docs_dirs": ["docs/", "documentation/"]
  },
  "dependencies": {
    "runtime": ["django>=4.0", "react>=18.0"],
    "dev": ["pytest>=7.0", "eslint>=8.0"],
    "build": ["webpack>=5.0", "docker>=20.0"]
  },
  "development": {
    "code_style": [".editorconfig", ".eslintrc"],
    "ci_cd": [".github/workflows/ci.yml"],
    "deployment": ["Dockerfile", "docker-compose.yml"]
  }
}
```

## 常见项目类型

### Web应用
- 前端: HTML/CSS/JavaScript框架
- 后端: Python/Java/Node.js框架
- 数据库: SQL/NoSQL数据库
- 部署: 容器化、云平台

### 库/包
- 语言特定: Python包、NPM包、Java库
- 构建工具: setuptools、webpack、Maven
- 文档: API文档、使用示例
- 测试: 单元测试、集成测试

### 工具/命令行应用
- 命令行接口: argparse、click、commander
- 配置文件: YAML、JSON、TOML
- 日志系统: 日志级别、输出格式
- 错误处理: 异常处理、错误码

### 数据科学/机器学习
- 数据处理: pandas、numpy
- 机器学习: scikit-learn、tensorflow
- 可视化: matplotlib、plotly
- 实验跟踪: MLflow、Weights & Biases

## 最佳实践

### 1. 优先分析关键文件
- 从README开始了解项目
- 检查package.json/requirements.txt了解依赖
- 查看.gitignore了解忽略规则

### 2. 识别项目模式
- 单仓库 vs 多仓库
- 微服务 vs 单体应用
- 前后端分离 vs 一体化

### 3. 提取关键信息
- 版本要求（Python版本、Node版本等）
- 环境变量配置
- 数据库配置
- API密钥和认证

### 4. 验证分析结果
- 检查依赖是否完整
- 验证配置文件有效性
- 测试构建和运行命令
- 确认部署流程