from app.chain.runnable import Runnable, RunnableSequence
from app.schemas import AIResp, GenPrompt, GeneratedPrompt, LLMOutput
import threading
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "HuggingFaceTB/SmolLM2-135M-Instruct"
#device_map = "auto"
device_map = {"": "cpu"}

tokenizer = None
model = None
lock = threading.Lock()

def model_name() -> str:
    global model_id
    return model_id

def model_loaded() -> bool:
    global model
    return False if model is None else True

def load_model() -> None:
    global tokenizer, model
    print("Loading model")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map=device_map,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
def unload_model() -> None:
    global tokenizer, model
    tokenizer = model = None

class PromptBuilder(Runnable[GenPrompt, GeneratedPrompt]):
    name: str = "prompt_builder"
    def invoke(self, gen_prompt: GenPrompt) -> GeneratedPrompt:
        return GeneratedPrompt(prompt=gen_prompt.q)

class LLMRunner(Runnable[GeneratedPrompt, LLMOutput]):
    name: str = "llm_runner"
    def invoke(self, gen_prompt: GeneratedPrompt) -> LLMOutput:
        global model, tokenizer
        gen = pipeline("text-generation", model=model, tokenizer=tokenizer)
        return LLMOutput(response=gen(gen_prompt.prompt))

class ResponseParser():
    @staticmethod
    def parse(llm_output: LLMOutput) -> str:
        return llm_output.response[0]["generated_text"]
