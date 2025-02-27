# Coronavirus Twitter Data Analysis

This project analyzes geotagged tweets sent in 2020 to monitor the spread of the coronavirus on social media. The dataset is approximately **2.7TB**. Using the [MapReduce](https://en.wikipedia.org/wiki/MapReduce) paradigm, the project processes a large-scale multilingual dataset to track hashtag usage trends across different languages and countries.

### Data Extraction
- Extracted **tweet language**, **hashtags**, and **country of origin**.
- Reduced and consolidated the data to about **33KB** of summarized JSON.
- Used **Matplotlib** for data visualization.

### Visualizations

#### **Top Countries by Hashtag Usage**
<img src=graphs/all.country%23coronavirus.png width=100% />
<img src=graphs/all.country%23코로나바이러스.png width=100% />

#### **Top Languages by Hashtag Usage**
<img src=graphs/all.lang%23coronavirus.png width=100% />
<img src=graphs/all.lang%23코로나바이러스.png width=100% />

#### **Hashtag Trends Over Time**
<img src=graphs/hashtag_trend.png width=100% />

## Conclusion
This project demonstrates the power of parallel computing in processing massive social media datasets. By leveraging MapReduce, Python scripting, and visualization techniques, we can uncover insights about how COVID-19-related discussions evolved across languages and countries throughout 2020.
