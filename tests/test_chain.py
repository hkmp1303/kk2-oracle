
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from app.chain.runnable import RunnableLambda
from app.chain.steps import (
    PromptBuilder,
    LLMRunner,
    ResponseParser
)
from app.schemas import (
    GenPrompt,
    GeneratedPrompt,
    LLMOutput
)
from app.data import Data

# Tests for chain module components (PromptBuilder + LLMRunner)
# Transformers are mocked, but data state is managed via fixtures

@pytest.fixture(autouse=True)
def clean_data():
    # Setup data for testing
    Data(pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]}))
    yield
    # Teardown test data
    Data.clear()


class TestPromptBuilder():
    # Verify PromptBuilder logic with fresh data for every test

    def test_promptbuilder_generates_correct_format(_):

        builder = PromptBuilder()
        gen_prompt = GenPrompt(q="What is the average of col1?", prefix_prompt="Analyze:")
        generated = builder.invoke(gen_prompt)

        # Verify components are injected into the prompt
        assert "Analyze:" in generated.prompt
        assert "What is the average of col1?" in generated.prompt


class TestLLMRunner():
    # Verify LLMRunner logic using mocks to ensure repeatability

    @patch("app.chain.steps.pipeline")
    def test_llm_runner_invokes_correctly(_, mock_pipeline):
        mock_gen = MagicMock()
        mock_gen.return_value = [{"generated_text": "It is 1.5"}]
        mock_pipeline.return_value = mock_gen

        runner = LLMRunner()
        prompt = GeneratedPrompt(prompt="test prompt", dataset_batch="{}")
        result = runner.invoke(prompt)

        # Verify the pipeline was called once correctly
        mock_gen.assert_called_once()
        assert isinstance(result, LLMOutput)
        assert "It is 1.5" in result.response[0]["generated_text"]


class TestResponseParser():
    # Verify ResponseParser logic for valid and edge cases

    def test_parse_valid_output(_):
        mock_out = LLMOutput(response=[{"generated_text": "Final Answer"}])
        result = ResponseParser.parse(mock_out)
        assert result == "Final Answer"

    def test_parse_missing_field(_):
        # Test behavior when the expected 'generated_text' key is absent
        mock_out = LLMOutput(response=[{"other_field": "some data"}])
        result = ResponseParser.parse(mock_out)
        assert result == "error"


class TestRunnableAbstractions():
    # Verify the Runnable and Sequence chaining logic

    def test_runnable_lambda_execution(_):
        func = lambda x: x + 1
        r = RunnableLambda(func=func)
        assert r.invoke(5) == 6


    def test_runnable_sequence_chaining(_):
        # Verify the | operator correctly chains logic steps
        r1 = RunnableLambda(func=lambda x: str(x))
        r2 = RunnableLambda(func=lambda x: x + "_processed")

        chain = r1 | r2
        assert chain.invoke(5) == "5_processed"
