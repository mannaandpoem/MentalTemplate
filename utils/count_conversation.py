import os


# count number of dialogues in a conversation

def count_dialogues(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        count = 0
        dialogues = f.readlines()
        for dialogue in dialogues:
            if dialogue != '\n':
                count += 1

        return count


if __name__ == '__main__':
    dataset_name = ["APA_CBT", "Culturally_Responsive_CBT_Strengths_and_Wellness", "Culturally_Responsive_CBT", "Self-Perceptions"]

    for name in dataset_name:
        dir_path = r'C:\Users\ASUS\PycharmProjects\mental_template\data\process_CBT_finish\{}'.format(name)
        # count number of conversations in a file
        all_count = 0
        i = 0
        for file in os.listdir(dir_path):
            filepath = os.path.join(dir_path, file)
            number = count_dialogues(filepath)
            all_count += number
            i += 1

        print(i)
        print(all_count)
        print(all_count / 2)
        print("===")

