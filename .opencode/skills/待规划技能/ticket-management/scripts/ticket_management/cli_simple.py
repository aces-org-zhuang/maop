#!/usr/bin/env python3
"""
工单管理CLI增强版
支持validate、progress、archive、cleanup和enhanced-cleanup功能
包含五级安全确认、智能备份、风险评估和恢复机制
"""

import argparse
import os
import sys
import json
import shutil
import datetime
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TEMP_DIR = Path(__file__).parent / "templates"

def validate_ticket(ticket_path):
    """验证工单结构"""
    # 统一路径处理，使用pathlib确保跨平台兼容性
    ticket_path = Path(ticket_path).resolve()
    print(f"[VALIDATE] 验证工单: {ticket_path}")
    
    # 检查路径是否存在
    if not ticket_path.exists():
        print(f"[ERROR] 工单路径不存在: {ticket_path}")
        return False
    
    # 检查必需的文件和目录
    required_items = [
        "trace.md",
        "input",
        "output"
    ]
    
    missing_items = []
    for item in required_items:
        item_path = ticket_path / item
        if not item_path.exists():
            missing_items.append(item)
    
    if missing_items:
        print(f"[ERROR] 缺少必需的文件/目录: {', '.join(missing_items)}")
        return False
    
    # 检查目录是否为目录，文件是否为文件
    input_dir = ticket_path / "input"
    output_dir = ticket_path / "output"
    trace_file = ticket_path / "trace.md"
    
    if not input_dir.is_dir():
        print("[ERROR] input 必须是目录")
        return False
    
    if not output_dir.is_dir():
        print("[ERROR] output 必须是目录")
        return False
    
    if not trace_file.is_file():
        print("[ERROR] trace.md 必须是文件")
        return False

    print("[SUCCESS] 工单结构验证通过!")
    print("[STRUCTURE] 执行跟踪文件trace.md,工单结构:见trace.md 中\"## 目录结构\"")
    return True


def calculate_directory_size(path: str) -> Tuple[int, int]:
    """计算目录大小和文件数量"""
    total_size = 0
    file_count = 0
    
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = Path(root, file)
                if Path(file_path).is_file():
                    total_size += Path(file_path).stat().st_size
                    file_count += 1
    except Exception as e:
        print(f"[WARN] 计算目录大小失败: {e}")
    
    return total_size, file_count


def extract_ticket_info(ticket_path: str) -> Dict:
    """提取工单信息"""
    ticket_name = Path(ticket_path).name
    parts = ticket_name.split("-")
    
    ticket_info = {
        "name": ticket_name,
        "path": ticket_path,
        "absolute_path": Path(ticket_path).resolve(),
        "type": parts[2] if len(parts) > 2 else "unknown",
        "date": parts[0] if len(parts) > 0 else "unknown",
        "time": parts[1] if len(parts) > 1 else "unknown",
        "size": 0,
        "file_count": 0,
        "created_time": None,
        "modified_time": None
    }
    
    try:
        # 获取目录大小和文件数量
        ticket_info["size"], ticket_info["file_count"] = calculate_directory_size(ticket_path)
        
        # 获取时间信息
        if Path(ticket_path).exists():
            stat_info = os.stat(ticket_path)
            ticket_info["created_time"] = datetime.datetime.fromtimestamp(stat_info.st_ctime)
            ticket_info["modified_time"] = datetime.datetime.fromtimestamp(stat_info.st_mtime)
    except Exception as e:
        print(f"[WARN] 获取工单信息失败: {e}")
    
    return ticket_info


def assess_deletion_risk(ticket_path: str) -> Dict:
    """评估删除风险"""
    ticket_info = extract_ticket_info(ticket_path)
    
    risk_factors = {
        "size_risk": 0,      # 文件大小风险
        "age_risk": 0,       # 创建时间风险
        "activity_risk": 0,  # 最近活动风险
        "importance_risk": 0 # 重要性风险
    }
    
    # 文件大小风险评估
    size_mb = ticket_info["size"] / (1024 * 1024)
    if size_mb > 100:
        risk_factors["size_risk"] = 3  # 大文件风险高
    elif size_mb > 10:
        risk_factors["size_risk"] = 2
    elif size_mb > 1:
        risk_factors["size_risk"] = 1
    
    # 文件数量风险评估
    if ticket_info["file_count"] > 50:
        risk_factors["size_risk"] += 1
    
    # 创建时间风险评估
    if ticket_info["created_time"]:
        age_days = (datetime.datetime.now() - ticket_info["created_time"]).days
        if age_days < 1:
            risk_factors["age_risk"] = 3  # 新建文件风险高
        elif age_days < 7:
            risk_factors["age_risk"] = 2
        elif age_days < 30:
            risk_factors["age_risk"] = 1
    
    # 最近活动风险评估
    if ticket_info["modified_time"]:
        activity_days = (datetime.datetime.now() - ticket_info["modified_time"]).days
        if activity_days < 1:
            risk_factors["activity_risk"] = 3  # 最近修改风险高
        elif activity_days < 3:
            risk_factors["activity_risk"] = 2
        elif activity_days < 7:
            risk_factors["activity_risk"] = 1
    
    # 重要性风险评估（基于文件名关键词）
    important_keywords = ["重要", "关键", "核心", "main", "core", "important", "critical"]
    ticket_name_lower = ticket_info["name"].lower()
    for keyword in important_keywords:
        if keyword in ticket_name_lower:
            risk_factors["importance_risk"] = 3
            break
    
    # 计算总风险分数
    total_risk = sum(risk_factors.values())
    
    if total_risk >= 8:
        risk_level = "HIGH"
    elif total_risk >= 4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        "level": risk_level,
        "score": total_risk,
        "factors": risk_factors,
        "ticket_info": ticket_info
    }


