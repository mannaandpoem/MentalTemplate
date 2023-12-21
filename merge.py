
# 将一个目录下的所有的json文件合并为一个json文件
import json
import os

dir_path = r'C:\Users\ASUS\PycharmProjects\mental_template\data\CBT'

all_data = []
for dir in os.listdir(dir_path):
    # 如果以ANNOTATE结尾，则加入
    if "ANNOTATE" in os.path.join(dir_path, dir):
        path = os.path.join(dir_path, dir)
    else:
        continue

    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_data.extend(data)

# 对all_data增加 instruction 和 history 两个字段
# instruction 在最前面
for i, data in enumerate(all_data):
    all_data[i]["instruction"] = "In your capacity as a psychological counselor, you are tasked with processing both the patient's conversational input and the existing psychological record board. Your responsibility involves generating the patient's response and updating the psychological record board accordingly."
    all_data[i]["history"] = ""


filepath = os.path.join(dir_path, "CBT_data.json")
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print(len(all_data))



