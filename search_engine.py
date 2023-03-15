#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 23:00:20 2023

@author: cesaralba
"""
from invertedIndex import InvertedIndex
from numpy import dot
from numpy.linalg import norm

class SearchEngine:
    def __init__(self):
        self.invertedIndex = InvertedIndex()
        
    def vectorSpaceModelSearch(self,query):
        matrix = self.invertedIndex.documentMatrixForQuery(query)
        
        # Calculates cosine similarity for each document
        query_vector = [1] * len(matrix.columns)
        matrix = matrix.assign(Similarity = lambda x: dot(x, query_vector) / (norm(x) * norm(query_vector)))
        
        #Sort matrix by similarity
        matrix=  matrix.sort_values(by=['Similarity'],ascending=False)
        
        print(matrix)
        
    
        
    
    