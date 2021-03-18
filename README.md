# Coronavirus twitter analysis

You will scan all geotagged tweets sent in 2020 to monitor for the spread of the coronavirus on social media.

**Due date:** 
Sunday, 11 April.

This homework will require LOTs of computation time.
I recommend that you have your code working by **21 Mar** to ensure that you will have enough time to execute the code.
No extensions will be granted for any reason.

You will continue to have assignments during the next few weeks,
and so if you delay working on this homework,
you will have some very heavy work loads ahead of you.

**Learning Objectives:**

1. work with large scale datasets
1. work with multilingual text
1. use the MapReduce divide-and-conquer paradigm to create parallel code

## Background

Approximately 500 million tweets are sent everyday.
Of those tweets, about 1% are *geotagged*.
That is, the user's device includes location information about where the tweets were sent from.
The lambda server's `/data-fast/twitter\ 2020` folder contains all geotagged tweets that were sent in 2020.
In total, there are about 1.1 billion tweets in this dataset.
We can calculate the amount of disk space used by the dataset with the `du` command as follows:
```
$ du -h /data-fast/twitter\ 2020
```

The tweets are stored as follows.
The tweets for each day are stored in a zip file `geoTwitterYY-MM-DD.zip`,
and inside this zip file are 24 text files, one for each hour of the day.
Each text file contains a single tweet per line in JSON format.
JSON is a popular format for storing data that is closely related to python dictionaries.

Vim is able to open compressed zip files,
and I encourage you to use vim to explore the dataset.
For example, run the command
```
$ vim /data-fast/twitter\ 2020/geoTwitter20-01-01.zip
```
Or you can get a "pretty printed" interface with a command like
```
$ unzip -p /data-fast/twitter\ 2020/geoTwitter20-01-01.zip | head -n1 | python3 -m json.tool | vim -
```

