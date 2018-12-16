# Twitter-Sentiment-Analyzer
An MRJob program to evaluate Tweets using AFINN dict.


To execute the MRJob you need a json file with raw tweets from Twitter.
Open a terminal and write:
```console
    cd Twitter-Sentiment-Analyzer
    python mrjob.py < your-tweets-file.json
```

This will output the results on stdout.