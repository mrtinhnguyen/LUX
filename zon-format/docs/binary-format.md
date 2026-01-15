# LUX Binary Format (LUX-B)

The LUX Binary Format (LUX-B) provides a compact binary encoding for LUX data, offering 40-60% space savings compared to JSON while maintaining full type fidelity and structure.

## Overview

LUX-B is a MessagePack-inspired binary format designed specifically for LUX data structures. It provides:

- **Compact Storage**: 40-60% smaller than equivalent JSON
- **Fast Encoding/Decoding**: Optimized binary operations
- **Type Preservation**: Full support for all LUX types
- **Magic Header**: Format validation with `LUB\x01`
- **Round-Trip Fidelity**: Perfect encoding/decoding cycle

## Quick Start

```python
from lux import encode_binary, decode_binary

# Encode to binary
data = {"name": "Alice", "age": 30, "active": True}
binary = encode_binary(data)

# Decode from binary
decoded = decode_binary(binary)
assert decoded == data
```

## Format Specification

### Magic Header

Every LUX-B file starts with a 4-byte magic header:
- Bytes 0-2: `LUB` (ASCII)
- Byte 3: Version (`0x01`)

### Type Markers

| Marker | Type | Size |
|--------|------|------|
| `0x00` | Null | 0 bytes |
| `0x01` | Boolean (False) | 0 bytes |
| `0x02` | Boolean (True) | 0 bytes |
| `0x10` | Positive Integer | Variable |
| `0x11` | Negative Integer | Variable |
| `0x20` | Float | 8 bytes (double) |
| `0x30` | String | Length + data |
| `0x40` | Array | Count + items |
| `0x50` | Object | Count + key-value pairs |

### Encoding Rules

#### Integers

Small integers (0-127) are encoded directly after the marker.
Larger integers use variable-length encoding:

```
0x10 <value>        # Positive: 0-127
0x10 0xFF <bytes>   # Positive: >127 (4 bytes)
0x11 <value>        # Negative: -1 to -128
0x11 0xFF <bytes>   # Negative: <-128 (4 bytes)
```

#### Strings

Strings are encoded as:
```
0x30 <length> <utf-8 bytes>
```

Length is variable-length encoded for efficiency.

#### Arrays

Arrays include element count and values:
```
0x40 <count> <item1> <item2> ...
```

#### Objects

Objects include key-value pair count:
```
0x50 <count> <key1> <value1> <key2> <value2> ...
```

Keys are always encoded as strings.

## API Reference

### encode_binary(data: Any) -> bytes

Encodes Python data to LUX-B binary format.

**Parameters:**
- `data`: Any JSON-serializable Python object

**Returns:**
- `bytes`: Binary-encoded data with LUX-B header

**Example:**
```python
from lux import encode_binary

data = {
    "users": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ],
    "total": 2
}

binary = encode_binary(data)
print(f"Binary size: {len(binary)} bytes")
```

### decode_binary(data: bytes) -> Any

Decodes LUX-B binary format to Python data.

**Parameters:**
- `data`: Binary data with LUX-B magic header

**Returns:**
- `Any`: Decoded Python object

**Raises:**
- `ValueError`: If magic header is invalid
- `ValueError`: If binary data is corrupted

**Example:**
```python
from lux import decode_binary

binary_data = b'LUB\x01...'  # LUX-B format
decoded = decode_binary(binary_data)
```

## Performance Comparison

### Size Comparison

For a typical dataset with 100 user records:

| Format | Size | Savings |
|--------|------|---------|
| JSON | 12,500 bytes | - |
| LUX (Text) | 8,200 bytes | 34% |
| **LUX-B (Binary)** | **5,000 bytes** | **60%** |

### Speed Comparison

Encoding/decoding 10,000 records:

| Operation | JSON | LUX Text | LUX-B |
|-----------|------|----------|-------|
| Encode | 45ms | 38ms | **25ms** |
| Decode | 52ms | 42ms | **30ms** |

## Use Cases

### 1. API Response Compression

```python
from lux import encode_binary
from flask import Response

@app.route('/api/data')
def get_data():
    data = fetch_large_dataset()
    binary = encode_binary(data)
    
    return Response(
        binary,
        mimetype='application/x-lux-binary',
        headers={'Content-Encoding': 'lux-binary'}
    )
```

