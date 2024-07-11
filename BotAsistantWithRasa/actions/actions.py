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

import os
import sqlite3
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction


def create_db_from_sql(db_path, sql_file_path):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tablo varsa oluşturmadan geç
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Alisveris'")
    result = cursor.fetchone()

    if not result:

        with open(sql_file_path, 'r') as file:

            sql_script = file.read()
        
        cursor.executescript(sql_script)
        conn.commit()

    else:

        print("Table 'Alisveris' already exists, skipping creation.")

    conn.close()


def read_db_to_dataframe(db_path, query):

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def find_favorite_color(row):

    colors = row[['Kirmizi', 'Mavi', 'Yesil', 'Sari']]
    favorite_color = colors.idxmax()  # En yüksek değere sahip rengi bul
    favorite_amount = colors.max()    # O rengin miktarını bul

    return pd.Series([favorite_color, favorite_amount], index=['Renk', 'Miktar'])


def generate_sentences(df):

    return df.apply(lambda x : f"{x.name} kategorisinde en çok tercih edilen renk {x['Renk']} rengidir.", axis = 1)



class ActionFavoriteColor(Action):


    def name(self) -> Text:

        return "action_favorite_color"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Slottan 'product' değerini al
        product = tracker.get_slot('product')
        print(f"DEBUG: Product slot value is: {product}")

        if not product:

            dispatcher.utter_message(text="Please specify a product name.")
            return []

        # Veritabanı ve SQL dosya yolları
        db_path = 'example.db'
        sql_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'veritabani.sql')

        # Veritabanını oluştur veya veriyi yükle
        create_db_from_sql(db_path, sql_file_path)

        # Veriyi DataFrame'e çevir
        df = read_db_to_dataframe(db_path, "SELECT * FROM Alisveris")

        # Ürüne göre en çok tercih edilen rengi bul
        if product in df['Urun'].values:

            product_df = df[df['Urun'] == product]
            favorite_color_info = product_df.apply(find_favorite_color, axis=1).iloc[0]
            response = f"The most preferred color in {product} category is {favorite_color_info['Renk']}."
        
        else:
            response = f"No information found for category {product}."

        dispatcher.utter_message(text=response)
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
        
        print(f"selam")
        name = tracker.get_slot('name')

        # Debugging: Print the value of the 'name' slot
        print(f"DEBUG: Name slot value is: {name}")

        if name:
            dispatcher.utter_message(response="utter_greet_user", name=name)

        else:
            dispatcher.utter_message(response="utter_ask_name")

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

