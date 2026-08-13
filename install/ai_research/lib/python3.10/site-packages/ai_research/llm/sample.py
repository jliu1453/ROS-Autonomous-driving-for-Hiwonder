from huggingface_hub import InferenceClient

messages = [{"role": "user", "content": "What is the Transformers library known for?"}]
client = InferenceClient("http://192.168.12.122:8000")

result = client.chat_completion(messages, model="Qwen/Qwen2.5-0.5B-Instruct", max_tokens=256)
print(result.choices[0].message.content)
