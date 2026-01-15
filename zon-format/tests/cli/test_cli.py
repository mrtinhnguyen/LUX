import unittest
import os
import shutil
import json
import subprocess
import sys
from lux import decode, encode

CLI_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/lux/cli.py'))
TEMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp_cli_test'))

class TestCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(TEMP_DIR):
            os.mkdir(TEMP_DIR)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)

    def run_cli(self, args, suppress_stderr=False):
        """Helper to run CLI commands."""
        cmd = [sys.executable, '-m', 'lux.cli'] + args.split()
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            env={**os.environ, 'PYTHONPATH': os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))}
        )
        if result.returncode != 0 and not suppress_stderr:
            print(f"CLI Error: {result.stderr}")
        return result

    def test_converts_json_to_lux(self):
        """Test converting JSON file to LUX."""
        data = {'name': 'Test', 'value': 123}
        input_file = os.path.join(TEMP_DIR, 'data.json')
        with open(input_file, 'w') as f:
            json.dump(data, f)

        result = self.run_cli(f"convert {input_file}")
        self.assertEqual(result.returncode, 0)
        decoded = decode(result.stdout)
        self.assertEqual(decoded, data)

    def test_converts_csv_to_lux(self):
        """Test converting CSV file to LUX."""
        csv_content = 'name,age,active\nAlice,30,true\nBob,25,false'
        input_file = os.path.join(TEMP_DIR, 'data.csv')
        with open(input_file, 'w') as f:
            f.write(csv_content)

        result = self.run_cli(f"convert {input_file}")
        self.assertEqual(result.returncode, 0)
        decoded = decode(result.stdout)
        
        decoded = decode(result.stdout)
        
        expected = [
            {'name': 'Alice', 'age': 30, 'active': True},
            {'name': 'Bob', 'age': 25, 'active': False}
        ]
        self.assertEqual(decoded, expected)

    def test_converts_yaml_to_lux(self):
        """Test converting YAML file to LUX."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")

        yaml_content = """
name: Test
items:
  - id: 1
    val: A
  - id: 2
    val: B
"""
        input_file = os.path.join(TEMP_DIR, 'data.yaml')
        with open(input_file, 'w') as f:
            f.write(yaml_content)

        result = self.run_cli(f"convert {input_file}")
        self.assertEqual(result.returncode, 0)
        decoded = decode(result.stdout)
        
        expected = {
            'name': 'Test',
            'items': [
                {'id': 1, 'val': 'A'},
                {'id': 2, 'val': 'B'}
            ]
        }
        self.assertEqual(decoded, expected)

    def test_supports_explicit_format_flag(self):
        """Test explicit format flag overrides extension."""
        json_content = '{"a":1}'
        input_file = os.path.join(TEMP_DIR, 'data.txt')
        with open(input_file, 'w') as f:
            f.write(json_content)

        result = self.run_cli(f"convert {input_file} --format=json")
        self.assertEqual(result.returncode, 0)
        decoded = decode(result.stdout)
        self.assertEqual(decoded, {'a': 1})

    def test_validate_correct_lux_file(self):
        """Test validation of a correct LUX file."""
        lux_content = 'name:Test\nvalue:123'
        input_file = os.path.join(TEMP_DIR, 'valid.luxf')
        with open(input_file, 'w') as f:
            f.write(lux_content)

        result = self.run_cli(f"validate {input_file}")
        self.assertEqual(result.returncode, 0)
        self.assertIn('Valid LUX file', result.stdout)

    def test_fails_on_invalid_lux_file(self):
        """Test validation fails on invalid LUX file."""
        invalid_content = 'users:@(2):id\n1'
        input_file = os.path.join(TEMP_DIR, 'invalid.luxf')
        with open(input_file, 'w') as f:
            f.write(invalid_content)

        result = self.run_cli(f"validate {input_file}", suppress_stderr=True)
        self.assertNotEqual(result.returncode, 0)

    def test_stats_command(self):
        """Test stats command output."""
        lux_content = 'users:@(2):id,name\n1,Alice\n2,Bob'
        input_file = os.path.join(TEMP_DIR, 'stats.luxf')
        with open(input_file, 'w') as f:
            f.write(lux_content)

        result = self.run_cli(f"stats {input_file}")
        self.assertEqual(result.returncode, 0)
        self.assertIn('LUX File Statistics', result.stdout)
        self.assertIn('Size:', result.stdout)

if __name__ == '__main__':
    unittest.main()