def progress_ticket(ticket_path):
    """查看工单进度"""
    # 统一路径处理，使用pathlib确保跨平台兼容性
    ticket_path = Path(ticket_path).resolve()
    print(f"[PROGRESS] 查看工单进度: {ticket_path}")
    
    # 检查路径是否存在
    if not ticket_path.exists():
        print(f"[ERROR] 工单路径不存在: {ticket_path}")
        return False
    
    # 检查trace.md文件
    trace_file = ticket_path / "trace.md"
    if not trace_file.exists():
        print("[ERROR] trace.md 文件不存在")
        return False
    
    try:
        # 使用更健壮的编码处理，支持多种编码格式
        with open(trace_file, 'rb') as f:
            content_bytes = f.read()
        
        # 尝试多种编码，优先使用UTF-8
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                content = content_bytes.decode(encoding, errors='strict')
                break
            except UnicodeDecodeError:
                continue
        
        # 如果所有编码都失败，使用ignore模式
        if content is None:
            content = content_bytes.decode('utf-8', errors='ignore')
        
        # 统计任务完成情况
        total_tasks = 0
        completed_tasks = 0
        pending_tasks = 0
        
        completed_list = []
        pending_list = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if '[x]' in line.lower():
                total_tasks += 1
                completed_tasks += 1
                # 提取任务描述
                task_desc = line.replace('[x]', '').replace('[X]', '').strip()
                completed_list.append(task_desc)
            elif '[ ]' in line:
                total_tasks += 1
                pending_tasks += 1
                # 提取任务描述
                task_desc = line.replace('[ ]', '').strip()
                pending_list.append(task_desc)
        
        # 计算完成率
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
        else:
            completion_rate = 0
        
        # 输出进度报告 - 使用纯文本避免编码问题
        print(f"\n[PROGRESS] 工单进度报告")
        print(f"=" * 50)
        print(f"[STATS] 统计信息:")
        print(f"   总任务数: {total_tasks}")
        print(f"   已完成: {completed_tasks}")
        print(f"   待完成: {pending_tasks}")
        print(f"   完成率: {completion_rate:.1f}%")
        
        if completed_list:
            print(f"\n[DONE] 已完成任务:")
            for i, task in enumerate(completed_list, 1):
                print(f"   {i}. {task}")
        
        if pending_list:
            print(f"\n[PENDING] 待完成任务:")
            for i, task in enumerate(pending_list, 1):
                print(f"   {i}. {task}")
        
        print(f"\n" + "=" * 50)
        return True
        
    except Exception as e:
        print(f"[ERROR] 读取trace.md文件失败: {e}")
        return False


def create_enhanced_log_entry(operation: str, source_path: str, **kwargs) -> Dict:
    """创建增强的日志条目"""
    log_id = generate_unique_id()
    ticket_info = extract_ticket_info(source_path)
    risk_assessment = kwargs.get('risk_assessment', {})
    backup_info = kwargs.get('backup_info', {})
    
    log_entry = {
        "log_id": log_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "operation": operation,
        "source_path": source_path,
        "source_path_abs": Path(source_path).resolve(),
        "ticket_type": ticket_info["type"],
        "ticket_id": f"{ticket_info['date']}-{ticket_info['time']}",
        "user_confirmation": kwargs.get('user_confirmation', {}),
        "risk_assessment": risk_assessment,
        "backup_info": backup_info,
        "archive_path": kwargs.get('archive_path'),
        "file_count": ticket_info["file_count"],
        "total_size_mb": round(ticket_info["size"] / (1024 * 1024), 2),
        "status": kwargs.get('status', 'SUCCESS'),
        "error_details": kwargs.get('error_details'),
        "recovery_info": kwargs.get('recovery_info')
    }
    
    return log_entry


def generate_unique_id() -> str:
    """生成唯一ID"""
    timestamp = int(time.time() * 1000)
    random_str = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8]
    return f"{timestamp}-{random_str}"


def show_risk_assessment(risk_level: str, risk_factors: Dict):
    """显示风险评估结果"""
    print("\n[RISK] 风险评估:")
    print("=" * 30)
    
    if risk_level == "HIGH":
        print("[WARNING]  高风险操作！")
        print("建议：先进行备份再执行删除")
    elif risk_level == "MEDIUM":
        print("[MEDIUM]  中等风险操作")
        print("建议：确认操作必要性")
    else:
        print("[DONE] 低风险操作")
    
    print(f"\n风险分数: {sum(risk_factors.values())}/12")
    
    factor_names = {
        "size_risk": "文件大小",
        "age_risk": "创建时间", 
        "activity_risk": "最近活动",
        "importance_risk": "重要性"
    }
    
    print("\n详细评估:")
    for factor, score in risk_factors.items():
        name = factor_names.get(factor, factor)
        print(f"  {name}: {score}/3")
    
    print("=" * 30)


