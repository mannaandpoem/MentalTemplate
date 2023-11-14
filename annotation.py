# 标注数据
# 1. 读取数据
# 2. 定义prompt template
# 3. 标注数据
# 4. 去除标注数据中的错误行
# 5. 保存标注数据
# 6. for循环遍历所有文件

from openai import OpenAI
import os

from prompt_template import system_prompt_template, mental_template, new_mental_template
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'
os.environ["OPENAI_PROXY"] = "http://127.0.0.1:7890"
# os.environ['OPENAI_API_KEY'] = "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"
# os.environ['OPENAI_API_KEY'] = "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"
# os.environ['OPENAI_API_KEY'] = "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"
# os.environ['OPENAI_API_KEY'] = "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"
os.environ['OPENAI_API_KEY'] = "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"

client = OpenAI()


@retry(wait=wait_random_exponential(min=40, max=60), stop=stop_after_attempt(6))
def get_completion(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt_template},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )
    print(completion.usage.total_tokens)
    return completion.choices[0].message.content


# 使用gpt标注数据
def first_annotate(dir_path, file_name, tokens):
    filepath = os.path.join(dir_path, file_name)
    dialogues = split_dialogue(filepath, tokens)

    responses = []
    for i, dialogue in enumerate(dialogues):
        if i == 0:
            prompt = mental_template.format(dialogue=dialogue)
        else:
            if "no update require" in responses[-1].lower():
                response = get_rsp_from_responses(responses)

            prompt = new_mental_template.format(template=response, dialogue=dialogue)

        prompt = "All conversations are within the same psychological consultation, so keep the contents of the psychological template in mind. \n\n" + prompt
        response = get_completion(prompt)
        print(response)
        responses.append(response)

    annotate_filepath = os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name)
    with open(annotate_filepath, 'w', encoding='utf-8') as f:
        f.write("\n||\n".join(responses))

    return responses[-1]


def split_dialogue(filepath, tokens):
    # 读取数据
    with open(filepath, 'r', encoding='utf-8') as f:
        dialogue = f.read().split('\n')
        dialogues = []
        text = ''
        for line in dialogue:
            # 添加后字符数小于4000才添加
            if len(text + line) < tokens:
                text += line + '\n'
            else:
                dialogues.append(text)
                text = ''
        # 最后一段
        dialogues.append(text)
    return dialogues


def get_rsp_from_responses(responses: list):
    # 从后往前找不包含“No update required”的元素
    for rsp in reversed(responses):
        if "no update required" not in rsp.lower():
            return rsp

    return None


def process_one_file(dir_path, file_name, rsp, tokens):
    # 处理单个文件
    filepath = os.path.join(dir_path, file_name)
    # split
    dialogues = split_dialogue(filepath, tokens)
    # 处理每个切片
    responses = [rsp]
    for i, dialogue in enumerate(dialogues):
        if "no update require" in rsp.lower():
            rsp = get_rsp_from_responses(responses)
        prompt = new_mental_template.format(template=rsp, dialogue=dialogue)
        if i == 0:
            prompt = "These are different courses of psychotherapy for the same patient, so the contents of the psychological template must be kept in mind. \n\n" + prompt
        else:
            prompt = "All conversations are within the same psychological consultation, so keep the contents of the psychological template in mind. \n\n" + prompt
        rsp = get_completion(prompt)
        print(rsp)
        responses.append(rsp)
    return responses


def annotate_cbt(dir_path, tokens):
    # 第一个文件的第一次需要特殊处理
    # 读取第一个文件
    file_name = os.listdir(dir_path)[0]
    if not os.path.exists(os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name)):
        rsp = first_annotate(dir_path, file_name, tokens)
    else:
        with open(os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name), "r", encoding="utf-8") as f:
            rsp = f.read().split("||")[-1]

    # for循环遍历 dir_path 下所有文件
    for file_name in os.listdir(dir_path)[1:]:
        if not os.path.exists(os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name)):
            responses = process_one_file(dir_path, file_name, rsp)
            # 保存单个文件的标注数据
            annotate_filepath = os.path.join(dir_path + "_ANNOTATE", 'annotate_' + file_name)
            with open(annotate_filepath, 'w', encoding='utf-8') as f:
                f.write("\n||\n".join(responses))

            print(file_name + '处理完成')
        else:
            with open(os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name), "r", encoding="utf-8") as f:
                rsp = f.read().split("||")[-1]

    print("所有文件处理完成")


if __name__ == '__main__':
    # 文件路径
    dir_path = r'C:\Users\ASUS\PycharmProjects\mental_template\data\process_CBT\Self-Perceptions'
    annotate_cbt(dir_path, 7000)
