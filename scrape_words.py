from bs4 import BeautifulSoup
from requests import get
from string import ascii_lowercase
from time import sleep


def get_all_words_from_page(soup: BeautifulSoup) -> list[str]:
    """
    Get all listed words from a page (in the form a bs4 soup).
    """
    entries = soup.find_all("div", {"class": "entries"})[0]
    return [word.text for word in entries.find_all("a")]

def filter_valid_words(words: list[str]) -> list[str]:
    """
    Filter all valid words from a list. Valid words need to be 5-letter long
    and only contain ascii characters.
    """
    return list(filter(
        lambda word: len(word) == 5 and all(
            map(lambda letter: letter in ascii_lowercase, word)
        ),
        words
    ))

def get_valid_words_from_url(url: str,
                             is_first: bool = False) -> tuple[int, list[str]]:
    """
    Get all valid words in a given url.

    :param url: page url
    :param is_first: whether or not the url is of the first page
    """
    soup = BeautifulSoup(get(url).text, 'html.parser')

    # first page: get total number of pages
    pages_n = 0
    if is_first:
        pages_n = int(
            soup.find_all(
                "span",
                {"class": "counters"}
            )[0].text.split()[-1]
        )

    return pages_n, filter_valid_words(get_all_words_from_page(soup))

def get_all_valid_words(sleep_t: int) -> list[str]:
    """
    Get all valid words from Merriam-Webster.

    :param sleep_t: sleep time in seconds to avoid too many requests
    """
    url = "https://www.merriam-webster.com/browse/thesaurus"
    words = []

    # scrape pages of each letter
    for letter in ascii_lowercase:

        # get total number of pages and first words
        pages_n, first_words = get_valid_words_from_url(
            f"{url}/{letter}",
            True
        )
        words += first_words

        sleep(sleep_t)

        # scrape from subsequent pages
        for i in range(2, pages_n + 1):
            _, page_words = get_valid_words_from_url(f"{url}/{letter}/{i}")
            words += page_words
            sleep(sleep_t)

    return words


if __name__ == "__main__":
    for word in get_all_valid_words(.125):
        print(word)
