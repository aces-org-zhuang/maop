# 项目类型分类

## 项目类型识别指南

### 识别方法

#### 1. 通过文件结构识别
```python
def identify_project_type_by_structure(repo_path):
    """通过文件结构识别项目类型"""
    files = os.listdir(repo_path)
    
    # Web应用特征
    if 'package.json' in files and any(f.endswith('.html') for f in files):
        return 'web-application'
    
    # Python包特征
    if 'setup.py' in files or 'pyproject.toml' in files:
        if 'src' in files or any(f.endswith('.py') for f in files):
            return 'python-package'
    
    # 命令行工具特征
    if 'cli' in files or 'bin' in files:
        return 'cli-tool'
    
    # 数据科学项目特征
    if any(f.endswith('.ipynb') for f in files) or 'data' in files:
        return 'data-science'
    
    # 库/框架特征
    if 'lib' in files or 'include' in files:
        return 'library'
    
    return 'unknown'
```

#### 2. 通过配置文件识别
```python
def identify_project_type_by_config(repo_path):
    """通过配置文件识别项目类型"""
    config_files = {
        'package.json': ['web-application', 'node-package', 'cli-tool'],
        'requirements.txt': ['python-web', 'data-science', 'python-package'],
        'pom.xml': ['java-application', 'java-library'],
        'Cargo.toml': ['rust-application', 'rust-library'],
        'go.mod': ['go-application', 'go-library'],
        'docker-compose.yml': ['microservices', 'web-application'],
        'k8s': ['kubernetes-application']
    }
    
    for config_file, project_types in config_files.items():
        if os.path.exists(os.path.join(repo_path, config_file)):
            return project_types[0]  # 返回第一个匹配类型
    
    return 'unknown'
```

## 项目类型分类

### 1. Web应用 (Web Application)

#### 特征
- 前端文件: HTML, CSS, JavaScript/TypeScript
- 后端框架: Django, Flask, Spring Boot, Express等
- 配置文件: package.json, requirements.txt, docker-compose.yml
- 目录结构: src/, public/, templates/, static/

#### 子类型
- **前后端分离**: frontend/ 和 backend/ 目录分离
- **全栈应用**: 前后端在同一项目中
- **微服务**: 多个服务目录，每个服务独立

#### 技能生成要点
- 环境配置: 前端和后端环境分别说明
- 开发流程: 前后端开发、API对接
- 部署: 容器化部署、云平台部署

### 2. 库/包 (Library/Package)

#### 特征
- 语言特定: __init__.py (Python), index.js (Node.js), lib.rs (Rust)
- 构建配置: setup.py, pyproject.toml, Cargo.toml
- 测试目录: tests/, spec/, __tests__
- 文档: README.md, docs/ 目录

#### 子类型
- **Python包**: setup.py, requirements.txt
- **NPM包**: package.json, node_modules/
- **Java库**: pom.xml, src/main/java/
- **Rust库**: Cargo.toml, src/lib.rs

#### 技能生成要点
- 安装方法: pip install, npm install, cargo build
- 使用示例: 代码示例、API文档
- 贡献指南: 代码规范、测试要求

### 3. 命令行工具 (CLI Tool)

#### 特征
- 入口文件: main.py, cli.js, src/main.rs
- 命令行参数解析: argparse, click, commander
- 配置文件: config.yaml, .env, settings.json
- 帮助文档: --help 输出

#### 子类型
- **系统工具**: 文件操作、进程管理
- **开发工具**: 代码生成、构建工具
- **数据工具**: 数据处理、转换工具

#### 技能生成要点
- 安装方法: 全局安装、源码安装
- 使用说明: 命令参考、选项说明
- 配置说明: 配置文件、环境变量

### 4. 数据科学/机器学习 (Data Science/ML)

#### 特征
- 数据文件: .csv, .json, .parquet
- 笔记本文件: .ipynb (Jupyter Notebook)
- 模型文件: .pkl, .h5, .pt
- 数据处理: pandas, numpy, scikit-learn

#### 子类型
- **数据分析**: 数据清洗、可视化
- **机器学习**: 模型训练、评估
- **深度学习**: 神经网络、GPU加速

#### 技能生成要点
- 环境配置: Python环境、GPU支持
- 数据准备: 数据下载、预处理
- 模型训练: 训练流程、参数调优

### 5. 移动应用 (Mobile Application)

