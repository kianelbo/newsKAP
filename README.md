# newsKAP
A full search engine for Persian news aggregation

## Retrieval Model
The ranked retrieval system uses tf-idf vectors for computing scores (similarity between queries and documents). News are retrieved from inverted indices constructed from dataset collections. The large-scale collections are clustered for fast retrieval using K-Means.

## Crawler
A Mercator based crawler is used for mining Persian news from various sources. ([View original Repository](https://github.com/arminkz/Crawler))  
Demo spider for [FarsNews](https://www.farsnews.ir/) is implemented as well.

## News Classification
The news are classified into several categories using multinomial naive bayes classifier. News categories can be specified in queries to filter out the results.

## Text Preprocessing
* Removing / substituting non-Persian and non-standard characters
* Normalizing text
* Matching equivalent spellings
* Handling compound terms
* Stemming

## Extra Features
* Sorting results by relevance or date
* Handling phrase queries (using positional indices)
* Filtering results by category or source
* Near duplicate detection of news (using min hash technique)
* Smart snippet generation for preview
* Elegant SPA built with Angular 8
