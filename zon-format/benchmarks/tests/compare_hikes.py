#!/usr/bin/env python3
"""
Compare the hiking data example in JSON, LUX, and TOON formats.
This is the example used on TOON's website.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
import lux


def count_tokens(text):
    """Approximate token count (rough estimation)."""
    return len(text) // 4


def main():
    data_dir = Path(__file__).parent.parent / 'data'
    
    # Load JSON data
    with open(data_dir / 'hikes.json') as f:
        data = json.load(f)
    
    # Load TOON reference
    with open(data_dir / 'hikes.toon') as f:
        toon_str = f.read().strip()
    
    json_formatted = json.dumps(data, indent=2)
    
    json_compact = json.dumps(data, separators=(',', ':'))
    
    if hasattr(lux, "encode") and callable(lux.encode):
        lux_str = lux.encode(data)
    elif hasattr(lux, "dumps") and callable(lux.dumps):
        lux_str = lux.dumps(data)
    elif hasattr(lux, "to_lux") and callable(lux.to_lux):
        lux_str = lux.to_lux(data)
    else:
        raise AttributeError("lux module does not provide 'encode', 'dumps', or 'to_lux' functions")

    print("=" * 100)
    print("  HIKING DATA COMPARISON - JSON vs LUX vs TOON")
    print("=" * 100)
    print("\nThis is the example used on TOON's official website (toonformat.dev)")
    print()
    
    print("─" * 100)
    print("JSON (formatted, 2-space indent)")
    print("─" * 100)
    print(json_formatted)
    print(f"\nSize: {len(json_formatted)} bytes")
    print(f"Estimated tokens: ~{count_tokens(json_formatted)}")
    
    print("\n" + "─" * 100)
    print("JSON (compact/minified)")
    print("─" * 100)
    print(json_compact)
    print(f"\nSize: {len(json_compact)} bytes")
    print(f"Estimated tokens: ~{count_tokens(json_compact)}")
    
    print("\n" + "─" * 100)
    print("LUX")
    print("─" * 100)
    print(lux_str)
    print(f"\nSize: {len(lux_str)} bytes")
    print(f"Estimated tokens: ~{count_tokens(lux_str)}")
    
    print("\n" + "─" * 100)
    print("TOON (reference format)")
    print("─" * 100)
    print(toon_str)
    print(f"\nSize: {len(toon_str)} bytes")
    print(f"Estimated tokens: ~{count_tokens(toon_str)}")
    
    print("\n" + "=" * 100)
    print("  SUMMARY")
    print("=" * 100)
    
    baseline = len(json_formatted)
    
    results = [
        ("JSON (formatted)", len(json_formatted), count_tokens(json_formatted)),
        ("JSON (compact)", len(json_compact), count_tokens(json_compact)),
        ("LUX", len(lux_str), count_tokens(lux_str)),
        ("TOON", len(toon_str), count_tokens(toon_str)),
    ]
    
    print(f"\n{'Format':<20} | {'Bytes':>8} | {'Est. Tokens':>12} | {'vs JSON':>12}")
    print("-" * 65)
    
    for name, size, tokens in results:
        compression = ((baseline - size) / baseline) * 100
        print(f"{name:<20} | {size:8} | {tokens:12} | {compression:11.1f}%")
    
    print("\n" + "=" * 100)
    print("  KEY FINDINGS")
    print("=" * 100)
    print(f"\n✅ LUX is {((baseline - len(lux_str)) / baseline * 100):.1f}% smaller than formatted JSON")
    print(f"✅ TOON is {((baseline - len(toon_str)) / baseline * 100):.1f}% smaller than formatted JSON")
    print(f"\n📊 LUX vs TOON: {abs(len(lux_str) - len(toon_str))} bytes difference")
    
    if len(lux_str) < len(toon_str):
        print(f"   LUX is {((len(toon_str) - len(lux_str)) / len(toon_str) * 100):.1f}% smaller than TOON")
    else:
        print(f"   TOON is {((len(lux_str) - len(toon_str)) / len(lux_str) * 100):.1f}% smaller than LUX")
    
    print("\n" + "=" * 100 + "\n")


if __name__ == '__main__':
    main()
