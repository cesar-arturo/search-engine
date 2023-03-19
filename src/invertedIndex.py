#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 23:49:18 2023

@author: cesaralba
"""

from textPreprocessor import TextPreprocessor
from collections import Counter
import pandas as pd

class InvertedIndex:
    def __init__(self):
        self.index = dict()
        self.textPreprocessor = TextPreprocessor(meaning_method = 'stemming')
        self.document_count = 0
        self.average_document_length=0
        self.word_count = 0
        self.term_freq = dict()
    
    def generateIndex(self, documents):
        # THe expected oobject is a list of tuples that (doc-id , text). Each tuple contains the document id and the text
        self.document_count = len(documents)
        for doc in documents:
            id = doc[0]
            # Prepare the text and return the list of tokens
            tokens =self.textPreprocessor.prepocess(doc[1])
            # Update the word count
            self.word_count += len(tokens)
            # Count the frequency of each term in the document
            token_freq = Counter(tokens)
            #Add terms to the index. If it's a new term it will the term to the dictionary and the document.
            #If term already exist it will add the document to the posting list
            #Posting list contains id of document, freq onf the term and document length
            for token in token_freq:
                if token in self.index:
                    self.index[token][id] = (token_freq[token], len(tokens))
                    # Count the total freq of the indext term in the corpus
                    self.term_freq[token] += token_freq[token]
                else:
                    posting = dict()
                    posting[id]= (token_freq[token], len(tokens))
                    self.index[token] = posting
                    self.term_freq[token] = token_freq[token]
            
        #Calculates the average document length
        self.average_document_length = self.word_count / self.document_count
        
        #After the index is genereated the elements and the posting list need to be sorted
        self.index = dict(sorted(self.index.items()))
        
    def documentMatrixForQuery(self, query):
        query_terms = self.textPreprocessor.prepocess(query) # Tokenize the query
        query_terms = self.textPreprocessor.uniqueTerms(query_terms)

        df = pd.DataFrame(columns = query_terms) #Creates an empty dataframe with the terms as columns

        for term in query_terms:
            if term in self.index: # If its an index term get the posting list
                documents = self.index.get(term)
                documents = documents.keys()
                for d in documents:
                    if not d in df.index: # If document doesn't in matrix add the document with 0 for all terms
                        df.loc[d] = [0] * len(query_terms)
                    df.at[d,term] = 1 # Set 1 for the document/term
        
        return df
        
        

            
        
        
        
    
