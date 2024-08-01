# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import re
import os
import sqlite3
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormValidationAction
from pymongo import MongoClient

# bu kısım bir sql database'i kurgulanmış ve burada kullanıcının talimatıyla 
# belieli ürünlerde kategorilere göre en çok tercih edilen ürün hangisiyse
# onun istatistikleri getirilir...
# bizim senaryomuzda sql olmayacağı için burayı yoruma alıyorum.
# bu kısıım belki koctas için kurgulanabilir
#
#
# def create_db_from_sql(db_path, sql_file_path):

#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     # Tablo varsa oluşturmadan geç
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Alisveris'")
#     result = cursor.fetchone()

#     if not result:

#         with open(sql_file_path, 'r') as file:

#             sql_script = file.read()
        
#         cursor.executescript(sql_script)
#         conn.commit()

#     else:

#         print("Table 'Alisveris' already exists, skipping creation.")

#     conn.close()


# def read_db_to_dataframe(db_path, query):

#     conn = sqlite3.connect(db_path)
#     df = pd.read_sql_query(query, conn)
#     conn.close()

#     return df


# def find_favorite_color(row):

#     colors = row[['Kirmizi', 'Mavi', 'Yesil', 'Sari']]
#     favorite_color = colors.idxmax()  # En yüksek değere sahip rengi bul
#     favorite_amount = colors.max()    # O rengin miktarını bul

#     return pd.Series([favorite_color, favorite_amount], index=['Renk', 'Miktar'])


# def generate_sentences(df):

#     return df.apply(lambda x : f"{x.name} kategorisinde en çok tercih edilen renk {x['Renk']} rengidir.", axis = 1)



# class ActionFavoriteColor(Action):


#     def name(self) -> Text:

#         return "action_favorite_color"


#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         # Slottan 'product' değerini al
#         product = tracker.get_slot('product')
#         print(f"DEBUG: Product slot value is: {product}")

#         if not product:

#             dispatcher.utter_message(text="Please specify a product name.")
#             return []

#         # Veritabanı ve SQL dosya yolları
#         db_path = 'example.db'
#         sql_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'veritabani.sql')

#         # Veritabanını oluştur veya veriyi yükle
#         create_db_from_sql(db_path, sql_file_path)

#         # Veriyi DataFrame'e çevir
#         df = read_db_to_dataframe(db_path, "SELECT * FROM Alisveris")

#         # Ürüne göre en çok tercih edilen rengi bul
#         if product in df['Urun'].values:

#             product_df = df[df['Urun'] == product]
#             favorite_color_info = product_df.apply(find_favorite_color, axis=1).iloc[0]
#             response = f"The most preferred color in {product} category is {favorite_color_info['Renk']}."
        
#         else:
#             response = f"No information found for category {product}."

#         dispatcher.utter_message(text=response)
#         return []



# ekrana bir mesaja basmadan entera basılırsa bu aksiyon bir şey yapılmamasını sağlaycak...

class ActionListenForNonEmptyMessage(Action): 

    def name(self) -> str:

        return "action_listen_for_non_empty_message"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:

        last_message = tracker.latest_message.get("text", "").strip()

        if not last_message:

            print(f"DEBUG: typing empty message")
            # Eğer mesaj boşsa veya sadece boşluksa, tepki vermeden geri dön
            return [UserUtteranceReverted()]

        return []



class ActionClothingAdvice(Action):


    def name(self) -> Text:

        return "action_clothing_advice"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mood = tracker.get_slot('mood')

        # Debugging: Print the value of the 'mood' slot
        print(f"DEBUG: Mood slot value is: {mood}")

        # Basit bir ruh hali ve renk eşlemesi
        mood_to_colors = {
            "happy": "bright colors like yellow and orange",
            "sad": "cool colors like blue and gray",
            "excited": "vibrant colors like red and purple",
            "nervous": "calm colors like green and beige",
            "calm": "neutral colors like white and light blue"
        }

        if mood:

            mood_cleaned = mood.lower()

            if "happy" in mood_cleaned:
                colors = mood_to_colors["happy"]

            elif "sad" in mood_cleaned:
                colors = mood_to_colors["sad"]

            elif "excited" in mood_cleaned:
                colors = mood_to_colors["excited"]

            elif "nervous" in mood_cleaned:
                colors = mood_to_colors["nervous"]

            elif "calm" in mood_cleaned:
                colors = mood_to_colors["calm"]

            else:
                colors = "a mix of colors"

        else:
            colors = "a mix of colors"

        dispatcher.utter_message(text=f"Based on your mood, people usually wear {colors}. You can try a combination with these colors!")

        return [SlotSet("mood", mood)]