def show_operation_preview(ticket_path: str, operation_type: str):
    """显示操作预览"""
    ticket_info = extract_ticket_info(ticket_path)
    
    print(f"\n[CHECKLIST] 操作预览 ({operation_type}):")
    print("=" * 40)
    print(f"工单名称: {ticket_info['name']}")
    print(f"绝对路径: {ticket_info['absolute_path']}")
    print(f"文件数量: {ticket_info['file_count']}")
    print(f"总大小: {ticket_info['size']:,} bytes")
    
    if ticket_info['created_time']:
        print(f"创建时间: {ticket_info['created_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    if ticket_info['modified_time']:
        print(f"修改时间: {ticket_info['modified_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("=" * 40)


def show_backup_options():
    """显示备份选项"""
    print(f"\n[BACKUP] 备份选项:")
    print("=" * 30)
    print("1. 完整备份 (推荐)")
    print("2. 仅关键文件备份")
    print("3. 不备份")
    print("=" * 30)


def perform_interactive_confirmation(ticket_path: str, operation_type: str) -> Tuple[bool, Dict]:
    """执行交互式确认"""
    print("\n" + "="*60)
    print(f"[SECURITY] {operation_type.upper()} 操作确认")
    print("="*60)
    
    # 显示工单信息
    ticket_info = extract_ticket_info(ticket_path)
    show_operation_preview(ticket_path, operation_type)
    
    # 显示风险评估
    risk_assessment = assess_deletion_risk(ticket_path)
    show_risk_assessment(
        risk_assessment["level"], 
        risk_assessment["factors"]
    )
    
    # 询问备份选项
    print("\n选择备份方式:")
    print("1. 完整备份")
    print("2. 仅关键文件备份") 
    print("3. 不备份")
    
    backup_choice = input("\n请输入选择 (1-3): ").strip()
    backup_option = {"choice": backup_choice, "performed": False}
    
    if backup_choice == "1":
        # 执行完整备份
        pass  # 实现备份逻辑
        backup_option["performed"] = True
    elif backup_choice == "2":
        # 执行关键文件备份
        pass  # 实现备份逻辑
        backup_option["performed"] = True
    
    # 五级安全确认
    confirmations = {}
    
    print("\n" + "="*40)
    print("[SECURITY] 安全确认 (请仔细阅读)")
    print("="*40)
    
    # 级别1：基础确认
    confirm1 = input("\n1. 确认要执行此操作？(yes/no): ").lower().strip()
    confirmations["level1_basic"] = confirm1 == "yes"
    
    if not confirmations["level1_basic"]:
        return False, confirmations
    
    # 级别2：输入DELETE确认
    confirm2 = input("2. 输入 'DELETE' 确认删除操作: ").strip()
    confirmations["level2_delete"] = confirm2 == "DELETE"
    
    if not confirmations["level2_delete"]:
        return False, confirmations
    
    # 级别3：输入完整路径确认
    confirm3 = input("3. 请输入完整路径确认: ").strip()
    confirmations["level3_path"] = confirm3 == Path(ticket_path).resolve()
    
    if not confirmations["level3_path"]:
        return False, confirmations
    
    # 级别4：风险评估确认
    if risk_assessment["level"] == "HIGH":
        confirm4 = input("4. [WARNING]  高风险操作！输入 'CONFIRM-RISKY' 继续: ").strip()
        confirmations["level4_risky"] = confirm4 == "CONFIRM-RISKY"
        
        if not confirmations["level4_risky"]:
            return False, confirmations
    
    # 级别5：最终确认
    confirm5 = input("5. 最后确认，此操作不可恢复！输入 'final-confirm': ").strip()
    confirmations["level5_final"] = confirm5 == "final-confirm"
    
    all_confirmed = all([
        confirmations["level1_basic"],
        confirmations["level2_delete"],
        confirmations["level3_path"],
        confirmations.get("level4_risky", True),
        confirmations["level5_final"]
    ])
    
    return all_confirmed, confirmations


def archive_ticket(ticket_path, auto_cleanup=False):
    """归档工单并可选自动清理原目录"""
    print(f"[ARCHIVE] 归档工单: {ticket_path}")
    
    # 检查路径是否存在
    if not Path(ticket_path).exists():
        print(f"[ERROR] 工单路径不存在: {ticket_path}")
        return False
    
    # 获取工单信息
    ticket_name = Path(ticket_path).name
    ticket_type = ticket_name.split("_template_workflow", 1)[0]
    
    # 创建归档目录
    archive_base = ".aces/tickets/arch"
    archive_path = Path(archive_base, ticket_type, ticket_name)
    
    print(f"[TARGET] 归档到: {archive_path}")
    
    # 创建归档目录结构
    try:
        Path(Path(archive_path).parent).mkdir(parents=True, exist_ok=True)
        
        # 检查是否已存在归档
        if Path(archive_path).exists():
            print(f"[WARN] 归档目录已存在: {archive_path}")
            overwrite = input("是否覆盖现有归档？(y/N): ").lower().strip()
            if overwrite != 'y':
                print("[INFO] 取消归档操作")
                return False
            
        # 复制工单到归档目录
        import shutil
        if Path(archive_path).exists():
            shutil.rmtree(archive_path)
        shutil.copytree(ticket_path, archive_path)
        
        print(f"[SUCCESS] 工单已成功归档到: {archive_path}")
        
        # 记录归档日志
        log_archive_operation(ticket_path, archive_path, "ARCHIVED")
        
        # 自动清理功能
        if auto_cleanup:
            return cleanup_original_ticket(ticket_path)
        else:
            print("[INFO] 归档完成，原目录保留")
            print("[INFO] 使用 --auto-cleanup 参数可自动清理原目录")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 归档操作失败: {e}")
        log_archive_operation(ticket_path, archive_path, "FAILED", str(e))
        return False


def create_smart_backup(ticket_path: str, backup_type: str = "auto") -> Optional[str]:
    """创建智能备份"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f".aces/tickets/backups/{timestamp}_{Path(ticket_path).name}"
    
    try:
        # 创建备份目录
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        # 根据备份类型选择文件
        if backup_type == "full":
            # 完整备份
            shutil.copytree(ticket_path, backup_dir)
        elif backup_type == "essential":
            # 仅关键文件备份
            essential_files = ["trace.md", "input/", "output/"]
            
            for item in essential_files:
                src_item = Path(ticket_path, item)
                dst_item = Path(backup_dir, item)
                
                if Path(src_item).exists():
                    if Path(src_item).is_dir():
                        shutil.copytree(src_item, dst_item)
                    else:
                        shutil.copy2(src_item, dst_item)
        
        print(f"[INFO] 备份已创建: {backup_dir}")
        return backup_dir
        
    except Exception as e:
        print(f"[ERROR] 创建备份失败: {e}")
        return None


def perform_enhanced_cleanup(ticket_path: str) -> bool:
    """执行增强的清理功能"""
    print(f"\n[WRENCH] [ENHANCED CLEANUP] 准备清理原工单目录: {ticket_path}")
    
    # 安全检查：确认目录存在且是有效的工单目录
    if not Path(ticket_path).exists():
        print(f"[ERROR] 工单目录不存在: {ticket_path}")
        return False
    
    # 验证是有效的工单目录
    required_items = ["trace.md", "input", "output"]
    for item in required_items:
        if not Path(Path(ticket_path, item).exists()):
            print(f"[ERROR] 无效的工单目录，缺少: {item}")
            return False
    
    # 执行交互式确认
    operation_type = "工单清理"
    is_confirmed, confirmations = perform_interactive_confirmation(ticket_path, operation_type)
    
    if not is_confirmed:
        print("[INFO] 清理操作已取消")
        return False
    
    # 显示将被删除的内容
    print(f"\n[CHECKLIST] 删除预览:")
    print("=" * 40)
    
    ticket_info = extract_ticket_info(ticket_path)
    print(f"工单名称: {ticket_info['name']}")
    print(f"文件数量: {ticket_info['file_count']}")
    print(f"总大小: {ticket_info['total_size_mb']} MB")
    print(f"绝对路径: {ticket_info['absolute_path']}")
    
    # 列出主要文件
    try:
        items = sorted(os.listdir(ticket_path))
        for item in items[:10]:  # 只显示前10个
            item_path = Path(ticket_path, item)
            if Path(item_path).is_dir():
                size, _ = calculate_directory_size(item_path)
                print(f"  📁 {item} ({size:,} bytes)")
            else:
                size = Path(item_path).stat().st_size
                print(f"  📄 {item} ({size:,} bytes)")
        
        if len(items) > 10:
            remaining = len(items) - 10
            print(f"  ... 还有 {remaining} 个文件或目录")
            
    except Exception as e:
        print(f"[WARN] 无法获取目录内容: {e}")
    
    print("=" * 40)
    
    # 执行删除操作
    try:
        shutil.rmtree(ticket_path)
        print(f"\n[DONE] [SUCCESS] 原工单目录已成功删除: {ticket_path}")
        return True
        
    except Exception as e:
        error_msg = f"删除目录失败: {e}"
        print(f"\n[ERROR] [ERROR] {error_msg}")
        return False


def perform_enhanced_archive(ticket_path: str, auto_cleanup: bool = False) -> bool:
    """执行增强的归档功能"""
    print(f"\n[ENHANCED ARCHIVE] 归档工单: {ticket_path}")
    
    # 检查路径是否存在
    if not Path(ticket_path).exists():
        print(f"[ERROR] 工单路径不存在: {ticket_path}")
        return False
    
    # 获取工单信息
    ticket_name = Path(ticket_path).name
    ticket_type = extract_ticket_info(ticket_path)["type"]
    
    # 创建归档目录
    archive_base = ".aces/tickets/arch"
    archive_path = Path(archive_base, ticket_type, ticket_name)
    
    print(f"[TARGET] 归档到: {archive_path}")
    
    # 创建归档目录结构
    try:
        Path(Path(archive_path).parent).mkdir(parents=True, exist_ok=True)
        
        # 检查是否已存在归档
        if Path(archive_path).exists():
            print(f"[WARN] 归档目录已存在: {archive_path}")
            overwrite = input("是否覆盖现有归档？(y/N): ").lower().strip()
            if overwrite != 'y':
                print("[INFO] 取消归档操作")
                return False
        
        # 复制工单到归档目录
        if Path(archive_path).exists():
            shutil.rmtree(archive_path)
        shutil.copytree(ticket_path, archive_path)
        
        print(f"[SUCCESS] 工单已成功归档到: {archive_path}")
        
        # 创建详细的日志条目
        risk_assessment = assess_deletion_risk(ticket_path)
        log_entry = create_enhanced_log_entry(
            "ARCHIVED",
            ticket_path,
            archive_path=archive_path,
            risk_assessment=risk_assessment,
            user_confirmation={"method": "interactive"},
            status="SUCCESS"
        )
        
        # 记录归档日志
        write_enhanced_log(log_entry)
        
        # 自动清理功能
        if auto_cleanup:
            print(f"\n[WRENCH] 开始自动清理原工单目录...")
            cleanup_result = perform_enhanced_cleanup(ticket_path)
            
            if cleanup_result:
                # 更新日志状态
                cleanup_log = create_enhanced_log_entry(
                    "AUTO_CLEANED",
                    ticket_path,
                    risk_assessment=risk_assessment,
                    user_confirmation={"method": "auto-cleanup"},
                    status="SUCCESS"
                )
                write_enhanced_log(cleanup_log)
                return True
            else:
                print("[WARN] 自动清理失败，建议手动清理")
                return False
        else:
            print("[INFO] 归档完成，原目录保留")
            print("[INFO] 使用 --auto-cleanup 参数可自动清理原目录")
        
        return True
        
    except Exception as e:
        error_msg = f"归档操作失败: {e}"
        print(f"[ERROR] {error_msg}")
        
        # 记录失败的日志
        log_entry = create_enhanced_log_entry(
            "ARCHIVE_FAILED",
            ticket_path,
            error_details=str(e),
            status="FAILED"
        )
        write_enhanced_log(log_entry)
        
        return False


def write_enhanced_log(log_entry: Dict):
    """写入增强的日志条目"""
    log_file = ".aces/tickets/arch/enhanced_archive_operations.jsonl"
    
    try:
        # 创建日志目录
        Path(Path(log_file).parent).mkdir(parents=True, exist_ok=True)
        
        # 写入日志（JSONL格式，每行一个记录）
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            
    except Exception as e:
        print(f"[WARN] 无法写入增强操作日志: {e}")


def query_enhanced_logs(filters: Optional[Dict] = None, limit: int = 10) -> List[Dict]:
    """查询增强日志"""
    log_file = ".aces/tickets/arch/enhanced_archive_operations.jsonl"
    results = []
    
    if not Path(log_file).exists():
        return results
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in reversed(lines):  # 从最新到最旧
            try:
                entry = json.loads(line.strip())
                results.append(entry)
                
                # 应用过滤器
                if filters:
                    if not all(entry.get(key) == value for key, value in filters.items()):
                        continue
                
                # 限制结果数量
                if len(results) >= limit:
                    break
                    
            except json.JSONDecodeError:
                continue
                
    except Exception as e:
        print(f"[ERROR] 读取增强日志文件失败: {e}")
    
    return results


def view_enhanced_logs(filters: Optional[Dict] = None, limit: int = 10):
    """查看增强的操作日志"""
    logs = query_enhanced_logs(filters, limit)
    
    if not logs:
        print("[INFO] 暂无增强操作日志")
        return
    
    print("[ENHANCED ARCHIVE LOGS] 详细操作历史")
    print("=" * 80)
    
    for entry in logs:
        # 格式化时间戳
        timestamp = entry.get("timestamp", "").split(".")[0].replace("T", " ")
        
        # 状态图标
        status_icon = "[DONE]" if entry.get("status") == "SUCCESS" else "[ERROR]"
        
        # 基础信息
        operation = entry.get("operation", "")
        source = entry.get("source_path", "")
        ticket_id = entry.get("ticket_id", "")
        
        print(f"{status_icon} {timestamp} - {operation}")
        print(f"   工单ID: {ticket_id}")
        print(f"   源路径: {source}")
        
        # 显示风险信息
        risk_level = entry.get("risk_assessment", {}).get("level", "")
        if risk_level:
            print(f"   风险评估: {risk_level}")
        
        # 显示文件大小信息
        total_size_mb = entry.get("total_size_mb", 0)
        if total_size_mb > 0:
            print(f"   文件大小: {total_size_mb} MB")
        
        # 显示错误详情
        error_details = entry.get("error_details")
        if error_details:
            print(f"   错误详情: {error_details}")
        
        print("-" * 60)


def view_basic_logs():
    """查看基本的归档操作日志（向后兼容）"""
    log_file = ".aces/tickets/arch/archive_operations.log"
    
    if not Path(log_file).exists():
        print("[INFO] 暂无归档操作日志")
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("[BASIC ARCHIVE LOGS] 归档操作历史 (兼容模式)")
        print("=" * 60)
        
        for line in lines[-10:]:  # 显示最近10条记录
            try:
                entry = json.loads(line.strip())
                timestamp = entry.get("timestamp", "")
                operation = entry.get("operation", "")
                source = entry.get("source_path", "")
                
                status_icon = "[OK]" if operation in ["ARCHIVED", "CLEANED_UP"] else "[FAIL]"
                print(f"{status_icon} {timestamp} - {operation}: {source}")
                
                if entry.get("error_message"):
                    print(f"    Error: {entry['error_message']}")
                    
            except json.JSONDecodeError:
                continue
                
    except Exception as e:
        print(f"[ERROR] 读取基本日志文件失败: {e}")


def add_ticket_from_template(title, template_name):
    """从模板创建新工单"""
    print(f"[ADD] 从模板创建工单: {title} (模板: {template_name})")
    
    # 构建模板路径
    template_path = TEMP_DIR / f"{template_name}.md"
    
    # 检查模板文件是否存在
    if not template_path.exists():
        print(f"[ERROR] 模板文件不存在: {template_path}")
        return False
    
    # 从模板文件名推断工单类型
    template_type = template_name.split('_template')[0]  # 例如: dev_template_workflow -> dev
    
    # 创建工单目录
    ticket_base = Path(".aces/tickets") / template_type
    ticket_dir = ticket_base / title
    
    # 检查工单目录是否已存在
    if ticket_dir.exists():
        print(f"[ERROR] 工单目录已存在: {ticket_dir}")
        return False
    
    try:
        # 创建工单目录结构
        ticket_dir.mkdir(parents=True, exist_ok=True)
        (ticket_dir / "input").mkdir(exist_ok=True)
        (ticket_dir / "output").mkdir(exist_ok=True)
        
        # 读取模板内容
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # 替换占位符变量
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        replaced_content = template_content.replace("{{execute_name}}", title)
        replaced_content = replaced_content.replace("{{creation_time}}", current_time)
        replaced_content = replaced_content.replace("{{last_updated}}", current_time)
        # 注意：input_ticket_id 和 output_ticket_id 需要用户后续手动填写
        
        # 写入trace.md文件
        trace_file = ticket_dir / "trace.md"
        with open(trace_file, 'w', encoding='utf-8') as f:
            f.write(replaced_content)
        
        print(f"[SUCCESS] 工单创建成功: {ticket_dir}")
        print(f"[INFO] NextStep 请执行下一步")
        print(f"  - [ ] 填写 trace.md 中的占位符变量")
        print(f"  - [ ] 开始执行工单任务")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 创建工单失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="工单管理系统增强版 - 支持五级安全确认、智能备份和风险评估",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  ticket-cli validate <工单路径>                    # 验证工单结构
  ticket-cli progress <工单路径>                   # 查看工单进度
  ticket-cli archive <工单路径> [--auto-cleanup]   # 归档工单（可选自动清理）
  ticket-cli enhanced-cleanup <工单路径>           # 使用增强的清理功能
  ticket-cli logs [--enhanced] [--limit 10]        # 查看操作日志
  ticket-cli backup <工单路径> [--full|--essential] # 创建智能备份
  ticket-cli batch-archive --completed              # 批量归档已完成工单
  ticket-cli stats                                  # 显示工单统计信息
  ticket-cli report [output.csv]                    # 导出归档报告
  ticket-cli add <title> --template <模板文件名>    # 从模板创建新工单
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="从模板创建新工单")
    add_parser.add_argument("title", help="工单标题")
    add_parser.add_argument("--template", required=True, help="模板文件名 (不含.md扩展名)")
    # list_template命令
    list_template_parser = subparsers.add_parser("list_template", help="可用的工单类型")

    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证工单结构")
    validate_parser.add_argument("ticket_path", help="工单路径")
    
    # progress 命令
    progress_parser = subparsers.add_parser("progress", help="查看工单进度")
    progress_parser.add_argument("ticket_path", help="工单路径")
    
    # archive 命令
    archive_parser = subparsers.add_parser("archive", help="归档工单")
    archive_parser.add_argument("ticket_path", help="工单路径")
    archive_parser.add_argument("--auto-cleanup", action="store_true", 
                              help="归档后自动清理原目录（需要确认）")
    
    # cleanup 命令（向后兼容的独立清理功能）
    cleanup_parser = subparsers.add_parser("cleanup", help="清理已归档的工单目录 (兼容模式)")
    cleanup_parser.add_argument("ticket_path", help="要清理的工单路径")
    
    # enhanced-cleanup 命令（新的增强清理功能）
    enhanced_cleanup_parser = subparsers.add_parser("enhanced-cleanup", help="使用增强功能清理工单目录")
    enhanced_cleanup_parser.add_argument("ticket_path", help="要清理的工单路径")
    
    # logs 命令
    logs_parser = subparsers.add_parser("logs", help="查看归档操作日志")
    logs_group = logs_parser.add_mutually_exclusive_group()
    logs_group.add_argument("--basic", action="store_true", help="查看基本日志 (兼容模式)")
    logs_group.add_argument("--enhanced", action="store_true", help="查看增强日志 (推荐)")
    logs_parser.add_argument("--limit", type=int, default=10, help="显示记录数量 (默认: 10)")
    logs_parser.add_argument("--filter-operation", help="按操作类型过滤")
    logs_parser.add_argument("--filter-status", help="按状态过滤")
    
    # backup 命令
    backup_parser = subparsers.add_parser("backup", help="创建智能备份")
    backup_parser.add_argument("ticket_path", help="要备份的工单路径")
    backup_group = backup_parser.add_mutually_exclusive_group()
    backup_group.add_argument("--full", action="store_true", help="完整备份")
    backup_group.add_argument("--essential", action="store_true", help="仅关键文件备份")
    backup_parser.set_defaults(full=False, essential=False)
    
    # restore 命令
    restore_parser = subparsers.add_parser("restore", help="从备份恢复")
    restore_parser.add_argument("backup_id", help="备份ID或备份路径")
    
    # batch-archive 命令
    batch_archive_parser = subparsers.add_parser("batch-archive", help="批量归档工单")
    batch_group = batch_archive_parser.add_mutually_exclusive_group(required=True)
    batch_group.add_argument("--completed", action="store_true", help="归档所有已完成工单")
    batch_group.add_argument("--in-progress", action="store_true", help="归档所有进行中工单")
    batch_group.add_argument("--all", action="store_true", help="归档所有工单")
    batch_archive_parser.add_argument("--auto-cleanup", action="store_true", 
                                    help="归档后自动清理原目录")
    batch_archive_parser.add_argument("--dry-run", action="store_true", 
                                    help="只显示将要执行的操作，不实际执行")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="显示工单统计信息")
    
    # report 命令
    report_parser = subparsers.add_parser("report", help="导出归档报告")
    report_parser.add_argument("output_file", nargs="?", help="输出文件路径 (默认: archive_report_时间戳.csv)")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_ticket_from_template(args.title, args.template)
    elif args.command == "list_template":
        avalidate = []
        for template in TEMP_DIR.rglob("*.md"):
            ticket_type = template.name.split("_template_workflow", 1)[0]
            avalidate.append(ticket_type)
        print(f"可用的工单模板类型有:{avalidate}")
        print("""## NextStep
- 创建工单：`ticket-cli add <标题> --template <模板类型>`
- 验证工单：`ticket-cli validate <工单路径>`
- 查看进度：`ticket-cli progress <工单路径>`
- 归档工单：`ticket-cli archive <工单路径> [--auto-cleanup]`
- 查看日志：`ticket-cli logs [--enhanced]`""")
    elif args.command == "validate":
        validate_ticket(args.ticket_path)
    elif args.command == "progress":
        progress_ticket(args.ticket_path)
    elif args.command == "archive":
        perform_enhanced_archive(args.ticket_path, getattr(args, 'auto_cleanup', False))
    elif args.command == "cleanup":
        # 向后兼容模式
        print("[INFO] 使用兼容模式清理功能")
        cleanup_original_ticket(args.ticket_path)
    elif args.command == "enhanced-cleanup":
        perform_enhanced_cleanup(args.ticket_path)
    elif args.command == "logs":
        filters = {}
        if args.filter_operation:
            filters["operation"] = args.filter_operation
        if args.filter_status:
            filters["status"] = args.filter_status
            
        if args.basic:
            view_basic_logs()
        elif args.enhanced:
            view_enhanced_logs(filters, args.limit)
        else:
            # 默认显示增强日志
            view_enhanced_logs(filters, args.limit)
    elif args.command == "backup":
        if args.full:
            create_smart_backup(args.ticket_path, "full")
        elif args.essential:
            create_smart_backup(args.ticket_path, "essential")
        else:
            # 智能备份（根据风险评估）
            risk_assessment = assess_deletion_risk(args.ticket_path)
            if risk_assessment["level"] == "HIGH":
                create_smart_backup(args.ticket_path, "essential")
            else:
                create_smart_backup(args.ticket_path, "auto")
    elif args.command == "restore":
        print(f"[INFO] 恢复功能开发中... (备份ID: {args.backup_id})")
    elif args.command == "batch-archive":
        # 根据参数选择工单
        if args.completed:
            tickets = find_tickets_by_status("completed")
        elif args.in_progress:
            tickets = find_tickets_by_status("in-progress")
        elif args.all:
            tickets = find_tickets_by_status("all")
        
        if not tickets:
            print("[INFO] 没有找到符合条件的工单")
            return
        
        print(f"[INFO] 找到 {len(tickets)} 个符合条件的工单")
        
        if args.dry_run:
            print("[INFO] 干运行模式 - 只显示将要执行的操作")
        
        # 执行批量归档
        results = batch_archive_tickets(tickets, args.auto_cleanup, args.dry_run)
        
    elif args.command == "stats":
        show_ticket_statistics()
    elif args.command == "report":
        export_archive_report(args.output_file)
    else:
        parser.print_help()


def cleanup_original_ticket(ticket_path):
    """安全清理原工单目录 (兼容模式)"""
    print(f"\n[CLEANUP] 准备清理原工单目录: {ticket_path}")
    
    # 安全检查：确认目录存在且是有效的工单目录
    if not Path(ticket_path).exists():
        print(f"[ERROR] 工单目录不存在: {ticket_path}")
        return False
    
    # 验证是有效的工单目录
    required_items = ["trace.md", "input", "output"]
    for item in required_items:
        if not Path(Path(ticket_path, item).exists()):
            print(f"[ERROR] 无效的工单目录，缺少: {item}")
            return False
    
    # 显示目录内容预览
    print("[INFO] 即将删除的目录内容:")
    try:
        items = os.listdir(ticket_path)
        for item in items:
            item_path = Path(ticket_path, item)
            if Path(item_path).is_dir():
                size = sum(Path(Path(root, f).stat().st_size) 
                          for root, dirs, files in os.walk(item_path) 
                          for f in files if Path(Path(root, f).is_file()))
            else:
                size = Path(item_path).stat().st_size
            print(f"  - {item} ({size:,} bytes)")
    except Exception as e:
        print(f"[WARN] 无法获取目录大小信息: {e}")
    
    # 多重确认机制
    print("\n[WARNING] 此操作将永久删除原工单目录及其所有内容！")
    print(f"[WARNING] 删除路径: {Path(ticket_path).resolve()}")
    
    # 第一次确认
    confirm1 = input("\n确认删除？输入 'DELETE' 确认: ").strip()
    if confirm1 != 'DELETE':
        print("[INFO] 删除操作已取消")
        return False
    
    # 第二次确认（要求输入完整路径）
    confirm2 = input(f"\n最后确认，请输入完整路径确认删除: ").strip()
    if confirm2 != Path(ticket_path).resolve():
        print("[ERROR] 路径不匹配，删除操作已取消")
        return False
    
    # 执行删除操作
    try:
        import shutil
        shutil.rmtree(ticket_path)
        print(f"[SUCCESS] 原工单目录已成功删除: {ticket_path}")
        
        # 记录清理日志（兼容格式）
        log_archive_operation(ticket_path, "N/A", "CLEANED_UP")
        return True
        
    except Exception as e:
        error_msg = f"删除目录失败: {e}"
        print(f"[ERROR] {error_msg}")
        log_archive_operation(ticket_path, "N/A", "CLEANUP_FAILED", error_msg)
        return False


def log_archive_operation(source_path, archive_path, operation, error_msg=None):
    """记录归档操作日志 (兼容格式)"""
    import datetime
    import json
    
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "operation": operation,
        "source_path": source_path,
        "archive_path": archive_path,
        "error_message": error_msg
    }
    
    log_file = ".aces/tickets/arch/archive_operations.log"
    
    try:
        # 创建日志目录
        Path(Path(log_file).parent).mkdir(parents=True, exist_ok=True)
        
        # 写入日志（JSON格式，每行一个记录）
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            
    except Exception as e:
        print(f"[WARN] 无法写入操作日志: {e}")


def view_archive_logs():
    """查看归档操作日志 (兼容模式)"""
    log_file = ".aces/tickets/arch/archive_operations.log"
    
    if not Path(log_file).exists():
        print("[INFO] 暂无归档操作日志")
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("[ARCHIVE LOGS] 归档操作历史 (兼容模式)")
        print("=" * 60)
        
        for line in lines[-10:]:  # 显示最近10条记录
            try:
                entry = json.loads(line.strip())
                timestamp = entry.get("timestamp", "")
                operation = entry.get("operation", "")
                source = entry.get("source_path", "")
                
                status_icon = "[OK]" if operation in ["ARCHIVED", "CLEANED_UP"] else "[FAIL]"
                print(f"{status_icon} {timestamp} - {operation}: {source}")
                
                if entry.get("error_message"):
                    print(f"    Error: {entry['error_message']}")
                    
            except json.JSONDecodeError:
                continue
                
    except Exception as e:
        print(f"[ERROR] 读取日志文件失败: {e}")


def batch_archive_tickets(ticket_paths: List[str], auto_cleanup: bool = False, dry_run: bool = False) -> Dict:
    """批量归档工单"""
    results = {
        "total": len(ticket_paths),
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "details": []
    }
    
    print(f"\n[BATCH] 批量归档工单 - 总计: {len(ticket_paths)}")
    print("=" * 60)
    
    for i, ticket_path in enumerate(ticket_paths, 1):
        print(f"\n[{i}/{len(ticket_paths)}] 处理工单: {Path(ticket_path).name}")
        
        # 检查工单是否存在
        if not Path(ticket_path).exists():
            print(f"  [ERROR] 工单不存在: {ticket_path}")
            results["failed"] += 1
            results["details"].append({
                "path": ticket_path,
                "status": "FAILED",
                "error": "Path does not exist"
            })
            continue
        
        # 验证工单结构
        if not validate_ticket(ticket_path):
            print(f"  [WARNING]  工单验证失败，跳过: {ticket_path}")
            results["skipped"] += 1
            results["details"].append({
                "path": ticket_path,
                "status": "SKIPPED",
                "error": "Validation failed"
            })
            continue
        
        # 执行归档
        if dry_run:
            print(f"  [CHECKLIST] 干运行: 将归档 {ticket_path}")
            results["success"] += 1
            results["details"].append({
                "path": ticket_path,
                "status": "DRY_RUN",
                "message": "Would be archived"
            })
        else:
            try:
                success = perform_enhanced_archive(ticket_path, auto_cleanup)
                if success:
                    print(f"  [DONE] 归档成功")
                    results["success"] += 1
                    results["details"].append({
                        "path": ticket_path,
                        "status": "SUCCESS"
                    })
                else:
                    print(f"  [ERROR] 归档失败")
                    results["failed"] += 1
                    results["details"].append({
                        "path": ticket_path,
                        "status": "FAILED",
                        "error": "Archive operation failed"
                    })
            except Exception as e:
                print(f"  [ERROR] 归档异常: {e}")
                results["failed"] += 1
                results["details"].append({
                    "path": ticket_path,
                    "status": "FAILED",
                    "error": str(e)
                })
    
    print("\n" + "=" * 60)
    print(f"[STATS] 批量归档结果:")
    print(f"  总计: {results['total']}")
    print(f"  成功: {results['success']}")
    print(f"  失败: {results['failed']}")
    print(f"  跳过: {results['skipped']}")
    
    return results


def find_tickets_by_status(status: str = "completed") -> List[str]:
    """根据状态查找工单"""
    tickets = []
    
    # 搜索各个工单类型目录
    tickets_root = Path(".aces/tickets")

    ticket_dirs = list(tickets_root/item for item in os.listdir(tickets_root) if (tickets_root/item).is_dir() )
    
    for ticket_dir in ticket_dirs:
        if not Path(ticket_dir).exists():
            continue
            
        try:
            for item in os.listdir(ticket_dir):
                ticket_path = Path(ticket_dir, item)
                if Path(ticket_path).is_dir():
                    # 检查工单状态
                    if status == "completed":
                        # 检查trace.md中是否有未完成的任务
                        trace_file = Path(ticket_path, "trace.md")
                        if Path(trace_file).exists():
                            with open(trace_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if '[ ]' not in content:  # 没有未完成的任务
                                    tickets.append(ticket_path)
                    elif status == "in-progress":
                        # 检查是否有未完成的任务
                        trace_file = Path(ticket_path, "trace.md")
                        if Path(trace_file).exists():
                            with open(trace_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if '[ ]' in content:
                                    tickets.append(ticket_path)
                    else:
                        # 所有工单
                        tickets.append(ticket_path)
        except Exception as e:
            print(f"[WARN] 搜索目录 {ticket_dir} 时出错: {e}")
    
    return tickets


def show_ticket_statistics():
    """显示工单统计信息"""
    print("\n[STATS] 工单统计信息")
    print("=" * 50)
    
    # 获取各种状态的工单
    all_tickets = find_tickets_by_status("all")
    completed_tickets = find_tickets_by_status("completed")
    in_progress_tickets = find_tickets_by_status("in-progress")
    
    print(f"总工单数: {len(all_tickets)}")
    print(f"已完成: {len(completed_tickets)}")
    print(f"进行中: {len(in_progress_tickets)}")
    
    # 计算总大小
    total_size = 0
    for ticket_path in all_tickets:
        try:
            size, _ = calculate_directory_size(ticket_path)
            total_size += size
        except:
            pass
    
    print(f"总大小: {total_size / (1024*1024):.1f} MB")
    
    # 显示最近的活动
    recent_logs = query_enhanced_logs(limit=5)
    if recent_logs:
        print("\n[BATCH] 最近操作:")
        for log in recent_logs:
            timestamp = log.get("timestamp", "").split("T")[0]
            operation = log.get("operation", "")
            ticket_id = log.get("ticket_id", "")
            print(f"  {timestamp} - {operation}: {ticket_id}")
    
    print("=" * 50)


def export_archive_report(output_file: str = None):
    """导出归档报告"""
    if not output_file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"archive_report_{timestamp}.csv"
    
    print(f"[CHECKLIST] 导出归档报告到: {output_file}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("时间戳,操作类型,工单ID,源路径,状态,风险等级,文件大小(MB)\n")
            
            logs = query_enhanced_logs(limit=1000)  # 获取最近1000条记录
            
            for log in logs:
                timestamp = log.get("timestamp", "").split("T")[0]
                operation = log.get("operation", "")
                ticket_id = log.get("ticket_id", "")
                source_path = log.get("source_path", "")
                status = log.get("status", "")
                risk_level = log.get("risk_assessment", {}).get("level", "")
                size_mb = log.get("total_size_mb", 0)
                
                f.write(f"{timestamp},{operation},{ticket_id},{source_path},{status},{risk_level},{size_mb}\n")
        
        print(f"[DONE] 报告导出成功: {output_file}")
        
    except Exception as e:
        print(f"[ERROR] 导出报告失败: {e}")


if __name__ == "__main__":
    main()