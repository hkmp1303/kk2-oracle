from app.chain.steps import LLMRunner, PromptBuilder, ResponseParser
from app.schemas import AIResp, GenPrompt

class Pipeline():

    @staticmethod
    def run(question: str) -> str:
        pipeline = PromptBuilder() | LLMRunner() | ResponseParser.parse
        return pipeline.invoke(GenPrompt(q=question))
