#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 20:06:30 2023

@author: cesaralba
"""

from search_engine import SearchEngine


if __name__ == "__main__":
    list_doc =[(1,"I speak spanish since i was a child althought is spanish is easier than english"),
            (2,"Spanish is my native language"),
           (3,"English is a complicated language")]
    # Creates an instance of the search engine
    searchEngine = SearchEngine()
    # Generates the index for the set of documents
    searchEngine.invertedIndex.generateIndex(list_doc)
    
    print(searchEngine.invertedIndex.index)
    
    query = "native spanish world"
    print("Query")
    searchEngine.vectorSpaceModelSearch(query)
    searchEngine.bm25Search(query)
    searchEngine.qlmSearch(query)


            
            
            
    
