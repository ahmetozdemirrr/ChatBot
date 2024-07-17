import json
from bson import ObjectId
from pymongo import MongoClient

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def dump_database_to_json():
    # MongoDB'ye bağlanma
    client = MongoClient('localhost', 27017)
    db = client.store
    sections = db.sections

    # Veritabanındaki tüm verileri çekme
    all_data = list(sections.find())

    # Verileri JSON formatında dosyaya yazma
    with open('database_dump.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4, cls=JSONEncoder)

    print("Veritabanındaki tüm veriler 'database_dump.json' dosyasına yazdırıldı.")

if __name__ == "__main__":
    dump_database_to_json()

