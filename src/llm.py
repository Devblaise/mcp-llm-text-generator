import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

model="qwen3-30b-a3b-instruct-2507"
#model="gpt-5-nano"

#api_key=os.getenv("OPENAI_API_KEY")
api_key=os.getenv("LLM_API_KEY")
base_url=os.getenv("LLM_BASE_URL")


client = AsyncOpenAI(api_key=api_key,
            base_url=base_url)

# client = AsyncOpenAI(api_key=api_key)

#-------------------------
# LLM INTERFACE
#-------------------------

async def generate_text_from_context(prompt: str) -> str:
  """
  Generate text from an explicit model context.
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
  return response.choices[0].message.content
