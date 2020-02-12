from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import sqlite3

from gensim.models import LdaModel
from gensim.corpora import Dictionary

from preprocess_texts import *
import pandas as pd

def readSqliteTable(cc,dc):
    sqliteConnection = sqlite3.connect('db/sgvheadlines.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    sqlite_select_query = """SELECT DISTINCT * FROM sgvheadlines"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    for row in records:
        cc.append(row[1])

    for row in records[-12:]:
        dc.append(row[1])
        
    cursor.close()

def create_wordcloud(corpus, image_name=None):
    processed_docs = []
    texts = preprocess_docs(corpus)
    for row in texts:
        processed_docs.append(" ".join(row))
    # join all documents in corpus
    text = " ".join(list(processed_docs))

    # STOPWORDS.add("") ## to do later if needed

    wc = WordCloud(
        background_color="white",
        stopwords=STOPWORDS,
        max_words=1000,
        # mask=mask,
        max_font_size=90,
        random_state=42,
        contour_width=1,
        contour_color="#119DFF",
    )
    wc.generate(text)
    
    wc.to_file(f"{image_name}.png")

def create_lda_assets(corpus, daily_corpus):
    common_texts =  preprocess_docs(corpus)
    daily_texts = preprocess_docs(daily_corpus)
    common_dictionary = Dictionary(common_texts)
    common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
    model = LdaModel(common_corpus, num_topics=6, id2word=common_dictionary)
    daily_common_corpus = [common_dictionary.doc2bow(text) for text in daily_texts]
    return model, common_corpus, common_dictionary, daily_common_corpus

def format_daily_df(ldamodel, daily_common_corpus, daily_texts):
    '''
    Using model trained on full dataset, show topics on daily docs
    '''
    daily_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[daily_common_corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic and Keywords for each document
        for j, (topic_num, cont) in enumerate(row):
            if j == 0:  # => dominant topic
                # wp = ldamodel.show_topic(topic_num)
                # topic_keywords = ", ".join([word for word, cont in wp])
                # daily_df = daily_df.append(pd.Series([int(topic_num), topic_keywords]),ignore_index=True)
                daily_df = daily_df.append(pd.Series([int(topic_num)]), ignore_index = True)
            else:
                break

    # Add original text to the end of the output
    contents = pd.Series(daily_texts)

    daily_df = pd.concat([daily_df, contents], axis=1)
    # daily_df.columns = ["Dominant Topic", "Dominant Topic Keywords", "Headline Texts"]
    daily_df.columns = ["Dominant Topic", "Headline Texts"]
    return daily_df

def format_topics_df(ldamodel):
    topics_df = pd.DataFrame()
    for num in range(0,6):
        key_words = ldamodel.show_topic(num)
        key_words = ", ".join([word for word, cont in key_words])
        topics_df = topics_df.append(pd.Series([int(num), key_words]), ignore_index=True)
    topics_df.columns = ["Topic Num", "Topic Keywords"]
    return topics_df