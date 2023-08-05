import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from nltk.corpus import stopwords
from nltk.util import ngrams

from sklearn.feature_extraction.text import CountVectorizer
import gensim
from collections import  Counter
import string
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk.tokenize import word_tokenize
import pyLDAvis
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
from spacy import displacy
import nltk
from textblob import TextBlob
from textstat import flesch_reading_ease

plt.rcParams.update({'font.size': 18})
plt.rcParams.update({'figure.figsize': [16, 12]})
plt.style.use('seaborn-whitegrid')


# In[ ]:


class vizzy_sentence:
    def __init__(self, data, column):
        from nltk.corpus import stopwords
        stop = set(stopwords.words('english'))
        data['text_without_stopwords'] = data[column].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop]))
        self.data = data
        self.column = column
        
    def show_char_count(self):
        '''Histogram of the length of your data column in characters'''
        char_plot = self.data[self.column].str.len().hist()
        return char_plot
    
    def print_char_count(self):
        '''Print average character count per text cell'''
        def average(numbers):
            avg = sum(numbers)/len(numbers)
            return avg
        counts = [len(word) for word in self.data[self.column]]
        print("The average number of characters in your text is {}".format(average(counts)))
        print("The max number of characters in your text is {}".format(max(counts)))
        print("The smallest number of characters in your text is {}".format(min(counts)))
    
    def show_word_count(self):
        '''Histogram of the length of data column in words'''
        count_plot = self.data[self.column].str.split().map(lambda x: len(x)).hist()
        return count_plot
    
    def print_word_count(self):
        '''Print length of data column in words'''
        def average(numbers):
            avg = sum(numbers)/len(numbers)
            return avg
        print("The average number of words in your text cells is {}".format(average(self.data[self.column].str.split().map(lambda x: len(x)))))
        print("The max number of words in your text cells is {}".format(max((self.data[self.column].str.split().map(lambda x: len(x))))))
        print("The smallest number of words in your text cells is {}".format(min((self.data[self.column].str.split().map(lambda x: len(x))))))
        
    def show_word_length(self):
        '''Hist of length of words in data column in characters'''
        len_plot = self.data[self.column].str.split().apply(lambda x : [len(i) for i in x]).map(lambda x: np.mean(x)).hist()
        return len_plot
    
    def print_word_length(self):
        '''Print length of words in data in characters'''
        def average(numbers):
            avg = sum(numbers)/len(numbers)
            return avg
        avg_len = self.data[self.column].str.split().apply(lambda x : [len(i) for i in x]).map(lambda x: np.mean(x))
        max_len = self.data[self.column].str.split().apply(lambda x: [len(i) for i in x]).map(lambda x: np.max(x))
        min_len = self.data[self.column].str.split().apply(lambda x: [len(i) for i in x]).map(lambda x: np.min(x))
        print("The average number of characters of the words in your text cells is {}".format(average(avg_len)))
        print("The max number of characters of the words in your text cells is {}".format(max(max_len)))
        print("The smallest number of characters of the words in your text cells is {}".format(min(min_len)))
    
    def show_common_stopwords(self):
        '''List of common stopwords in data'''
        stop = set(stopwords.words('english'))
        corpus=[]
        new= self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        from collections import defaultdict
        dic=defaultdict(int)
        for word in corpus:
            if word in stop:
                dic[word]+=1
        top=sorted(dic.items(), key=lambda x:x[1],reverse=True)[:10] 
        x,y=zip(*top)
        plot = plt.bar(x,y)
        return plot
    
    def print_common_stopwords(self):
        '''Print top 10 common stopwords'''
        stop=set(stopwords.words('english'))
        corpus=[]
        new= self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]

        from collections import defaultdict
        dic=defaultdict(int)
        for word in corpus:
            if word in stop:
                dic[word]+=1
        top=sorted(dic.items(), key=lambda x:x[1],reverse=True)[:10] 
        x,y=zip(*top)
        print("The most common stopwords in your text cells are:")
        for word, count in zip(x,y):
            print(str(word) + " : " + str(count))
    
    def show_common_words(self):
        '''Common words in data'''
        stop = set(stopwords.words('english'))
        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        counter=Counter(corpus)
        most=counter.most_common()
        x, y=[], []
        for word,count in most[:40]:
            try:
                if (word not in stop):
                    x.append(word)
                    y.append(count)
            except:
                x.append(word)
                y.append(count)
        sns.barplot(x=y,y=x)
        
    def print_common_words(self):
        '''Prints top 20 most common words in corpus'''
        stop = set(stopwords.words('english'))

        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        counter=Counter(corpus)
        most=counter.most_common()
        x, y=[], []
        for word,count in most[:40]:
            try:
                if (word not in stop):
                    x.append(word)
                    y.append(count)
            except:
                x.append(word)
                y.append(count)
        for word, count in zip(x,y):
            print(str(word) + " : " + str(count))
        
    def show_sentiment(self):
        '''Sentiment in data'''
        text = self.data[self.column]
        def polarity(text):
            return TextBlob(text).sentiment.polarity
        self.data['polarity_score']=self.data[self.column].apply(lambda x : polarity(x))
        hist = self.data['polarity_score'].hist()
        return hist

    def show_sentiment_cats(self):
        '''Plot data by sentiment (pos, neu, neg)'''
        def polarity(text):
            return TextBlob(text).sentiment.polarity
        self.data['polarity_score']=self.data[self.column].apply(lambda x : polarity(x))
        def sentiment(x):
            if x<0:
                return 'neg'
            elif x==0:
                return 'neu'
            else:
                return 'pos'
        self.data['polarity']=self.data['polarity_score'].map(lambda x: sentiment(x))
        plot = plt.bar(self.data.polarity.value_counts().index, self.data.polarity.value_counts())
        return plot
    
    def print_neg_sentiment(self):
        '''Show negative sentiment'''
        def polarity(text):
            return TextBlob(text).sentiment.polarity
        self.data['polarity_score']=self.data[self.column].apply(lambda x : polarity(x))
        def sentiment(x):
            if x<0:
                return 'neg'
            elif x==0:
                return 'neu'
            else:
                return 'pos'
        self.data['polarity']=self.data['polarity_score'].map(lambda x: sentiment(x))
        results = self.data[self.data['polarity']=='neg'][self.column].head(5)
        return results
    
    def print_pos_sentiment(self):
        '''Show positive sentiment'''
        def polarity(text):
            return TextBlob(text).sentiment.polarity
        self.data['polarity_score']=self.data[self.column].apply(lambda x : polarity(x))
        def sentiment(x):
            if x<0:
                return 'neg'
            elif x==0:
                return 'neu'
            else:
                return 'pos'
        self.data['polarity']=self.data['polarity_score'].map(lambda x: sentiment(x))
        results = self.data[self.data['polarity']=='pos'][self.column].head(5)
        return results
    
    def show_flesch_kincaid(self):
        '''show flesch kincaid score'''
        hist = self.data[self.column].apply(lambda x : flesch_reading_ease(x)).hist()
        return hist
    
    def print_flesch_kincaid(self):
        '''prints flesch kincaid scores'''
        def average(numbers):
            avg = sum(numbers)/len(numbers)
            return avg
        scores = self.data[self.column].apply(lambda x : flesch_reading_ease(x))
        print("The average Flesch-Kincaid score for your text is {}".format(average(scores)))
        print("The max Flesch-Kincaid score for your text is {}".format(max(scores)))
        print("The min Flesch-Kincaid score for your text is {}".format(min(scores)))
    
    def show_bi_grams(self):
        '''show most common bi-grams'''
        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        def get_top_ngram(corpus, n=None):
            vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0) 
            words_freq = [(word, sum_words[0, idx]) 
                          for word, idx in vec.vocabulary_.items()]
            words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
            return words_freq[:10]

        top_n_bigrams=get_top_ngram(self.data[self.column],2)[:10]
        x,y=map(list,zip(*top_n_bigrams))
        plot = sns.barplot(x=y,y=x)
        return plot
        
    def print_bi_grams(self):
        '''prints most common bi-grams'''
        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        def get_top_ngram(corpus, n=None):
            vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0) 
            words_freq = [(word, sum_words[0, idx]) 
                          for word, idx in vec.vocabulary_.items()]
            words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
            return words_freq[:10]

        top_n_bigrams=get_top_ngram(self.data[self.column],2)[:10]
        x,y=map(list,zip(*top_n_bigrams))
        print("The most common bi-grams in your text are:")
        for word, count in zip(x,y):
            print(str(word) + " : " + str(count))
        
        
    def show_tri_grams(self):
        '''show most common tri-grams'''
        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        def get_top_ngram(corpus, n=None):
            vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0) 
            words_freq = [(word, sum_words[0, idx]) 
                          for word, idx in vec.vocabulary_.items()]
            words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
            return words_freq[:10]

        top_n_bigrams=get_top_ngram(self.data[self.column],3)[:10]
        x,y=map(list,zip(*top_n_bigrams))
        plot = sns.barplot(x=y,y=x)
        return plot

    def print_tri_grams(self):
        '''prints most common tri-grams'''
        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        def get_top_ngram(corpus, n=None):
            vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0) 
            words_freq = [(word, sum_words[0, idx]) 
                          for word, idx in vec.vocabulary_.items()]
            words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
            return words_freq[:10]

        top_n_bigrams=get_top_ngram(self.data[self.column],3)[:10]
        x,y=map(list,zip(*top_n_bigrams))
        print("The most common tri-grams in your text are:")
        for word, count in zip(x,y):
            print(str(word) + " : " + str(count))
 
        
