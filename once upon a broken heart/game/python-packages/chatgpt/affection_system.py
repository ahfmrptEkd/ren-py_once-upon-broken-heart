import re

def extract_affection_points(response):
    match = re.search(r'\(([+-]?\d+)\)$', response)
    if match:
        return int(match.group(1))
    return 0

def process_ai_response(response, persistent_love):
    affection_points = extract_affection_points(response)
    
    # ȣ���� ���� (���� ����)
    persistent_love[0] = max(0, min(100, persistent_love[0] + affection_points))
    
    # ��ȣ ���� ���� ���� ����
    clean_response = re.sub(r'\s*\([+-]?\d+\)$', '', response)
    
    return clean_response, affection_points