import json
import os

from annotation import split_dialogue
from prompt.prompt_template import mental_template, system_prompt_template


# 构建数据集
# 1. 读取 process_CBT\APA_CBT 和 process_CBT\APA_CBT_ANNOATE 下的文件内容，组织input和output，构建数据集
# 2. 保存数据集

def get_patient_name(responses):
    # 从response中获取病人姓名
    for response in responses:
        for line in response.split("\n"):
            if "name" in line.lower():
                return line.split(":")[1].strip().lower()
    return None


def get_therapist_name(responses, dialogues):
    patient_name = get_patient_name(responses)
    # 从response中获取治疗师姓名
    for dialogue in dialogues:
        try:
            if patient_name not in dialogue.lower()[:10]:
                # 异常处理
                therapist_name = dialogue.split(":")[0].strip().lower()
                return therapist_name
        except IndexError:
            continue

    return None


def organize_dataset(dir_path, patient_name):
    # 读取 process_CBT\APA_CBT 和 process_CBT\APA_CBT_ANNOATE
    # 第一个文件特殊处理
    filepath = os.path.join(dir_path, os.listdir(dir_path)[0])
    annotation_filepath = os.path.join(dir_path + "_ANNOTATE", 'annotate_' + os.listdir(dir_path)[0])

    # split dialogue
    dialogues = split_dialogue(filepath, patient_name)

    with open(annotation_filepath, "r", encoding="utf-8") as f:
        responses = f.read().split("||")

    # patient_name = get_patient_name(responses[0])
    therapist_name = get_therapist_name(responses, dialogues)

    # 使用字典组织input和output，构建数据集
    dataset = []
    instruction = system_prompt_template

    # 处理第一个文件
    for i, dialogue in enumerate(dialogues):
        response = responses[i]
        if i == 0:
            input = mental_template.template(dialogue=dialogue)
        else:
            input = mental_template.template(template=response, dialogue=dialogue)
            instruction += "All conversations are within the same psychological consultation, so keep the contents of the psychological template in mind."

        answer = "The therapist: "
        if i + 1 < len(dialogues):
            for sentence in dialogues[i + 1].split("\n"):
                if therapist_name in sentence.lower():
                    # 只剔除第一个patient_name的词语，后续的不剔除
                    # s = sentence.lower().replace(therapist_name+":", "", 1)
                    s = sentence.split(":")[1].strip().lower()
                    answer += s
                    break
        else:
            answer = "Conversation end."

        output = answer + "\n\n" + "The psychological template is: " + response
        history = ""
        dataset.append({"instruction": instruction, "input": input, "output": output, "history": history})

    # 处理后续文件
    for file in os.listdir(dir_path)[1:]:
        filepath = os.path.join(dir_path, file)
        annotation_filepath = os.path.join(dir_path + "_ANNOTATE", 'annotate_' + file)

        # split dialogue
        dialogues = split_dialogue(filepath, patient_name)

        with open(annotation_filepath, "r", encoding="utf-8") as f:
            responses = f.read().split("||")

        # 使用字典组织input和output，构建数据集
        for i, dialogue in enumerate(dialogues):
            response = responses[i]
            if i == 0:
                instruction += "These are different courses of psychotherapy for the same patient, so the contents of the psychological template must be kept in mind. "
            else:
                instruction += "All conversations are within the same psychological consultation, so keep the contents of the psychological template in mind. "

            input = mental_template.template(template=response, dialogue=dialogue)
            answer = "The therapist: "
            if i + 1 < len(dialogues):
                for sentence in dialogues[i + 1].split("\n"):
                    if therapist_name in sentence.lower():
                        # s = sentence.lower().replace(therapist_name+":", "", 1)
                        s = sentence.split(":")[1].strip().lower()
                        answer += s
                        break
            else:
                answer = "Conversation end."

            output = answer + "\n\n" + "The psychological template is: " + response
            history = ""
            dataset.append({"instruction": instruction, "input": input, "output": output, "history": history})
    return dataset


if __name__ == '__main__':
    # 构建数据集
    # 1. 读取 process_CBT\APA_CBT 和 process_CBT\APA_CBT_ANNOATE 下的文件内容，组织input和output，构建数据集
    # 2. 保存数据集
    # dataset_name = ["APA_CBT", "Culturally_Responsive_CBT_Strengths_and_Wellness"]        # 8000
    dataset_name = ["Culturally_Responsive_CBT", "Self-Perceptions"]  # 7000
    for name in dataset_name:
        # dir_path = r"C:\Users\ASUS\PycharmProjects\mental_template\data\process_CBT\{}".format(name)
        dir_path = r"C:\Users\ASUS\PycharmProjects\mental_template\data\CBT\{}".format(name)
        dataset = organize_dataset(dir_path, patient_name)
        print(dataset)
        print(len(dataset))
        # 保存数据集
        json_path = dir_path + ".json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)