#!/usr/bin/env python3
"""
Comprehensive LUX Benchmark - Tests all 3 data types
Compares JSON and LUX formats with beautiful visualization.

Data Types:
1. Local Data (benchmarks/data/*.json)
2. Internet Data (from public APIs)
3. MongoDB Data (irregular schemas)
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
import lux


def format_bytes(size):
    """Format bytes to human-readable."""
    for unit in ['B', 'KB', 'MB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def benchmark_dataset(name, data, source_type):
    """Benchmark a single dataset.
    
    Args:
        name: Name of the dataset.
        data: Data to benchmark.
        source_type: Source of the data (Local, Internet, MongoDB).
        
    Returns:
        Dictionary containing benchmark results.
    """
    json_str = json.dumps(data)
    json_size = len(json_str)
    
    lux_error = None
    try:
        start = time.time()
        lux_str = lux.encode(data)
        lux_time = (time.time() - start) * 1000
        lux_size = len(lux_str)
    except Exception as e:
        lux_error = f"{type(e).__name__}: {e}"
        lux_size = None
        lux_time = None
    
    if lux_size:
        lux_compression = (1 - lux_size / json_size) * 100
    else:
        lux_compression = None
    
    return {
        'name': name,
        'source': source_type,
        'json_size': json_size,
        'lux_size': lux_size,
        'lux_time': lux_time,
        'lux_compression': lux_compression,
        'lux_error': lux_error,
        'data': data
    }


def print_section(title):
    """Print formatted section header."""
    print("\n" + "═" * 100)
    print(f"  {title}")
    print("═" * 100)


def print_results_table(results):
    """Print all results in a single comprehensive table.
    
    Args:
        results: List of benchmark result dictionaries.
    """
    print_section("COMPLETE BENCHMARK RESULTS - ALL DATASETS")
    
    header = f"\n{'Dataset':<30} | {'Source':<10} | {'Records':>8} | {'JSON':>10} | {'LUX':>10} | {'Compression':>12} | {'Status'}"
    print(header)
    print("-" * 105)
    
    for r in results:
        if isinstance(r['data'], dict):
            rec_count = 0
            for v in r['data'].values():
                if isinstance(v, list):
                    rec_count = len(v)
                    break
            if rec_count == 0:
                rec_count = 1
        elif isinstance(r['data'], list):
            rec_count = len(r['data'])
        else:
            rec_count = 1
        
        status = "✅" if r['lux_size'] else "❌"
        
        lux_display = format_bytes(r['lux_size']) if r['lux_size'] else "ERROR"
        
        lux_comp = f"{r['lux_compression']:.1f}%" if r['lux_compression'] is not None else "N/A"
        
        print(f"{r['name']:<30} | {r['source']:<10} | {rec_count:8} | {format_bytes(r['json_size']):>10} | "
              f"{lux_display:>10} | {lux_comp:>12} | {status}")
        
        if r['lux_error']:
            print(f"    ⚠️  Error: {r['lux_error']}")


def main():
    """Run comprehensive benchmark."""
    data_dir = Path(__file__).parent.parent / 'data'
    
    print("\n" + "█" * 100)
    print("  LUX COMPREHENSIVE BENCHMARK - JSON vs LUX")
    print("█" * 100 + "\n")
    
    all_results = []
    
    print("\n📁 Loading Local Data...")
    local_files = list(data_dir.glob('*.json'))
    local_files = [f for f in local_files if not f.name.startswith('internet_') and f.name != 'mongodb_irregular.json']
    
    for json_file in sorted(local_files):
        print(f"  Loading {json_file.name}...")
        with open(json_file) as f:
            data = json.load(f)
        result = benchmark_dataset(json_file.stem, data, "Local")
        all_results.append(result)
    
    print("\n🌐 Loading Internet Data...")
    internet_files = list(data_dir.glob('internet_*.json'))
    
    if internet_files:
        for json_file in sorted(internet_files):
            print(f"  Loading {json_file.name}...")
            with open(json_file) as f:
                data = json.load(f)
            result = benchmark_dataset(json_file.stem.replace('internet_', ''), data, "Internet")
            all_results.append(result)
    else:
        print("  ⚠️  No internet data found. Run: python benchmarks/fetch_internet_data.py")
    
    print("\n🗄️  Loading MongoDB Data...")
    mongodb_file = data_dir / 'mongodb_irregular.json'
    
    if mongodb_file.exists():
        print(f"  Loading {mongodb_file.name}...")
        with open(mongodb_file) as f:
            data = json.load(f)
        result = benchmark_dataset('mongodb_irregular', data, "MongoDB")
        all_results.append(result)
    
    if all_results:
        print_results_table(all_results)
        
        print_section("📊 OVERALL SUMMARY")
        
        total_json = sum(r['json_size'] for r in all_results)
        total_lux = sum(r['lux_size'] for r in all_results if r['lux_size'])
        
        lux_success = len([r for r in all_results if r['lux_size']])
        lux_failed = len([r for r in all_results if not r['lux_size']])
        
        print(f"\nTotal Datasets: {len(all_results)}")
        print(f"  - Local: {len([r for r in all_results if r['source'] == 'Local'])}")
        print(f"  - Internet: {len([r for r in all_results if r['source'] == 'Internet'])}")
        print(f"  - MongoDB: {len([r for r in all_results if r['source'] == 'MongoDB'])}")
        
        print(f"\nTotal JSON Size: {format_bytes(total_json)}")
        print(f"Total LUX Size:  {format_bytes(total_lux)}")
        print(f"\nCompression: {(1 - total_lux / total_json) * 100:.1f}%")
        print(f"Success Rate: {lux_success}/{len(all_results)}")
        
        if lux_failed > 0:
            print(f"\n⚠️  FAILURES DETECTED:")
            for r in all_results:
                if r['lux_error']:
                    print(f"    - {r['name']}: {r['lux_error']}")
        
        print("\n" + "═" * 100)
        print("  ✅ Benchmark Complete!")
        print("═" * 100 + "\n")


if __name__ == '__main__':
    main()
