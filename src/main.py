#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 20:06:30 2023

@author: cesaralba
"""

from search_engine import SearchEngine

from pathlib import Path
import pandas as pd


def create_output_file_trec_eval(output_file, data):
    f = open(output_file, 'w')
    for line in data:
        txt = "{query_id} {iter} {doc_id} {rank} {sim:.4f} {run_id}\n"
        f.write(txt.format(query_id = line[0], iter = line[1], doc_id = line[2], rank = line[3], sim = line[4], run_id= line[5]))
    
def generate_data_trec_eval(ranking, query_id, iter = 0, rank = 1, run_id =1):
    data = []
    for row in ranking:
        data.append((query_id, iter , row, rank, ranking[row], run_id ))
    return data

if __name__ == "__main__":
    # Creates an instance of the search engine
    searchEngine = SearchEngine()
    
    # Convert collection (XML format) to dataframe
    collection_path = '../data/trec-dataset/cran.all.1400.xml'
    collection_xml = txt = Path(collection_path).read_text()
    collection_xml = "<root> " + collection_xml + " </root> " #Add root element to avoid problems while parsing
    df_collection = pd.read_xml(collection_xml, xpath='.//doc')
    df_collection = df_collection[['docno', 'text']]
    collection = list(df_collection.itertuples(index=False,name=None)) # Convert dataframe to list
    
    # Generates the inverted index from collection
    searchEngine.invertedIndex.generateIndex(collection)
    
    # Get the list of queries
    queries_path = '../data/trec-dataset/cran.qry.xml'
    queries_xml = txt = Path(queries_path).read_text()
    df_queries = pd.read_xml(queries_xml)
    
    data_vsm = []
    data_bm25 = []
    data_lm = []
    
    #Get the top 100 results per query using the 3 mthods implemented ( Vector Space Model , BM25 and LM)
    for index, row in df_queries.iterrows():
        #if row['num'] % 10 == 0:
            #print("Processing query ",row['num'], "...\n"  )
        results_vsm = searchEngine.vectorSpaceModelSearch(row['title'], maxResults = 100)
        data_vsm.extend(generate_data_trec_eval(results_vsm, row['num']))
        
        results_bm25 = searchEngine.bm25Search(row['title'], maxResults = 100)
        data_bm25.extend(generate_data_trec_eval(results_bm25, row['num']))
        
        results_lm = searchEngine.qlmSearch(row['title'], maxResults = 100)
        data_lm.extend(generate_data_trec_eval(results_lm, row['num']))
        
    # Generate the file for evaluation
    output_path_vsm = '../data/output/vsm.txt'
    output_path_bm25 = '../data/output/bm25.txt'
    output_path_lm = '../data/output/lm.txt'
    
    create_output_file_trec_eval(output_path_vsm ,data_vsm )
    create_output_file_trec_eval(output_path_bm25 ,data_bm25 )
    create_output_file_trec_eval(output_path_lm ,data_lm )
    
    
    


            
            
            
    
