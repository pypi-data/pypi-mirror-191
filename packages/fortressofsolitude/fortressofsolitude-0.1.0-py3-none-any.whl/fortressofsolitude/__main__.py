from web_scraper import WebScraper
from fortressofsolitude.comic_release_url_builder import ComicReleaseDateBuilder
from fortressofsolitude.date import ReleaseDay


def main():
    url_builder = ComicReleaseDateBuilder(ReleaseDay().release_date)
    url = url_builder.build()
    webscraper = WebScraper()
    comics = webscraper.scrape_comics(url)
    print(comics)


if __name__ == '__main__':
    main()
