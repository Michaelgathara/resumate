from openai import OpenAI
client = OpenAI()

MODEL = "gpt-3.5-turbo"


def call_gpt(system_prompt: str, prompt: str, model: str):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return completion


print(call_gpt("You are a programmer",
      "Write a program", MODEL).choices[0].message)
