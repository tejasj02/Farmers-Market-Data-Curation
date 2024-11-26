# Farmers-Market-Data-Curation

## Executive Summary
Farmers' markets are an important part of building community, ethically sourcing food,
and creating a culture around sustainable habits. In this project, I worked to source
data for farmers' markets in North Carolina. Due to their impact on the community,
I also joined this data with census data to obtain a better understanding of
how they are distributed and what insights they can provide us socially and economically.
This dataset can also be used with other census data as it has digestible location data
and further research in social science fields.

## Data
The data includes farmers' market data, web scraped from the North Carolina Department of Agriculture and Food Services, joined with census data from 2019, the most recent year I could find. The web scraping gathered the farmers' market name, address, and contact info, while the census data provided total population, median income, and the number of people aged 18-30 based on zipcode. This data is unique in this field due to its recency. It is possible to find similar data through the Department of Agriculture, but that data is often outdated and can contain mistakes on a more granular level. This script I've constructed allows the most recent data to be pulled in North Carolina.

## Power Analysis
I conducted a power analysis with the intention of finding if the populations based on zip codes with farmers' markets were significantly different from the average zip code population of North Carolina, using a significance level of .05 and a power of .8, resulting in a required sample size of 127.52.

## Exploratory Data Analysis
You can find exploratory data analysis in the eda.py file to better acclimate yourself with the data. There were 247 farmers' markets collected, and three census variables were attached. Other distribution metrics are included with viusalizations as well as general information on the data.

## Link to Kaggle
https://www.kaggle.com/datasets/tejasjyothi/north-carolina-farmers-market-data/data

## Ethics statement
This dataset was curated from publicly available sources with the intention of furthering research and information in this social science field. All scraping and data gathering was done ethically, not breaching any rules. Farmers' market data was obtained from the North Carolina Department of Agriculture and Consumer Services while the census data was imported from the censusdata Python library. Data is public and up to date as of 11/25/2024 and can be run with adjusted code to be updated. The dataset is open source and should adhere to normal ethical boundaries.

## License
This dataset is released under the [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/). You are free to copy, modify, distribute, and use the data for any purpose without asking for permission.

![License: CC0 1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)
