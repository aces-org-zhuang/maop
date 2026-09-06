#!/usr/bin/env python3
"""Disk Space Scanner"""

import os
import click


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """CLI"""
    pass


@cli.command()
@click.option('--scan-path', '-p', default='.', help='Path to scan')
@click.option('--size-threshold', '-s', default=1.0, type=float, help='Size threshold in GB')
@click.option('--max-depth', '-d', default=3, type=int, help='Maximum depth to scan')
@click.option('--output', '-o', default='scan-results.json', help='Output JSON file')
def scan(scan_path, size_threshold, max_depth, output):
    from scan_diskspace import scan_diskspace
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return scan_diskspace.main(['--scan-path', scan_path, '--size-threshold', str(size_threshold), '--max-depth', str(max_depth), '--output', output])


@cli.command()
@click.option('--input', '-i', default='scan-results.json', help='Input JSON scan results')
@click.option('--output', '-o', default='disk-report.md', help='Output markdown report file')
@click.option('--format', '-f', type=click.Choice(['markdown', 'json']), default='markdown', help='Output format')
def report(input, output, format):
    from generate_report import generate_report
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return generate_report.main(['--input', input, '--output', output, '--format', format])


@cli.command()
@click.option('--input', '-i', default='scan-results.json', help='Input JSON scan results')
@click.option('--output', '-o', default='analysis-results.json', help='Output analysis results')
@click.option('--min-size', '-s', default=100, type=int, help='Minimum size threshold in MB')
@click.option('--top-n', '-n', default=10, type=int, help='Show top N largest directories')
def analyze(input, output, min_size, top_n):
    from aggregate_results import aggregate_results
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return aggregate_results.main(['--input', input, '--output', output, '--min-size', str(min_size), '--top-n', str(top_n)])


@cli.command()
@click.option('--scan-path', '-p', default='.', help='Path to scan')
@click.option('--size-threshold', '-s', default=1.0, type=float, help='Size threshold in GB')
@click.option('--max-depth', '-d', default=3, type=int, help='Maximum depth to scan')
@click.option('--min-size', '-m', default=100, type=int, help='Minimum size for analysis in MB')
def all_in_one(scan_path, size_threshold, max_depth, min_size):
    from scan_diskspace import scan_diskspace
    from generate_report import generate_report
    from aggregate_results import aggregate_results
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    scan_result = scan_diskspace.main(['--scan-path', scan_path, '--size-threshold', str(size_threshold), '--max-depth', str(max_depth), '--output', 'scan-results.json'])
    if scan_result != 0:
        return scan_result
    
    report_result = generate_report.main(['--input', 'scan-results.json', '--output', 'disk-report.md', '--format', 'markdown'])
    if report_result != 0:
        return report_result
    
    analyze_result = aggregate_results.main(['--input', 'scan-results.json', '--output', 'analysis-results.json', '--min-size', str(min_size), '--top-n', '10'])
    return analyze_result


if __name__ == '__main__':
    cli()