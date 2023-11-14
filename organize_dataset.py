import json
import os

from annotation import split_dialogue
from prompt_template import mental_template, new_mental_template, system_prompt_template


# 构建数据集
# 1. 读取 process_CBT\APA_CBT 和 process_CBT\APA_CBT_ANNOATE 下的文件内容，组织input和output，构建数据集
# 2. 保存数据集

def organize_dataset(dir_path, tokens):
    # 读取 process_CBT\APA_CBT 和 process_CBT\APA_CBT_ANNOATE
    # 第一个文件特殊处理
    filepath = os.path.join(dir_path, os.listdir(dir_path)[0])
    annotation_filepath = os.path.join(dir_path + "_ANNOTATE", 'annotate_' + os.listdir(dir_path)[0])

    # split dialogue
    dialogues = split_dialogue(filepath, tokens)

    with open(annotation_filepath, "r", encoding="utf-8") as f:
        responses = f.read().split("||")

    # 使用字典组织input和output，构建数据集
    dataset = []
    system_prompt = system_prompt_template
    for i, dialogue in enumerate(dialogues):
        if i == 0:
            input = mental_template.format(dialogue=dialogue)
            output = responses[i]
        else:
            system_prompt += "All conversations are within the same psychological consultation, so keep the contents of the psychological template in mind."
            input = new_mental_template.format(template=output, dialogue=dialogue)
            output = responses[i]

        dataset.append({"system_prompt": system_prompt, "input": input, "output": output})

    # 处理后续文件
    for file in os.listdir(dir_path)[1:]:
        filepath = os.path.join(dir_path, file)
        annotation_filepath = os.path.join(dir_path + "_ANNOTATE", 'annotate_' + file)

        # split dialogue
        dialogues = split_dialogue(filepath, tokens)

        with open(annotation_filepath, "r", encoding="utf-8") as f:
            responses = f.read().split("||")

        # 使用字典组织input和output，构建数据集
        for i, dialogue in enumerate(dialogues):
            if i == 0:
                system_prompt += "These are different courses of psychotherapy for the same patient, so the contents of the psychological template must be kept in mind. "
            else:
                system_prompt += "All conversations are within the same psychological consultation, so keep the contents of the psychological template in mind. "
            input = new_mental_template.format(template=output, dialogue=dialogue)
            print(input)
            output = responses[i]

            dataset.append({"system_prompt": system_prompt, "input": input, "output": output})
    return dataset

if __name__ == '__main__':
    # 构建数据集
    # 1. 读取 process_CBT\APA_CBT 和 process_CBT\APA_CBT_ANNOATE 下的文件内容，组织input和output，构建数据集
    # 2. 保存数据集
    dir_path = r"C:\Users\ASUS\PycharmProjects\mental_template\data\process_CBT\Strengths_and_Wellness"
    dataset = organize_dataset(dir_path, 8000)
    print(dataset)
    print(len(dataset))
    # 保存数据集
    json_path = dir_path + ".json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
