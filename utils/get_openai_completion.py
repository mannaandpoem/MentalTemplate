import os
import random

import openai
from openai import OpenAI

# 可能要使用代理，不需要则注释
os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'
os.environ["OPENAI_PROXY"] = "http://localhost:7890"

# 使用OpenAI
# api_keys 已过期
API_KEYS = [
    "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",
    # "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",
    # "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",
    # "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",
    # "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",
    # "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",
    # "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",
    # "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",
    # "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"
]  # 添加你的多个API密钥


def get_random_key():
    return random.choice(API_KEYS)


api_key = get_random_key()
base_url = "https://api.openai-forward.com/v1"
client = OpenAI(api_key=api_key, base_url=base_url)


def get_openai_completion(user_prompt, system_prompt="You are a assistant."):
    completion = client.chat.completions.create(
        # model="gpt-4",
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message


if __name__ == '__main__':
    text = "hello"
    print(get_openai_completion(text).content)

    # 使用Azure
    # endpoint = "https://deepwisdom.openai.azure.com/"
    # api_key = "02ae6058d09849c691176befeae2107c"
    # azure = True
    #
    # client = openai.AzureOpenAI(
    #     azure_endpoint=endpoint,
    #     api_key=api_key,
    #     api_version="2023-07-01-preview"
    # )
