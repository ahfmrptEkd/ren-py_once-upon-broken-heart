import re
import random
import renpy.exports as renpy

def check_affection(day, love_value):
    if day == 1 and love_value < 10: # 10
        return "random_bad_ending"
    elif day == 2 and love_value < 20: # 20
        return "random_bad_ending"
    elif day == 3 and love_value < 30: # 30
        return "random_bad_ending"
    else:
        return None  # 계속 진행

def read_and_format_endings(filename):
    with renpy.file(f"{filename}") as f:
        content = f.read().decode("utf-8").strip()
    
    # 각 엔딩을 분리
    endings = re.split(r'\n\s*\n', content)
    formatted_endings = []

    for ending in endings:
        # 번호와 제목, 내용 분리
        match = re.match(r'(\d+\))\s*([^:]+):(.*)', ending, re.DOTALL)
        if match:
            number, title, text = match.groups()
            number = number.strip()
            title = title.strip()
            text = text.strip()

            # 내용을 문장 단위로 나누기
            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
            sentences = [s.strip() for s in sentences if s.strip()]

            formatted_endings.append((number, title, sentences))

    return formatted_endings