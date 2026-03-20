import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

model="qwen3-30b-a3b-instruct-2507"
#model="openai-gpt-oss-120b"


api_key=os.getenv("GWDG_API_KEY")
base_url=os.getenv("GWDG_API_BASE")


client = AsyncOpenAI(api_key=api_key,
            base_url=base_url)


#-------------------------
# LLM INTERFACE
#-------------------------

async def generate_text_from_context(prompt: str) -> dict:
  """
  Generate text from an explicit model context.
  Returns a dict with 'text' and 'token_usage' keys.
  """
  
  if not prompt.strip():
    raise ValueError("Prompt must not be empty.")
  
  response = await client.chat.completions.create(
    messages=[
      {"role": "system", "content": prompt},
    ],
    temperature=0.4,
    model= model
  )

  token_usage = None
  if response.usage:
    token_usage = {
      "prompt_tokens": response.usage.prompt_tokens,
      "completion_tokens": response.usage.completion_tokens,
      "total_tokens": response.usage.total_tokens,
    }

  return {
    "text": response.choices[0].message.content,
    "token_usage": token_usage,
  }
