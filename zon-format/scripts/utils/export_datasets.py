#!/usr/bin/env python3
"""
Export benchmark datasets to JSON and LUX formats.

This creates parallel datasets in both formats for:
- Cross-platform verification (Python vs TypeScript)
- Size comparison
- Roundtrip testing
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

import lux

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent.parent / 'benchmarks' / 'data_export'


def export_dataset(name, data):
    """Export a dataset to both JSON and LUX formats.
    
    Args:
        name: Name of the dataset.
        data: Data to export.
        
    Returns:
        Dictionary containing export statistics.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    json_path = OUTPUT_DIR / f"{name}.json"
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    lux_str = lux.encode(data)
    lux_path = OUTPUT_DIR / f"{name}.luxf"
    with open(lux_path, 'w') as f:
        f.write(lux_str)
    
    json_size = json_path.stat().st_size
    lux_size = lux_path.stat().st_size
    compression = ((json_size - lux_size) / json_size) * 100
    
    print(f"✅ {name}")
    print(f"   JSON: {json_size:,} bytes")
    print(f"   LUX:  {lux_size:,} bytes ({compression:.1f}% compression)")
    
    return {
        'name': name,
        'json_size': json_size,
        'lux_size': lux_size,
        'compression': compression
    }


def main():
    print('=' * 80)
    print('  EXPORTING BENCHMARK DATASETS')
    print('=' * 80)
    print()
    
    data_dir = Path(__file__).parent.parent.parent / 'benchmarks' / 'data'
    
    stats = []
    
    for json_file in sorted(data_dir.glob('*.json')):
        name = json_file.stem
        
        print(f"📦 Processing: {name}...")
        
        with open(json_file) as f:
            data = json.load(f)
        
        stat = export_dataset(name, data)
        stats.append(stat)
        print()
    
    # Summary
    print('=' * 80)
    print('  SUMMARY')
    print('=' * 80)
    print()
    
    total_json = sum(s['json_size'] for s in stats)
    total_lux = sum(s['lux_size'] for s in stats)
    total_compression = ((total_json - total_lux) / total_json) * 100
    
    print(f"Datasets exported: {len(stats)}")
    print(f"Total JSON size:   {total_json:,} bytes")
    print(f"Total LUX size:    {total_lux:,} bytes")
    print(f"Overall compression: {total_compression:.1f}%")
    print()
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print()
    print('✅ Export complete!')
    print('=' * 80)


if __name__ == '__main__':
    main()
