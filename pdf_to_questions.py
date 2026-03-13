import pdfplumber
import json
import re

# =========================
# PDF 檔案名稱
# =========================

PDF_FILE = "boat_exam.pdf"

# =========================
# 解析 PDF
# =========================

def extract_text():

    print("解析 PDF...")

    text = ""

    with pdfplumber.open(PDF_FILE) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# =========================
# 抽取題目
# =========================

def parse_questions(text):

    print("解析題目...")

    questions = []

    # 用數字分割題目
    blocks = re.split(r"\n\d+\.", text)

    for b in blocks:

        lines = b.strip().split("\n")

        if len(lines) < 5:
            continue

        question = lines[0]

        options = []

        for i in range(1,5):

            options.append(lines[i].strip())

        questions.append({
            "q": question,
            "a": options,
            "c": 0
        })

    return questions


# =========================
# 存 JSON
# =========================

def save_json(data):

    with open("questions.json","w",encoding="utf-8") as f:

        json.dump(data,f,ensure_ascii=False,indent=2)

    print("questions.json 已生成")


# =========================
# 主程式
# =========================

def main():

    text = extract_text()

    questions = parse_questions(text)

    save_json(questions)

    print("題目數量:",len(questions))


if __name__ == "__main__":

    main()