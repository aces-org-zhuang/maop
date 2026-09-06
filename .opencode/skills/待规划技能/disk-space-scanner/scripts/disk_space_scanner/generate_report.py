#!/usr/bin/env python3
"""Generate Report"""

import os
import json
import click
from datetime import datetime


def format_size(size_bytes):
    """Format bytes"""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def generate_recommendations(scan_data):
    """Generate recommendations"""
    recommendations = []
    
    if scan_data['summary']['directories_over_threshold'] > 0:
        recommendations.append("Check directories over threshold for cleanup opportunities")
    
    cache_dirs = [d for d in scan_data['directories'] if 'cache' in d['path'].lower() or '.cache' in d['path']]
    if cache_dirs:
        recommendations.append("Consider cleaning cache directories")
    
    temp_dirs = [d for d in scan_data['directories'] if 'temp' in d['path'].lower() or 'tmp' in d['path'].lower()]
    if temp_dirs:
        recommendations.append("Clean temporary file directories")
    
    if not recommendations:
        recommendations.append("Disk usage is normal, no cleanup needed")
    
    return recommendations


@click.command()
@click.option('--input', '-i', default='scan-results.json', help='Input JSON scan results')
@click.option('--output', '-o', default='disk-report.md', help='Output markdown report file')
@click.option('--format', '-f', type=click.Choice(['markdown', 'json']), default='markdown', help='Output format')
def generate_report(input, output, format):
    """Generate disk space report"""
    if not os.path.exists(input):
        click.echo(f"Error: Input file {input} does not exist", err=True)
        return 1
    
    try:
        with open(input, 'r', encoding='utf-8') as f:
            scan_data = json.load(f)
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON file {input}: {e}", err=True)
        return 1
    
    if format == 'json':
        output_path = os.path.join(os.getcwd(), output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scan_data, f, indent=2, ensure_ascii=False)
        click.echo(f"JSON report saved to: {output_path}")
        return 0
    
    scan_info = scan_data['scan_info']
    summary = scan_data['summary']
    directories = scan_data['directories']
    
    report_lines = [
        f"# Disk Space Usage Report\n",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"**Scan Path**: `{scan_info['scan_path']}`\n",
        f"**Scan Time**: {scan_info['scan_time']}\n",
        f"**Size Threshold**: {scan_info['size_threshold_gb']} GB\n",
        f"**Max Depth**: {scan_info['max_depth']}\n",
        "\n## Summary\n",
        f"- **Total Size**: {format_size(summary['total_size'])}\n",
        f"- **Total Files**: {summary['total_files']}\n",
        f"- **Directories Over Threshold**: {summary['directories_over_threshold']}\n",
        "\n## Top Largest Directories\n"
    ]
    
    sorted_dirs = sorted(directories, key=lambda x: x['size_bytes'], reverse=True)
    for i, dir_info in enumerate(sorted_dirs[:10], 1):
        report_lines.append(f"{i}. **{dir_info['path']}** - {dir_info['size_formatted']} ({dir_info['file_count']} files)\n")
    
    recommendations = generate_recommendations(scan_data)
    report_lines.extend(["\n## Recommendations\n"])
    
    for i, rec in enumerate(recommendations, 1):
        report_lines.append(f"{i}. {rec}\n")
    
    output_path = os.path.join(os.getcwd(), output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(report_lines)
    
    click.echo(f"Report generated successfully: {output_path}")
    return 0


if __name__ == '__main__':
    generate_report()