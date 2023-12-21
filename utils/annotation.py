# 标注数据
# 1. 读取数据
# 2. 定义prompt template
# 3. 标注数据
# 4. 去除标注数据中的错误行
# 5. 保存标注数据
# 6. for循环遍历所有文件
import json
import random

from openai import OpenAI
import os

from prompt.prompt_template import system_prompt_template, mental_template, guide_prompt, \
    first_template, template_schema, summarize_template
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

LINE_NUMS = 15

os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'
os.environ["OPENAI_PROXY"] = "http://127.0.0.1:7890"

api_keys = ["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",
            "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",
            "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",
            "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",
            "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",
            "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",
            "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",
            "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",
            "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"]  # 添加你的多个API密钥

def get_random_key_and_ip():
    api_key = random.choice(api_keys)
    ip_address = "http://localhost:7890"
    return api_key, ip_address


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_completion(prompt):
    api_key = get_random_key_and_ip()[0]
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt_template},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    content = completion.choices[0].message.content
    print(completion.usage.prompt_tokens)
    print(completion.usage.completion_tokens)
    print(completion.usage.total_tokens)
    if completion.usage.completion_tokens > 1500:
        # 进行总结
        return summarize_completion(client, content)
    return content


def summarize_completion(client, content):
    prompt = summarize_template.template(schema=template_schema, template=content)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You will act as a professional CBT cognitive behavioral therapy psychologist. Your task is to summarize the content of the CBT Psychological Template attribute."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    print(completion.usage.completion_tokens)
    return completion.choices[0].message.content


# 使用gpt标注数据
def first_annotate(dir_path, file_name, doctor_name):
    filepath = os.path.join(dir_path, file_name)
    dialogues = split_dialogue(filepath, doctor_name, LINE_NUMS)

    responses = []
    pairs = []
    for i, dialogue in enumerate(dialogues):
        pairs_dict = {}
        if i == 0:
            prompt = mental_template.template(dialogue=dialogue, template=first_template, guide=guide_prompt, schema=template_schema)
        else:
            if "no update require" in responses[-1].lower():
                response = get_rsp_from_responses(responses)

            prompt = mental_template.template(template=response, dialogue=dialogue, guide=guide_prompt, schema=template_schema)

        # prompt = "All conversations are within the same psychological consultation, so keep the contents of the psychological template in mind. \n\n" + prompt
        response = get_completion(prompt)
        print(response)
        responses.append(response)
        pairs_dict["input"] = dialogue + "\n\n" + response
        pairs_dict["output"] = response
        pairs.append(pairs_dict)

    # 后缀变为.json
    annotate_filepath = os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name).replace(".txt", ".json")
    with open(annotate_filepath, 'w', encoding='utf-8') as f:
        # f.write("\n||\n".join(responses))
        json.dump(pairs, f, ensure_ascii=False, indent=4)

    return responses[-1]

