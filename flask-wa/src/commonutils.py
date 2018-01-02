#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Rohan Damodar and Ankan Roy"

"""
Commonutils.py module is used to define functions
whch are required to execute at the time of server
inialisation.
"""

# Headers
import json
from demjson import decode
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

class Commonutils(object):

    def cleanJson(filename):
        """
        Function used to convert the Q&A dataset to a Json file
        Input : Path of the dataset
        Output : Json file
        """

        # print "Your file will be saved as 'newFile.json' in current directory!"

        with open(filename) as f:
            contents = f.readlines()

        with open('newFile.json', 'a') as outfile:
            for line in contents:
                dic = decode(line)  # convert line from JSON to Python dictionary
                # convert dic to a string representing a json object
                json_obj = json.dumps(dic)
                outfile.write(json_obj)  # write to outfile
                outfile.write("\n")


    def sentiments(column):
        """
        Function used to calculate the sentimets
        Input : Data frame column
        Output : Positive and negative sentiments
        """
        lis = []
        analyser = SentimentIntensityAnalyzer()
        for i in column:
            sent = analyser.polarity_scores(i)
            lis.append(sent['compound'])
        return list(map(lambda i: 'positive' if 0 <= i else 'negative', lis))


    def load_QA_dataset():
        """
        Function used to load the QA dataset
        Input : newFile.json generated by the cleanJson funtion
        Output : Dataframe
        """
        QA_DataFrame = pd.read_json('newFile.json', lines=True)
        return QA_DataFrame


    def load_reveiws_dataset(filename):
        """
        Functions used to load reveiw dataset
        Input : Path of the dataset
        Output : Data frame
        """
        review_DataFrame = pd.read_json(filename, lines=True)
        return review_DataFrame