class ActionGreetUser(Action):

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Debugging: Print the current intent and slots
        print(f"DEBUG: Current intent is: {tracker.latest_message['intent']['name']}")
        # print(f"DEBUG: Slots before action: {tracker.current_slot_values()}")
        
        name = tracker.get_slot('name')

        if name:
            dispatcher.utter_message(response="utter_greet_user", name=name)
        else:
            dispatcher.utter_message(response="utter_ask_name")

        # Debugging: Print the slots after action
        # print(f"DEBUG: Slots after action: {tracker.current_slot_values()}")

        return [SlotSet("name", name)]



class ValidateNewSeasonProductsForm(FormValidationAction):


    def name(self) -> Text:

        return "validate_new_season_products_form"


    def validate_product(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        
        if slot_value.lower() in ["tişört", "ceket", "pantolon", "elbise", "gömlek", "çorap"]:
            
            return {"product": slot_value}
        
        dispatcher.utter_message(text="Geçersiz giyim türü. Lütfen tişört, ceket, pantolon, elbise, gömlek veya çorap seçin.")
        
        return {"product": None}


    def validate_size(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        
        if slot_value.lower() in ["small", "medium", "large", "xl", "xxl"]:
            
            return {"size": slot_value}
        
        dispatcher.utter_message(text="Geçersiz beden. Lütfen small, medium, large, xl veya xxl seçin.")
        
        return {"size": None}


    def validate_color(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        
        if slot_value.lower() in ["siyah", "beyaz", "kırmızı", "mavi", "yeşil", "sarı"]:
            
            return {"color": slot_value}
       
        dispatcher.utter_message(text="Geçersiz renk. Lütfen siyah, beyaz, kırmızı, mavi, yeşil veya sarı seçin.")
        
        return {"color": None}


    def validate_material(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        
        if slot_value.lower() in ["pamuklu", "polyester", "yün", "ipek"]:
            
            return {"material": slot_value}
       
        dispatcher.utter_message(text="Geçersiz kumaş türü. Lütfen pamuklu, polyester, yün veya ipek seçin.")
       
        return {"material": None}


    def validate_feedback(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:

        return {"feedback": slot_value}



class ActionSubmitNewSeasonProductsForm(Action):


    def name(self) -> Text:

        return "action_submit_new_season_products_form"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product = tracker.get_slot('product')
        size = tracker.get_slot('size')
        color = tracker.get_slot('color')
        material = tracker.get_slot('material')

        dispatcher.utter_message(text=f"Tercihleriniz: {size} beden, {color} renklerde, {material} {product}. Doğru mu?")
        
        return []



class ActionFindProductLocationKoctas(Action):


    def name(self) -> Text:

        return "action_find_product_location_koctas"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        koctas_product = tracker.get_slot('koctas_product')
        koctas_product_color = tracker.get_slot('koctas_product_color')
        koctas_product_size = tracker.get_slot('koctas_product_size')
        koctas_product_weight = tracker.get_slot('koctas_product_weight')
        koctas_product_price = tracker.get_slot('koctas_product_price')
        koctas_product_warranty = tracker.get_slot('koctas_product_warranty')
        koctas_product_campaign = tracker.get_slot('koctas_product_campaign')
        campaign_ok = tracker.get_slot('campaign_ok')

        # Debugging: Print the current slot values
        print(f"DEBUG: Slots before action: Product: {koctas_product}, Color: {koctas_product_color}, Size: {koctas_product_size}, Weight: {koctas_product_weight}, Price: {koctas_product_price}, Warranty: {koctas_product_warranty}, Campaign: {koctas_product_campaign}, Campaign_OK: {campaign_ok}")

        # Check if the essential slot is provided
        if not koctas_product:

            dispatcher.utter_message(text="Lütfen bir ürün adı belirtin.")
            return []

        if not campaign_ok:

            dispatcher.utter_message(response="utter_ask_koctas_campaign")
            return [FollowupAction(name="action_listen")]

        # Convert campaign_ok to a boolean value for the query
        if campaign_ok.lower() == 'evet':

            koctas_product_campaign = True

        else:

            koctas_product_campaign = False


        try:

            client = MongoClient('localhost', 27017)
            db = client.home_store
            sections = db.sections

            # Build the query
            query = {
                'aisles.shelves.shelves.product_category': koctas_product.capitalize() if koctas_product else None,
            }

            # Add optional criteria if provided
            if koctas_product_color:
                query['aisles.shelves.shelves.product.renk'] = koctas_product_color.lower()

            if koctas_product_size:
                query['aisles.shelves.shelves.product.boyut'] = koctas_product_size

            if koctas_product_weight:
                query['aisles.shelves.shelves.product.ağırlık'] = koctas_product_weight

            if koctas_product_price:
                query['aisles.shelves.shelves.product.fiyat'] = koctas_product_price

            if koctas_product_warranty:
                query['aisles.shelves.shelves.product.garanti'] = koctas_product_warranty

            query['aisles.shelves.shelves.product.kampanyali'] = koctas_product_campaign

            print(f"DEBUG: MongoDB query: {query}")

            pipeline = [
                { '$unwind': '$aisles' },
                { '$unwind': '$aisles.shelves' },
                { '$unwind': '$aisles.shelves.shelves' },
                { '$match': query },
                { '$project': {
                    'section_name': '$name',
                    'aisle_num': '$aisles.koctas_aisle_num',
                    'side': '$aisles.shelves.koctas_side',
                    'shelf_num': '$aisles.shelves.shelves.koctas_shelf_num',
                    'product_category': '$aisles.shelves.shelves.product_category',
                    'product': '$aisles.shelves.shelves.product'
                }}
            ]

            print(f"DEBUG: MongoDB pipeline: {pipeline}")

            results = list(sections.aggregate(pipeline))

            print(f"DEBUG: MongoDB results: {results}")

            if not results:

                dispatcher.utter_message(text="Üzgünüm, aradığınız özelliklerde bir ürün bulamadım.")
                
                return [
                    SlotSet("koctas_product", None),
                    SlotSet("koctas_product_color", None),
                    SlotSet("koctas_product_size", None),
                    SlotSet("koctas_product_weight", None),
                    SlotSet("koctas_product_price", None),
                    SlotSet("koctas_product_warranty", None),
                    SlotSet("koctas_product_campaign", None),
                    SlotSet("campaign_ok", None)
                ]

            locations = []

            for result in results:
               
                product_category = result['product_category']
                product_details = result['product']

                if isinstance(product_details, list):
                    
                    for product in product_details:
                        
                        if not koctas_product_color or (product_category and product['renk'] == koctas_product_color.lower()):
                           
                            location = {
                                'section_name': result['section_name'],
                                'aisle_num': result['aisle_num'],
                                'side': result['side'],
                                'shelf_num': result['shelf_num']
                            }
                            locations.append(location)
                
                else:
                    
                    if not koctas_product_color or (product_category and product_details['renk'] == koctas_product_color.lower()):
                    
                        location = {
                            'section_name': result['section_name'],
                            'aisle_num': result['aisle_num'],
                            'side': result['side'],
                            'shelf_num': result['shelf_num']
                        }
                        locations.append(location)

            if locations:
                
                for location in locations:
                    
                    dispatcher.utter_message(text=f"Aradığınız ürün {location['section_name']} reyonunda, {location['aisle_num']} koridorunda, {location['side']} tarafında, {location['shelf_num']} rafında bulunuyor.")
           
            else:
              
                dispatcher.utter_message(text="Üzgünüm, aradığınız özelliklerde bir ürün bulamadım.")

        except Exception as e:
           
            dispatcher.utter_message(text=f"Veritabanı sorgusu sırasında bir hata oluştu: {e}")

        # Debugging: Print the current slot values after action
        print(f"DEBUG: Slots after action: Product: {koctas_product}, Color: {koctas_product_color}, Size: {koctas_product_size}, Weight: {koctas_product_weight}, Price: {koctas_product_price}, Warranty: {koctas_product_warranty}, Campaign: {koctas_product_campaign}")

        # slotları sonraki ürün sorgularında yanlış bilgi verilmemesi açısından temizliyoruz
        return [
            SlotSet("koctas_product", None),
            SlotSet("koctas_product_color", None),
            SlotSet("koctas_product_size", None),
            SlotSet("koctas_product_weight", None),
            SlotSet("koctas_product_price", None),
            SlotSet("koctas_product_warranty", None),
            SlotSet("koctas_product_campaign", None),
            SlotSet("campaign_ok", None)
        ]
