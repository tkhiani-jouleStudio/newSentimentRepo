"""Tests for feedback input parsing logic."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest
from unittest.mock import MagicMock, patch, AsyncMock


@pytest.fixture
def agent():
    """Create a SampleAgent instance with mocked LLM."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer"), \
         patch("agent.SummarizationMiddleware"):
        from agent import SampleAgent
        return SampleAgent()


def test_parse_single_feedback_item(agent):
    """Single text input returns a single-item list."""
    result = agent._parse_feedback_input("The product is great!")
    assert result == ["The product is great!"]


def test_parse_json_array_input(agent):
    """JSON array input is parsed into multiple items."""
    import json
    items = ["Great product!", "Terrible service.", "It was okay."]
    result = agent._parse_feedback_input(json.dumps(items))
    assert result == items


def test_parse_empty_input_returns_empty_list(agent):
    """Empty input returns an empty list."""
    result = agent._parse_feedback_input("")
    assert result == []


def test_parse_whitespace_only_returns_empty_list(agent):
    """Whitespace-only input returns an empty list."""
    result = agent._parse_feedback_input("   ")
    assert result == []


def test_parse_invalid_json_treated_as_single_item(agent):
    """Input that looks like JSON but isn't is treated as a single item."""
    result = agent._parse_feedback_input("[not valid json")
    assert len(result) == 1
    assert "[not valid json" in result[0]
