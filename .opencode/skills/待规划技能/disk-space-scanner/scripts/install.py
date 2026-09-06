#!/usr/bin/env python3
"""手动安装脚本，解决pip依赖问题"""

import sys
import os
import shutil

def install_package():
    """手动安装disk-space-scanner包"""
    
    # 获取 site-packages 目录
    site_packages = [p for p in sys.path if 'site-packages' in p][0]
    print(f'安装到: {site_packages}')
    
    # 复制 disk_space_scanner 包
    dest_dir = os.path.join(site_packages, 'disk_space_scanner')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    src_dir = os.path.join(os.getcwd(), 'disk_space_scanner')
    shutil.copytree(src_dir, dest_dir)
    print('✓ 包文件复制完成')
    
    # 创建入口脚本
    entry_script = os.path.join(site_packages, 'disk-space-scanner.py')
    with open(entry_script, 'w') as f:
        f.write('''#!/usr/bin/env python3
import sys
from disk_space_scanner.disk_space_scanner import cli

if __name__ == '__main__':
    sys.exit(cli())
''')
    print('✓ 入口脚本创建完成')
    
    # 创建Windows命令文件
    scripts_dir = os.path.join(os.path.dirname(sys.executable), 'Scripts')
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    
    cmd_path = os.path.join(scripts_dir, 'disk-space-scanner.cmd')
    with open(cmd_path, 'w') as f:
        f.write(f'@echo off\n{sys.executable} "{entry_script}" %*\n')
    
    print(f'✓ Windows命令创建: {cmd_path}')
    print(f'\n安装完成！现在可以使用 disk-space-scanner 命令了')
    print(f'测试命令: disk-space-scanner --help')

if __name__ == '__main__':
    install_package()