# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import numpy as np
df = pd.read_csv("Corpus.csv")

#
#
skill_submitted = []
class ActionShowIdeas(Action):

    def name(self) -> Text:
        return "action_show_ideas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        skill_submitted.extend(tracker.get_slot('skill'))

        print(skill_submitted)
        ideas = []
        for s in skill_submitted:
            ideas.append(df.loc[df['Idea'] == s,'Idea'].to_list())
        
        # ideas = ' ,'.join(ideas)

        # print(ideas)
        if(not skill_submitted):
            dispatcher.utter_message(text="Sorry, didnt get what you meant")
        else:
            dispatcher.utter_message(text="You can think about {ideas}".format(ideas = ideas))
            # dispatcher.utter_message(text="But considering your skills, these seem to be a good match: ")

        return []


class ActionTakeIdeaForward(Action):

    def name(self) -> Text:
        return "action_take_idea_forward"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        idea_submitted = tracker.get_slot('idea')
        skill_submitted = tracker.get_slot('skill')

        print(idea_submitted, skill_submitted)
        if(not idea_submitted and not skill_submitted):
            dispatcher.utter_message(text = 'didnt quite get what the idea was...')
        else:
            if(idea_submitted):
                dispatcher.utter_message(text = 'Taking 1 your idea of '+ str(tracker.get_slot('idea'))+' to the next level!')
            elif(skill_submitted):
                dispatcher.utter_message(text = 'Taking your idea of '+ str(tracker.get_slot('skill'))+' to the next level!')
        # res = df.loc[df['Idea'] == 'Papad Making', 'Skills'].to_list()
        # res = res[0]
        # print(res)
        # print(tracker.get_slot('idea'))
        # if (tracker.get_slot('idea') in ['cooking', 'cook', 'food']):
        #     #dispatcher.utter_message(text="Here's somehting you need to know about cooking")
        #     dispatcher.utter_message(text="Okay, the skills needed are {skills}".format(skills = res))
        #     return [FollowupAction("action_tell_investment_returns")]

        return []



class ActionTellInvestment(Action):

    def name(self) -> Text:
        return "action_tell_investment_returns"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        res = df.loc[df['Idea'] == 'Papad Making', 'Investment':'Income'].to_dict()
        print(res)
        if (tracker.get_slot('idea') in ['cooking', 'cook', 'food']):
            dispatcher.utter_message(text="Here's some more info")
            dispatcher.utter_message(text="Investment : {inv} and skills : {skills}".format(inv = res['Investment'][0], skills = res['Income'][0]))

        return []