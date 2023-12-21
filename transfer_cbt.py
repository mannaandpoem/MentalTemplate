import os
import re

import os
from docx import Document

def has_chinese(line):
    # Function to check if a line contains Chinese characters
    return any('\u4e00' <= char <= '\u9fff' for char in line)

def has_english(line):
    # Function to check if a line contains English words using a regular expression
    # This example considers a line to have English characters if it contains at least one English word
    english_pattern = re.compile(r'\b[a-zA-Z]+\b')
    return bool(english_pattern.search(line))


def remove_timestamp(line):
    # Function to remove timestamp from a line
    # Assumes the timestamp is in the format "00:00" at the beginning of the line
    timestamp_pattern = re.compile(r'^\d{2}:\d{2}')
    return re.sub(timestamp_pattern, '', line).strip()


def docx_to_txt(dir_path, docx_file):
    # Open the docx file
    doc_path = os.path.join(dir_path, docx_file)
    doc = Document(doc_path)

    # Create a new list to store lines with English characters
    new_lines = []

    # Iterate through paragraphs in the document
    for paragraph in doc.paragraphs:
        # Split the paragraph into lines and check each line
        for line in paragraph.text.split('\n'):
            # Check if the line contains English characters
            # if has_english(line):
            if not has_chinese(line):
                # Remove timestamp from the line
                line = remove_timestamp(line)
                # 对每一行检测是否存在" " (non-breaking space)，第一个替换为": "，其他替换为" " (breaking space)
                line = line.replace(" ", ": ", 1).replace(" ", " ")
                # Add the line to the new list
                new_lines.append(line)

    # Save the filtered content into a new text file
    name = os.path.splitext(docx_file)[0]
    # new_path = "C:\\Users\\ASUS\\PycharmProjects\\mental_template\\data\\process_CBT\\new_" + name + ".txt"
    new_path = "C:\\Users\\ASUS\\PycharmProjects\\mental_template\\data\\CBT\\new_" + name + ".txt"
    # txt_path = os.path.join(dir_path, f"new_{name}.txt")
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))


if __name__ == '__main__':
    # 文件路径
    # dir_path = r'C:\Users\ASUS\PycharmProjects\mental_template\data\大模型 CBT 预处理'
    # # for循环遍历 dir_path 下所有文件
    # for file_name in os.listdir(dir_path):
    #     # 判断文件是否为docx文件
    #     if file_name.endswith('.docx'):
    #         # 调用 transfer_cbt 函数
    #         docx_to_txt(dir_path, file_name)
    #         print(file_name + '处理完成')

    filepath = r'C:\Users\ASUS\PycharmProjects\mental_template'
    docx_to_txt(filepath, '1706.03762.docx')

