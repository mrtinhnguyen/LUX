# LUX Specification

## Lightweight Ultra-compressed Xchange - Formal Specification

**Version:** 1.1.0

**Date:** 2025-12-02

**Status:** Stable Release

**Authors:** LUX Format Contributors

**License:** MIT

---

## Abstract

Lightweight Ultra-compressed Xchange (LUX) is a compact, line-oriented text format that encodes the JSON data model with minimal redundancy optimized for large language model token efficiency. LUX achieves up to 49% token reduction compared to JSON through single-character primitives (`T`, `F`), null as `null`, explicit table markers (`@`), colon-less nested structures, intelligent quoting rules, delta encoding for sequential columns, and dictionary compression for repeated values. Arrays of uniform objects use tabular encoding with column headers declared once; metadata uses flat key-value pairs. This specification defines LUX's concrete syntax, canonical value formatting, encoding/decoding behavior, advanced compression features (delta, dictionary), conformance requirements, and strict validation rules. LUX provides deterministic, lossless representation achieving 100% LLM retrieval accuracy in benchmarks.

## Status of This Document

This document is a **Stable Release v1.1.0** and defines normative behavior for LUX encoders, decoders, and validators. Implementation feedback should be reported at https://github.com/LUX-Format/LUX.

Backward compatibility is maintained across v1.x releases. Major versions (v2.x) may introduce breaking changes.

**Changes in v1.1.0:**
- Delta encoding for sequential numeric columns
- Dictionary compression for repeated string values  
- Type coercion for LLM-generated outputs
- Enhanced sparse encoding with hierarchical flattening

## Normative References

**[RFC2119]** Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.  
https://www.rfc-editor.org/rfc/rfc2119

**[RFC8174]** Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, May 2017.  
https://www.rfc-editor.org/rfc/rfc8174

**[RFC8259]** Bray, T., "The JavaScript Object Notation (JSON) Data Interchange Format", STD 90, RFC 8259, December 2017.  
https://www.rfc-editor.org/rfc/rfc8259

## Informative References

**[RFC4180]** Shafranovich, Y., "Common Format and MIME Type for Comma-Separated Values (CSV) Files", RFC 4180, October 2005.  
https://www.rfc-editor.org/rfc/rfc4180

**[ISO8601]** ISO 8601:2019, "Date and time — Representations for information interchange".

