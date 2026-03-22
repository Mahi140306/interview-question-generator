skills_list = [
    "python", "machine learning", "html", "css", "sql",
    "java", "data structures", "javascript"
]

def extract_skills(text):
    text = text.lower()
    found = []

    for skill in skills_list:
        if skill in text:
            found.append(skill)

    return list(set(found))