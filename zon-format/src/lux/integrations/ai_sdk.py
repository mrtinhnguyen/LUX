"""AI SDK integration for LUX format streaming."""

from typing import AsyncGenerator, Any, AsyncIterable
from ..core.stream import ZonStreamDecoder

async def parse_lux_stream(stream: AsyncIterable[str]) -> AsyncGenerator[Any, None]:
    """Parse a stream of LUX text from an LLM into objects.
    
    Args:
        stream: Async iterable yielding LUX text chunks
        
    Yields:
        Parsed objects as they become available
    """
    decoder = ZonStreamDecoder()
    async for item in decoder.decode(stream):
        yield item
