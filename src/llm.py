import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

#model="openai-gpt-oss-120b"
model="gpt-5-nano"

api_key=os.getenv("OPENAI_API_KEY")
# base_url=os.getenv("base_url")


#client = OpenAI(api_key=api_key,
#               base_url=base_url)

client = OpenAI(api_key=api_key)
#-------------------------
# LLM INTERFACE
#-------------------------

def generate_text_from_context(prompt: str) -> str:
  """
  Generate text from an explicit model context.
  """
  
  if not prompt.strip():
    raise ValueError("Prompt must not be empty.")
  
  response = client.chat.completions.create(
    messages=[
      {"role": "system", "content": prompt},
    ],
   # temperature=0.4,
    model= model
  )  
  return response.choices[0].message.content
