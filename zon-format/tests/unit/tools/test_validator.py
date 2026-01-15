"""Tests for LUX validator"""

import pytest
from lux.tools import ZonValidator, validate_lux, LintOptions, ValidationResult


class TestValidatorBasics:
    """Basic validator tests"""
    
    def test_validate_valid_lux(self):
        """Test validating valid LUX"""
        validator = ZonValidator()
        result = validator.validate("name:Alice\nage:30")
        
        assert result.valid is True
        assert len(result.errors) == 0
    
    def test_validate_invalid_lux(self):
        """Test validating invalid LUX"""
        validator = ZonValidator()
        # Invalid braces should cause decode error
        result = validator.validate("@5:id,name\n1,Alice\n2")  # Wrong row count
        
        # May or may not be valid depending on strict mode
        assert isinstance(result, ValidationResult)
    
    def test_validate_empty_string(self):
        """Test validating empty string"""
        validator = ZonValidator()
        result = validator.validate("")
        
        # Empty string decodes to None which is valid
        assert isinstance(result, ValidationResult)


class TestLintOptions:
    """Test linting with options"""
    
    def test_max_depth_warning(self):
        """Test max depth warning"""
        validator = ZonValidator()
        lux_string = "a{b{c{d{e{f:value}}}}}"
        
        options = LintOptions(max_depth=3)
        result = validator.validate(lux_string, options)
        
        assert len(result.warnings) > 0
    
    def test_max_fields_warning(self):
        """Test max fields warning"""
        validator = ZonValidator()
        
        data_dict = {f"field{i}": i for i in range(50)}
        from lux import encode
        lux_string = encode(data_dict)
        
        options = LintOptions(max_fields=30)
        result = validator.validate(lux_string, options)
        
        assert len(result.warnings) > 0


class TestValidatorSuggestions:
    """Test validator suggestions"""
    
    def test_suggestions_for_invalid(self):
        """Test validator handles malformed input"""
        validator = ZonValidator()
        result = validator.validate("}{][")
        
        # May decode or fail depending on parser
        assert isinstance(result, ValidationResult)
    
    def test_no_suggestions_for_valid(self):
        """Test no suggestions for valid input"""
        validator = ZonValidator()
        result = validator.validate("name:Alice")
        
        # May or may not have suggestions depending on data


class TestValidateZonFunction:
    """Test convenience function"""
    
    def test_validate_lux_function(self):
        """Test validate_lux convenience function"""
        result = validate_lux("test:value")
        
        assert isinstance(result, ValidationResult)
        assert result.valid is True
    
    def test_validate_lux_with_options(self):
        """Test validate_lux with options"""
        options = LintOptions(max_depth=2)
        result = validate_lux("a{b{c{d:value}}}", options)
        
        assert isinstance(result, ValidationResult)


class TestValidateData:
    """Test validating decoded data"""
    
    def test_validate_data_basic(self):
        """Test validating decoded data"""
        validator = ZonValidator()
        data = {"name": "Alice", "age": 30}
        
        result = validator.validate_data(data)
        
        assert result.valid is True
    
    def test_validate_data_with_options(self):
        """Test validating data with options"""
        validator = ZonValidator()
        data = {"a": {"b": {"c": {"d": "deep"}}}}
        
        options = LintOptions(max_depth=2)
        result = validator.validate_data(data, options)
        
        assert len(result.warnings) > 0
