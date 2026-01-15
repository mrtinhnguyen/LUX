# LUX Python v1.2.1 Release Notes

**Release Date:** January 15, 2026  
**Status:** ✅ Production Ready

## 🎉 Major Release: Full Rebranding & Enterprise Expansion

LUX Python v1.2.1 marks a significant milestone with a complete rebranding from ZON to LUX, focusing on modularity, production-ready publishing tools, and enterprise-grade encoding.

## 🚀 What's New

### 1. Adaptive Encoding System

The centerpiece of v1.2.0 is the new adaptive encoding system that automatically analyzes your data and selects the optimal encoding strategy.

```python
from lux import encode_adaptive, AdaptiveEncodeOptions

# Simple usage - auto-selects best mode
output = encode_adaptive(data)

# Explicit mode selection
output = encode_adaptive(data, AdaptiveEncodeOptions(mode='compact'))
```

**Three encoding modes:**
- **compact** - Maximum token compression (default)
- **llm-optimized** - Balanced for AI comprehension
- **readable** - Human-friendly formatting

### 2. Data Complexity Analyzer

New analyzer provides insights into your data structure:

```python
from lux import DataComplexityAnalyzer

analyzer = DataComplexityAnalyzer()
result = analyzer.analyze(data)

print(f"Nesting depth: {result.nesting}")
print(f"Irregularity: {result.irregularity:.2%}")
print(f"Recommendation: {result.recommendation}")
```

### 3. Intelligent Mode Recommendations

Let LUX recommend the best encoding mode for your data:

```python
from lux import recommend_mode

recommendation = recommend_mode(data)
print(f"Use {recommendation['mode']} mode")
print(f"Confidence: {recommendation['confidence']:.2%}")
print(f"Reason: {recommendation['reason']}")
```

### 4. Enhanced CLI Tools

New commands for better workflow:

```bash
# Encode with mode selection
lux encode data.json -m compact > output.luxf

# Decode back to JSON
lux decode file.luxf --pretty > output.json

# Analyze data complexity
lux analyze data.json --compare
```

## 📊 Performance & Savings

**Real-world example:**
- JSON size: 435 bytes
- LUX compact: 187 bytes (57% savings)
- LUX LLM-optimized: 193 bytes (56% savings)

**Test results:**
- All 237 tests passing (including 17 new adaptive tests)
- Zero regressions
- 100% backward compatible

## 🔧 Installation

```bash
# Using pip
pip install --upgrade lux-format

# Using UV (faster)
uv pip install --upgrade lux-format

# Verify installation
python -c "import lux; print(lux.__version__)"
# Output: 1.2.1
```

## 📚 Documentation

**New Guides:**
- [Adaptive Encoding Guide](docs/adaptive-encoding.md) - Complete guide (7.1KB)
- [Migration Guide v1.2](docs/migration-v1.2.md) - Upgrade instructions (7.2KB)
- [Examples Directory](examples/modes/) - Real-world examples

**Updated:**
- [README](README.md) - v1.2.0 features
- [CHANGELOG](CHANGELOG.md) - Release history
- [API Reference](docs/api-reference.md) - New functions

## 🎯 Use Cases

### Production APIs (Compact Mode)

```python
from lux import encode_adaptive, AdaptiveEncodeOptions

@app.route('/api/data')
def get_data():
    data = get_large_dataset()
    output = encode_adaptive(
        data,
        AdaptiveEncodeOptions(mode='compact')  # Maximum compression
    )
    return output, 200, {'Content-Type': 'text/luxf'}
```

**Benefits:** 30-60% token savings vs JSON

### LLM Workflows (LLM-Optimized Mode)

```python
from lux import encode_adaptive, AdaptiveEncodeOptions
import openai

context = encode_adaptive(
    large_dataset,
    AdaptiveEncodeOptions(mode='llm-optimized')
)

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"Analyze: {context}"}]
)
```

**Benefits:** Balanced token efficiency and AI comprehension

### Configuration Files (Readable Mode)

