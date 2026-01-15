"""LangChain output parser integration for LUX format."""

import re
from typing import Any, Optional, TypeVar
from lux import decode

T = TypeVar("T")

try:
    from langchain_core.output_parsers import BaseOutputParser
except ImportError:
    class BaseOutputParser:
        pass

class ZonOutputParser(BaseOutputParser):
    """LangChain output parser for LUX format responses.
    
    Parses LLM output in LUX format and provides format instructions
    for prompting the model.
    """
    
    def get_format_instructions(self) -> str:
        """Get instructions for formatting output as LUX.
        
        Returns:
            Format instructions string for LLM prompts
        """
        return """Your response must be formatted as LUX (Lightweight Ultra-compressed Xchange).
LUX is a compact format for structured data.
Rules:
1. Use 'key:value' for properties.
2. Use 'key{...}' for nested objects.
3. Use 'key[...]' for arrays.
4. Use '@(N):col1,col2' for tables.
5. Use 'T'/'F' for booleans, 'null' for null.

Example:
user{name:Alice,role:admin}
items:@(2):id,name
1,Item A
2,Item B
"""

    def parse(self, text: str) -> Any:
        """Parse LLM output text as LUX format.
        
        Automatically removes markdown code blocks if present.
        
        Args:
            text: LLM output string
            
        Returns:
            Parsed Python data structure
            
        Raises:
            ValueError: If parsing fails
        """
        try:
            cleaned = re.sub(r'```(lux|luxf)?', '', text).strip()
            cleaned = cleaned.replace('```', '').strip()
            return decode(cleaned)
        except Exception as e:
            raise ValueError(f"Failed to parse LUX output: {str(e)}")

    @property
    def _type(self) -> str:
        """Return parser type identifier."""
        return "lux_output_parser"
