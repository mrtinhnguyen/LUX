# Schema Validation Guide

**Version:** 1.1.0

## Overview

LUX includes runtime schema validation to ensure LLM outputs match expected formats.

---

## Quick Start

```python
from lux import validate, lux

# Define schema
UserSchema = lux.object({
    'name': lux.string().describe("User's full name"),
    'age': lux.number().describe("Age in years"),
    'role': lux.enum(['admin', 'user']).describe("Access level"),
    'tags': lux.array(lux.string()).optional()
})

# Validate
result = validate(llm_output, UserSchema)

if result.success:
    data = result.data
else:
    print(f"Error: {result.error}")
    print(f"Issues: {result.issues}")
```

---

## Schema Types

### String

```python
name = lux.string() \
    .min_length(1) \
    .max_length(100) \
    .describe("User name")
```

### Number

```python
age = lux.number() \
    .min(0) \
    .max(120) \
    .describe("Age in years")
```

### Boolean

```python
active = lux.boolean() \
    .default(True) \
    .describe("Is active")
```

### Array

```python
tags = lux.array(lux.string()) \
    .min_items(1) \
    .describe("User tags")
```

### Object

```python
address = lux.object({
    'street': lux.string(),
    'city': lux.string(),
    'zip': lux.string()
}).describe("Mailing address")
```

### Enum

```python
role = lux.enum(['admin', 'user', 'guest']) \
    .describe("User role")
```

---

## Optional Fields

```python
schema = lux.object({
    'name': lux.string(),                    # Required
    'email': lux.string().optional(),        # Optional
    'phone': lux.string().default('N/A')    # Optional with default
})
```

---

## Generate System Prompts

```python
schema = lux.object({
    'users': lux.array(lux.object({
        'id': lux.number(),
        'name': lux.string(),
        'role': lux.enum(['admin', 'user'])
    }))
})

prompt = schema.to_prompt()
print(prompt)
# object:
#   - users: array of [object]:
#     - id: number
#     - name: string
#     - role: enum(admin, user)
```

---

## Self-Correcting LLMs

Feed validation errors back to the LLM:

```python
def query_with_validation(llm, prompt, schema, max_retries=3):
    for attempt in range(max_retries):
        output = llm.query(prompt)
        result = validate(output, schema)
        
        if result.success:
            return result.data
        
        # Feed error back to LLM
        error_msg = f"Invalid format: {result.error}. Issues: {result.issues}"
        prompt = f"{prompt}\n\nPrevious attempt failed: {error_msg}. Please fix."
    
    raise ValueError("Failed after max retries")
```

---

## See Also

- [API Reference](api-reference.md)
- [LLM Best Practices](llm-best-practices.md)