class vizzy_token:
    def __init__(self, dataframe, text, labels=None):
        self.data = dataframe
        self.text = text
        self.labels = labels
        
    def show_labels_count(self):
        '''show count of each label'''
        labels = self.data[self.labels]
        counter = Counter(labels)
        x = list(counter.keys())
        y = list(counter.values())
        plot = sns.barplot(x=y,y=x)
        return plot
    
    def print_labels_count(self):
        '''print count of each label'''
        labels = self.data[self.labels]
        counter = Counter(labels)
        x = list(counter.keys())
        y = list(counter.values())
        z = zip(x,y)
        for label, count in z:
            print("Total number of {}: {}".format(label, count))
            
    def print_case(self):
        def count_upper_lower_integer(df, column):
            upper = 0
            lower = 0
            integer = 0
            for token in df[column]:
                if isinstance(token, int):
                    integer += 1
                elif isinstance(token, str):
                    if token.islower():
                        lower += 1
                    elif token.isupper():
                        upper += 1
            return {'upper': upper, 'lower': lower, 'integer': integer}
        result = count_upper_lower_integer(self.data, self.text)
        print(result)
    
    def show_case(self):
        def count_upper_lower_integer(df, column):
            upper = 0
            lower = 0
            integer = 0
            for token in df[column]:
                if isinstance(token, int):
                    integer += 1
                elif isinstance(token, str):
                    if token.islower():
                        lower += 1
                    elif token.isupper():
                        upper += 1
            return {'upper': upper, 'lower': lower, 'integer': integer}
        result = count_upper_lower_integer(self.data, self.text)
        keys = []
        items = []
        for key, item in result.items():
            keys.append(key)
            items.append(item)
        plt.pie(items, labels=keys, autopct='%1.1f%%')
        plt.title('Tokens by case')
        plt.show



