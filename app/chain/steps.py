import logging
import threading
import torch
from app.chain.runnable import Runnable, RunnableSequence
from app.data import Data
from app.schemas import AIResp, GenPrompt, GeneratedPrompt, LLMOutput
from logging import getLogger
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, logging as tf_log

info = logging.info
model_id = "HuggingFaceTB/SmolLM2-135M-Instruct"
#device_map = "auto"
device_map = {"": "cpu"}

tokenizer = None
model = None
lock = threading.Lock()
log = getLogger(__name__)

def model_name() -> str:
    global model_id
    return model_id

def model_loaded() -> bool:
    global model
    return False if model is None else True

def load_model() -> None:
    global tokenizer, model
    log("Loading model")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    #tf_log.set_verbosity_debug()
    #tf_log.enable_default_handler()
    #tf_log.enable_explicit_format()
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
        batch = Data.desc()
        columns = Data.getShape()[0]
        rows = Data.getShape()[1]
        return GeneratedPrompt(prompt=f"""
{gen_prompt.prefix_prompt}

Dataset columns:
{columns}

Dataset rows:
{rows}

Dataset statistics:
{batch}

User question:
{gen_prompt.q}

Respond with one factual answer that is under 30 words.
Answer using only the dataset statistics provided.
Give only the answer.
If the answer cannot be determined from the dataset statistics, reply with "I don't know based on the provided data."
Do not repeat the question.
Do not invent new questions.
Do not explain unless explicitly asked.
""")
        # return GeneratedPrompt(user_prompt=gen_prompt.prefix_prompt, system_prompt=gen_prompt.q, dataset_batch=batch)

class LLMRunner(Runnable[GeneratedPrompt, LLMOutput]):
    name: str = "llm_runner"
    def invoke(self, gen_prompt: GeneratedPrompt) -> LLMOutput:
        global model, tokenizer, info
        gen = pipeline("text-generation", model=model, tokenizer=tokenizer)
        # [
        #    {"role": "context", "content": gen_promp.dataset_batch},
        #    {"role": "system", "content": gen_prompt.system_prompt},
        #    {"role": "user", "content": gen_prompt.user_prompt},
        # ]
        response = gen(text_inputs=gen_prompt.prompt, return_full_text=False, max_new_tokens=256, clean_up_tokenization_spaces=False, temperature=0.2)
        print("resp len: %d " % len(response))
        #for line in response:
        #    for k, v in line.items():
        #        print(f"{k}: {v}")
        return LLMOutput(response=response)

class ResponseParser():
    @staticmethod
    def parse(llm_output: LLMOutput) -> str:
        out = llm_output.response[0]["generated_text"] if len(llm_output.response) > 0 and "generated_text" in llm_output.response[0] else "error"
        return out
