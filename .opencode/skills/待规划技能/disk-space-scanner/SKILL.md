---
name: disk-space-scanner
description: Comprehensive disk space analysis tool for Windows disk management. Use when Codex needs to:1- Analyze disk usage patterns across directories, 2- Identify large directories and files exceeding size thresholds, 3- Generate detailed storage reports with recommendations, 4- Find cleanup candidates for optimization, 5- Monitor disk space trends and set up alerts, or perform any disk space analysis task
---

# Disk Space Scanner

A comprehensive disk space analysis tool that scans directories, identifies large storage consumers, and generates actionable reports for storage optimization.

## Quick Start

### Python Click (Recommended)
```bash
# Install the tool
cd scripts && pip install -e .

# Basic scan
disk-space-scanner scan --scan-path "." --size-threshold 1

# Complete workflow
disk-space-scanner all-in-one --scan-path "D:\" --size-threshold 10

# Generate reports
disk-space-scanner report --input scan-results.json --output report.md
```

## Scripts

- [disk_space_scanner.py](scripts/disk_space_scanner.py) - Main CLI entry point
- [scan_diskspace.py](scripts/scan_diskspace.py) - Scanning functionality
- [generate_report.py](scripts/generate_report.py) - Report generation
- [aggregate_results.py](scripts/aggregate_results.py) - Data analysis
- [setup.py](scripts/setup.py) - Installation script

## Parameters

### Scan Command
- `--scan-path` / `-p`: Starting directory (default: current directory)
- `--size-threshold` / `-s`: Minimum size in GB for reporting (default: 1)
- `--max-depth` / `-d`: Maximum directory depth (default: 3)
- `--output` / `-o`: Output JSON file (default: scan-results.json)

### Report Command
- `--input` / `-i`: Input JSON scan results (default: scan-results.json)
- `--output` / `-o`: Output report file (default: disk-report.md)
- `--format` / `-f`: Output format (markdown|json, default: markdown)

### Analyze Command
- `--input` / `-i`: Input JSON scan results (default: scan-results.json)
- `--output` / `-o`: Output analysis file (default: analysis-results.json)
- `--min-size` / `-s`: Minimum size threshold in MB (default: 100)
- `--top-n` / `-n`: Show top N largest directories (default: 10)

## Workflow

1. **Scan**: Execute directory scanning with recursive traversal
2. **Report**: Generate markdown/JSON reports with recommendations
3. **Analyze**: Aggregate results and identify patterns

## Usage Examples

### Complete Analysis
```bash
# Run complete workflow
disk-space-scanner all-in-one --scan-path "E:\" --size-threshold 5
```

### Individual Commands
```bash
# Scan disk space
disk-space-scanner scan --scan-path "D:\Projects" --size-threshold 2

# Generate report
disk-space-scanner report --format markdown --output my-report.md

# Analyze results
disk-space-scanner analyze --min-size 50 --top-n 20
```

## Best Practices

- Test with small thresholds first
- Review recommendations before cleanup
- Use read-only mode for initial analysis
- Schedule scans during off-peak hours

## Installation

1. Navigate to scripts directory: `cd scripts`
2. Install with pip: `pip install -e .`
3. Verify installation: `disk-space-scanner --help`

## Troubleshooting

### Python Version
Check installation: `disk-space-scanner --version`
Debug mode: Add `--help` to any command for detailed options