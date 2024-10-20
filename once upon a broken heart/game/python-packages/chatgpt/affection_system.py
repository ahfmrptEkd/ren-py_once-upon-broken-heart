import re

def extract_affection_points(response):
    match = re.search(r'\(([+-]?\d+)\)$', response)
    if match:
        return int(match.group(1))
    return 0

def process_ai_response(response, persistent_love):
    affection_points = extract_affection_points(response)
    
    # 호감도 변경 (감점 포함)
    persistent_love[0] = max(0, min(100, persistent_love[0] + affection_points))
    
    # 괄호 안의 점수 정보 제거
    clean_response = re.sub(r'\s*\([+-]?\d+\)$', '', response)
    
    return clean_response, affection_points