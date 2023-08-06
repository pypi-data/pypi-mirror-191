from dataclasses import dataclass, field
from typing import List
from functools import reduce

PUBLISHERS = {
    'dc': 1,
    'marvel': 2,
    'dark-horse': 5,
    'image': 7,
    'dynamite': 12,
    'boom-studios': 13,
    'oni-press': 29,
}

FORMATS = {
    'single-issue': 1,
    'tradepaperback': 3,
    'hardcover': 4
}


def resolve_url_param_type(translation_dict, param_type, selected_params) -> str:
    if selected_params:
        return reduce(lambda param_string, param:
                      param_string + f'&{param_type}[]={translation_dict.pop(param)}',
                      selected_params, '')
    return ''


@dataclass
class ComicReleaseDateBuilder:
    date: str
    publishers: List = None
    formats: List = None
    base_url: str = 'https://leagueofcomicgeeks.com/comic/get_comics'
    base_url_params: List = field(
        default_factory=lambda: ['view=text', 'list=releases', 'date_type=week'])

    def resolve_base_params(self):
        return '?' + '&'.join(self.base_url_params)

    def build(self) -> str:
        return self.base_url + self.resolve_base_params() + f'&date={self.date}' + \
            resolve_url_param_type(FORMATS, 'format', self.formats) + \
            resolve_url_param_type(PUBLISHERS, 'publisher', self.publishers)

    def print_format_options(self):
        print(FORMATS.keys())

    def print_publisher_options(self):
        print(PUBLISHERS.keys())

    def with_publishers(self, *args):
        for publisher in args:
            self.publishers.append(publisher)
        return self

    def with_formats(self, *args):
        for format in args:
            self.formats.append(format)
        return self

