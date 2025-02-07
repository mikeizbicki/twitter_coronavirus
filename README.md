# Coronavirus twitter analysis

You will scan all geotagged tweets sent in 2020 to monitor for the spread of the coronavirus on social media.

**Learning Objectives:**

1. work with large scale datasets
1. work with multilingual text
1. use the MapReduce divide-and-conquer paradigm to create parallel code

## Background

**About the Data:**

Approximately 500 million tweets are sent everyday.
Of those tweets, about 2% are *geotagged*.
That is, the user's device includes location information about where the tweets were sent from.
The lambda server's `/data/Twitter dataset` folder contains all geotagged tweets that were sent in 2020.
In total, there are about 1.1 billion tweets in this dataset.

The tweets are stored as follows.
The tweets for each day are stored in a zip file `geoTwitterYY-MM-DD.zip`,
and inside this zip file are 24 text files, one for each hour of the day.
Each text file contains a single tweet per line in JSON format.
JSON is a popular format for storing data that is closely related to python dictionaries.

Vim is able to open compressed zip files,
and I encourage you to use vim to explore the dataset.
For example, run the command
```
$ vim /data/Twitter\ dataset/geoTwitter20-01-01.zip
```
Or you can get a "pretty printed" interface with a command like
```
$ unzip -p /data/Twitter\ dataset/geoTwitter20-01-01.zip | head -n1 | python3 -m json.tool | vim -
```

**About MapReduce:**

