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

import json

f = open("Corpus.json")
corpus = json.load(f)

skill_submitted = []
class ActionShowIdeas(Action):

    def name(self) -> Text:
        return "action_show_ideas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            skill_submitted.extend(tracker.get_slot('idea'))
        except TypeError:
            investment_level = tracker.get_slot('investment_level')
            levels = []
            for content in corpus:
                if content['investment_level'] == investment_level :
                    levels.append(content['category'])
            dispatcher.utter_message(text="You can think about {text}".format(text = ", ".join(levels)))
            buttons = []
            buttons.append({'title': 'Tell me more about it!' , 'payload': '/request_for_idea_details'})
            dispatcher.utter_message(text="press button to continue... or tell me a new idea if you want to talk about it...", buttons=buttons)
            
            return[SlotSet("idea", levels)]
            

        print(skill_submitted)
        ideas = []

        for s in skill_submitted:
            print(s)
            for content in corpus:
                if s in list(map(lambda x : x.lower(), content['detailed_tags'])):
                    ideas.append(content)
        
        options = []
        options.extend(i['detailed_tags'][:-1] for i in ideas)
        print(options)
        

        if(not skill_submitted):
            dispatcher.utter_message(text="Sorry, didnt get what you meant")
            return []
        else:
            dispatcher.utter_message(text="You can think about {ideas}".format(ideas = ', '.join(options[-1])))
    
        buttons = []
        buttons.append({'title': 'Tell me more about it!' , 'payload': '/request_for_idea_details'})
        dispatcher.utter_message(text="press button to continue... or tell me a new idea if you want to talk about it...", buttons=buttons)

        return []


class ActionTakeIdeaForward(Action):

    def name(self) -> Text:
        return "action_take_idea_forward"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        idea_submitted = tracker.get_slot('idea')

        ideas = []

        for s in idea_submitted:
            print(s)
            for content in corpus:
                if s in list(map(lambda x : x.lower(), content['detailed_tags'])):
                    ideas.append(content)

        print(idea_submitted)
        print(ideas)

        if not idea_submitted:
            dispatcher.utter_message(text = "Sorry, didnt get what you meant. Can you be more specific?")
        else:
            dispatcher.utter_message(text = 'Here\'s some more info about {idea}'.format(idea = idea_submitted[-1]))
            dispatcher.utter_message(text = "Here's some general information...{info}".format(info = ideas[-1]['generalInfo']))
            dispatcher.utter_message(text = "{idea} has these sub categories : {info}".format(idea =idea_submitted[-1], info = ", ".join(ideas[-1]["detailed_tags"][:-1])))


        return []



class ActionTellInvestment(Action):

    def name(self) -> Text:
        return "action_tell_investment_returns"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        idea_submitted = tracker.get_slot('idea')

        ideas = []

        for s in idea_submitted:
            print(s)
            for content in corpus:
                if s in list(map(lambda x : x.lower(), content['detailed_tags'])):
                    ideas.append(content)

        print(ideas)

        if not idea_submitted:
            dispatcher.utter_message(text = "Sorry, didnt get what you meant. Can you be more specific?")
        else:
            dispatcher.utter_message(text = 'You may need an investment in the range {min} to {max} INR.'.format(min = ideas[-1]['investment'][0], max = ideas[-1]['investment'][1] ))
            dispatcher.utter_message(text = '{time}'.format(time = ideas[-1]['timeInvestment']))

        return []


class ActionSummarize(Action):

    def name(self) -> Text:
        return "action_summarize"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        x, y = tracker.get_slot('has_customers'), tracker.get_slot('has_competitors')

        idea_submitted = tracker.get_slot('idea')
        
        ideas = []

        for s in idea_submitted[-1:]:
            print(s)
            for content in corpus:
                if s in list(map(lambda x : x.lower(), content['detailed_tags'])):
                    ideas.append(content)

        if not idea_submitted:
            dispatcher.utter_message(text = "Sorry, didnt get what you meant. Can you be more specific?")
        else:
            dispatcher.utter_message(text="So to summarize, we spoke about {ideas}".format(ideas = ', '.join(list(set(idea_submitted)))))
            dispatcher.utter_message(text="You are interested in {idea}".format(idea = idea_submitted[-1]))

            dispatcher.utter_message(text = 'You may need an investment in the range {min} to {max} INR.'.format(min = ideas[-1]['investment'][0], max = ideas[-1]['investment'][1] ))
            dispatcher.utter_message(text = '{time}'.format(time = ideas[-1]['timeInvestment']))

            dispatcher.utter_message(text = "I hope I could help. Wishing you tons of luck!") 

        return []