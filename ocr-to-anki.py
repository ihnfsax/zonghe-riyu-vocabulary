import csv
import re


input_list = ["2-1 新出単語", "2-1 練習用単語"]
output = "2-1"


def find_number(text):
    pattern = r"[⓪①②③④⑤⑥⑦⑧⑨]"
    matches = list(re.finditer(pattern, text))
    if not matches:
        return ""
    if len(matches) == 1:
        return matches[0].group()
    first_pos = matches[0].start()
    last_pos = matches[-1].end()
    return text[first_pos:last_pos]


def extract_chinese_bracket(text):
    pattern = r"（(.*?)）"
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def handle_csv_file(input_file, tags):
    print('读取文件"' + input_file + '"...')
    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        words = list(reader)
        col0 = ""
        col1 = ""
        result = []

        for word in words:
            # 抽取单词部分
            match = re.match(r"^([^（⓪①②③④⑤⑥⑦⑧⑨]*)", word[0])
            if match:
                col0 = match.group(1)
            else:
                print("警告：单词“" + word[0] + "”无法抽取单词部分")
            # 抽取发音部分
            col1 = extract_chinese_bracket(word[0])
            number = find_number(word[0])
            if len(col1) == 0:  # 如果没有中文括号
                match = re.match(r"^([^〖⓪①②③④⑤⑥⑦⑧⑨]*)", word[0])
                if match:
                    col1 = match.group(1)
                else:
                    print("警告：单词“" + word[0] + "”无法抽取发音部分")
            if len(number) > 0:
                col1 += " " + number
            word[0] = col0.strip()
            word.insert(1, col1.strip())
            word[2] = word[2].replace("<", "&lt;")
            word[2] = word[2].replace(">", "&gt;")
            word.append("")  # 例句
            word.append(tags)
            result.append(word)
        return result


if __name__ == "__main__":
    data = []
    for filename in input_list:
        res = handle_csv_file(filename + ".csv", filename)
        data += res
    print('结果写入文件"' + output + '.csv"...')
    with open(output + ".csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
