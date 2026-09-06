#!/usr/bin/env python3
"""
技能验证脚本
用于验证生成的onboard skill的完整性和正确性
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='验证onboard skill的完整性和正确性',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s /path/to/skill --verbose
  %(prog)s /path/to/skill --output validation-report.json
        '''
    )
    
    parser.add_argument(
        'skill_dir',
        help='技能目录路径'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='验证报告输出文件路径'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )
    
    parser.add_argument(
        '--fix',
        action='store_true',
        help='自动修复发现的问题'
    )
    
    return parser.parse_args()

def check_skill_structure(skill_dir: Path) -> Tuple[bool, List[str], List[str]]:
    """检查技能目录结构"""
    required_dirs = ['references', 'scripts', 'assets']
    required_files = ['SKILL.md']
    
    missing_dirs = []
    missing_files = []
    
    # 检查必需目录
    for dir_name in required_dirs:
        dir_path = skill_dir / dir_name
        if not dir_path.exists() or not dir_path.is_dir():
            missing_dirs.append(dir_name)
    
    # 检查必需文件
    for file_name in required_files:
        file_path = skill_dir / file_name
        if not file_path.exists() or not file_path.is_file():
            missing_files.append(file_name)
    
    structure_valid = len(missing_dirs) == 0 and len(missing_files) == 0
    
    return structure_valid, missing_dirs, missing_files

def check_skill_md(skill_dir: Path) -> Tuple[bool, List[str]]:
    """检查SKILL.md文件"""
    issues = []
    skill_md_path = skill_dir / 'SKILL.md'
    
    if not skill_md_path.exists():
        issues.append("SKILL.md文件不存在")
        return False, issues
    
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查YAML frontmatter
        if not content.startswith('---'):
            issues.append("SKILL.md缺少YAML frontmatter")
        else:
            # 提取frontmatter
            lines = content.split('\n')
            if '---' in lines[1:]:
                end_index = lines[1:].index('---') + 1
                frontmatter = '\n'.join(lines[1:end_index])
                
                # 检查必需字段
                required_fields = ['name', 'description']
                for field in required_fields:
                    if f'{field}:' not in frontmatter:
                        issues.append(f"SKILL.md frontmatter缺少{field}字段")
        
        # 检查必需章节
        required_sections = [
            '概述',
            '快速开始',
            '开发指南',
            '部署指南',
            '贡献指南',
            '检查清单'
        ]
        
        for section in required_sections:
            if f'# {section}' not in content and f'## {section}' not in content:
                issues.append(f"SKILL.md缺少'{section}'章节")
        
        # 检查链接有效性
        import re
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        for link_text, link_url in links:
            # 检查内部链接
            if link_url.startswith('references/') or link_url.startswith('scripts/'):
                linked_file = skill_dir / link_url
                if not linked_file.exists():
                    issues.append(f"内部链接无效: {link_url}")
            
            # 检查外部链接格式
            elif link_url.startswith('http'):
                # 只检查格式，不实际访问
                if ' ' in link_url:
                    issues.append(f"外部链接包含空格: {link_url}")
        
        # 检查代码块语法
        code_block_pattern = r'```[a-z]*\n.*?\n```'
        if not re.search(code_block_pattern, content, re.DOTALL):
            issues.append("SKILL.md缺少代码示例")
        
    except Exception as e:
        issues.append(f"读取SKILL.md时出错: {e}")
        return False, issues
    
    skill_md_valid = len(issues) == 0
    return skill_md_valid, issues

def check_reference_files(skill_dir: Path) -> Tuple[bool, List[str]]:
    """检查参考文件"""
    issues = []
    references_dir = skill_dir / 'references'
    
    if not references_dir.exists():
        issues.append("references目录不存在")
        return False, issues
    
    # 检查必需参考文件
    required_refs = [
        'project-overview.md',
        'setup-guide.md',
        'development.md',
        'deployment.md'
    ]
    
    missing_refs = []
    for ref_file in required_refs:
        ref_path = references_dir / ref_file
        if not ref_path.exists():
            missing_refs.append(ref_file)
    
    if missing_refs:
        issues.append(f"缺少参考文件: {', '.join(missing_refs)}")
    
    # 检查参考文件内容
    for ref_file in references_dir.iterdir():
        if ref_file.is_file() and ref_file.suffix == '.md':
            try:
                with open(ref_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查文件是否为空
                if len(content.strip()) == 0:
                    issues.append(f"参考文件为空: {ref_file.name}")
                
                # 检查是否有占位符
                placeholders = ['TODO', 'FIXME', 'XXX', '占位符', '待补充']
                for placeholder in placeholders:
                    if placeholder in content:
                        issues.append(f"参考文件包含占位符: {ref_file.name} -> {placeholder}")
                        break
                
            except Exception as e:
                issues.append(f"读取参考文件时出错 {ref_file.name}: {e}")
    
    references_valid = len(issues) == 0
    return references_valid, issues

def check_script_files(skill_dir: Path) -> Tuple[bool, List[str]]:
    """检查脚本文件"""
    issues = []
    scripts_dir = skill_dir / 'scripts'
    
    if not scripts_dir.exists():
        issues.append("scripts目录不存在")
        return False, issues
    
    # 检查必需脚本
    recommended_scripts = [
        'setup-environment.sh',
        'run-tests.sh',
        'build-and-deploy.sh'
    ]
    
    missing_scripts = []
    for script in recommended_scripts:
        script_path = scripts_dir / script
        if not script_path.exists():
            missing_scripts.append(script)
    
    if missing_scripts:
        issues.append(f"缺少推荐脚本: {', '.join(missing_scripts)}")
    
    # 检查脚本文件
    for script_file in scripts_dir.iterdir():
        if script_file.is_file():
            # 检查文件权限
            if script_file.suffix in ['.sh', '.py']:
                import stat
                mode = os.stat(script_file).st_mode
                if not (mode & stat.S_IEXEC):
                    issues.append(f"脚本文件不可执行: {script_file.name}")
            
            # 检查文件内容
            try:
                with open(script_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline()
                
                # 检查shebang
                if script_file.suffix == '.sh' and not first_line.startswith('#!/'):
                    issues.append(f"Shell脚本缺少shebang: {script_file.name}")
                elif script_file.suffix == '.py' and not first_line.startswith('#!/'):
                    # Python脚本的shebang是可选的
                    pass
                
            except Exception as e:
                issues.append(f"读取脚本文件时出错 {script_file.name}: {e}")
    
    scripts_valid = len(issues) == 0
    return scripts_valid, issues

def check_assets_directory(skill_dir: Path) -> Tuple[bool, List[str]]:
    """检查资产目录"""
    issues = []
    assets_dir = skill_dir / 'assets'
    
    if not assets_dir.exists():
        issues.append("assets目录不存在")
        return False, issues
    
    # 检查目录是否为空
    if not any(assets_dir.iterdir()):
        issues.append("assets目录为空")
    
    # 检查README文件
    readme_path = assets_dir / 'README.md'
    if not readme_path.exists():
        issues.append("assets目录缺少README.md文件")
    
    assets_valid = len(issues) == 0
    return assets_valid, issues

def check_content_consistency(skill_dir: Path) -> Tuple[bool, List[str]]:
    """检查内容一致性"""
    issues = []
    
    # 读取SKILL.md
    skill_md_path = skill_dir / 'SKILL.md'
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            skill_md_content = f.read()
    except:
        return False, ["无法读取SKILL.md"]
    
    # 检查项目名称一致性
    import re
    project_name_match = re.search(r'name:\s*(.+)', skill_md_content)
    if project_name_match:
        project_name = project_name_match.group(1).strip()
        
        # 检查技能目录名称
        if project_name.replace('-', '_') not in skill_dir.name:
            issues.append(f"项目名称'{project_name}'与目录名称'{skill_dir.name}'不一致")
    
    # 检查链接一致性
    references_dir = skill_dir / 'references'
    if references_dir.exists():
        # 获取所有参考文件
        ref_files = [f.name for f in references_dir.iterdir() if f.is_file() and f.suffix == '.md']
        
        # 检查SKILL.md中提到的参考文件是否存在
        for ref_file in ref_files:
            if f'({ref_file})' not in skill_md_content and f'references/{ref_file}' not in skill_md_content:
                issues.append(f"参考文件'{ref_file}'在SKILL.md中未引用")
    
    consistency_valid = len(issues) == 0
    return consistency_valid, issues

def generate_validation_report(skill_dir: Path, args) -> Dict[str, Any]:
    """生成验证报告"""
    report = {
        'skill_info': {
            'path': str(skill_dir),
            'name': skill_dir.name,
            'validation_timestamp': str(os.path.getmtime(skill_dir))
        },
        'checks': {},
        'summary': {
            'total_checks': 0,
            'passed_checks': 0,
            'failed_checks': 0,
            'issues_found': 0
        },
        'issues': []
    }
    
    # 执行检查
    checks = [
        ('structure', check_skill_structure),
        ('skill_md', check_skill_md),
        ('references', check_reference_files),
        ('scripts', check_script_files),
        ('assets', check_assets_directory),
        ('consistency', check_content_consistency)
    ]
    
    for check_name, check_func in checks:
        if args.verbose:
            print(f"检查 {check_name}...")
        
        try:
            valid, issues = check_func(skill_dir)
            
            report['checks'][check_name] = {
                'valid': valid,
                'issues': issues
            }
            
            report['summary']['total_checks'] += 1
            if valid:
                report['summary']['passed_checks'] += 1
            else:
                report['summary']['failed_checks'] += 1
            
            report['summary']['issues_found'] += len(issues)
            report['issues'].extend([f"{check_name}: {issue}" for issue in issues])
            
            if args.verbose:
                if valid:
                    print(f"  ✓ {check_name} 通过")
                else:
                    print(f"  ✗ {check_name} 失败: {', '.join(issues[:3])}")
                    if len(issues) > 3:
                        print(f"    ... 还有 {len(issues)-3} 个问题")
        
        except Exception as e:
            error_msg = f"检查{check_name}时出错: {e}"
            report['checks'][check_name] = {
                'valid': False,
                'error': str(e)
            }
            report['issues'].append(error_msg)
            
            report['summary']['total_checks'] += 1
            report['summary']['failed_checks'] += 1
            report['summary']['issues_found'] += 1
            
            if args.verbose:
                print(f"  ✗ {check_name} 错误: {e}")
    
    # 计算总体状态
    all_valid = all(check['valid'] for check in report['checks'].values() if 'valid' in check)
    report['overall_valid'] = all_valid
    
    return report

def fix_issues(skill_dir: Path, report: Dict[str, Any]):
    """自动修复问题"""
    print("尝试自动修复问题...")
    
    fixes_applied = 0
    
    # 修复目录结构问题
    if 'structure' in report['checks']:
        structure_check = report['checks']['structure']
        if not structure_check['valid'] and 'missing_dirs' in structure_check:
            for dir_name in structure_check.get('missing_dirs', []):
                dir_path = skill_dir / dir_name
                dir_path.mkdir(exist_ok=True)
                print(f"  创建目录: {dir_name}")
                fixes_applied += 1
    
    # 修复资产目录README
    assets_dir = skill_dir / 'assets'
    readme_path = assets_dir / 'README.md'
    if not readme_path.exists() and assets_dir.exists():
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("# 资产文件\n\n此目录包含项目相关的资产文件。\n")
        print(f"  创建资产README文件")
        fixes_applied += 1
    
    # 修复脚本权限
    scripts_dir = skill_dir / 'scripts'
    if scripts_dir.exists():
        for script_file in scripts_dir.iterdir():
            if script_file.is_file() and script_file.suffix in ['.sh', '.py']:
                import stat
                mode = os.stat(script_file).st_mode
                if not (mode & stat.S_IEXEC):
                    os.chmod(script_file, mode | stat.S_IEXEC)
                    print(f"  设置执行权限: {script_file.name}")
                    fixes_applied += 1
    
    print(f"应用了 {fixes_applied} 个修复")
    return fixes_applied

def main():
    """主函数"""
    args = parse_arguments()
    
    # 检查技能目录
    skill_dir = Path(args.skill_dir)
    if not skill_dir.exists():
        print(f"错误: 技能目录不存在: {skill_dir}")
        sys.exit(1)
    
    # 生成验证报告
    print(f"验证技能: {skill_dir}")
    report = generate_validation_report(skill_dir, args)
    
    # 显示摘要
    print(f"\n验证完成!")
    print(f"检查总数: {report['summary']['total_checks']}")
    print(f"通过检查: {report['summary']['passed_checks']}")
    print(f"失败检查: {report['summary']['failed_checks']}")
    print(f"发现问题: {report['summary']['issues_found']}")
    
    if report['overall_valid']:
        print("✓ 技能验证通过!")
    else:
        print("✗ 技能验证失败!")
        
        # 显示问题
        if report['issues']:
            print("\n发现的问题:")
            for i, issue in enumerate(report['issues'][:10], 1):
                print(f"  {i}. {issue}")
            
            if len(report['issues']) > 10:
                print(f"  ... 还有 {len(report['issues'])-10} 个问题")
        
        # 自动修复
        if args.fix:
            fixes_applied = fix_issues(skill_dir, report)
            if fixes_applied > 0:
                print(f"\n修复后重新验证...")
                report = generate_validation_report(skill_dir, args)
                
                if report['overall_valid']:
                    print("✓ 修复后技能验证通过!")
                else:
                    print("✗ 修复后仍有问题，请手动修复")
    
    # 输出报告
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n验证报告已保存到: {output_path}")
    
    # 返回退出码
    sys.exit(0 if report['overall_valid'] else 1)

if __name__ == '__main__':
    main()