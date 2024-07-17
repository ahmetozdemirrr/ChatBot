from pymongo import MongoClient
import random

client = MongoClient('localhost', 27017)
db = client.store
sections = db.sections

section_names = ["erkek", "kadın", "çocuk", "unisex"]

product_categories = {
    'Pantolon': ['kesim', 'renk', 'kumaş', 'fiyat', 'beden'],
    'Jean': ['kesim', 'renk', 'kumaş', 'fiyat', 'beden'],
    'Kazak': ['renk', 'kumaş', 'fiyat', 'beden'],
    'Tişört': ['renk', 'kumaş', 'fiyat', 'beden'],
    'Gömlek': ['renk', 'kumaş', 'fiyat', 'beden'],
    'Ayakkabı': ['numara', 'renk', 'fiyat'],
    'Çorap': ['renk', 'malzeme', 'fiyat'],
    'Atkı': ['renk', 'malzeme', 'fiyat'],
    'Şapka': ['renk', 'malzeme', 'fiyat'],
    'Ceket': ['renk', 'kumaş', 'fiyat', 'beden'],
    'Mont': ['renk', 'kumaş', 'fiyat', 'beden'],
    'Bot': ['numara', 'renk', 'fiyat'],
    'Pijama': ['renk', 'kumaş', 'fiyat', 'beden'],
    'Eşofman': ['renk', 'kumaş', 'fiyat', 'beden'],
    'Saat': ['marka', 'fiyat'],
    'Parfüm': ['esans', 'miktar', 'fiyat']
}

product_features = {
    'kesim': ['dar', 'bol', 'normal'],
    'renk': ['kırmızı', 'mavi', 'yeşil', 'siyah', 'beyaz', 'mor', 'yeşil', 'ekru', 'bej', 'kahverengi'],
    'kumaş': ['pamuk', 'polyester', 'yün', 'kot', 'keten', 'kadife', 'ipek'],
    'fiyat': [50, 75, 100, 125, 150],
    'beden': ['small', 'medium', 'large', 'xl', 'xxl'],
    'numara': [36, 38, 40, 42, 44],
    'malzeme': ['yün', 'pamuk', 'kaşmir'],
    'marka': ['markaA', 'markaB', 'markaC'],
    'esans': ['çiçeksi', 'odunsu', 'baharatlı'],
    'miktar': [50, 75, 100, 125, 150]
}

for section_name in section_names:

    section = {
        'name': section_name,
        'aisles': []
    }
    
    for aisle_num in range(1, 31):

        aisle = {
            'aisle_num': aisle_num,
            'shelves': []
        }
        
        for side in ['L', 'R']:

            shelf_side = {
                'side': side,
                'shelves': []
            }
            
            for shelf_num in range(1, 4):

                shelf = {
                    'shelf_num': shelf_num,
                    'sections': []
                }
                
                for section_num in range(1, 6):

                    product_category = random.choice(list(product_categories.keys()))
                    product = {feature: random.choice(product_features[feature]) for feature in product_categories[product_category]}
                    section_code = f"{section_name[:2].lower()}-{aisle_num}-{side}-{shelf_num}-{section_num}"
                    
                    section_details = {
                        'code': section_code,
                        'product_category': product_category,
                        'product': product
                    }
                    
                    shelf['sections'].append(section_details)
                
                shelf_side['shelves'].append(shelf)
            
            aisle['shelves'].append(shelf_side)
        
        section['aisles'].append(aisle)
    
    sections.insert_one(section)

print("Veritabanı oluşturuldu ve veriler eklendi.")
