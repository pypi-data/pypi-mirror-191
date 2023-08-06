from dataclasses import dataclass
import requests
from fortressofsolitude.comic import Comic
from bs4 import BeautifulSoup, Tag


def comic_title_finder(tag: Tag) -> bool:
    return tag.has_attr('class') and 'title' in tag.get('class')


@dataclass
class WebScraper:
    parser: str = 'html.parser'

    def scrape_comics(self, url: str):
        comic_releases_response = requests.get(url)
        if comic_releases_response.status_code == 200:
            comic_releases_html = comic_releases_response.json().pop('list')
            soup = BeautifulSoup(comic_releases_html, self.parser)
            all_comic_titles = soup.findAll(comic_title_finder)
            return list(map(lambda link: Comic(link.attrs.pop('href'),
                                               link.contents[0].strip()),
                            all_comic_titles))
        return []
