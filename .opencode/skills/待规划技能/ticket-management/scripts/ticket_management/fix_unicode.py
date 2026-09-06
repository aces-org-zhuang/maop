#!/usr/bin/env python3
"""
修复CLI脚本中的Unicode字符问题
"""

import re

def fix_unicode_in_file(filepath):
    """修复文件中的Unicode字符"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Unicode表情符号替换表
    unicode_replacements = {
        '📊': '[STATS]',
        '✅': '[DONE]',
        '⏳': '[PENDING]',
        '📦': '[ARCHIVE]',
        '🔧': '[CLEANUP]',
        '🔍': '[RISK]',
        '💾': '[BACKUP]',
        '📋': '[PREVIEW]',
        '⚠️': '[WARNING]',
        '❌': '[ERROR]',
        '⚖️': '[MEDIUM]',
        '🔐': '[SECURITY]',
        '🔄': '[BATCH]',
        '📈': '[REPORT]',
        '✓': '[OK]',
        '✗': '[FAIL]',
        '🔑': '[KEY]',
        '🚀': '[LAUNCH]',
        '🎯': '[TARGET]',
        '📚': '[DOCS]',
        '🛡️': '[SECURITY]',
        '🌐': '[WEB]',
        '🔧': '[TOOL]',
        '📖': '[MANUAL]',
        '🏭': '[FACTORY]',
        '🎊': '[CELEBRATE]',
        '🎉': '[SUCCESS]',
        '🎁': '[GIFT]',
        '🏆': '[ACHIEVE]',
        '🚀': '[ROCKET]',
        '📈': '[CHART]',
        '👥': '[TEAM]',
        '📋': '[CHECKLIST]',
        '🌐': '[NETWORK]',
        '🛡️': '[SHIELD]',
        '🔧': '[WRENCH]',
        '📖': '[BOOK]',
        '🏭': '[INDUSTRY]',
        '🎊': '[PARTY]',
        '🎉': '[CONFETTI]',
        '🎁': '[PRESENT]',
        '🏆': '[TROPHY]',
        '👥': '[PEOPLE]',
    }
    
    # 替换所有Unicode表情符号
    for unicode_char, replacement in unicode_replacements.items():
        content = content.replace(unicode_char, replacement)
    
    # 写入修复后的内容
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修复文件: {filepath}")
    print(f"替换了 {len(unicode_replacements)} 种Unicode字符")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "cli_simple.py"
    
    fix_unicode_in_file(filepath)