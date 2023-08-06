# A PYTHON PACKAGE FOR SCRAPING GOOGLE SEARCH RESULTS

This package is meant to scrape the google search results!

- PYPI link for this package - [simplegoogle-scraper-python](https://pypi.org/project/simplegoogle-scraper-python/)

## Getting Started

### Installation

### Note "installation steps"
First let's do an easy pip installation of the library by running the following command -
```bash
pip install simplegoogle-scraper-python
```

### Short example
```python
from simplegoogle_scraper_python import scrapeGooGle_results

search_query = "How are you?"
search_number = 10
scrapeGooGle_results.search(search_query,search_number)
```


| Args      | Type | Description     |
| :---:|:----:   |:---: |
| search_query      | string       | Your desired search query.   |
|  search_number  | integer        | Your desired number of results.      |
|  return  | list       | list of json outputs with title, link and snippet.      |


#### *Note:
The length of search output might not be equal to your desired search_number. 
