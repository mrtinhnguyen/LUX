import unittest
import sys
import os
import json

import lux

class TestZonCoreFeatures(unittest.TestCase):
    """Test core features of LUX v1.0"""

    def test_float_preservation(self):
        """Test that floats are preserved as floats, even if they look like ints."""
        data = {
            "float_val": 127.0,
            "int_val": 127,
            "small_float": 0.0001,
            "large_float": 1.23e10
        }
        
        encoded = lux.encode(data)
        decoded = lux.decode(encoded)
        
        self.assertIsInstance(decoded["float_val"], float)
        self.assertIsInstance(decoded["int_val"], int)
        self.assertEqual(decoded["float_val"], 127.0)
        self.assertEqual(decoded["int_val"], 127)
        self.assertEqual(decoded["small_float"], 0.0001)

    def test_irregular_schema(self):
        """Test handling of lists with irregular schemas (different keys)."""
        data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "role": "admin"}
        ]
        
        encoded = lux.encode(data)
        decoded = lux.decode(encoded)
        
        self.assertEqual(decoded, data)
        self.assertNotIn("email", decoded[0])
        self.assertNotIn("role", decoded[0])

    def test_boolean_parsing(self):
        """Test parsing of various boolean representations."""
        self.assertEqual(lux.decode("val:T")["val"], True)
        self.assertEqual(lux.decode("val:F")["val"], False)
        
        self.assertEqual(lux.decode("val:true")["val"], True)
        self.assertEqual(lux.decode("val:TRUE")["val"], True)
        self.assertEqual(lux.decode("val:false")["val"], False)
        self.assertEqual(lux.decode("val:FALSE")["val"], False)

    def test_null_parsing(self):
        """Test parsing of various null representations."""
        self.assertIsNone(lux.decode("val:null")["val"])
        self.assertIsNone(lux.decode("val:NULL")["val"])
        self.assertIsNone(lux.decode("val:None")["val"])
        self.assertIsNone(lux.decode("val:nil")["val"])

    def test_nested_structures(self):
        """Test deep nesting and mixed types."""
        data = {
            "level1": {
                "level2": {
                    "level3": [1, 2, {"deep": "value"}]
                }
            }
        }
        
        encoded = lux.encode(data)
        decoded = lux.decode(encoded)
        
        self.assertEqual(decoded, data)
        self.assertEqual(decoded["level1"]["level2"]["level3"][2]["deep"], "value")

    def test_type_safety_strings(self):
        """Test that strings looking like other types are preserved."""
        data = {
            "str_true": "true",
            "str_null": "null",
            "str_int": "123",
            "str_float": "123.45"
        }
        
        encoded = lux.encode(data)
        decoded = lux.decode(encoded)
        
        self.assertIsInstance(decoded["str_true"], str)
        self.assertIsInstance(decoded["str_null"], str)
        self.assertIsInstance(decoded["str_int"], str)
        self.assertIsInstance(decoded["str_float"], str)
        
        self.assertEqual(decoded["str_true"], "true")

if __name__ == '__main__':
    unittest.main()
