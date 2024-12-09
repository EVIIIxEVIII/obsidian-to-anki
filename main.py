import os
import ankiConnector
import mdToHtml

OBSIDIAN_VAULT_PATH = "/home/alderson/Apps/obsidian/main/3. Resources/Math"
RESOURCES_DIR = "3. Resources/"
IMAGES_PATH = "/home/alderson/Apps/obsidian/main/3. Resources/_Images"

def read_file_in_dir(dir):
    for root, _, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_name = get_file_name(file_path)
                deck_name = get_deck_name(file_path)
                html_content = mdToHtml.convert_to_html(file_path);

                ankiConnector.import_card(deck_name, file_name, html_content)

            except Exception as e:
                print(f"Could not read file {file_path}: {e}")

def get_deck_name(filePath):
    directories = filePath.split(RESOURCES_DIR)[1].split("/")[:-1]
    return "/".join(directories)

def get_file_name(filePath):
    return filePath.split("/")[-1].split(".")[0]

read_file_in_dir(OBSIDIAN_VAULT_PATH)
