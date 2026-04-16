import os
import json


# =========================
# GENERIC JSON LOADER
# =========================

def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# LOAD ALL FILES FROM FOLDER
# =========================

def load_json_folder(folder_path):
    data = []

    if not os.path.exists(folder_path):
        return data

    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            file_path = os.path.join(folder_path, file)
            content = load_json_file(file_path)
            data.append(content)

    return data


# =========================
# LOAD ALL MODULE NOTES
# =========================

def load_all_notes(base_path="data/iot"):
    all_notes = []

    for module in os.listdir(base_path):
        notes_path = os.path.join(base_path, module, "notes")

        if os.path.exists(notes_path):
            files = load_json_folder(notes_path)

            for file_data in files:
                all_notes.extend(file_data)

    return all_notes


# =========================
# LOAD ALL DIAGRAMS
# =========================

def load_all_diagrams(base_path="data/iot"):
    all_diagrams = []

    for module in os.listdir(base_path):
        diag_path = os.path.join(base_path, module, "diagrams", "diagrams.json")

        if os.path.exists(diag_path):
            diagrams = load_json_file(diag_path)
            all_diagrams.extend(diagrams)

    return all_diagrams
