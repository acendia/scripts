import os
import math
import json
import string
import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# ignore warnings
import warnings
warnings.filterwarnings('ignore')

class ArticleSimilarityAnalyzer:
    def __init__(self):
        self.df = None

    def create_df(self):
        directory = "myxalandri.gr/txt_files"

        # create pandas dataframe with column names ["index", "article_text"]:
        self.df = pd.DataFrame(columns=["file_index", "url", "article_text"])

        ## Default values
        # start = 0
        # offset = -1 
        ## Custom values   
        start = 200
        offset = 30

        for filename in os.listdir(directory)[start:start + offset]:
            if filename.endswith(".txt"):
                metadata_file = "myxalandri.gr/metadata_files/" + filename[:-4] + ".meta"
                # read from metadata file:
                with open(metadata_file, "r") as file:
                    # get og:url from json
                    data = json.load(file)
                og_url = data["og:url"]

                with open(os.path.join(directory, filename), "r") as file:
                    contents = file.read()
                    description_index = contents.find("Description:")
                    if description_index != -1:
                        description = contents[description_index + len("Description:"):]
                        self.df = pd.concat([self.df, pd.DataFrame([{"file_index": int(filename[:-4]), "url": og_url, "article_text": description}])], ignore_index=True)

    @staticmethod
    def preprocess(text):
        # remove punctuation from text (!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~):
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        return nltk.word_tokenize(text.lower().translate(remove_punctuation_map))

    @staticmethod
    def compute_similarity(a, b):
        # list of greek stopwords:
        ita_stopwords = stopwords.words('greek')

        # convert a collection of raw documents to a matrix of TF-IDF features
        vectorizer = TfidfVectorizer(tokenizer=ArticleSimilarityAnalyzer.preprocess, stop_words=ita_stopwords)
        tfidf = vectorizer.fit_transform([a, b])

        return ((tfidf * tfidf.T).toarray())[0, 1]

    def print_similar_articles(self, top):
        # list for storing similar articles (vice versa)
        similart_articles_list = list()

        for col in top.columns:
            similar_articles = top.index[top[col].notnull()]
            for article in similar_articles:
                # To avoid printing self-comparisons
                if article != col:
                    # if list already contains the similarity between the two articles (vice versa), then skip it
                    if article+col in similart_articles_list or col+article in similart_articles_list:
                        continue
                    
                    # add the two articles to the list (vice versa)
                    similart_articles_list.append(article+col)
                    similart_articles_list.append(col+article)

                    # in df get Index column value for specific url:
                    article_index = self.df.file_index[self.df["url"] == article].tolist()[0]
                    col_index = self.df.file_index[self.df["url"] == col].tolist()[0]
                    similarity = int(math.ceil(top.loc[article, col] * 100))
                    print("-" * 40)
                    print(f"Article {col_index}: {col} \nArticle {article_index}: {article} \nSimilarity: {similarity}%")
                    print("-" * 40)
                    # save it to a file:
                    with open("myxalandri.gr/similar_articles.txt", "a") as file:
                        file.write("-" * 40 + "\n")
                        file.write(f"Article {col_index}: {col} \nArticle {article_index}: {article} \nSimilarity: {similarity}%\n")
                        file.write("-" * 40 + "\n")

    @staticmethod
    def get_similarity_heatmap(top, mask):
        plt.figure(figsize=(12, 12))
        sns.heatmap(
            top,
            square=True,
            annot=True,
            robust=True,
            fmt='.2f',
            annot_kws={'size': 7, 'fontweight': 'bold'},
            yticklabels=top.columns,
            xticklabels=top.columns,
            cmap="YlGnBu",
            mask=mask,
            linewidths=0.1,
        )

        plt.title('Similarity heatmap', fontdict={'fontsize': 24})
        plt.show()

    def get_similar_articles(self):
        nltk.download('punkt')
        nltk.download('stopwords')

        # we create a matrix to contain the results of article a with article b
        M = np.zeros((self.df.shape[0], self.df.shape[0]))

        # we iterate over the rows of the dataframe and compute the similarity between each pair of articles
        for i, row in tqdm(self.df.iterrows(), total=self.df.shape[0], desc='1st level'):
            for j, next_row in self.df.iterrows():
                M[i, j] = self.compute_similarity(row.article_text, next_row.article_text)

        # we create a dataframe from the matrix
        similarity_df = pd.DataFrame(M, columns=self.df.url, index=self.df.url)

        # we select the articles with similarity > 0.4
        similarity_threshold = 0.35
        top = similarity_df[similarity_df > similarity_threshold]
        # top = similarity_df

        # Mask to remove the upper triangle of the matrix
        mask = np.triu(np.ones_like(top, dtype=bool))

        self.print_similar_articles(top)
        ArticleSimilarityAnalyzer.get_similarity_heatmap(top, mask)

    def main(self):
        self.create_df()
        # self.df = self.df.sort_values(by=["index"], ascending=True)
        # print(self.df)
        self.df.to_csv("myxalandri.gr/descriptions.csv", index=False)
        self.get_similar_articles()


if __name__ == "__main__":
    analyzer = ArticleSimilarityAnalyzer()
    analyzer.main()
