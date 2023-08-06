from typing import List, Optional

import requests

from bs4 import BeautifulSoup
from spotdl_romanized_lyrics.providers.translate.base import TranslateProvider


class Lyricstranslate(TranslateProvider):

    def get_lyrics(self, name: str, artists: List[str], **_) -> Optional[str]:
        url = "https://lyricstranslate.com"
        try:

            artist_str = ", ".join(
                artist for artist in artists if artist.lower() not in name.lower()
            )

            name = "+".join(_ for _ in name.split())
            artist_str = "+".join(_ for _ in artist_str.split())

            search_response = requests.get(
                url + "/en/site-search",
                params={"query": f"{name}+{artist_str}"},
                timeout=10
            )

            counter = 0
            soup = BeautifulSoup(
                search_response.text.replace("<br/>", "\n"), "html.parser"
            )
            song = soup.select_one('td.ltsearch-songtitle').a['href']

            while counter < 4:
                song_response = requests.get(
                    url + song,
                    timeout=10
                )

                if not song_response.ok:
                    counter += 1
                    continue

                soup = BeautifulSoup(
                    song_response.text.replace("<br/>", "\n"), "html.parser"
                )

                break

            if soup is None:
                return None

            translate = soup.select_one('li.song-node-info-translate').a['href']
            text_response = requests.get(
                url + translate,
                timeout=10
            )

            soup = BeautifulSoup(
                text_response.text.replace("<br/>", "\n"), "html.parser"
            )
            translate_containers = soup.select("div[class=translate-node-text]")
            translate = "\n".join(con.get_text() for con in translate_containers)

            return translate.strip()
        except Exception:
            return None