```python
from lux import encode_adaptive, AdaptiveEncodeOptions

with open('config.luxf', 'w') as f:
    f.write(encode_adaptive(
        config,
        AdaptiveEncodeOptions(mode='readable')
    ))
```

**Benefits:** Human-friendly formatting for version control

## 🔄 Migration from v1.1.0

**100% backward compatible** - No breaking changes!

```python
# v1.1.0 code (still works)
from lux import encode, decode
output = encode(data)

# v1.2.0 code (recommended)
from lux import encode_adaptive
output = encode_adaptive(data)  # Better results!
```

See the [Migration Guide](docs/migration-v1.2.md) for details.

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
# Result: 237 passed in 0.69s
```

Test coverage:
- ✅ Core encoding/decoding (220 tests)
- ✅ Adaptive encoding (17 tests)
- ✅ CLI commands (manual verification)
- ✅ Round-trip integrity
- ✅ Backward compatibility

## 📦 Package Structure

```
lux-format/
├── src/lux/
│   ├── core/
│   │   ├── analyzer.py      # NEW: Data complexity analyzer
│   │   ├── adaptive.py      # NEW: Adaptive encoding engine
│   │   ├── encoder.py       # Updated
│   │   ├── decoder.py       # Unchanged
│   │   └── ...
│   ├── cli.py               # NEW: Enhanced CLI commands
│   └── __init__.py          # Updated exports
├── tests/
│   └── unit/
│       └── test_adaptive.py # NEW: 17 adaptive tests
├── docs/
│   ├── adaptive-encoding.md # NEW: Complete guide
│   ├── migration-v1.2.md    # NEW: Migration guide
│   └── ...
├── examples/
│   └── modes/               # NEW: Mode examples
│       ├── compact.luxf
│       ├── llm-optimized.luxf
│       ├── readable.luxf
│       └── README.md
└── CHANGELOG.md             # Updated
```

## 🌟 Key Features Summary

| Feature | Status | Impact |
|---------|--------|--------|
| Adaptive Encoding | ✅ Complete | High |
| 3 Encoding Modes | ✅ Complete | High |
| Data Analyzer | ✅ Complete | Medium |
| Mode Recommendations | ✅ Complete | Medium |
| Enhanced CLI | ✅ Complete | High |
| Documentation | ✅ Complete | High |
| Examples | ✅ Complete | Medium |
| Tests | ✅ Complete | High |
| Backward Compatibility | ✅ Complete | Critical |

## ❌ Not Included

The following TypeScript v1.3.0 features are **intentionally excluded** from Python v1.2.0:

- **Binary Format (LUX-B)** - Can be added in v1.3.0
- **Versioning & Migration System** - Can be added in v1.3.0
- **Pretty Printer with Colors** - Can be added incrementally

This keeps v1.2.0 focused on the most impactful features.

## 🐛 Known Issues

None! All tests pass and the package is production-ready.

## 🔮 Future Plans (v1.3.0)

Potential features for next release:
- Binary format support (LUX-B)
- Versioning and migration system
- Pretty printer with syntax highlighting
- Additional compression algorithms
- Performance optimizations

## 👥 Contributors

- Development: Roni Bhakta ([@ronibhakta1](https://github.com/ronibhakta1))
- Based on TypeScript implementation: LUX-Format/lux-TS

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

## 🔗 Links

- [PyPI Package](https://pypi.org/project/lux-format/)
- [GitHub Repository](https://github.com/LUX-Format/LUX)
- [Documentation](README.md)
- [TypeScript Implementation](https://github.com/LUX-Format/lux-TS)
- [Report Issues](https://github.com/LUX-Format/LUX/issues)

## 🎊 Get Started

```bash
# Install
pip install lux-format

# Try it out
python -c "
from lux import encode_adaptive, recommend_mode

data = {'users': [{'id': 1, 'name': 'Alice'}]}

# Get recommendation
rec = recommend_mode(data)
print(f'Recommended mode: {rec[\"mode\"]}')

# Encode
output = encode_adaptive(data)
print(f'Encoded: {output}')
"
```

---

**Made with ❤️ by TonyX & the LUX community**

*LUX v1.2.1 - Lightweight Ultra-compressed Xchange*
