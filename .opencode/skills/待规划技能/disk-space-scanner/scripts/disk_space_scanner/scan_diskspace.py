#!/usr/bin/env python3
"""Scan Diskspace"""

import os
import json
import click
from datetime import datetime


def format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_directory_size(path):
    total_size = 0
    file_count = 0
    
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                    file_count += 1
                except (OSError, FileNotFoundError):
                    continue
    except (OSError, PermissionError):
        pass
    
    return total_size, file_count


@click.command()
@click.option('--scan-path', '-p', default='.', help='Path to scan')
@click.option('--size-threshold', '-s', default=1.0, type=float, help='Size threshold in GB')
@click.option('--max-depth', '-d', default=3, type=int, help='Maximum depth to scan')
@click.option('--output', '-o', default='scan-results.json', help='Output JSON file')
def scan_diskspace(scan_path, size_threshold, max_depth, output):
    click.echo(f"Starting disk space scan for: {scan_path}")
    
    threshold_bytes = size_threshold * 1024 * 1024 * 1024
    scan_path = os.path.abspath(scan_path)
    
    if not os.path.exists(scan_path):
        click.echo(f"Error: Path {scan_path} does not exist", err=True)
        return 1
    
    results = {
        'scan_info': {
            'scan_path': scan_path,
            'scan_time': datetime.now().isoformat(),
            'size_threshold_gb': size_threshold,
            'max_depth': max_depth
        },
        'directories': [],
        'summary': {
            'total_size': 0,
            'total_files': 0,
            'directories_over_threshold': 0
        }
    }
    
    def scan_directory(current_path, current_depth=0):
        if current_depth > max_depth:
            return
        
        try:
            dir_size, file_count = get_directory_size(current_path)
            
            if dir_size >= threshold_bytes or current_depth == 0:
                dir_info = {
                    'path': current_path,
                    'size_bytes': dir_size,
                    'size_formatted': format_size(dir_size),
                    'file_count': file_count,
                    'depth': current_depth
                }
                
                results['directories'].append(dir_info)
                results['summary']['total_size'] += dir_size
                results['summary']['total_files'] += file_count
                
                if dir_size >= threshold_bytes:
                    results['summary']['directories_over_threshold'] += 1
            
            if current_depth < max_depth:
                try:
                    for item in os.listdir(current_path):
                        item_path = os.path.join(current_path, item)
                        if os.path.isdir(item_path):
                            scan_directory(item_path, current_depth + 1)
                except (OSError, PermissionError):
                    pass
                    
        except (OSError, PermissionError):
            pass
    
    scan_directory(scan_path)
    
    output_path = os.path.join(os.getcwd(), output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    click.echo(f"Scan completed. Results saved to: {output_path}")
    click.echo(f"Total size: {format_size(results['summary']['total_size'])}")
    click.echo(f"Total files: {results['summary']['total_files']}")
    click.echo(f"Directories over threshold: {results['summary']['directories_over_threshold']}")
    
    return 0


if __name__ == '__main__':
    scan_diskspace()