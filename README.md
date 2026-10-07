# README: Hashtag Geolocation Analysis

This project tracks hashtag usage patterns across languages and countries using a MapReduce-style pipeline over 2020 tweet data.

## Methodology

1. **Map Phase**: Process each day's tweets, extracting hashtag counts partitioned by language and `country_code` (with safe handling of missing metadata).
2. **Reduce Phase**: Aggregate all mapper outputs into consolidated `.lang` and `.country` dictionaries.
3. **Visualization**: Generate top-10 bar charts per hashtag, plus temporal line plots for alternative trend analysis.

## Results
**Top 10 Language breakdown** (coronavirus):
![lang coronavirus]("./lang_%23coronavirus_bar.png")

**Top 10 Country breakdown** (coronavirus):
![country coronavirus]("./country_%23coronavirus_bar.png")

**Top 10 Language breakdown** (코로나바이러스):
![lang coronavirus_kr]("./lang_%23kr_bar.png")

**Top 10 Country breakdown** (코로나바이러스):
![country coronavirus_kr]("./country_%23kr_bar.png")

**Temporal comparison of hashtag mentions across the year**:
![timeline trends]("./hashtag_lineplot.png")














