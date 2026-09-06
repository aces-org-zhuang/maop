#!/usr/bin/env python3
"""
代码仓分析脚本
用于分析指定代码仓的结构、技术栈和配置信息
"""

import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='分析代码仓结构和技术栈',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s /path/to/repo --output analysis.json
  %(prog)s https://github.com/user/repo --clone --output analysis.json
        '''
    )
    
    parser.add_argument(
        'target',
        help='代码仓路径或URL'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='repo-analysis.json',
        help='输出文件路径 (默认: repo-analysis.json)'
    )
    
    parser.add_argument(
        '--clone',
        action='store_true',
        help='如果是URL，则克隆代码仓'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )
    
    return parser.parse_args()

def identify_language_by_extension(file_path: Path) -> str:
    """通过文件扩展名识别编程语言"""
    extension_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript (React)',
        '.tsx': 'TypeScript (React)',
        '.java': 'Java',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.cpp': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.go': 'Go',
        '.rs': 'Rust',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.swift': 'Swift',
        '.r': 'R',
        '.jl': 'Julia',
        '.sh': 'Shell',
        '.bash': 'Bash',
        '.ps1': 'PowerShell',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'SASS',
        '.less': 'LESS',
        '.sql': 'SQL',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.xml': 'XML',
        '.md': 'Markdown',
        '.txt': 'Text',
        '.ipynb': 'Jupyter Notebook'
    }
    
    ext = file_path.suffix.lower()
    return extension_map.get(ext, 'Unknown')

def analyze_file_structure(repo_path: Path) -> Dict[str, Any]:
    """分析文件结构"""
    structure = {
        'languages': set(),
        'files_by_type': {},
        'directories': [],
        'config_files': [],
        'readme_files': [],
        'license_files': []
    }
    
    for root, dirs, files in os.walk(repo_path):
        # 跳过.git目录
        if '.git' in root.split(os.sep):
            continue
            
        rel_root = Path(root).relative_to(repo_path)
        
        # 记录目录
        if str(rel_root) != '.':
            structure['directories'].append(str(rel_root))
        
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(repo_path)
            
            # 识别语言
            language = identify_language_by_extension(file_path)
            if language != 'Unknown':
                structure['languages'].add(language)
            
            # 按类型分类文件
            file_type = file_path.suffix.lower()[1:] if file_path.suffix else 'no-extension'
            if file_type not in structure['files_by_type']:
                structure['files_by_type'][file_type] = []
            structure['files_by_type'][file_type].append(str(rel_path))
            
            # 识别配置文件
            config_files = [
                'package.json', 'requirements.txt', 'pom.xml', 'build.gradle',
                'Cargo.toml', 'go.mod', 'docker-compose.yml', 'dockerfile',
                '.env', '.env.example', 'config.json', 'settings.py',
                'application.properties', 'application.yml', 'webpack.config.js',
                'tsconfig.json', 'babel.config.js', 'jest.config.js',
                'pytest.ini', '.eslintrc', '.prettierrc', '.editorconfig',
                '.gitignore', '.gitattributes', 'Makefile', 'CMakeLists.txt'
            ]
            
            if file.lower() in [cf.lower() for cf in config_files]:
                structure['config_files'].append(str(rel_path))
            
            # 识别README文件
            if file.lower().startswith('readme'):
                structure['readme_files'].append(str(rel_path))
            
            # 识别LICENSE文件
            if file.lower().startswith('license') or file.lower().startswith('licence'):
                structure['license_files'].append(str(rel_path))
    
    # 转换set为list以便JSON序列化
    structure['languages'] = list(structure['languages'])
    
    return structure

def analyze_package_json(file_path: Path) -> Dict[str, Any]:
    """分析package.json文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        analysis = {
            'name': data.get('name', ''),
            'version': data.get('version', ''),
            'description': data.get('description', ''),
            'main': data.get('main', ''),
            'scripts': data.get('scripts', {}),
            'dependencies': data.get('dependencies', {}),
            'devDependencies': data.get('devDependencies', {}),
            'engines': data.get('engines', {}),
            'keywords': data.get('keywords', []),
            'author': data.get('author', ''),
            'license': data.get('license', '')
        }
        
        # 识别框架
        frameworks = []
        dependencies = {**analysis['dependencies'], **analysis['devDependencies']}
        
        framework_indicators = {
            'react': ['react', 'react-dom'],
            'vue': ['vue', '@vue/cli-service'],
            'angular': ['@angular/core', '@angular/cli'],
            'express': ['express'],
            'nestjs': ['@nestjs/core'],
            'nextjs': ['next'],
            'nuxtjs': ['nuxt'],
            'svelte': ['svelte'],
            'jquery': ['jquery'],
            'bootstrap': ['bootstrap']
        }
        
        for framework, packages in framework_indicators.items():
            for package in packages:
                if package in dependencies:
                    frameworks.append(framework)
                    break
        
        analysis['frameworks'] = frameworks
        
        return analysis
    except Exception as e:
        return {'error': str(e)}

def analyze_requirements_txt(file_path: Path) -> Dict[str, Any]:
    """分析requirements.txt文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        dependencies = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # 提取包名（去除版本说明）
                package = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].strip()
                if package:
                    dependencies.append(package)
        
        # 识别框架
        frameworks = []
        framework_indicators = {
            'django': ['django', 'djangorestframework'],
            'flask': ['flask', 'flask-restful'],
            'fastapi': ['fastapi'],
            'tornado': ['tornado'],
            'celery': ['celery'],
            'sqlalchemy': ['sqlalchemy'],
            'pandas': ['pandas'],
            'numpy': ['numpy'],
            'tensorflow': ['tensorflow'],
            'pytorch': ['torch'],
            'scikit-learn': ['scikit-learn']
        }
        
        for framework, packages in framework_indicators.items():
            for package in packages:
                if any(package in dep.lower() for dep in dependencies):
                    frameworks.append(framework)
                    break
        
        return {
            'dependencies': dependencies,
            'frameworks': frameworks
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_dockerfile(file_path: Path) -> Dict[str, Any]:
    """分析Dockerfile"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            'base_image': '',
            'exposed_ports': [],
            'volumes': [],
            'environment_variables': [],
            'commands': []
        }
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip().upper()
            
            if line.startswith('FROM'):
                analysis['base_image'] = line[4:].strip()
            elif line.startswith('EXPOSE'):
                ports = line[6:].strip().split()
                analysis['exposed_ports'].extend(ports)
            elif line.startswith('VOLUME'):
                volumes = line[6:].strip().split()
                analysis['volumes'].extend(volumes)
            elif line.startswith('ENV'):
                env_vars = line[3:].strip()
                analysis['environment_variables'].append(env_vars)
            elif line.startswith('RUN') or line.startswith('CMD') or line.startswith('ENTRYPOINT'):
                analysis['commands'].append(line)
        
        return analysis
    except Exception as e:
        return {'error': str(e)}

def analyze_config_files(repo_path: Path, structure: Dict[str, Any]) -> Dict[str, Any]:
    """分析配置文件"""
    config_analysis = {}
    
    for config_file in structure['config_files']:
        file_path = repo_path / config_file
        file_name = file_path.name.lower()
        
        try:
            if file_name == 'package.json':
                config_analysis['package.json'] = analyze_package_json(file_path)
            elif file_name == 'requirements.txt':
                config_analysis['requirements.txt'] = analyze_requirements_txt(file_path)
            elif file_name == 'dockerfile' or file_name == 'dockerfile.txt':
                config_analysis['dockerfile'] = analyze_dockerfile(file_path)
            elif file_name.endswith('.yml') or file_name.endswith('.yaml'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_analysis[config_file] = yaml.safe_load(f)
            elif file_name.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_analysis[config_file] = json.load(f)
        except Exception as e:
            config_analysis[config_file] = {'error': str(e)}
    
    return config_analysis

def generate_analysis_report(repo_path: Path, args) -> Dict[str, Any]:
    """生成分析报告"""
    print(f"分析代码仓: {repo_path}")
    
    # 分析文件结构
    print("分析文件结构...")
    structure = analyze_file_structure(repo_path)
    
    # 分析配置文件
    print("分析配置文件...")
    config_analysis = analyze_config_files(repo_path, structure)
    
    # 构建报告
    report = {
        'repo_info': {
            'path': str(repo_path),
            'name': repo_path.name,
            'analysis_timestamp': str(os.path.getmtime(repo_path))
        },
        'structure': {
            'languages': structure['languages'],
            'directories': sorted(structure['directories']),
            'file_types': {k: len(v) for k, v in structure['files_by_type'].items()},
            'config_files': structure['config_files'],
            'readme_files': structure['readme_files'],
            'license_files': structure['license_files']
        },
        'config_analysis': config_analysis,
        'summary': {
            'total_languages': len(structure['languages']),
            'total_directories': len(structure['directories']),
            'total_file_types': len(structure['files_by_type']),
            'total_config_files': len(structure['config_files'])
        }
    }
    
    # 识别项目类型
    project_type = identify_project_type(report)
    report['project_type'] = project_type
    
    return report

def identify_project_type(report: Dict[str, Any]) -> str:
    """识别项目类型"""
    structure = report['structure']
    config = report['config_analysis']
    
    # 检查Web应用特征
    if 'package.json' in config:
        pkg_config = config['package.json']
        if 'scripts' in pkg_config and any('start' in script for script in pkg_config.get('scripts', {})):
            return 'web-application'
    
    # 检查Python包特征
    if 'requirements.txt' in config or any('.py' in lang for lang in structure['languages']):
        if 'setup.py' in structure['config_files'] or 'pyproject.toml' in structure['config_files']:
            return 'python-package'
    
    # 检查命令行工具特征
    if any('cli' in dir.lower() for dir in structure['directories']) or 'bin' in structure['directories']:
        return 'cli-tool'
    
    # 检查数据科学项目
    if any('ipynb' in file_type for file_type in structure['file_types']) or 'data' in structure['directories']:
        return 'data-science'
    
    # 检查移动应用
    if any(dir in ['android', 'ios'] for dir in structure['directories']):
        return 'mobile-application'
    
    return 'unknown'

def main():
    """主函数"""
    args = parse_arguments()
    
    # 检查目标路径
    target_path = Path(args.target)
    
    if not target_path.exists():
        print(f"错误: 路径不存在: {target_path}")
        sys.exit(1)
    
    # 生成分析报告
    report = generate_analysis_report(target_path, args)
    
    # 输出报告
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"分析完成! 报告已保存到: {output_path}")
    
    # 显示摘要
    if args.verbose:
        print("\n分析摘要:")
        print(f"  项目类型: {report['project_type']}")
        print(f"  编程语言: {', '.join(report['structure']['languages'])}")
        print(f"  目录数量: {report['summary']['total_directories']}")
        print(f"  配置文件: {report['summary']['total_config_files']}")

if __name__ == '__main__':
    main()