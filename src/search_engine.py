#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 23:00:20 2023

@author: cesaralba
"""
from invertedIndex import InvertedIndex
from numpy import dot
from numpy import log
from numpy.linalg import norm
import itertools

import pandas as pd

class SearchEngine:
    def __init__(self):
        self.invertedIndex = InvertedIndex()
        
    def vectorSpaceModelSearch(self, query, maxResults = None):
        matrix = self.invertedIndex.documentMatrixForQuery(query)
        
        # Calculates cosine similarity for each document
        query_vector = [1] * len(matrix.columns)
        matrix = matrix.assign(Similarity = lambda x: dot(x, query_vector) / (norm(x) * norm(query_vector)))
        
        #Sort matrix by similarity
        matrix = matrix.sort_values(by=['Similarity'],ascending=False)
        matrix = matrix[['Similarity']]
        doc_ranking = matrix.to_dict()
        doc_ranking = doc_ranking['Similarity']
        
        # Returns the top N documents if the maxResults parameter is specified
        if maxResults is not None:
            doc_ranking = dict(itertools.islice(doc_ranking.items(), maxResults))
        
        return doc_ranking
        
    def bm25Search(self, query, k=2.0, b=0.75, maxResults = None):
        query_terms = self.invertedIndex.textPreprocessor.prepocess(query) # Tokenize the query
        query_terms = self.invertedIndex.textPreprocessor.uniqueTerms(query_terms)
        doc_ranking = dict()
        
        df = pd.DataFrame(columns = query_terms) #Creates an empty dataframe with the terms as columns
        
        for term in query_terms:
            if term in  self.invertedIndex.index:
                # Get documents that contains the term
                documents = self.invertedIndex.index[term]
                for doc_id in documents:
                    term_doc_info = documents[doc_id]
                    freq_term_doc = term_doc_info[0]
                    doc_len = term_doc_info[1]
                    #calculates IDF of the term on document
                    IDF = log((( self.invertedIndex.document_count - len(documents) + 0.5) / (len(documents) + 0.5)) + 1)
                    weighted_frequency =  (freq_term_doc * ( k +1)) / ((freq_term_doc + k) * (1 - b + (b * (doc_len / self.invertedIndex.average_document_length))))
                    bm25_score = (IDF * weighted_frequency)
                    # Sum the score to the total score of the document
                    if doc_id in doc_ranking:
                        doc_ranking[doc_id] += bm25_score
                        
                    else:
                        doc_ranking[doc_id] = bm25_score
                        df.loc[doc_id] = [0] * len(query_terms)
                    
                    df.at[doc_id,term] = bm25_score
        df.loc[:,'Row_Total'] = df.sum(numeric_only=True, axis=1)     
         # Sort descending
        doc_ranking = sorted(doc_ranking.items(), key= lambda x:x[1], reverse= True)
        doc_ranking = dict(doc_ranking)
        
        # Returns the top N documents if the maxResults parameter is specified
        if maxResults is not None:
            doc_ranking = dict(itertools.islice(doc_ranking.items(), maxResults))
        
        return doc_ranking
        
    def qlmSearch(self, query, lam = 0.35, maxResults = None):
        # lambda OF 0.35 is the standard useb by TREC
        query_terms = self.invertedIndex.textPreprocessor.prepocess(query) # Tokenize the query
        query_terms = self.invertedIndex.textPreprocessor.uniqueTerms(query_terms)
        doc_ranking = dict()
        for term in query_terms:
            if term in  self.invertedIndex.index:
                # Get documents that contains the term
                documents = self.invertedIndex.index[term]
                for doc_id in documents:
                    term_doc_info = documents[doc_id]
                    freq_term_doc = term_doc_info[0]
                    doc_len = term_doc_info[1]
                    #calculates ql value
                    doc_freq = (1 - lam) * (freq_term_doc / doc_len )
                    corp_freq = lam * ( self.invertedIndex.term_freq[term] / self.invertedIndex.word_count)
                    score = doc_freq + corp_freq
                    # Sum the score to the total score of the document
                    if doc_id in doc_ranking:
                        doc_ranking[doc_id] += score
                    else:
                        doc_ranking[doc_id] = score
        # Sort descending
        doc_ranking = sorted(doc_ranking.items(), key= lambda x:x[1], reverse= True)
        doc_ranking = dict(doc_ranking)
        
        # Returns the top N documents if the maxResults parameter is specified
        if maxResults is not None:
            doc_ranking = dict(itertools.islice(doc_ranking.items(), maxResults))
        
        return doc_ranking
                        
                    
                    
                
        
        
    
    