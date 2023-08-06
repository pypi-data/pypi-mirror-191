import httpx
import re
from ensure import ensure_annotations
from simplegoogle_scraper_python.custom_exceptions import InvalidSearchqueryException
from simplegoogle_scraper_python.logger import logger


@ensure_annotations
def clean_pettern() -> str:
    pattern = (
        '<div class="yuRUbf"><a href="(.*?)" data-jsarwt=".*?" '
        'data-usg=".*?" data-ved=".*?"><br><h3 class="LC20lb MBeuO DKV0Md">(.*?)</h3>.*?'
        '<div class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf" style="-webkit-line-clamp:2">'
        "<span>(.*?)</span></div>"
    )
    return pattern


@ensure_annotations
def search(
    search_query: str, search_number: int
) -> list:
    """
    This is a simple google search result scraping algorithm.

    Args:
        search_query -> string: Your search query in string format.
        search_number -> integer: Your desiered number of search results.

    Return:
        List of json outputs containing title, link and snippet.
        example:
            {
                url:url for the matched search string,
                title:title of the url,
                description:short description of the scraped results
            }
    Exception:
        If the searching query is absent, it will raise InvalidSearchqueryException.
    
    Author: Biswajit Rajaguru Mohapatra

    Version: 0.1.4
    """
    try:
        if search_query is None:
            raise InvalidSearchqueryException("Search Query can not be None!")

        results = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
        }

        if search_number != None:
            base_url = f"https://www.google.com/search?q={search_query}&num={search_number}&hl=en"
        else:
            base_url = (
                f"https://www.google.com/search?q={search_query}&num=10&hl=en"
            )

        page = httpx.get(base_url, headers=headers).text

        logger.info(f"Fetched the search result for the provided query!")

        for i in re.findall(pattern=clean_pettern(), string=page):
            results.append(
                {
                    "url": i[0],
                    "title": i[1],
                    "description": re.sub("<[^<>]+>", "", i[2]),
                }
            )

        return results
    except Exception as e:
        raise e