You will follow the [MapReduce](https://en.wikipedia.org/wiki/MapReduce) procedure to analyze these tweets.
MapReduce is a famous procedure for large scale parallel processing that is widely used in industry.
It is a 3 step procedure summarized in the following image:

<img src=img/mapreduce.png width=100% />

I have already done the partition step for you (by splitting up the tweets into one file per day).
You will have to do the map and reduce steps.

**MapReduce Runtime:**

Let $n$ be the size of the dataset and $p$ be the number of processors used to do the computation.
The simplest and most common scenario is that the map procedure takes time $O(n)$ and the reduce procedure takes time $O(1)$.
(These will be the runtimes of our map/reduce procedures.)
In this case, the overall runtime is $O(n/p + \log p)$.
In the typical case when $p$ is much smaller than $n$,
then the runtime simplifies to $O(n/p)$.
This means that:
1. doubling the amount of data will cause the analysis to take twice as long;
1. doubling the number of processors will cause the analysis to take half as long;
1. if you want to add more data and keep the processing time the same, then you need to add a proportional number of processors.

More complex runtimes are possible.
Merge sort over MapReduce is the classic example. 
Here, mapping is equivalent to sorting and so takes time $O(n \log n)$,
and reducing is a call to the `_merge` function that takes time $O(n)$.
But they are both rare in practice and require careful math to describe,
so we will ignore them.
In the merge sort example, it requires $p=n$ processors just to reduce the runtime down to $O(n)$...
that's a lot of additional computing power for very little gain,
and so is impractical.

It is currently not known which algorithms can be parallelized with MapReduce and which algorithms cannot be parallelized this way.
Most computer scientists believe there are some algorithms which cannot be parallelized,
but we don't yet have a proof that this is the case.
In theoretical computer science, this problem is called the [$NC\stackrel{?}{=}P$ problem](https://en.wikipedia.org/wiki/NC_(complexity)),
and is closely related to the more famous $P\stackrel{?}{=}NP$ problem.

## Background Tasks

We will walk through these steps in class.

**Task 0: Setup**

Fork this repo and clone it onto the lambda server.

**Task 1: Map**

In the [posix-mapreduce lab](https://github.com/mikeizbicki/lab-posix-mapreduce), you wrote a 1 line shell command that counts the number of tweets sent in each language on a particular day.
It might have looked something like
```
$ unzip -p "$file" | jq '.lang' | sort | uniq -c | sort -n 
```
For this first task, you should translate this into python.
The python file should be called `map.py` and be located in a folder `src`.

The "disadvantage" of python is that it is more verbose.
The advantage is that we can do more complicated data analysis problems.

After creating the `map.py` file above,
adjust it so that for each hashtag in the `./hashtags` file,
it tracks how many tweets were sent in each language.

> **NOTE:**
> We didn't completely finish writing our `map.py` file in class.
> A completed version is already in the git history of this repo, however,
> and so it is in the `.git` folder of your cloned project.
> You can checkout the file from the history and copy it into your working directory with the incantation
> ```
> $ git checkout bf76137 -- src/map.py
> ```

**Task 2: Reduce**

Now write a python file `./src/reduce.py` that takes as input the outputs from the `map.py` file above and reduces them together.
This file should do an element-wise addition of all the counts.

> **NOTE:**
> To get access to the reduce file, modify the git command in the previous note.
> The file is located in the same commit.

## Main Tasks

Complete the following tasks:

**Task 0: Create the mapper**

Modify the `map.py` file so that it tracks the usage of the hashtags on both a language and country level.
This will require creating a variable `counter_country` similar to the variable `counter_lang`, 
and modifying this variable in the `#search hashtags` section of the code appropriately.
The output of running `map.py` should be two files now, one that ends in `.lang` for the language dictionary (same as before),
and one that ends in `.country` for the country dictionary.

> **HINT:**
> Most tweets contain a `place` key,
> which contains a dictionary with the `country_code` key.
> This is how you should lookup the country that a tweet was sent from.
> Some tweets, however, do not have a `country_code` key.
> This can happen, for example, if the tweet was sent from international waters or the [international space station](https://web.archive.org/web/20220124224726/https://unistellaroptics.com/10-years-ago-today-the-first-tweet-was-sent-directly-from-space/).
> Your code will have to be generic enough to handle edge cases similar to this without failing.

**Task 1: Run the mapper**

> **HINT:**
> You should thoroughly test your `map.py` file on a single day's worth of tweets and verify that you are getting reasonable results before moving on to this step.

Create a shell script called `run_maps.sh`.
This file will loop over each file in the dataset and run the `map.py` command on that file.
Each call to `map.py` can take up to a day to finish, so you should use the `nohup` command to ensure the program continues to run after you disconnect and the `&` operator to ensure that all `map.py` commands run in parallel.

> **HINT:**
> Use the glob `*` to select only the tweets from 2020 and not all tweets.

**Task 2: Reduce**

> **HINT:**
> You should manually inspect the output of your mapper code to ensure that it is reasonable and that you did not run into any error messages.
> If you have errors above that you don't deal with,
> then everything else below will be incorrect.

After your modified `map.py` has run on all the files,
you should have a large number of files in your `outputs` folder.
Use the `reduce.py` file to combine all of the `.lang` files into a single file,
and all of the `.country` files into a different file.

**Task 3: Visualize**

You can visualize your output files with the command
```
$ ./src/visualize.py --input_path=PATH --key=HASHTAG
```
Currently, this prints the top keys to stdout.

Modify the `visualize.py` file so that it generates a bar graph of the results and stores the bar graph as a png file.
The horizontal axis of the graph should be the keys of the input file,
and the vertical axis of the graph should be the values of the input file.
The final results should be sorted from low to high, and you only need to include the top 10 keys.

> **HINT:**
> We are not covering how to create images from python code in this class.
> I recommend you use the matplotlib library,
> and you can find some samples to base your code off of [in the documentation here](https://matplotlib.org/3.1.1/tutorials/introductory/sample_plots.html).

Then, run the `visualize.py` file with the `--input_path` equal to both the country and lang files created in the reduce phase, and the `--key` set to `#coronavirus` and `#코로나바이러스`.
This should generate four plots in total.

**Task 4: Alternative Reduce**

Create a new file `alternative_reduce.py`.
This file should take as input on the command line a list of hashtags,
and output a line plot where:
1. There is one line per input hashtag.
1. The x-axis is the day of the year.
1. The y-axis is the number of tweets that use that hashtag during the year.

Your `alternative_reduce.py` file have to follow a similar structure to a combined version of the `reduce.py` and `visualize.py` files.
First, you will scan through all of the data in the `outputs` folder created by the mapping step.
In this scan, you will construct a dataset that contains the information that you need to plot.
Then, after you have extracted this information,
you should call the appropriate matplotlib functions to plot the data.

> **HINT:**
> The specifications for this program and plot are intentionally underspecified
> (similar to how many real-world problems are underspecified).
> Feel free to ask clarifying questions.

**Task 5: Uploading**

Commit all of your code and images output files to your github repo and push the results to github.
You must:
1. Delete the current contents of the `README.md` file
1. Insert into the `README.md` file a brief explanation of your project, including the 4 generated png files.
    This explanation should be suitable for a future employer to look at while they are interviewing you to get a rough idea of what you accomplished.
    (And you should tell them about this in your interviews!)

## Submission

Upload a link to you github repository on sakai.
I will look at your code and visualization to determine your grade.

**Grading:**

The assignment is worth 32 points:

1. 8 points for getting the map/reduce to work
1. 8 points for your repo/readme file
1. 8 points for Task 3 plots
1. 8 points for Task 4 plots

The most common ways to miss points are:
1. having incorrect data plotted (because the map program didn't finish running on all of the inputs)
1. having illegible plots that are not "reasonably" formatted

Notice that we are not using CI to grade this assignment.
There's two reasons:

1. You can get slightly different numbers depending on some of the design choices you make in your code.
    For example, should the term `corona` count tweets that contain `coronavirus` as well as tweets that contain just `corona`?
    These are relatively insignificant decisions.
    I'm more concerned with your ability to write a shell script and use `nohup`, `&`, and other process control tools effectively.

1. The dataset is too large to upload to github actions.
    In general, writing test cases for large data analysis tasks is tricky and rarely done.
    Writing correct code without test cases is hard,
    and so many (most?) analysis of large datasets contain lots of bugs.