class vizzy_doc:
    def __init__(self, data, column1, column2=None, column3=None, column4=None, column5=None, date_column=None, date_format=None):
        self.data = data
        self.column1 = column1
        self.column2 = column2
        self.column3 = column3
        self.column4 = column4
        self.column5 = column5
        self.date_column = date_column
        self.date_format = date_format
        
    def print_doc_stats(self):
        '''Print the statistics of your document'''
        def counter(data, column):
            return data[column].nunique()
        docs = max(idx for idx, other in self.data.iterrows())
        print("Here is your data summary:")
        print("Total number of documents: {}".format(docs))
        print("Total number of {}: {}".format(str(self.column1), (counter(self.data, self.column1))))
        if self.column2 != None:
            print("Total number of {}: {}".format(str(self.column2), (counter(self.data, self.column2))))
        else:
            pass
        if self.column3 != None:
             print("Total number of {}: {}".format(str(self.column3), (counter(self.data, self.column3))))
        else:
            pass
        if self.column4 != None:
             print("Total number of {}: {}".format(str(self.column4), (counter(self.data, self.column4))))
        else:
            pass
        if self.column5 != None:
             print("Total number of {}: {}".format(str(self.column5), (counter(self.data, self.column5))))
        else:
            pass            

    
    def show_doc_stats(self):
        if self.date_column != None and self.date_format != None:
            def extract_year(data, column, date_format=self.date_format, new_column=None):
                # Extract the year from the date column
                data[new_column] = pd.to_datetime(data[column], format = date_format).dt.year
                return data
            df = extract_year(self.data, self.date_column, date_format=self.date_format, new_column='year')
            year_counts = df['year'].value_counts()
            year_percents = year_counts / year_counts.sum() * 100
            plt.figure(0)
            plt.pie(year_percents, labels=year_percents.index[0:40], autopct='%1.1f%%')
            plt.title("Docs by {}".format(str(self.date_column)))
        else:
            pass
        
        if self.column2 != None:
            col2_counts = self.data[self.column2].value_counts()
            col2_percents = col2_counts/col2_counts.sum() * 100
            plt.figure(1)
            plt.pie(col2_percents, labels = col2_percents.index, autopct = '%1.1f%%')
            plt.title("Docs by {}".format(str(self.column2)))
        else:
            pass
            
        if self.column3 != None:
            col3_counts = self.data[self.column3].value_counts()
            col3_percents = col3_counts/col3_counts.sum() * 100 
            plt.figure(2)
            plt.pie(col3_percents, labels = col3_percents.index, autopct = '%1.1f%%')
            plt.title("Docs by {}".format(str(self.column3)))
        else:
            pass
        
        if self.column4 != None:
            col4_counts = self.data[self.column4].value_counts()
            col4_percents = col4_counts/col4_counts.sum() * 100 
            plt.figure(3)
            plt.pie(col4_percents, labels = col4_percents.index, autopct = '%1.1f%%')
            plt.title("Docs by {}".format(str(self.column4)))
        else:
            pass
        
        if self.column5 != None:
            col5_counts = self.data[self.column5].value_counts()
            col5_percents = col5_counts/col5_counts.sum() * 100 
            plt.figure(4)
            plt.pie(col5_percents, labels = col5_percents.index, autopct = '%1.1f%%')
            plt.title("Docs by {}".format(str(self.column5)))
        else:
            pass
        
        plt.show()

       