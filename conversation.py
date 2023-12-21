import os

import openai

from prompt.prompt_template import *


endpoint = "..."
api_key = "..."
azure = True

client = openai.AzureOpenAI(
    # OPENAI_API_TYPE: "eastus2"
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2023-07-01-preview"
)


def get_openai_completion(prompt, system="You are a assistant"):
    if azure:
        model = "GPT-4"
    else:
        model = "gpt-3.5-turbo-1106"
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.usage.completion_tokens)
    return completion.choices[0].message.content


def one_step_conversation(prompt):
    rsp = get_openai_completion(prompt, system_prompt_template)
    template_updated, assistant_msg = rsp.split("===")
    return template_updated, assistant_msg


# 进行对话
# input: system_msg + user_msg + template
# output: assistant_msg + template_updated
def conversation():
    user_msgs = ["I am a yolanada, hello",
                 "Uhm, that's been busy. Uhm, work my first full week last week, this is the second week and its only gonna get busier.",
                 "Like, like good busy or it's just... I'm anticipating that it-- it's gonna be stressful. I just wanna maintain my peace."]

    prompt = mental_template.format(dialogue=user_msgs[0], template=first_template, guide=guide_prompt,
                                    schema=template_schema)
    template_updated, assistant_msg = one_step_conversation(prompt)
    print(template_updated)
    print(assistant_msg)

    i = 1
    while True:
        # user_msg = input("User: ")
        user_msg = user_msgs[i]
        i += 1
        prompt = mental_template.format(dialogue=user_msg, template=template_updated, guide=guide_prompt,
                                        schema=template_schema)
        template_updated, assistant_msg = one_step_conversation(prompt)
        print(template_updated)
        print(assistant_msg)

        # 对输出的assistant_msg进行评分！输出是否通过（True or False）和评分。
        # 如果False，需要重写生成输出。
        # 如果True，则对patient和therapist的pair进行评分。
        prompt = "Patient: " + user_msg + "\nTherapist: " + assistant_msg
        rsp = get_openai_completion(prompt, system=score_system_template)
        print(rsp)


if __name__ == '__main__':
    conversation()