def get_patient_name(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = "\n".join(f.readlines()[:10])

    prompt = text + "\nBased on the above text, output the words referring to patients. Only output the words:"
    patient_name = get_completion(prompt)
    return patient_name.strip().lower()

def get_doctor_name(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = "\n".join(f.readlines()[:10])

    prompt = text + "\nBased on the above text, output the name of the Consultant. Only output the name:"
    doctor_name = get_completion(prompt)
    return doctor_name.strip().lower()

def line_is_patient(doctor_name, line):
    if doctor_name not in line[:20]:
        return True
    else:
        return False


def split_dialogue(filepath, doctor_name, line_nums):
    # 读取数据
    with open(filepath, 'r', encoding='utf-8') as f:
        dialogue = f.read().lower().split('\n')
        # 窗口大小为10，当line_num >=10 且为患者发言时，则进行一次切分

    dialogues = []
    current_chunk = []

    nums = 0
    for line in dialogue:
        # Assuming patients' lines are identified by some criteria (you may need to modify this condition)
        is_patient_line = line_is_patient(doctor_name, line)

        if line != '':
            current_chunk.append(line)
        nums += 1

        if nums >= line_nums and is_patient_line:
            # Perform the split when line_num is greater than or equal to 10 and it's a patient's utterance
            dialogues.append('\n'.join(current_chunk))
            current_chunk = []  # Reset the chunk
            nums = 0

    # Add the remaining lines if any
    if current_chunk:
        dialogues.append('\n'.join(current_chunk))

    return dialogues


def get_rsp_from_responses(responses: list):
    # 从后往前找不包含“No update required”的元素
    for rsp in reversed(responses):
        if "no update required" not in rsp.lower():
            return rsp

    return None


def process_one_file(dir_path, file_name, rsp, doctor_name):
    # 处理单个文件
    filepath = os.path.join(dir_path, file_name)
    # split
    dialogues = split_dialogue(filepath, doctor_name, LINE_NUMS)
    # rsp = summarize_completion(OpenAI(api_key=get_random_key_and_ip()[0]), rsp)
    # 处理每个切片
    responses = [rsp]
    # 构建dialogue-response pairs_dict
    pairs = []
    for i, dialogue in enumerate(dialogues):
        pairs_dict = {}
        if "no update require" in rsp.lower():
            rsp = get_rsp_from_responses(responses)
        prompt = mental_template.template(template=rsp, dialogue=dialogue, guide=guide_prompt, schema=template_schema)
        # if i == 0:
        #     prompt = "These are different courses of psychotherapy for the same patient, so the contents of the psychological template must be kept in mind. \n\n" + prompt
        # else:
        #     prompt = "All conversations are within the same psychological consultation, so keep the contents of the psychological template in mind. \n\n" + prompt

        rsp = get_completion(prompt)
        print(rsp)
        responses.append(rsp)

        input = dialogue + "\n\n" + "context: \n" + responses[i]
        pairs_dict["input"] = input
        pairs_dict["output"] = rsp
        pairs.append(pairs_dict)

    return pairs, responses[-1]


def annotate_cbt(dir_path, summary=False):
    if summary:
        return summary_json(os.path.join(dir_path + "_ANNOTATE"))

    # 第一个文件的第一次需要特殊处理
    # 读取第一个文件
    file_name = os.listdir(dir_path)[0]
    # patient_name = get_patient_name(os.path.join(dir_path, file_name))
    doctor_name = get_doctor_name(os.path.join(dir_path, file_name))
    if not os.path.exists(os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name).replace(".txt", ".json")):
        rsp = first_annotate(dir_path, file_name, doctor_name)
    else:
        with open(os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name).replace(".txt", ".json"), "r", encoding="utf-8") as f:
            pairs = json.load(f)
            rsp = pairs[-1]["output"]

    # for循环遍历 dir_path 下所有文件
    for file_name in os.listdir(dir_path)[1:]:
        if not os.path.exists(os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name).replace(".txt", ".json")):
            pairs, rsp = process_one_file(dir_path, file_name, rsp, doctor_name)
            # 保存单个文件的标注数据
            annotate_filepath = os.path.join(dir_path + "_ANNOTATE", 'annotate_' + file_name).replace(".txt", ".json")
            with open(annotate_filepath, 'w', encoding='utf-8') as f:
                # 将pairs转换为json格式保存
                json.dump(pairs, f, ensure_ascii=False, indent=4)

            print(file_name + '处理完成')
        else:
            with open(os.path.join(dir_path + "_ANNOTATE", "annotate_" + file_name).replace(".txt", ".json"), "r", encoding="utf-8") as f:
                pairs = json.load(f)
                rsp = pairs[-1]["output"]
    print("所有文件处理完成")


def summary_json(dir_path):
    for file in os.listdir(dir_path):
        os.path.join(dir_path, "annotate_" + file).replace(".txt", ".json")
        if file.endswith(".json"):
            with open(os.path.join(dir_path, file), "r", encoding="utf-8") as f:
                # 读取json 的output字段，对其进行总结
                data = json.load(f)
                for i, pair in enumerate(data):
                    output = pair["output"]
                    if len(output) > 9000:
                        # 进行总结
                        rsp = summarize_completion(OpenAI(api_key=get_random_key_and_ip()[0]), output)
                        data[i]["output"] = rsp
                        print(rsp)
                        print("===")

            with open(os.path.join(dir_path, file), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(file + "处理完成")

    print("所有文件处理完成")


if __name__ == '__main__':
    # 文件路径
    dir_path = r'/data/CBT/Culturally_Responsive_CBT_Strengths_and_Wellness_ANNOTATE'
    annotate_cbt(dir_path)

    