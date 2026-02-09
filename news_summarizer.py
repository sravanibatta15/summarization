import re
import string
from heapq import nlargest
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from newspaper import Article
import sys
from log_code import Logger
logger=Logger.get_logs('news_summary')

class news_summarization:
    def __init__(self, url):
        try:
            self.url = url
            self.stopwords = list(STOP_WORDS)
            self.nlp = spacy.load("en_core_web_sm")
            self.punctuation = string.punctuation + "\n"
            print("NLP & Config Loaded Successfully")
        except Exception as e:
            er_ty, er_msg, er_lin = sys.exc_info()
            print(f"Init Error : {er_lin.tb_lineno} : due to {er_msg}")

    def fetch_article(self):
        try:
            self.reg = Article(self.url)
            self.reg.download()
            self.reg.parse()
            self.reg.nlp()
            self.text = self.reg.text
            print("Article Downloaded & Parsed")
        except Exception as e:
            er_ty, er_msg, er_lin = sys.exc_info()
            print(f"Fetch Error : {er_lin.tb_lineno} : due to {er_msg}")

    def summarization(self):
        try:
            doc = self.nlp(self.text)
            self.word_frequencies = {}

            for token in doc:
                if token.text.lower() not in self.stopwords:
                    if token.text.lower() not in self.punctuation:
                        if token.text.lower() not in self.word_frequencies:
                            self.word_frequencies[token.text.lower()] = 1
                        else:
                            self.word_frequencies[token.text.lower()] += 1

            max_freq = max(self.word_frequencies.values())
            for word in self.word_frequencies:
                self.word_frequencies[word] /= max_freq

            sentence_tokens = [sent for sent in doc.sents]
            self.sentence_scores = {}

            for sent in sentence_tokens:
                for word in sent:
                    if word.text.lower() in self.word_frequencies:
                        self.sentence_scores[sent] = self.sentence_scores.get(sent, 0) + self.word_frequencies[word.text.lower()]

            select_length = int(len(sentence_tokens) * 0.3)
            self.summary = nlargest(select_length, self.sentence_scores, key=self.sentence_scores.get)
            self.summary_main = ' '.join([sent.text for sent in self.summary])

            print("\n----- Before Cleaning -----\n")
            print(self.summary_main)

        except Exception as e:
            er_ty, er_msg, er_lin = sys.exc_info()
            print(f"Summarization Error : {er_lin.tb_lineno} : due to {er_msg}")

    def cleaning(self):
        try:
            review = self.summary_main
            review = re.sub('http\\S+', ' ', review)
            review = re.sub('RT|cc', '', review)
            review = re.sub('#\\S+', ' ', review)
            review = re.sub('@\\S+', ' ', review)
            review = re.sub('[!"#$%&\'()*+,/;<=>?@[\\]^_`{|}~”“]', '', review)
            review = re.sub('\\s+', ' ', review)

            self.cleaned_summary = review.strip()

            print("\n----- Cleaned Summary -----\n")
            print(self.cleaned_summary)

        except Exception as e:
            er_ty, er_msg, er_lin = sys.exc_info()
            print(f"Cleaning Error : {er_lin.tb_lineno} : due to {er_msg}")
