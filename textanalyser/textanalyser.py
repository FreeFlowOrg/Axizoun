#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:27:35 2018
@author: jayesh
"""

from gensim.models import Word2Vec
from pattern import en
import textract
from os import listdir
from os.path import isfile, join
import numpy as np
from scipy import spatial




def read_All_CV(filename):
    text = textract.process(filename)
    return text.decode('utf-8')

#
#def preprocess_training_data1(dir_cvs, dir_model_name):
#    dircvs = [join(dir_cvs, f) for f in listdir(dir_cvs) if isfile(join(dir_cvs, f))]
#    alltext = ' '
#    for cv in dircvs:
#        yd = read_All_CV(cv)
#        alltext += yd + " "
#    alltext = alltext.lower()
#    vector = []
#
#    for sentence in en.parsetree(alltext, tokenize=True, lemmata=True, tags=True):
#        temp = []
#        for chunk in sentence.chunks:
#            for word in chunk.words:
#                if word.tag == 'NN' or word.tag == 'VB':
#                    temp.append(word.lemma)
#        vector.append(temp)
#
#    global model
#    model = Word2Vec(vector, size=200, window=5, min_count=3, workers=4)
#    model.save(dir_model_name)
#
# data1 : path to Job Description
# dircvs : path to folder containing CVs
# model : path to trained model

def find(data1,dircvs,model1):
    model = Word2Vec.load(model1)
    data = textract.process(data1).decode('utf-8')
    w2v = []
    val = True


    if val:
        data = data.lower()
    for sentence in en.parsetree(data, tokenize=True, lemmata=True, tags=True):
        for chunk in sentence.chunks:
            for word in chunk.words:
                if val==True:
                    if word.lemma in model.wv.vocab:
                        w2v.append(model.wv[word.lemma])
                    else:
                        if word.lemma.lower() in model.wv.vocab:
                            w2v.append(model.wv[word.lemma.lower()])

    Q_w2v = np.mean(w2v, axis=0)
    dircvsd = [join(dircvs, f) for f in listdir(dircvs) if isfile(join(dircvs, f))]
    D_w2v = []

    for cv in dircvsd:

        yd = textract.process(cv).decode('utf-8')
        w2v = []
        for sentence in en.parsetree(yd.lower(), tokenize=True, lemmata=True, tags=True):
            for chunk in sentence.chunks:
                for word in chunk.words:
                    if val==True:
                        if word.lemma in model.wv.vocab:
                            w2v.append(model.wv[word.lemma])
                        else:
                            if word.lemma.lower() in model.wv.vocab:
                                w2v.append(model.wv[word.lemma.lower()])

        D_w2v.append((np.mean(w2v, axis=0),cv))
    retrieval = []

    for i in range(len(D_w2v)):

        retrieval.append((1 - spatial.distance.cosine(Q_w2v, D_w2v[i][0]),D_w2v[i][1]))
    retrieval.sort(reverse=True)
#    ret_data = {"cv1":url_for('static', filename="test/"+retrieval[0][1][retrieval[0][1].rfind('/')+1:]), "score1": str(round(retrieval[0][0], 4)), "cv2":url_for('static', filename="test/"+retrieval[1][1][retrieval[1][1].rfind('/')+1:]), "score2": str(round(retrieval[1][0], 4)),"cv3":url_for('static', filename="test/"+retrieval[2][1][retrieval[2][1].rfind('/')+1:]), "score3": str(round(retrieval[2][0], 4))   }
#    return jsonify(ret_data)
    return retrieval