You will follow the [MapReduce](https://en.wikipedia.org/wiki/MapReduce) procedure to analyze these tweets.
MapReduce is a famous procedure for large scale parallel processing that is widely used in industry.
It is a 3 step procedure summarized in the following image:

<img src=mapreduce.png width=100% />

I have already done the partition step for you (by splitting up the tweets into one file per day).
You will have to do the map and reduce steps.

**Runtime:**

The simplest and most common scenario is that the map procedure takes time O(n) and the reduce procedure takes time O(1).
If you have p<<n processors, then the overall runtime will be O(n/p).
This means that:
1. doubling the amount of data will cause the analysis to take twice as long;
1. doubling the number of processors will cause the analysis to take half as long;
1. if you want to add more data and keep the processing time the same, then you need to add a proportional number of processors.

More complex runtimes are possible.
Merge sort over MapReduce is the classic example. 
Here, mapping is equivalent to sorting and so takes time O(n log n),
and reducing is a call to the `_reduce` function that takes time O(n).
But they are both rare in practice and require careful math to describe,
so we will ignore them.
In the merge sort example, it requires p=n processors just to reduce the runtime down to O(n)...
that's a lot of additional computing power for very little gain,
and so is impractical.

## Background Tasks

Complete the following tasks to familiarize yourself with the sample code:

1. Fork the [twitter\_coronavirus](https://github.com/mikeizbicki/twitter_coronavirus) repo and clone your fork onto the lambda server.

1. **Mapping:**
   The `map.py` file processes a single zip file of tweets.
   From the root directory of your clone, run the command
   ```
   $ ./src/map.py --input_path=/data-fast/twitter\ 2020/geoTwitter20-02-16.zip
   ```
   This command will take a few minutes to run as it is processing all of the tweets within the zip file.
   After the command finishes, you will now have a folder `outputs` that contains a file `geoTwitter20-02-16.zip.lang`.
   This is a file that contains JSON formatted information summarizing the tweets from 16 February.

1. **Visualizing:**
   The `visualize.py` file displays the output from running the `map.py` file.
   Run the command
   ```
   $ ./src/visualize.py --input_path=outputs/geoTwitter20-02-16.zip.lang --key='#coronavirus'
   ```
   This displays the total number of times the hashtag `#coronavirus` was used on 16 February in each of the languages supported by twitter.
   Now manually inspect the output of the `.lang` file using vim:
   ```
   $ vim outputs/geoTwitter20-02-16.zip.lang
   ```
   You should see that the file contains a dictionary of dictionaries.
   The outermost dictionary has languages as the keys, 
   and the innermost dictionary has hashtags as the keys.
   The `visualize.py` file simply provides a nicer visualization of these dictionaries.

1. **Reducing:**
   The `reduce.py` file merges the outputs generated by the `map.py` file so that the combined files can be visualized.
   Generate a new output file by running the command
   ```
   $ ./src/map.py --input_path=/data-fast/twitter\ 2020/geoTwitter20-02-17.zip
   ```
   Then merge these output files together by running the command
   ```
   $ ./src/reduce.py --input_paths outputs/geoTwitter20-02-16.zip.lang outputs/geoTwitter20-02-17.zip.lang --output_path=reduced.lang
   ```
   Alternatively, you can use the glob to merge all output files with the command
   ```
   $ ./src/reduce.py --input_paths outputs/geoTwitter*.lang --output_path=reduced.lang
   ```
   Now you can visualize the `reduced.lang` file with the command
   ```
   $ ./src/visualize.py --input_path=reduced.lang --key='#coronavirus'
   ```
   and this displays the combined result.

## Tasks

Complete the following tasks:

1. Modify the `map.py` file so that it tracks the usage of the hashtags on both a language and country level.
   This will require creating a variable `counter_country` similar to the variable `counter_lang`, 
   and modifying this variable in the `#search hashtags` section of the code appropriately.
   The output of running `map.py` should be two files now, one that ends in `.lang` for the lanuage dictionary (same as before),
   and one that ends in `.country` for the country dictionary.

   **HINT:**
   Most tweets contain a `place` key,
   which contains a dictionary with the `country_code` key.
   This is how you should lookup the country that a tweet was sent from.
   Some tweets, however, do not have a `country_code` key.
   This can happen, for example, if the tweet was sent from international waters or the [international space station](https://unistellaroptics.com/10-years-ago-today-the-first-tweet-was-sent-directly-from-space/).
   Your code will have to be generic enough to handle edge cases similar to this without failing.

1. Once your `map.py` file has been modified to track results for each country,
   you should run the map file on all the tweets in the `/data-fast/twitter\ 2020` folder.
   In order to do this, you should create a shell script `run_maps.sh` that loops over each file in the dataset and runs `map.py` on that file.
   Each call to `map.py` can take between minutes to hours to finish.
   (The exact runtime will depend on the server's load due to other students.)
   So you should use the `nohup` command to ensure the program continues to run after you disconnect and the `&` operator to ensure that all `map.py` commands run in parallel.

1. After your modified `map.py` has run on all the files,
   you should have a large number of files in your `outputs` folder.
   Use the `reduce.py` file to combine all of the `.lang` files into a single file,
   and all of the `.country` files into a different file.
   Then use the `visualize.py` file to count the total number of occurrences of each of the hashtags.

   For each hashtag, you should create an output file in your repo using output redirection
   ```
   $ ./src/visualize.py --input_path=PATH --key=HASHTAG | head > viz/HASHTAG
   ```
   but replace `PATH` with the path to the output of your `reduce.py` file and `HASHTAG` is replaced with the hashtag you are analyzing.

1. Commit all of your code and visualization output files to your github repo and push the results to github.
    You must edit the `README.md` file to provide a brief explanation of your results.
    This explanation should be suitable for a future employer to look at while they are interviewing you to get a rough idea of what you accomplished.
    (And you should tell them about this in your interviews!)

## Submission

Upload a link to you github repository on sakai.
I will look at your code and visualization to determine your grade.

Notice that we are not using CI to grade this assignment.
That's because you can get slightly different numbers depending on some of the design choices you make in your code.
For example, should the term `corona` count tweets that contain `coronavirus` as well as tweets that contain just `corona`?
These are relatively insignificant decisions.
I'm more concerned with your ability to write a shell script and use `nohup`, `&`, and other process control tools effectively.