#### 特征
- 平台特定: Android (Java/Kotlin), iOS (Swift/Objective-C)
- 构建工具: Gradle, Xcode
- 资源文件: res/, assets/, Images.xcassets
- 配置文件: build.gradle, Podfile, Info.plist

#### 子类型
- **原生应用**: Android Studio, Xcode项目
- **跨平台**: React Native, Flutter, Xamarin
- **混合应用**: Cordova, Ionic

#### 技能生成要点
- 开发环境: Android SDK, Xcode, 模拟器
- 构建发布: 签名、应用商店发布
- 测试调试: 单元测试、UI测试

### 6. 桌面应用 (Desktop Application)

#### 特征
- GUI框架: Electron, Qt, Tkinter, JavaFX
- 平台特定: .exe (Windows), .app (macOS), .deb/.rpm (Linux)
- 资源文件: icons/, resources/, assets/
- 打包工具: PyInstaller, electron-builder, Inno Setup

#### 技能生成要点
- 跨平台支持: 不同平台的构建说明
- 打包发布: 安装包生成、签名
- 自动更新: 更新机制、版本管理

## 技术栈识别

### 编程语言识别
```python
def identify_languages(repo_path):
    """识别项目使用的编程语言"""
    language_files = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.rs': 'Rust',
        '.go': 'Go',
        '.cpp': 'C++',
        '.cs': 'C#',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.r': 'R',
        '.jl': 'Julia'
    }
    
    languages = set()
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            for ext, lang in language_files.items():
                if file.endswith(ext):
                    languages.add(lang)
    
    return list(languages)
```

### 框架识别
```python
def identify_frameworks(repo_path):
    """识别项目使用的框架"""
    framework_indicators = {
        'Django': ['manage.py', 'wsgi.py', 'asgi.py'],
        'Flask': ['app.py', 'flask_app.py', 'requirements.txt:Flask'],
        'React': ['package.json:react', 'src/App.js', 'src/App.tsx'],
        'Vue': ['package.json:vue', 'vue.config.js', 'src/main.js'],
        'Spring Boot': ['pom.xml:spring-boot', 'Application.java'],
        'Express': ['package.json:express', 'app.js', 'server.js'],
        'FastAPI': ['requirements.txt:fastapi', 'main.py:FastAPI'],
        'TensorFlow': ['requirements.txt:tensorflow', 'model.py'],
        'PyTorch': ['requirements.txt:torch', 'model.py']
    }
    
    frameworks = []
    for framework, indicators in framework_indicators.items():
        for indicator in indicators:
            if ':' in indicator:
                file, content = indicator.split(':')
                file_path = os.path.join(repo_path, file)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        if content in f.read():
                            frameworks.append(framework)
                            break
            elif os.path.exists(os.path.join(repo_path, indicator)):
                frameworks.append(framework)
                break
    
    return frameworks
```

## 项目复杂度评估

### 简单项目
- 文件数量: < 50
- 依赖数量: < 10
- 目录深度: 1-2层
- 示例: 工具脚本、简单库

### 中等项目
- 文件数量: 50-200
- 依赖数量: 10-30
- 目录深度: 2-3层
- 示例: Web应用、命令行工具

### 复杂项目
- 文件数量: > 200
- 依赖数量: > 30
- 目录深度: > 3层
- 示例: 企业应用、微服务架构

## 技能生成策略

### 根据项目类型调整
1. **简单项目**:
   - 简化技能结构
   - 重点说明核心功能
   - 减少不必要的部分

2. **中等项目**:
   - 完整技能结构
   - 详细的环境配置
   - 完整的开发流程

3. **复杂项目**:
   - 模块化技能结构
   - 分步骤指南
   - 故障排除和优化

### 内容深度控制
- **初学者友好**: 详细步骤、截图示例
- **开发者导向**: 技术细节、最佳实践
- **专家级别**: 高级配置、性能优化

## 最佳实践

### 1. 类型识别优先
- 先识别项目类型，再生成技能
- 根据类型调整技能结构
- 使用类型特定的模板

### 2. 渐进式披露
- 从简单开始，逐步深入
- 提供快速入门指南
- 链接到详细文档

### 3. 验证和测试
- 验证生成命令的可执行性
- 测试环境配置步骤
- 确认所有链接有效

### 4. 持续更新
- 跟踪项目变化
- 更新技能内容
- 收集用户反馈