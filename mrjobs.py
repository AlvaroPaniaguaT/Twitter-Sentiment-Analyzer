from mrjob.job import MRJob, MRStep
import re
import json
import unicodedata

#WORD_RE = re.compile(r"[\w']+", re.IGNORECASE)

Sentiment_Dict_US = dict()
Sentiment_Dict_ES = dict()


class TweetAnalyser(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer_count)#,
           # Uncomment line below to get higher value con twitter evaluation 
            #MRStep(reducer=self.find_max)
        ]

    def mapper(self, key, word):
        mytweet = self.filter_tweets(word)
        if not mytweet is None:
            country, city = self.extract_country_city(mytweet)
            if ((country == "ES") | (country == "US")):
                tweet_text = self.extract_text(mytweet)
                list_words = tweet_text.split(" ")
                calification = self.valuate_tweet(list_words, country)
                yield (city, (calification, 1))
    
    def reducer_count(self, city, evaluation):
        count = 0
        total_evaluation = 0
        for calification, counter in evaluation:
            count += counter
            total_evaluation += calification

        mean_calification = total_evaluation/count        
        yield (round(mean_calification, 2), city)

        #Uncomment line below to get higher value
        #yield None ,(round(mean_calification, 2), city)
    
    def find_max(self, _, calification_country):
        yield max(calification_country)

    def extract_country_city(self, tweet):
        if tweet['place']['place_type'] == "city":
            return tweet['place']['country_code'], tweet['place']['name'].encode("utf-8")
        else:
            return None, None

    def valuate_tweet(self, list_of_words, country):
        calification = 0
        num_words_calificated = 0
        for word in list_of_words:
            if country == "US":
                if word in Sentiment_Dict_US.keys():
                    calification += float(Sentiment_Dict_US[word])
                    num_words_calificated += 1
            else:
                if word in Sentiment_Dict_ES.keys():
                    calification += float(Sentiment_Dict_ES[word])
                    num_words_calificated += 1

        if num_words_calificated == 0:
            return calification
        else:
            return calification/num_words_calificated

    def extract_text(self, tweet):
        list_item_to_remove = [",", ".", "(", ")", '"', "'", "/\/", "/", "|", "$", "%", "&", ':', '@', '#', '_']
        try:
            text = tweet['text']
            for item in list_item_to_remove:
                text = text.replace(item, ' ')
            return text.upper()
        except Exception as e:
            pass

    def filter_tweets(self, tweet):
        '''
            INPUT:
                @tweet: Input tweet as string type
            
            OUTPUT:
                @tweet: Tweet filtered by geolocation
        '''
        try:
            tweet_json = json.loads(tweet)
            if ('place' in tweet_json.keys()) & (not tweet_json['place'] is None):
                return tweet_json
            return None
        except Exception as e:
            pass


if __name__ == "__main__":
    
    file_US = open("language/AFINN-111.txt", "r")
    file_ES = open("language/Redondo_words.csv", "r")

    for word_val in file_US.read().decode("utf-8").split("\n"):
        values = word_val.split("\t")
        Sentiment_Dict_US[values[0].upper()] = float(values[1]) + 5


    for word_val in file_ES.read().decode("utf-8").split("\n"):
        values = word_val.split("\t")
        Sentiment_Dict_ES[values[0].upper()] = float(values[1])

    TweetAnalyser.SORT_VALUES = True
    TweetAnalyser.run()
