# coding: utf-8

"""
asa.py is a simple (Arabic) Sentiment Analysis using Word Embeddings.
Author: Aziz Alto
Date: Aug. 2016
"""

import argparse
from logging import info, basicConfig, INFO
from gensim.models import KeyedVectors
import numpy as np
from nltk.tokenize import wordpunct_tokenize
from sklearn.preprocessing import Imputer
import pickle
import os

LOG_HEAD = '[%(asctime)s] %(levelname)s: %(message)s'
basicConfig(format=LOG_HEAD, level=INFO)


class ArSentimentPredict(object):
    def __init__(self, embeddings_file=None):
        """
        :param embeddings_file: path to the embeddings file.
        """
        self.server_location = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        m_name = '{}/{}'.format(self.server_location, embeddings_file)
        self.embeddings, self.dimension = self.load_vectors(m_name)
        self.classifier = self.load_model()
        info("ArSentiment model is loaded ..!")

    @staticmethod
    def load_vectors(model_name, binary=True):
        """load the pre-trained embedding model"""
        if binary:
            w2v_model = KeyedVectors.load_word2vec_format(model_name, binary=True)
        else:
            w2v_model = KeyedVectors.load(model_name)

        w2v_model.init_sims(replace=True)  # to save memory
        vocab, vector_dim = w2v_model.syn0.shape
        return w2v_model, vector_dim

    @staticmethod
    def tokenize(text):
        """
        :param text: a paragraph string
        :return: a list of words
        """
        try:
            try:
                txt = unicode(text, 'utf-8')  # py2
            except NameError:
                txt = text  # py3
            words = wordpunct_tokenize(txt)
            length = len(words)
        except TypeError:
            words, length = ['NA'], 0

        return words, length

    def tokenize_data(self, examples_txt, type_='NaN'):
        tokens = []
        info('Tokenizing the {} dataset ..'.format(type_))
        total_tokens = []
        for txt in examples_txt:
            words, num = self.tokenize(txt)
            tokens.append(words)
            total_tokens.append(num)
        info(' ... total {} {} tokens.'.format(sum(total_tokens), type_))
        return tokens

    def feature(self, words):
        """average words' vectors"""

        feature_vec = np.zeros((self.dimension,), dtype="float32")
        retrieved_words = 0
        #print words
        for token in words:
            try:
                feature_vec = np.add(feature_vec, self.embeddings[token])
                retrieved_words += 1
            except KeyError:
                pass  # if a word is not in the embeddings' vocabulary discard it

        np.seterr(divide='ignore', invalid='ignore')
        feature_vec = np.divide(feature_vec, retrieved_words)

        return feature_vec

    def average_feature_vectors(self, examples, type_='NaN'):
        """
        :param examples: a list of lists (each list contains words) e.g. [['hi','do'], ['you','see'], ... ]
        :param type_: (optional) type of examples text e.g. train / test
        :return: the average word vector of each list
        """

        feature_vectors = np.zeros((len(examples), self.dimension), dtype="float32")
        info("Vectorizing {} tokens ..".format(type_))
        for i, example in enumerate(examples):
            feature_vectors[i] = self.feature(example)

        info(" ... total {} {}".format(len(feature_vectors), type_))

        return feature_vectors


    @staticmethod
    def remove_nan(x):
        """remove NaN values from data vectors"""
        imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
        x_clean = imp.fit_transform(x)
        return x_clean

    def load_model(self, model_name='model/model_pickle_sa.p'):
        m_name = '{}/{}'.format(self.server_location, model_name)
        classifier = pickle.load(open(m_name, 'rb'))
        return classifier

    def get_arsentiment(self, words):
        word_tok = self.tokenize_data(words)
        words_vectors = self.average_feature_vectors(word_tok, 'testing')
        clean_words = self.remove_nan(words_vectors)
        senti_score = self.classifier.predict(clean_words)

        return senti_score[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", help="path a pre-trained vectors model.")

    args = parser.parse_args()
    vec = args.vectors

    # vectors file
    embeddings_path = args.vectors if args.vectors else "embeddings/arabic-news.bin"

    # run
    ar_senti = ArSentimentPredict(embeddings_path)
    # ex1 = ['الناس حمار وهبل']
    # ex2 = ['الوضع جميل']
    # print ar_senti.get_arsentiment(ex1)
    # print ar_senti.get_arsentiment(ex2)
