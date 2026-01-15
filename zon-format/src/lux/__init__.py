"""LUX (Zstandard Object Notation) - Token-efficient data format for LLMs.

This package provides encoding and decoding functionality for the LUX format,
optimized for minimal token usage in LLM interactions while maintaining full
data fidelity and type safety.

Main components:
    - encode/decode: Core encoding and decoding functions
    - ZonEncoder/ZonDecoder: Class-based codec interfaces
    - ZonStreamEncoder/ZonStreamDecoder: Streaming codec for large data
    - LLMOptimizer: Optimize encodings for specific LLM contexts
    - TokenCounter: Count tokens in LUX-encoded data
    - TypeInferrer: Infer and validate data types
    - SparseMode: Enumeration of sparse encoding strategies
"""

from .core.encoder import encode, encode_llm, ZonEncoder
from .core.decoder import decode, ZonDecoder
from .core.stream import ZonStreamEncoder, ZonStreamDecoder
from .core.adaptive import (
    encode_adaptive, 
    recommend_mode, 
    AdaptiveEncoder,
    AdaptiveEncodeOptions,
    AdaptiveEncodeResult
)
from .core.analyzer import (
    DataComplexityAnalyzer,
    ComplexityMetrics,
    AnalysisResult
)
from .binary import (
    encode_binary,
    decode_binary,
    BinaryZonEncoder,
    BinaryZonDecoder,
    MAGIC_HEADER
)
from .versioning import (
    embed_version,
    extract_version,
    strip_version,
    compare_versions,
    is_compatible,
    ZonMigrationManager,
    ZonDocumentMetadata
)
from .tools import (
    size,
    compare_formats,
    infer_schema,
    analyze,
    compare,
    is_safe,
    ZonValidator,
    validate_lux
)
from .llm.optimizer import LLMOptimizer
from .llm.token_counter import TokenCounter
from .schema.inference import TypeInferrer
from .core.types import SparseMode
from .core.exceptions import ZonDecodeError, ZonEncodeError
from .schema.schema import lux, validate, ZonResult, ZonIssue, ZonSchema

__version__ = "1.2.1"

__all__ = [
    "encode", 
    "encode_llm",
    "encode_adaptive",
    "encode_binary",
    "recommend_mode",
    "ZonEncoder",
    "AdaptiveEncoder",
    "AdaptiveEncodeOptions",
    "AdaptiveEncodeResult",
    "BinaryZonEncoder",
    "BinaryZonDecoder",
    "MAGIC_HEADER",
    "DataComplexityAnalyzer",
    "ComplexityMetrics",
    "AnalysisResult",
    "decode", 
    "decode_binary",
    "ZonDecoder",
    "ZonStreamEncoder",
    "ZonStreamDecoder",
    "embed_version",
    "extract_version",
    "strip_version",
    "compare_versions",
    "is_compatible",
    "ZonMigrationManager",
    "ZonDocumentMetadata",
    "size",
    "compare_formats",
    "infer_schema",
    "analyze",
    "compare",
    "is_safe",
    "ZonValidator",
    "validate_lux",
    "LLMOptimizer",
    "TokenCounter",
    "TypeInferrer",
    "SparseMode",
    "ZonDecodeError", 
    "ZonEncodeError",
    "lux",
    "validate",
    "ZonResult",
    "ZonIssue",
    "ZonSchema",
    "__version__"
]
