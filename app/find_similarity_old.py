import sys
import string
import requests
import json
import pymysql 
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA, RandomizedPCA, TruncatedSVD
from sklearn.preprocessing import Normalizer

def find_companies(investorname):
    investorname = np.int(investorname)
    rmatrix= np.loadtxt(open("investorcompanyPCA.csv"),delimiter=",")
    investor_id = np.loadtxt(open("investorIDorder.csv"),delimiter=",")
    investor_id = investor_id.astype(int)
    count=0
    score = []
    target=[]
    for row in investor_id:
        if row == investorname:
            target = rmatrix[count]
        count += 1
    
    counter2 = 0
    for row in rmatrix:
        score.append([cosine_similarity(target,row).tolist()[0][0], investor_id[counter2]])
        counter2 += 1
    score = sorted(score,reverse=True)
    con = pymysql.connect(host='localhost', user='root', passwd='1234')
    cur = con.cursor()
    cur.execute('''USE Venturenetwork14;''')
    current_query='''SELECT startupID FROM Investor_comp'''
    company_total = pd.io.sql.frame_query(current_query, con)
    company_total = list(company_total['startupID'])
    similarcomp=[]

    current_query='''SELECT * FROM Investor_comp'''
    rows = pd.io.sql.frame_query(current_query, con)
    df = pd.Series(list(rows['startupID']),list(rows['investor_id']))

    for company in company_total[0:50]:
        score1=float(0)
        for row in score[0:2]: 
            if company in list(df[row[1]]) and company not in list(df[investorname]):
                #print row, company
                score1 += row[0]
        similarcomp.append([score1,company])
    return sorted(similarcomp, reverse=True)[0:40]   

if __name__ == "__main__":
    result = find_companies(sys.argv[1])
    #print result
