import yaml
import os
import dotenv
from jinja2 import Template
from pymongo import MongoClient

dotenv.load_dotenv()

with open("presets.yml", "r") as file:
    data = yaml.safe_load(file)[0]

with open(data["promptPrefix"], "r") as template_file:
    template = Template(template_file.read(), trim_blocks=True, lstrip_blocks=True)
    data["promptPrefix"] = template.render(**data)

address = "192.168.1.67:27017"
credentials = f"librechat:{os.getenv('MONGO_PASS')}"
db_address = f"mongodb://{credentials}@{address}/LibreChat"

client = MongoClient(db_address)
client.LibreChat.presets.update_one({"presetId": data["presetId"]}, {"$set": data})
