import os

def load_keywords_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_all_keyword_categories(base_path="keywords"):
    keyword_dict = {
        "school_threat": load_keywords_from_file(os.path.join(base_path, "threat_school.txt")),
        "terror_threat": load_keywords_from_file(os.path.join(base_path, "threat_terror.txt")),
        "child_exploitation": load_keywords_from_file(os.path.join(base_path, "threat_csex.txt")),
        "intent_phrases": load_keywords_from_file(os.path.join(base_path, "threat_phrases.txt")),
    }
    return keyword_dict

