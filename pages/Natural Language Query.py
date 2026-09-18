from encoding_dsv4 import encode_messages
import transformers

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is 2+2?"},
]
prompt = encode_messages(messages, thinking_mode="thinking")

tokenizer = transformers.AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V4-Pro")
tokens = tokenizer.encode(prompt)
print(tokens)