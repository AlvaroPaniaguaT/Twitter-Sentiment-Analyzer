# Twitter-Sentiment-Analyzer
An MRJob program to evaluate Tweets using AFINN and Redondo_words dicts.

To execute the MRJob you need a json file with raw tweets from Twitter.

Three ways to execute MRJobs.

- Inline: Used to run MRJob in local but don't simulating Hadoop system. To run this mode open Bash and type:
    
    ```console
        python mrjobs.py -r inline <path to local file with tweets *.json*> \ 
        --ESdict <path to local dict in Spanish> \
        --USdict <path to local dict for USA>
    ```

  - Local: Used to run MRJob in local simulating a Hadoop system, usually slower than *inline* mode.

    ```console
        python mrjobs.py -r local <path to local file with tweets *.json*> \ 
        --ESdict <path to local dict in Spanish> \
        --USdict <path to local dict for USA>
    ```

  - Hadoop: Used to run MRJob in real hadoop system.

    ```console
        python mrjobs.py -r hadoop <path to HDFS file with tweets *.json*> \ 
        --ESdict <path to local dict in Spanish> \
        --USdict <path to local dict for USA>
    ```

  - EMR: Used to run MRJob on AWS EMR clusters. You need to use mrjob.conf, you can pass it through *--conf-path* parameter or 
    having mrjob.conf file in $HOME on your system. To run on EMR is needed to put AWS keys on mrjob.conf file and modify 
    *ec2_instance_type* and *num_ec2_core_instances* to use the type and number of EC2 machines wanted to run in the cluster.

    ```console
        python mrjobs.py -r emr <path to S3 file with tweets *.json*> \ 
        --ESdict <path to local dict in Spanish> \
        --USdict <path to local dict for USA> \
        --conf_path <path in your local machine to configuration file> (optional)
    ```