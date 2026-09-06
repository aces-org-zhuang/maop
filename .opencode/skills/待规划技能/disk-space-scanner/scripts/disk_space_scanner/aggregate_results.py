#!/usr/bin/env python3
"""Aggregate Results"""

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


def analyze_directory_patterns(directories):
    """Analyze patterns"""
    patterns = {'media': [], 'code': [], 'other': []}
    
    for dir_info in directories:
        path_lower = dir_info['path'].lower()
        
        if any(keyword in path_lower for keyword in ['media', 'video', 'audio', 'music', 'picture', 'image']):
            patterns['media'].append(dir_info)
        elif any(keyword in path_lower for keyword in ['.git', 'src', 'code', 'project']):
            patterns['code'].append(dir_info)
        else:
            patterns['other'].append(dir_info)
    
    return patterns


@click.command()
@click.option('--input', '-i', default='scan-results.json', help='Input JSON scan results')
@click.option('--output', '-o', default='analysis-results.json', help='Output analysis results')
@click.option('--min-size', '-s', default=100, type=int, help='Minimum size threshold in MB')
@click.option('--top-n', '-n', default=10, type=int, help='Show top N largest directories')
def aggregate_results(input, output, min_size, top_n):
    """Aggregate and analyze"""
    if not os.path.exists(input):
        click.echo(f"Error: Input file {input} does not exist", err=True)
        return 1
    
    try:
        with open(input, 'r', encoding='utf-8') as f:
            scan_data = json.load(f)
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON file {input}: {e}", err=True)
        return 1
    
    min_size_bytes = min_size * 1024 * 1024
    
    filtered_dirs = [d for d in scan_data['directories'] if d['size_bytes'] >= min_size_bytes]
    filtered_dirs.sort(key=lambda x: x['size_bytes'], reverse=True)
    
    patterns = analyze_directory_patterns(filtered_dirs)
    total_filtered_size = sum(d['size_bytes'] for d in filtered_dirs)
    total_filtered_files = sum(d['file_count'] for d in filtered_dirs)
    
    recommendations = []
    large_dirs = [d for d in filtered_dirs if d['size_bytes'] > 1024**3]
    if large_dirs:
        recommendations.append({
            'type': 'large_directories',
            'priority': 'low',
            'description': f"Found {len(large_dirs)} directories larger than 1GB",
            'action': 'Review large directories for potential cleanup or archiving'
        })
    
    analysis = {
        'analysis_info': {
            'analysis_time': datetime.now().isoformat(),
            'input_file': input,
            'min_size_mb': min_size,
            'total_directories_analyzed': len(filtered_dirs)
        },
        'summary': {
            'total_directories': len(filtered_dirs),
            'total_size_bytes': total_filtered_size,
            'total_size_formatted': format_size(total_filtered_size),
            'total_files': total_filtered_files
        },
        'patterns': {
            category: {
                'count': len(data),
                'total_size': sum(d['size_bytes'] for d in data),
                'total_size_formatted': format_size(sum(d['size_bytes'] for d in data))
            } for category, data in patterns.items()
        },
        'top_directories': filtered_dirs[:top_n],
        'recommendations': recommendations
    }
    
    output_path = os.path.join(os.getcwd(), output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    click.echo("Analysis completed successfully!")
    click.echo(f"Results saved to: {output_path}")
    click.echo("")
    click.echo("=== Analysis Summary ===")
    click.echo(f"Directories analyzed: {len(filtered_dirs)}")
    click.echo(f"Total size: {format_size(total_filtered_size)}")
    click.echo(f"Total files: {total_filtered_files}")
    click.echo("")
    
    click.echo("=== Category Analysis ===")
    for category, data in analysis['patterns'].items():
        click.echo(f"{category.upper()}: {data['count']} directories, {data['total_size_formatted']}")
    
    click.echo("")
    click.echo("=== Recommended Actions ===")
    for i, rec in enumerate(recommendations, 1):
        click.echo(f"{i}. [{rec['priority'].upper()}] {rec['description']}")
        click.echo(f"   Action: {rec['action']}")
    
    return 0


if __name__ == '__main__':
    aggregate_results()