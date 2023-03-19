#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 21:40:39 2023

@author: cesaralba
"""
import nltk
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from nltk import pos_tag

import contractions
import string


class TextPreprocessor:
    def __init__(self,meaning_method = 'stemming', tokenizer = 'word'):
        self.meaning_method = meaning_method
        self.tokenizer = tokenizer
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        nltk.download('averaged_perceptron_tagger')
        # self.stemmer = PorterStemmer()  # Stemmer based on the Porter stemming algorithm
        self.stemmer = SnowballStemmer(language='english')
        self.lemmatizer = WordNetLemmatizer()
        self.deleteCharacters = {'-' :'' , '/' : '' }
        self.POSexclude = ['VB','VBN','VBP','VBZ','WDT','UH','WP','WRB','CD']
        self.POSinclude = ['NN','NNP','NNS']
        
    
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
        tokens = []
        if text is not None:
            text = text.strip()
            # Converto to lowercase
            text = text.lower()
            # Delete characters
            text = self.replaceCharacters(text,self.deleteCharacters)
            # Expand contractions
            text = self.expandContractions(text)
            # Tokenize word
            tokens= word_tokenize(text)
            #Remove punctuation
            tokens =[token for token in tokens if not token in string.punctuation]
            tokens =[self.removePunctuation(token) for token in tokens]
            #Remove tokens that are only numbers,emptry strings or short words <2 
            tokens =[token for token in tokens if (len(token) >1 and token.isnumeric() == False and self.isNumber(token) == False)]

        return tokens
    
    def replaceCharacters(self, text, characters):
        text_new = text.translate(str.maketrans(characters))
        return text_new
    
    def removePunctuation(self, text):
        text_new = text.translate(str.maketrans('', '', string.punctuation))
        return text_new
    
    def expandContractions(self, text ):
        expanded_words =[]
        for word in text.split():
            expanded_words.append(contractions.fix(word))
        expanded_text = ' '.join(expanded_words)
        return expanded_text
    
    def isNumber(self, text):
        if text.replace('.', '').isnumeric():
            return True
        else:
            return False
        
    def uniqueTerms(self, terms):
        terms = list(dict.fromkeys(terms))
        return terms
    
    def removePOS(self, tokens):
        tagged = pos_tag(tokens)
        tagged =[t[0] for t in tagged if t[1] in self.POSinclude]
        return tagged
        

        
    
    def prepocess(self, text):
        # Convert text to tokens
        tokens = self.tokenization(text)
        # Remove stopwords
        tokens = self.stopwords_removal(tokens)
        # Experiment removing specific POS
        # tokens = self.removePOS(tokens)
        # Executes stemming or lematization depening on the selected method
        if self.meaning_method == "stemming":
            tokens = self.stemming(tokens)
        else:
            tokens = self.lemmatization(tokens)
        return tokens
    
            
        
            
        
        
        
        
        
        
        
        
    
    
        
            
        
    