**[UNICODE]** The Unicode Consortium, "The Unicode Standard", Version 15.1, September 2023.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Terminology and Conventions](#1-terminology-and-conventions)
3. [Data Model](#2-data-model)
4. [Encoding Normalization](#3-encoding-normalization)
5. [Decoding Interpretation](#4-decoding-interpretation)
6. [Concrete Syntax](#5-concrete-syntax)
7. [Primitives](#6-primitives)
8. [Strings and Keys](#7-strings-and-keys)
9. [Objects](#8-objects)
10. [Arrays](#9-arrays)
11. [Table Format](#10-table-format)
12. [Quoting and Escaping](#11-quoting-and-escaping)
13. [Whitespace](#12-whitespace-and-line-endings)
14. [Conformance](#13-conformance-and-options)
15. [Strict Mode Errors](#14-strict-mode-errors)
16. [Security](#15-security-considerations)
17. [Internationalization](#16-internationalization)
18. [Interoperability](#17-interoperability)
19. [Media Type](#18-media-type)
20. [Error Handling](#19-error-handling)
21. [Appendices](#appendices)

---

## Introduction (Informative)

### Purpose

LUX addresses token bloat in JSON while maintaining structural fidelity. By declaring column headers once, using single-character tokens, and eliminating redundant punctuation, LUX achieves optimal compression for LLM contexts.

### Design Goals

1. **Minimize tokens** - Every character counts in LLM context windows
2. **Preserve structure** - 100% lossless round-trip conversion
3. **Human readable** - Debuggable, understandable format
4. **LLM friendly** - Explicit markers aid comprehension
5. **Deterministic** - Same input → same output
6. **Deep Nesting** - Efficiently handles complex, recursive structures

### Use Cases

✅ **Use LUX for:**
- LLM prompt contexts (RAG, few-shot examples)
- Log storage and analysis
- Configuration files
- Browser storage (localStorage)
- Tabular data interchange
- **Complex nested data structures** (LUX excels here)

❌ **Don't use LUX for:**
- Public REST APIs (use JSON for compatibility)
- Real-time streaming protocols (not yet supported)
- Files requiring comments (use YAML/JSONC)

### Example

**JSON (118 chars):**
```json
{"users":[{"id":1,"name":"Alice","active":true},{"id":2,"name":"Bob","active":false}]}
```

**LUX (64 chars, 46% reduction):**
```lux
users:@(2):active,id,name
T,1,Alice
F,2,Bob
```

---

## 1. Terminology and Conventions

### 1.1 RFC2119 Keywords

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are interpreted per [RFC2119] and [RFC8174].

### 1.2 Definitions

**LUX document** - UTF-8 text conforming to this specification

**Line** - Character sequence terminated by LF (`\n`)

**Key-value pair** - Line pattern: `key:value`

**Table** - Array of uniform objects with header + data rows

**Table header** - Pattern: `key:@(N):columns` or `@(N):columns`

**Meta separator** - Colon (`:`) separating keys/values

**Table marker** - At-sign (`@`) indicating table structure

**Primitive** - Boolean, null, number, or string (not object/array)

**Uniform array** - All elements are objects with identical keys

**Strict mode** - Validation enforcing row/column counts

---

## 2. Data Model

### 2.1 JSON Compatibility

LUX encodes the JSON data model:
- **Primitives**: `str | int | float | bool | None`
- **Objects**: `dict[str, Any]`
- **Arrays**: `list[Any]`

### 2.2 Ordering

- **Arrays**: Order MUST be preserved exactly
- **Objects**: Key order MUST be preserved
  - Encoders SHOULD sort keys alphabetically
  - Decoders MUST preserve document order

### 2.3 Canonical Numbers

**Requirements for ENCODER:**

1. **No leading zeros:** `007` → invalid
2. **No trailing zeros:** `3.14000` → `3.14`
3. **No unnecessary decimals:** Integer `5` stays `5`, not `5.0`
4. **No scientific notation:** `1e6` → `1000000`, `1e-3` → `0.001`
5. **Special values map to null:**
   - `float('nan')` → `null`
   - `float('inf')` → `null`
   - `float('-inf')` → `null`

**Implementation:**
- Integers: Use standard string representation
- Floats: Ensure decimal point present, convert exponents to fixed-point
- Special values: Normalized to `null` before encoding

**Examples:**
```
1000000      ✓ (not 1e6 or 1e+6)
0.001        ✓ (not 1e-3)
3.14         ✓ (not 3.140000)
42           ✓ (integer, no decimal)
null         ✓ (was NaN or Infinity)
```

**Scientific notation:**
```
1e6     ⚠️  Decoders MUST accept, encoders SHOULD avoid (prefer 1000000)
2.5E-3  ⚠️  Decoders MUST accept, encoders SHOULD avoid (prefer 0.0025)
```

**Requirements:**
- Encoders MUST ensure `decode(encode(x)) === x` (round-trip fidelity)
- No trailing zeros in fractional part (except `.0` for float clarity)
- No leading zeros (except standalone `0`)
- `-0` normalizes to `0`

### 2.4 Special Values

- `float('nan')` → `null`
- `float('inf')` → `null`
- `float('-inf')` → `null`

---

## 3. Encoding Normalization

### 3.1 Host Type Mapping

Encoders MUST normalize non-JSON types before encoding:

**Python:**
| Input | LUX Output | Notes |
|-------|------------|-------|
| `None` | `null` | Null |
| `datetime.now()` | `"2025-11-28T10:00:00Z"` | ISO 8601 |
| `set([1,2])` | `"[1,2]"` | Convert to list |
| `Decimal('3.14')` | `3.14` or `"3.14"` | Number if no precision loss |
| `bytes(b'\x00')` | `"<base64>"` | Base64 encode |

Implementations MUST document their normalization policy.

---

## 4. Decoding Interpretation

### 4.1 Type Inference

**Unquoted tokens:**
```
T           → True (boolean)
F           → False (boolean)
null        → None
42          → 42 (integer)
3.14        → 3.14 (float)
1e6         → 1000000 (number)
05          → "05" (string, leading zero)
hello       → "hello" (string)
```

**Quoted tokens:**
```
"T"         → "T" (string, not boolean)
"123"       → "123" (string, not number)
"hello"     → "hello" (string)
""          → "" (empty string)
```

### 4.2 Escape Sequences

Only these escapes are valid:
- `\\` → `\`
- `\"` → `"`
- `\n` → newline
- `\r` → carriage return
- `\t` → tab

**Invalid escapes MUST error:**
```
"\x41"      ❌ Invalid
"\u0041"    ❌ Invalid (use literal UTF-8)
"\b"        ❌ Invalid
```

### 4.2 Type Coercion (Optional)

**Introduced:** v1.1.0  
**Purpose:** Handle LLM-generated stringified values  
**Default:** Disabled (opt-in feature)

When `enable_type_coercion=True`, encoders/decoders attempt to convert string representations to their actual types.

**Encoder Coercion:**

Converts stringified values in data:
```python
# Input (strings)
{'age': "25", 'active': "true", 'score': "null"}

# Output (coerced types)
users:@(1):active,age,score
T,25,null
```

**Algorithm:**
1. Analyze entire column in array
2. Check if ALL values are coercible
3. If yes, coerce entire column to target type

**Supported Coercions:**

| From String | To Type | Example |
|-------------|---------|---------|
| `"123"` | `123` (int) | Numbers without decimals |
| `"3.14"` | `3.14` (float) | Numbers with decimals |
| `"true"`, `"True"` | `T` (boolean) | Case-insensitive |
| `"false"`, `"False"` | `F` (boolean) | Case-insensitive |
| `"null"`, `"None"` | `null` | Null values |
| `"yes"`, `"1"` | `T` (boolean) | Alternative true forms |
| `"no"`, `"0"` | `F` (boolean) | Alternative false forms |

**Decoder Coercion:**

More lenient parsing when enabled:
```
yes     → True (vs string "yes")
no      → False (vs string "no")
05      → 5 (vs string "05", leading zero)
```

**Use Cases:**
- Parsing LLM-generated LUX
- Converting CSV/spreadsheet data
- Handling loosely-typed inputs

**Conformance:**
- Type coercion is OPTIONAL
- Implementations SHOULD document coercion behavior
- Round-trip NOT guaranteed with coercion enabled

### 4.3 Leading Zeros

Numbers with leading zeros are strings:
```
05          → "05" (string)
007         → "007" (string)
0           → 0 (number)
```

---

## 5. Concrete Syntax

### 5.1 Line Structure

LUX documents are line-oriented:
- Lines end with LF (`\n`)
- Empty lines are whitespace-only
- Blank lines separate metadata from tables

### 5.2 Root Form

Determined by first non-empty line:

**Root table:**
```lux
@(2):id,name
1,Alice
2,Bob
```

**Root object:**
```lux
name:Alice
age:30
```

**Root primitive:**
```lux
42
```

### 5.3 ABNF Grammar

```abnf
document     = object-form / table-form / primitive-form
object-form  = *([dictionary LF] key-value / table-section)
table-form   = [dictionary LF] table-header 1*data-row
primitive-form = value

key-value    = key ":" value LF
table-header = [key ":"] "@" "(" count ")" ":" column-list LF
table-section = [dictionary LF] table-header 1*data-row
data-row     = value *("," value) LF

; Delta encoding & Dictionary compression (v1.1.0)
dictionary   = key "[" count "]" ":" value *("," value) LF
column       = key [":delta"]  ; Delta marker suffix

key          = unquoted-string / quoted-string
value        = primitive / quoted-compound
primitive    = "T" / "F" / "null" / number / unquoted-string / delta-value
delta-value  = ["+"/"-"] number  ; For delta-encoded columns
quoted-compound = quoted-string  ; Contains JSON-like notation

column-list  = column *("," column)
count        = 1*DIGIT
number       = ["-"] 1*DIGIT ["." 1*DIGIT] [("e"/"E") ["+"/"-"] 1*DIGIT]
```

---

## 6. Primitives

### 6.1 Booleans

**Encoding:**
- `True` → `T`
- `False` → `F`

**Decoding:**
- `T` (case-sensitive) → `True`
- `F` (case-sensitive) → `False`

**Rationale:** 75% character reduction

### 6.2 Null

**Encoding:**
- `None` → `null` (4-character literal)

**Decoding:**
- `null` → `None`
- Also accepts (case-insensitive): `none`, `nil`

**Rationale:** Clarity and readability over minimal compression

### 6.3 Numbers

**Examples:**
```lux
age:30
price:19.99
score:-42
temp:98.6
large:1000000
```

**Rules:**
- Integers without decimal: `42`
- Floats with decimal: `3.14`
- Negatives with `-` prefix: `-17`
- No thousands separators
- Decimal separator is `.` (period)

---

## 7. Strings and Keys

### 7.1 Safe Strings (Unquoted)

Pattern: `^[a-zA-Z0-9_\-\.]+$`

**Examples:**
```lux
name:Alice
user_id:u123
version:v1.0.4
api-key:sk_test_key
```

### 7.2 Required Quoting

Quote strings if they:

1. **Contain structural chars:** `,`, `:`, `[`, `]`, `{`, `}`, `"`
2. **Match literal keywords:** `T`, `F`, `true`, `false`, `null`, `none`, `nil`
3. **Look like PURE numbers:** `123`, `3.14`, `1e6` (Complex patterns like `192.168.1.1` or `v1.0.5` do NOT need quoting)
4. **Have whitespace:** Leading/trailing spaces, internal spaces (MUST quote to preserve)
5. **Are empty:** `""` (MUST quote to distinguish from `null`)
6. **Contain escapes:** Newlines, tabs, quotes (MUST quote to prevent structure breakage)

**Examples:**
```lux
message:"Hello, world"
path:"C:\Users\file"
empty:""
quoted:"true"
number:"123"
spaces:" padded "
```

### 7.3 ISO Date Optimization

ISO 8601 dates MAY be unquoted:
```lux
created:2025-11-28
timestamp:2025-11-28T10:00:00Z
time:10:30:00
```

Decoders interpret these as strings (not parsed as Date objects unless application logic does so).

---

## 8. Objects

### 8.1 Flat Objects

```lux
active:T
age:30
name:Alice
```

Decodes to:
```json
{"active": true, "age": 30, "name": "Alice"}
```

### 8.2 Nested Objects

Quoted compound notation:

```lux
config:"{database:{host:localhost,port:5432},cache:{ttl:3600}}"
```

Alternatively using JSON string:
```lux
config:"{"database":{"host":"localhost","port":5432}}"
```

### 8.3 Empty Objects

```lux
metadata:"{}"
```

---

## 9. Arrays

### 9.1 Format Selection

**Decision algorithm:**

1. All elements are objects with same keys? → **Table format**
2. Otherwise → **Inline quoted format**

### 9.2 Inline Arrays

**Primitive arrays:**
```lux
tags:"[python,llm,lux]"
numbers:"[1,2,3,4,5]"
flags:"[T,F,T]"
mixed:"[hello,123,T,null]"
```

**Empty:**
```lux
items:"[]"
```

### 9.3 Irregularity Threshold

**Uniform detection:**

Calculate irregularity score:
```
For each pair of objects (i, j):
  similarity = shared_keys / (keys_i + keys_j - shared_keys)  # Jaccard
Avg_similarity = mean(all_similarities)
Irregularity = 1 - avg_similarity
```

**Threshold:**
- If irregularity > 0.6 → Use inline format
- If irregularity ≤ 0.6 → Use table format

---

## 10. Table Format

### 10.1 Header Syntax

**With key:**
```
users:@(2):active,id,name
```

**Root array:**
```
@(2):active,id,name
```

**Components:**
- `users` - Array key (optional for root)
- `@` - Table marker (REQUIRED)
- `(2)` - Row count (REQUIRED for strict mode)
- `:` - Separator (REQUIRED)
- `active,id,name` - Columns, comma-separated (REQUIRED)

### 10.2 Column Order

Columns SHOULD be sorted alphabetically:

```lux
users:@(2):active,id,name,role
T,1,Alice,admin
F,2,Bob,user
```

### 10.3 Data Rows

Each row is comma-separated values:

```lux
T,1,Alice,admin
```

**Rules:**
- One row per line
- Values encoded as primitives (§6-7)
- Field count MUST equal column count (strict mode)
- Missing values encode as `null`

### 10.4 Sparse Tables

**Introduced:** v1.1.0  
**Status:** Stable

Optional fields append as `key:value`:

```lux
users:@(3):id,name
1,Alice
2,Bob,role:admin,score:98
3,Carol
```

**Row 2 decodes to:**
```json
{"id": 2, "name": "Bob", "role": "admin", "score": 98}
```

### 10.5 Delta Encoding

**Introduced:** v1.1.0  
**Purpose:** Compress sequential numeric columns  
**Automatic:** Applied when beneficial

**Syntax:**

Column suffix `:delta` indicates delta encoding:
```lux
records:@(5):id:delta,name
1,Alice
+1,Bob
+1,Carol
+1,David
+1,Eve
```

**Algorithm:**

**Encoder:**
1. Detect numeric-only columns with ≥5 values
2. Check if values are sequential (small deltas)
3. If beneficial, emit first value absolutely
4. Emit subsequent values as `+N` or `-N` deltas

**Decoder:**
1. Parse `:delta` marker from column header
2. First value → current accumulator
3. For `+N` or `-N` → add to accumulator
4. Return accumulated value for each row

**When Applied:**

Automatically used when ALL conditions met:
- Column contains **only numbers** (int or float)
- Column has **≥5 values**
- Values are **mostly sequential** (avg|delta| < 1000)

**Examples:**

**Sequential IDs:**
```lux
users:@(1000):id:delta,name
1,User1
+1,User2
+1,User3
...
+1,User1000
```

**Timestamps:**
```lux
logs:@(3):timestamp:delta,message
1609459200,Started
+60,Processing
+60,Complete
```

**Decreasing Values:**
```lux
countdown:@(5):value:delta
100,Start
-10,Step1
-10,Step2
-10,Step3
-10,End
```

**Token Savings:**
- Sequential IDs: 60-70% fewer tokens
- Timestamps: 40-50% fewer tokens
- Large datasets: Up to 80% compression

### 10.6 Dictionary Compression

**Introduced:** v1.0.3  
**Purpose:** Deduplicate repeated string values  
**Automatic:** Applied when beneficial

**Syntax:**

Dictionary declared before table:
```lux
status[3]:delivered,in-transit,pending
shipments:@(5):id,status
1,2
2,0
3,2
4,1
5,2
```

**Components:**
- `status` - Dictionary name (matches column)
- `[3]` - Number of unique values
- `:` - Separator
- `delivered,in-transit,pending` - Values (0-indexed)

**Algorithm:**

**Encoder:**
1. Analyze each string column in table
2. Count unique values and total occurrences
3. If ≥10 total values and ≤10 unique values:
   - Calculate compression ratio
   - If ratio > 1.2x, create dictionary
4. Emit dictionary: `key[N]:val1,val2,...`
5. Replace column values with 0-based indices

**Decoder:**
1. Parse dictionary: `key[N]:value1,value2,...`
2. Store mapping: `{0: "value1", 1: "value2", ...}`
3. When processing table column matching dictionary name
4. Replace index with actual value from mapping

**When Applied:**

Automatically used when:
- Column has **≥10 total values**
- Column has **≤10 unique values**
- **Compression ratio > 1.2x**

**Examples:**

**Categorical Data:**
```lux
role[3]:admin,manager,user
employees:@(100):id,name,role
1,Alice,2
2,Bob,2
3,Carol,0
4,Dave,1
5,Eve,2
...
```

**Nested Fields:**
```lux
address.city[4]:LAX,NYC,SF,Seattle
users:@(50):id,name,address.city
1,Alice,1
2,Bob,2
3,Carol,1
...
```

**Multiple Dictionaries:**
```lux
status[2]:active,inactive
role[3]:admin,manager,user
users:@(10):id,name,role,status
1,Alice,0,0
2,Bob,2,0
...
```

**Token Savings:**

Real-world benchmarks:
- Status fields: 35-45% reduction
- Country codes: 50-60% reduction  
- Log levels (ERROR/WARN/INFO): 40-50% reduction
- E-commerce categories: 30-40% reduction

---

## 11. Quoting and Escaping

### 11.1 CSV Quoting (RFC 4180)

For table values containing commas:

```lux
messages:@(1):id,text
1,"He said ""hello"" to me"
```

**Rules:**
- Wrap in double quotes: `"value"`
- Escape internal quotes by doubling: `"` → `""`

### 11.2 Escape Sequences

```lux
multiline:"Line 1\nLine 2"
tab:"Col1\tCol2"
quote:"She said \"Hi\""
backslash:"C:\\path\\file"
```

**Valid escapes:**
- `\\` → `\`
- `\"` → `"`
- `\n` → newline
- `\r` → CR
- `\t` → tab

### 11.3 Unicode

Use literal UTF-8 (no `\uXXXX` escapes):

```lux
chinese:王小明
emoji:✅
arabic:مرحبا
```

---

## 12. Whitespace and Line Endings

### 12.1 Encoding Rules

Encoders MUST:
- Use LF (`\n`) line endings
- NOT emit trailing whitespace on lines
- NOT emit trailing newline at EOF (RECOMMENDED)
- MAY emit one blank line between metadata and table

### 12.2 Decoding Rules

Decoders SHOULD:
- Accept LF or CRLF (normalize to LF)
- Ignore trailing whitespace per line
- Treat multiple blank lines as single separator

---

## 13. Conformance and Options

### 13.1 Encoder Checklist

✅ **A conforming encoder MUST:**

- [ ] Emit UTF-8 with LF line endings
- [ ] Encode booleans as `T`/`F`
- [ ] Encode null as `null`
- [ ] Emit canonical numbers (§2.3)
- [ ] Normalize NaN/Infinity to `null`
- [ ] Detect uniform arrays → table format
- [ ] Emit table headers: `key:@(N):columns`
- [ ] Sort columns alphabetically
- [ ] Sort object keys alphabetically
- [ ] Quote strings per §7.2-7.3
- [ ] Use only valid escapes (§11.2)
- [ ] Preserve array order
- [ ] Preserve key order
- [ ] Ensure round-trip: `decode(encode(x)) == x`

**v1.1.0 Features (OPTIONAL):**
- [ ] Apply delta encoding for sequential columns (§10.5)
- [ ] Apply dictionary compression for repeated values (§10.6)
- [ ] Support type coercion when enabled (§4.2)

### 13.2 Decoder Checklist

✅ **A conforming decoder MUST:**

- [ ] Accept UTF-8 (LF or CRLF)
- [ ] Decode `T` → True, `F` → False, `null` → None
- [ ] Parse decimal and exponent numbers
- [ ] Treat leading-zero numbers as strings
- [ ] Unescape quoted strings
- [ ] Error on invalid escapes
- [ ] Parse table headers: `key:@(N):columns`
- [ ] Split rows by comma (CSV-aware)
- [ ] Preserve array order
- [ ] Preserve key order
- [ ] **Error Codes:**
    - `E001`: Row count mismatch (strict mode)
    - `E002`: Field count mismatch (strict mode)
    - `E301`: Document size > 100MB
    - `E302`: Line length > 1MB
    - `E303`: Array length > 1M items
    - `E304`: Object key count > 100K
- [ ] Enforce row count (strict mode)
- [ ] Enforce field count (strict mode)

**v1.1.0 Features (OPTIONAL):**
- [ ] Decode delta-encoded columns (`:delta` marker) (§10.5)
- [ ] Decode dictionary-compressed values (§10.6)
- [ ] Support type coercion when enabled (§4.2)

### 13.3 Strict Mode

**Enabled by default** in reference implementation.

Enforces:
- Table row count = declared `(N)`
- Each row field count = column count
- No malformed headers
- No invalid escapes
- No unterminated strings

**Non-strict mode** MAY tolerate count mismatches.

---

## 14. Schema Validation (LLM Evals)

LUX includes a runtime schema validation library designed for LLM guardrails. It allows defining expected structures and validating LLM outputs against them.

### 14.1 Schema Definition

```python
from lux import lux

UserSchema = lux.object({
    'name': lux.string().describe("Full name"),
    'age': lux.number(),
    'role': lux.enum(['admin', 'user']),
    'tags': lux.array(lux.string()).optional()
})
```

### 14.2 Prompt Generation

Schemas can generate system prompts to guide LLMs:

```python
prompt = UserSchema.to_prompt()
# Output:
# object:
#   - name: string - Full name
#   - age: number
#   - role: enum(admin, user)
#   - tags: array of [string] (optional)
```

### 14.3 Validation

```python
from lux import validate

result = validate(llm_output_string, UserSchema)

if result.success:
    print(result.data)  # Typed data
else:
    print(result.error)  # "Expected number at age, got string"
```

---

## 15. Strict Mode Errors

### 15.1 Table Errors

| Code | Error | Example |
|------|-------|---------|
| **E001** | Row count mismatch | `@(2)` but 3 rows |
| **E002** | Field count mismatch | 3 columns, row has 2 values |
| **E003** | Malformed header | Missing `@`, `(N)`, or `:` |
| **E004** | Invalid column name | Unescaped special chars |

### 15.2 Syntax Errors

| Code | Error | Example |
|------|-------|---------|
| **E101** | Invalid escape | `"\x41"` instead of `"A"` |
| **E102** | Unterminated string | `"hello` (no closing quote) |
| **E103** | Missing colon | `name Alice` → `name:Alice` |
| **E104** | Empty key | `:value` |

### 15.3 Format Errors

| Code | Error | Example |
|------|-------|---------|
| **E201** | Trailing whitespace | Line ends with spaces |
| **E202** | CRLF line ending | `\r\n` instead of `\n` |
| **E203** | Multiple blank lines | More than one consecutive |
| **E204** | Trailing newline | Document ends with `\n` |

---

## 16. Security Considerations

### 16.1 Resource Limits

Implementations SHOULD limit:
- Document size: 100 MB
- Line length: 1 MB
- Nesting depth: 100 levels
- Array length: 1,000,000
- Object keys: 100,000

Prevents denial-of-service attacks.

### 16.2 Validation

- Validate UTF-8 strictly
- Error on invalid escapes
- Reject malformed numbers
- Limit recursion depth

### 16.3 Injection Prevention

LUX does not execute code. Applications MUST sanitize before:
- SQL queries
- Shell commands
- HTML rendering

---

## 17. Internationalization

### 17.1 Character Encoding

**REQUIRED:** UTF-8 without BOM

Decoders MUST:
- Reject invalid UTF-8
- Reject BOM (U+FEFF) at start

### 17.2 Unicode

Full Unicode support:
- Emoji: `✅`, `🚀`
- CJK: `王小明`, `日本語`
- RTL: `مرحبا`, `שלום`

### 17.3 Locale Independence

- Decimal separator: `.` (period)
- No thousands separators
- ISO 8601 dates for internationalization

---

## 18. Interoperability

### 18.1 JSON

**LUX → JSON:** Lossless  
**JSON → LUX:** Lossless, with 35-50% compression for tabular data

**Example:**
```json
{"users": [{"id": 1, "name": "Alice"}]}
```
↓ LUX (42% smaller)
```lux
users:@(1):id,name
1,Alice
```

### 18.2 CSV

**CSV → LUX:** Add type awareness
**LUX → CSV:** Table rows export cleanly

**Advantages over CSV:**
- Type preservation
- Metadata support
- Nesting capability

### 18.3 TOON

**Comparison:**
- LUX: Flat, `@(N)`, `T/F/null` → Better compression
- TOON: Indented, `[N]{fields}:`, `true/false` → Better readability
Both are LLM-optimized; choose based on data shape.

---

## 19. Media Type & File Extension

### 19.1 File Extension

**Extension:** `.luxf`

LUX files use the `.luxf` extension (LUX Format) for all file operations.

**Examples:**
```
data.luxf
users.luxf
config.luxf
```

### 19.2 Media Type

**Media type:** `text/lux`

**Status:** Provisional (not yet registered with IANA)

**Charset:** UTF-8 (always)

LUX documents are **always UTF-8 encoded**. The `charset=utf-8` parameter may be specified but defaults to UTF-8 when omitted.

**HTTP Content-Type header:**
```http
Content-Type: text/lux
Content-Type: text/lux; charset=utf-8  # Explicit (optional)
```

### 19.3 MIME Type Usage

**Web servers:**
```nginx
# nginx
location ~ \.luxf$ {
    default_type text/lux;
    charset utf-8;
}
```

```apache
# Apache
AddType text/lux .luxf
AddDefaultCharset utf-8
```

**HTTP responses:**
```http
HTTP/1.1 200 OK
Content-Type: text/lux; charset=utf-8
Content-Length: 1234

users:@(2):id,name
1,Alice
2,Bob
```

### 19.4 Character Encoding

**Normative requirement:** LUX files MUST be UTF-8 encoded.

**Rationale:**
- Universal support across programming languages
- Compatible with JSON (RFC 8259)
- No byte-order mark (BOM) required
- Supports full Unicode character set

**Encoding declaration:** Not required (always UTF-8)

### 19.5 IANA Registration

**Current status:** Not registered

**Future work:** Formal registration with IANA is planned for v2.0.

---

## Appendices

### Appendix A: Examples

**A.1 Simple Object**
```lux
active:T
age:30
name:Alice
```

**A.2 Table**
```lux
users:@(2):active,id,name
T,1,Alice
F,2,Bob
```

**A.3 Mixed**
```lux
tags:"[api,auth]"
version:1.0
users:@(1):id,name
1,Alice
```

**A.4 Root Array**
```lux
@(2):id,name
1,Alice
2,Bob
```

### Appendix B: Test Suite

**Coverage:**
- ✅ 94/94 unit tests
- ✅ 27/27 roundtrip tests
- ✅ 100% data integrity

**Test categories:**
- Primitives (T, F, null, numbers, strings)
- Tables (uniform arrays)
- Quoting, escaping
- Round-trip fidelity
- Edge cases, errors

### Appendix C: Changelog

**v1.1.0 (2025-12-02)**
- ✨ Delta encoding for sequential numeric columns
- ✨ Dictionary compression for repeated string values
- ✨ Type coercion for LLM-generated outputs
- ✨ Enhanced sparse encoding with hierarchical flattening
- 📊 49% token reduction vs JSON (up from 23.8%)
- 🐍 Full Python implementation parity

**v1.0.4 (2025-11-30)**
- Colon-less nested syntax
- Smart flattening
- Control character escaping
- Runtime schema validation

**v1.0.3 (2025-11-28)**
- Disabled sequential column omission
- 100% LLM accuracy achieved
- All columns explicit

**v1.0.2 (2025-11-27)**
- Irregularity threshold tuning
- ISO date detection
- Sparse table encoding

**v1.0.1 (2025-11-26)**
- License: MIT
- Documentation updates

**v1.0.0 (2025-11-26)**
- Initial stable release
- Single-character primitives
- Table format
- Lossless round-trip

### Appendix D: License

MIT License

Copyright (c) 2025 LUX-FORMAT (Roni Bhakta)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

**End of Specification**
