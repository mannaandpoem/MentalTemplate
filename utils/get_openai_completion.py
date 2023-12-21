import os
import random

import openai
from openai import OpenAI

# os.environ['http_proxy'] = 'http://localhost:7890'
# os.environ['https_proxy'] = 'http://localhost:7890'
# os.environ["OPENAI_PROXY"] = "http://127.0.0.1:7890"
#
# api_keys = ["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",
#             "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",
#             "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",
#             "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",
#             "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",
#             "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",
#             "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",
#             "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",
#             "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"]  # 添加你的多个API密钥
#
#
# def get_random_key_and_ip():
#     api_key = random.choice(api_keys)
#     ip_address = "http://localhost:7890"
#     return api_key, ip_address


os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["AZURE_OPENAI_API_KEY"] = "..."

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]

azure = True

if azure:
    client = openai.AzureOpenAI(
        # OPENAI_API_TYPE: "eastus2"

        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2023-09-01-preview"
    )
else:
    client = OpenAI(api_key=api_key)


def get_openai_completion(prompt):
    if azure:
        model = "GPT-35-TURBO-16K"
    else:
        model = "gpt-3.5-turbo-1106"
    completion = client.chat.completions.create(
        # model="GPT-4",
        # model="GPT-35-TURBO-16K",
        # model="gpt-3.5-turbo-1106",
        model=model,
        messages=[
            {"role": "system",
             "content": "You are a assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message)
    return completion.choices[0].message.content


if __name__ == '__main__':
    text = """hello
    """
    print(get_openai_completion(text))
    print()