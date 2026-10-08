import argparse
import os
import re
from langchain_experimental.pal_chain import PALChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, ChatGeneration, ChatResult

parser = argparse.ArgumentParser(description="A simple script to accept user input via flags.")
# Add a command line argument for user input
parser.add_argument('--user_input', type=str, help='prompt')
parser.add_argument('--api_key', type=str, help='openai api key')
# Parse the command line arguments
args = parser.parse_args()
openaiapikey = args.api_key


def _strip_code_fences(text):
    """Remove markdown code fences (e.g. ```python ... ```) from LLM output."""
    if not text:
        return text
    stripped = re.sub(r"^\s*```[\w+-]*[ \t]*\r?\n?", "", text.strip())
    stripped = re.sub(r"\r?\n?```\s*$", "", stripped)
    return stripped.strip()


def _extract_code(text):
    """Extract raw Python code from a chat-model reply.

    Chat models may wrap code in markdown fences and/or surround it with
    prose. Take the first fenced block if present, otherwise strip any
    fences and surrounding whitespace so the PAL chain can parse the code.
    """
    if not text:
        return text
    match = re.search(r"```[\w+-]*[ \t]*\r?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return _strip_code_fences(text)


class PALChatOpenAI(ChatOpenAI):
    """ChatOpenAI adapted for the PAL chain on modern chat endpoints.

    Two tweaks versus plain ChatOpenAI:
    1. The PAL chain asks the API to stop at "\\n\\n" (so the model doesn't
       continue with more Q/A examples). Reasoning models such as GLM think
       in a hidden chain-of-thought before answering, and that stop sequence
       cuts the generation during reasoning, yielding an empty answer. Chat
       models end their turn on their own, so the stop sequence is dropped.
    2. The PAL chain parses the LLM output as raw Python code, but modern
       chat models tend to wrap code in ```python ... ``` blocks, sometimes
       with prose around it. The actual code is extracted from the reply.
    """

    def _generate(self, messages, stop=None, run_manager=None, stream=None, **kwargs):
        result = super()._generate(
            messages, stop=None, run_manager=run_manager, stream=stream, **kwargs
        )
        generations = []
        for generation in result.generations:
            message = generation.message
            if isinstance(message.content, str):
                stripped = _extract_code(message.content)
                if stripped != message.content:
                    message = message.copy(update={"content": stripped})
                    generation = ChatGeneration(
                        message=message,
                        generation_info=generation.generation_info,
                    )
            generations.append(generation)
        return ChatResult(generations=generations, llm_output=result.llm_output)


llm_options = {
    "temperature": 0,
    "openai_api_key": openaiapikey,
    "model_name": os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
}
if os.environ.get("OPENAI_BASE_URL"):
    llm_options["openai_api_base"] = os.environ["OPENAI_BASE_URL"]
llm = PALChatOpenAI(**llm_options)
pal_chain = PALChain.from_math_prompt(llm, verbose=True)

# Check if the 'user_input' flag is provided
try:
    if args.user_input:
        result = pal_chain.run(args.user_input)
        print(result)
        #print(f"User input: {args.user_input}")
    else:
        print("No user input provided.")
except Exception as e:
    print(f"Exception Occured: {type(e).__name__}: {e}")
