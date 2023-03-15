#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 21:40:39 2023

@author: cesaralba
"""
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords

import string


class TextPreprocessor:
    def __init__(self,meaning_method = 'stemming', tokenizer = 'word'):
        self.meaning_method = meaning_method
        self.tokenizer = tokenizer
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        self.stemmer = PorterStemmer()  # Stemmer based on the Porter stemming algorithm
        self.lemmatizer = WordNetLemmatizer()
    
    def stemming(self, tokens):
        # Applies the stemmer for all the elements on the list
        new_tokens = [self.stemmer.stem(token) for token in tokens]
        return new_tokens
    
    def lemmatization(self, tokens):
        # Convert tokens to their base form
        new_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return new_tokens
    
    def stopwords_removal(self, tokens):
        # FIlter out tokens on stopwords list
        new_tokens = [token for token in tokens if not token in stopwords.words('english')]
        return new_tokens
    
    def tokenization(self, text):
        # Remove leading and trailing spaces
        text = text.strip()
        # Converto to lowercase
        text = text.lower()
        tokens= word_tokenize(text)
        #Remove punctuation
        tokens =[token for token in tokens if not token in string.punctuation]
        return tokens
    
    def prepocess(self, text):
        # Convert text to tokens
        tokens = self.tokenization(text)
        # Remove stopwords
        tokens = self.stopwords_removal(tokens)
        # Executes stemming or lematization depening on the selected method
        if self.meaning_method == "stemming":
            tokens = self.stemming(tokens)
        else:
            tokens = self.lemmatization(tokens)
        return tokens
    
            
        
            
        
        
        
        
        
        
        
        
    
    
        
            
        
    