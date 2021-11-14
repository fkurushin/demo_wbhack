import joblib
import numpy as np
from scipy import spatial
from gensim.similarities.annoy import AnnoyIndexer
from pymystem3 import Mystem


class FindSearchTags(object):
    """docstring for FindSearchTags."""

    def __init__(self):
        self.modelW2V = joblib.load('model_files/word2vec.pkl')
        self.embeddings =  np.load('model_files/embeddings.npz')
        self.vectorizer = joblib.load('model_files/sentence_embeddings.pkl')

        with open('model_files/sentences.txt') as file_in:
            lines = list()
            for line in file_in:
                lines.append(line[:-1])
        self.sentences = lines


    def find_related_queries(self, query, depth = 100000, topN = 10):
        query_embedding = self.vectorizer.encode(query)

        score = list()
        for emb in self.embeddings['arr_0'][:depth]:
            score.append(1 - spatial.distance.cosine(query_embedding, emb))

        sent_score = dict(zip(self.sentences, score))

        sorted_dict = {k: v for k, v in sorted(sent_score.items(), key=lambda item: item[1], reverse=True)}
         # надо фиксить здесь добавить проверку set'ов
        sorted_related_queries = list(sorted_dict.keys())[1:topN + 1]

        return sorted_related_queries

    def find_related_products(self, query, topN = 1):
        """
        Для поиска по двум и более слов есть смысл строку mystem = Mystem()

        """
        mystem = Mystem()

        try:
            tag = mystem.analyze(query)[0]['analysis'][0]['gr'].split('=')[0].split(',')[0]
        except IndexError as IE:
            return 'None'

        if tag == 'S':
            indexer = AnnoyIndexer(self.modelW2V, 100)
            return self.modelW2V.wv.most_similar(str(query+'_NOUN'), topn = topN + 1, indexer=indexer)
        else:
            return 'None'

if __name__ == '__main__':
    fsg = FindSearchTags()
    print(fsg.find_related_queries("куртка женская осенняя"))
