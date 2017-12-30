
# -*- coding: utf-8 -*-

__author__ = "Ankan Roy and Nikhil Akki"

"""
initialise.py is used to initialise all the datasets and
other processing when sever starts.
"""

# Headers
from commonutils import Commonutils
from preprocessor import Preprocessor
import pandas as pd
from pymongo import MongoClient
from mongodbcreate.MongoDBCreate import import_content

# Path to the datasets
QA_dataset_path = "../../../dataset/json/newFile.json"
review_dataset_path = "../../../dataset/json/Beauty_5.json"

# init MongoClient
client = MongoClient('localhost', 32768)

def question_preprocess(QA_filtered_df):
    """
    Function used to preprosess Questions
    Input:Question dataset
    Output:Tokenised questions
    """
    tokenised_question = []
    for questions in QA_filtered_df:
        tokens = Preprocessor.tokenise(questions)
        stopwords_free = Preprocessor.stopword_removal(tokens)
        stemmed_word = Preprocessor.stemmer(stopwords_free)
        tokenised_question.append(stemmed_word)

    return tokenised_question


def review_preprocess(review_filtered_df):
    """
    Function used to preprosess reviews
    Input:review dataset
    Output:Tokenised review
    """
    tokenised_review = []
    for review in review_filtered_df:
        tokens = Preprocessor.tokenise(review)
        stopwords_free = Preprocessor.stopword_removal(tokens)
        stemmed_word = Preprocessor.stemmer(stopwords_free)
        tokenised_review.append(stemmed_word)
    return tokenised_review


# check the usage of the function from help(cleanJson)
# Commonutils.cleanJson(QA_dataset_path) ## since we are using newFile.json and Beauty_5.json which are already cleaned

# check the usage of the function from help(load_QA_dataset)
# QA_df = load_QA_dataset()
QA_df = pd.read_json(QA_dataset_path, lines=True)

# check the usage of the function from help(load_reveiws_dataset)
# review_df = load_reveiws_dataset(review_dataset_path)
review_df = pd.read_json(review_dataset_path, lines=True)

# check the usage of the function from help(question_preprocess)
tokenised_question = question_preprocess(QA_df['question'])
QA_df['tokenised question'] = tokenised_question

# check the usage of the function from help(review_preprocess)
tokenised_review = review_preprocess(review_df['reviewText'])
review_df['tokenised reviews'] = tokenised_review

# performs sentiment analysis
QA_df['answer_sentiments']      = Commonutils.sentiments(QA_df['answer'])
review_df['review_sentiments']  = Commonutils.sentiments(review_df['reviewText'])

# Write to CSV for further export to MongoDB
QA_df.to_csv('QA.csv')
review_df.to_csv('Reviews.csv')

# Creating MongoDB Database, Collections and appending processed CSV files
port   = 32768
dbname = 'fractal'
filepath1 = 'QA_csv.csv'
filepath2 = 'Reviews.csv'

import_content(filepath1, port=port, dbname=dbname, tablename='qa')
import_content(filepath2, port=port, dbname=dbname, tablename='reviews')
