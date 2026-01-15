# CLI Guide

**Version:** 1.1.0

## Installation

The `lux` command is installed automatically with the package:

**Using pip:**
```bash
pip install lux-format
```

**Using UV (faster):**
```bash
uv pip install lux-format
# or
uv add lux-format
```

**Verify installation:**
```bash
lux --version
# lux-format 1.1.0
```

---

## Commands

### `encode`

Convert JSON to LUX format.

**Usage:**
```bash
lux encode <input_file> [-o <output_file>]
```

**Examples:**
```bash
# Encode JSON file
lux encode data.json > data.luxf

# Encode with output file
lux encode data.json -o data.luxf

# Encode from stdin
cat data.json | lux encode > data.luxf
```

---

### `decode`

Convert LUX to JSON format.

**Usage:**
```bash
lux decode <input_file> [-o <output_file>]
```

**Examples:**
```bash
# Decode LUX file
lux decode data.luxf > data.json

# Decode with output file
lux decode data.luxf -o data.json

# Decode from stdin
cat data.luxf | lux decode > data.json
```

---

### `validate`

Validate LUX file structure.

**Usage:**
```bash
lux validate <input_file>
```

**Example:**
```bash
lux validate data.luxf
# ✅ Valid LUX format
# 📊 3 tables, 150 total rows
```

---

### `stats`

Show compression statistics.

**Usage:**
```bash
lux stats <json_file>
```

**Example:**
```bash
lux stats users.json

# 📊 LUX Statistics
# ==================
# Original JSON:  2,842 bytes (939 tokens)
# LUX Format:     1,399 bytes (513 tokens)
# Compression:    50.8% size reduction
# Token Savings:  45.4% fewer tokens
```

---

### `format`

Canonicalize LUX output.

**Usage:**
```bash
lux format <input_file>
```

**Purpose:** Ensures consistent formatting for diffs.

**Example:**
```bash
lux format data.luxf > canonical.luxf
```

---

## File Extensions

### `.luxf`

The conventional file extension for LUX files:

```bash
# Encode
lux encode users.json > users.luxf

# Decode
lux decode users.luxf > users.json
```

---

## Pipe Usage

### Chain Commands

```bash
# Compress multiple files
for file in *.json; do
    lux encode "$file" > "${file%.json}.luxf"
done

# Validate all LUX files
find . -name "*.luxf" -exec lux validate {} \;

# Convert LUX to JSON for processing
lux decode data.luxf | jq '.users[] | select(.active == true)'
```

---

## Options

### Common Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message |
| `-v, --version` | Show version |
| `-o, --output` | Output file (instead of stdout) |
| `--pretty` | Pretty-print JSON output |

### Encoding Options

| Option | Description |
|--------|-------------|
| `--no-dict` | Disable dictionary compression |
| `--no-delta` | Disable delta encoding |
| `--coerce` | Enable type coercion |

**Example:**
```bash
# Encode without dictionary compression
lux encode --no-dict data.json > data.luxf

# Encode with type coercion
lux encode --coerce llm_output.json > output.luxf
```

### Decoding Options

| Option | Description |
|--------|-------------|
| `--no-strict` | Disable strict validation |
| `--coerce` | Enable type coercion |

**Example:**
```bash
# Decode with relaxed validation
lux decode --no-strict data.luxf > data.json

# Decode with type coercion
lux decode --coerce llm_output.luxf > data.json
```

---

## Examples

### Convert API Response

```bash
# Fetch API data and convert to LUX
curl https://api.example.com/users | lux encode > users.luxf

# Later, decode for processing
lux decode users.luxf | python process.py
```

### Compress LLM Context

```bash
# Before: Large JSON context
cat context.json
# 15,234 bytes

# After: Compressed LUX
lux encode context.json > context.luxf
cat context.luxf
# 8,912 bytes (41.5% savings)
```

### Validate LLM Output

```bash
# LLM generates LUX
llm_generate.sh > output.luxf

# Validate format
lux validate output.luxf
# ✅ Valid

# Convert to JSON
lux decode output.luxf > output.json
```

---

## See Also

- [API Reference](api-reference.md) - Python API
- [LLM Best Practices](llm-best-practices.md) - Using LUX with LLMs
