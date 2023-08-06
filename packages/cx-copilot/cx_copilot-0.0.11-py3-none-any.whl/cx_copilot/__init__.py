"""Python Package Template"""
from __future__ import annotations

from .blocks.cache import RedisCache
from .blocks.completion import GPTCompletionBlock
from .blocks.embedding import OpenAIEmbeddingBlock
from .blocks.tickets import FrontConversationRepository
from .blocks.vectordb import PineconeVectorDBBlock
from .compound.compound import CXCopilot
from .utils.eval import TestExample, TestPipeline
from .utils.eval_two_pipelines import TestABPipelines

__version__ = "0.0.11"