### 2. File Storage

```python
from lux import encode_binary, decode_binary
import os

# Save to file
data = load_config()
binary = encode_binary(data)
with open('config.luxb', 'wb') as f:
    f.write(binary)

# Load from file
with open('config.luxb', 'rb') as f:
    binary = f.read()
data = decode_binary(binary)
```

### 3. Database Storage

```python
from lux import encode_binary, decode_binary

# Store in database
binary = encode_binary(user_data)
db.execute(
    "INSERT INTO cache (key, value) VALUES (?, ?)",
    (cache_key, binary)
)

# Retrieve from database
row = db.execute(
    "SELECT value FROM cache WHERE key = ?",
    (cache_key,)
).fetchone()
data = decode_binary(row[0])
```

### 4. Network Transmission

```python
import socket
from lux import encode_binary, decode_binary

# Send
data = {"message": "Hello", "timestamp": 1234567890}
binary = encode_binary(data)
sock.send(len(binary).to_bytes(4, 'big') + binary)

# Receive
size = int.from_bytes(sock.recv(4), 'big')
binary = sock.recv(size)
data = decode_binary(binary)
```

## Best Practices

### 1. Validate Magic Header

Always validate the header before decoding:

```python
def is_luxb_format(data: bytes) -> bool:
    return len(data) >= 4 and data[:3] == b'LUB' and data[3] == 0x01

binary_data = load_file()
if is_luxb_format(binary_data):
    decoded = decode_binary(binary_data)
else:
    raise ValueError("Not a valid LUX-B file")
```

### 2. Handle Errors Gracefully

```python
from lux import decode_binary

try:
    data = decode_binary(binary_input)
except ValueError as e:
    logger.error(f"Failed to decode LUX-B: {e}")
    # Fallback to alternative format
    data = decode_json(json_input)
```

### 3. Use for Large Datasets

Binary format is most beneficial for larger datasets:

```python
from lux import encode_binary, encode

# Use binary for large data
if len(data) > 1000 or size_estimate(data) > 10_000:
    return encode_binary(data)
else:
    return encode(data)  # Text format for small data
```

### 4. Version Compatibility

Check version compatibility when decoding:

```python
def decode_with_version_check(binary: bytes):
    if binary[3] != 0x01:
        raise ValueError(f"Unsupported LUX-B version: {binary[3]}")
    return decode_binary(binary)
```

## Limitations

1. **Binary Format**: Not human-readable (use text LUX for debugging)
2. **Version Locking**: Format version must match (currently v1)
3. **No Streaming**: Must encode/decode entire structure
4. **Platform Dependent**: Endianness matters for cross-platform use

## Migration Guide

### From JSON

```python
import json
from lux import encode_binary, decode_binary

# Before: JSON
json_str = json.dumps(data)
data = json.loads(json_str)

# After: LUX-B
binary = encode_binary(data)
data = decode_binary(binary)
```

### From Text LUX

```python
from lux import encode, decode, encode_binary, decode_binary

# Convert text LUX to binary
text_lux = encode(data)
data = decode(text_lux)
binary = encode_binary(data)

# Or directly
binary = encode_binary(data)
```

## CLI Support

The CLI currently focuses on text LUX format. For binary format operations, use the Python API:

```bash
# Encode JSON to text LUX
lux encode data.json -o output.luxf

# Decode LUX to JSON
lux decode output.luxf --pretty -o result.json

# Analyze data and compare sizes
lux analyze data.json --compare
```

For binary format, use Python:

```python
from lux import encode_binary, decode_binary
import json

# JSON to LUX-B
with open('data.json') as f:
    data = json.load(f)
binary = encode_binary(data)
with open('data.luxb', 'wb') as f:
    f.write(binary)

# LUX-B to JSON
with open('data.luxb', 'rb') as f:
    binary = f.read()
data = decode_binary(binary)
with open('result.json', 'w') as f:
    json.dump(data, f)
```

## Further Reading

- [Performance Benchmarks](../benchmarks/README.md)
- [API Reference](api-reference.md)
- [Format Specification](SPEC.md)
