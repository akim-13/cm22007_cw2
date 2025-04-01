from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

if __name__ == "__main__":
    completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "user", "content": "Hi can you explain to me how caching works in computers"}
            ],
            response_format={"type": "json_object"},
        )
    print(completion)
    response = completion.choices[0].message.content
    print(response)