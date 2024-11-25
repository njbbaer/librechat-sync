import os
import yaml
import dotenv
from jinja2 import Template
from pymongo import MongoClient

dotenv.load_dotenv()


def render_template(file_path, context):
    with open(file_path, "r") as template_file:
        template = Template(template_file.read(), trim_blocks=True, lstrip_blocks=True)
    return template.render(**context)


def get_mongo_client():
    address = "192.168.1.67:27017"
    credentials = f"librechat:{os.getenv('MONGO_PASS')}"
    db_address = f"mongodb://{credentials}@{address}/LibreChat"
    return MongoClient(db_address)


def update_preset(client, preset):
    result = client.LibreChat.presets.update_one(
        {"presetId": preset["presetId"]}, {"$set": preset}
    )
    if result.matched_count == 0:
        raise ValueError(f"Preset with ID {preset['presetId']} not found")


def apply_preset(preset):
    preset["promptPrefix"] = render_template(preset["promptPrefix"], preset)
    client = get_mongo_client()
    update_preset(client, preset)


def load_presets(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def main():
    presets = load_presets("presets.yml")
    for preset in presets:
        apply_preset(preset)


if __name__ == "__main__":
    main()
