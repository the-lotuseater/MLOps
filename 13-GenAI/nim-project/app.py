from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="meta/llama-3.1-70b-instruct",
  messages=[{"role":"user","content":"Write an article about soccer."}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices and chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")


