import pandas as pd
import random

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# Load dataset
df = pd.read_csv("quotes.csv")

# Clean dataset
df = df[['quote', 'author', 'category']]
df = df.dropna()


class ActionGetQuote(Action):

    def name(self) -> Text:
        return "action_get_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category = tracker.get_slot("category")

        if category:
            filtered = df[df['category'].str.lower() == category.lower()]

            if len(filtered) > 0:
                row = filtered.sample(1).iloc[0]
            else:
                row = df.sample(1).iloc[0]
        else:
            row = df.sample(1).iloc[0]

        quote = row['quote']
        author = row['author']

        dispatcher.utter_message(text=f'"{quote}" — {author}')

        return []