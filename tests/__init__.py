"""Tests for did:peer:4."""
from pathlib import Path


def examples():
    """Load json from examples directory and return generator over examples."""
    examples_dir = Path(__file__).parent / "examples"
    yield from examples_dir.glob("*.json")


EXAMPLES = list(examples())
