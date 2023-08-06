from dataclasses import dataclass


@dataclass(repr=False)
class Comic:
    link_suffix: str
    title: str
    base_url: str = 'https://leagueofcomicgeeks.com'

    def get_link(self) -> str:
        return self.base_url + self.link_suffix

    def __repr__(self):
        return self.base_url + self.link_suffix
