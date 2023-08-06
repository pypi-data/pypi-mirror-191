import cloudscraper
import json, re

from typing import Dict, List, Optional, Tuple, Type, Union
from types import TracebackType
from bs4 import BeautifulSoup, Tag, ResultSet
from urllib.parse import unquote, urlencode, quote
from enum import Flag, auto
from .exception import AnimeFLVParseError
from dataclasses import dataclass


def removeprefix(str: str, prefix: str) -> str:
    """
    Remove the prefix of a given string if it contains that
    prefix for compatability with Python >3.9

    :param _str: string to remove prefix from.
    :param episode: prefix to remove from the string.
    :rtype: str
    """

    if type(str) is type(prefix):
        if str.startswith(prefix):
            return str[len(prefix) :]
        else:
            return str[:]


def parse_table(table: Tag):
    columns = list([x.string for x in table.thead.tr.find_all("th")])
    rows = []

    for row in table.tbody.find_all("tr"):
        values = row.find_all("td")

        if len(values) != len(columns):
            raise AnimeFLVParseError("Don't match values size with columns size")

        rows.append({h: x for h, x in zip(columns, values)})

    return rows


BASE_URL = "https://animeflv.net"
BROWSE_URL = "https://animeflv.net/browse"
SEARCH_URL = 'https://animeflv.net/browse?q='
ANIME_VIDEO_URL = "https://animeflv.net/ver/"
ANIME_URL = "https://animeflv.net/"
BASE_EPISODE_IMG_URL = "https://cdn.animeflv.net/screenshots/"
ORDER_TITLE = 'https://animeflv.net/browse?order=title&page='


@dataclass
class EpisodeInfo:
    id: Union[str, int]
    anime: str
    image_preview: Optional[str] = None


@dataclass
class AnimeInfo:
    id: Union[str, int]
    title: str
    poster: Optional[str] = None
    banner: Optional[str] = None
    synopsis: Optional[str] = None
    rating: Optional[str] = None
    genres: Optional[List[str]] = None
    debut: Optional[str] = None
    type: Optional[str] = None
    episodes: Optional[List[EpisodeInfo]] = None


@dataclass
class DownloadLinkInfo:
    server: str
    url: str


class EpisodeFormat(Flag):
    Subtitled = auto()
    Dubbed = auto()


class AnimeFLV(object):
    def __init__(self, *args, **kwargs):
        session = kwargs.get("session", None)
        self._scraper = cloudscraper.create_scraper(session)

    def close(self) -> None:
        self._scraper.close()

    def __enter__(self) -> "AnimeFLV":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def get_links(
        self,
        id: str,
        episode: Union[str, int],
        format: EpisodeFormat = EpisodeFormat.Subtitled,
        **kwargs,
    ) -> List[DownloadLinkInfo]:
        """
        Get download links of specific episode.
        Return a list of dictionaries like:
        [
            {
                "server": "...",
                "url": "..."
            },
            ...
        ]

        :param id: Anime id, like as 'nanatsu-no-taizai'.
        :param episode: Episode id, like as '1'.
        :param **kwargs: Optional arguments for filter output (see doc).
        :rtype: list
        """
        response = self._scraper.get(f"{ANIME_VIDEO_URL}{id}-{episode}")
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("table", attrs={"class": "RTbl"})

        try:
            rows = parse_table(table)
            ret = []

            for row in rows:
                if (
                    row["FORMATO"].string == "SUB"
                    and EpisodeFormat.Subtitled in format
                    or row["FORMATO"].string == "LAT"
                    and EpisodeFormat.Dubbed in format
                ):
                    ret.append(
                        DownloadLinkInfo(
                            server=row["SERVIDOR"].string,
                            url=re.sub(
                                r"^http[s]?://ouo.io/[A-Za-z0-9]+/[A-Za-z0-9]+\?[A-Za-z0-9]+=",
                                "",
                                unquote(row["DESCARGAR"].a["href"]),
                            ),
                        )
                    )

            return ret
        except Exception as exc:
            raise AnimeFLVParseError(exc)

    def list(self, page: int = None) -> List[Dict[str, str]]:
        """
        Shortcut for search(query=None)
        """

        return self.search(page=page)

    def search(self, query):
        """
        Search in animeflv.net by query.
        :param query: Query information like: 'Nanatsu no Taizai'.
        :param page: Page of the information return.
        :rtype: list[AnimeInfo]
        """

        res = self._scraper.get(f"{SEARCH_URL}{quote(query)}")
        body = res.text
        soup = BeautifulSoup(body, 'lxml')
        elements = soup.select('div.Container ul.ListAnimes li article')

        ret = []
        for element in elements:
            try:
                ret.append({
                    'id': element.select_one('div.Description a.Button')['href'][1:],
                    'title': element.select_one('a h3').string,
                    'poster': element.select_one('a div.Image figure img')['src'] or element.select('a div.Image figure img')['data-cfsrc'],
                    'banner': (element.select_one('a div.Image figure img')['src'] or element.select('a div.Image figure img')['data-cfsrc']).replace('covers' , 'banners').strip(),
                    'type': element.select_one('div.Description p span.Type').string,
                    'synopsis': element.select('div.Description p')[1].string,
                    'rating': element.select_one('div.Description p span.Vts').string,
                    'debut': element.select_one('a span.Estreno').string.lower() if element.select_one('a span.Estreno') else None
                })
            except Exception:
                pass

        return ret

    def get_video_servers(
        self,
        id,
        format: EpisodeFormat = EpisodeFormat.Subtitled,
        **kwargs,
    ):
        """
        Get in video servers, this work only using the iframe element.
        Return a list of dictionaries.

        :param id: Anime id, like as 'nanatsu-no-taizai'.
        :param episode: Episode id, like as '1'.
        :rtype: list
        """

        response = self._scraper.get(f"{ANIME_VIDEO_URL}{id}")
        soup = BeautifulSoup(response.text, "lxml")
        scripts = soup.find_all("script")

        servers = []

        for script in scripts:
            content = str(script)
            if "var videos = {" in content:
                videos = content.split("var videos = ")[1].split(";")[0]
                data = json.loads(videos)

                if "SUB" in data and EpisodeFormat.Subtitled in format:
                    servers.append(data["SUB"])
                if "LAT" in data and EpisodeFormat.Dubbed in format:
                    servers.append(data["LAT"])

        return servers

    def getLatestEpisodes(self):
            """
            List of the latest episodes uploaded by the platform
            """
            res = self._scraper.get(f"{BASE_URL}")
            body = res.text
            soup = BeautifulSoup(body, 'lxml')
            elements = soup.select("main.Main ul.ListEpisodios li")
            response = []
            for element in elements:
                try:
                    response.append({
                        'id': element.select_one('a.fa-play')['href'][1:],
                        'title': element.select_one('a.fa-play strong.Title').string,
                        'chapter': element.select_one('a.fa-play span.Capi').string,
                        'image':  element.select("a.fa-play span.Image img"),
                    })
                except Exception:
                    pass
            return response

    def ultimateAnime(self):
            """
            List of the ultimate added anime
            """
            res = self._scraper.get(f"{BASE_URL}")
            body = res.text
            soup = BeautifulSoup(body, 'lxml')
            elements = soup.select('main.Main ul.ListAnimes li article.alt')
            response = []
            for element in elements:
                try:
                    response.append({
                        'id': element.select_one('a')['href'][1:],
                        'title': element.select_one('a h3.Title').string,
                        'image': BASE_URL + element.select_one('a div.Image figure img')['src'],
                        'type': element.select_one('a span.Type').string,
                    })
                except Exception:
                    pass
            return response
    def emissionAnime(self):
        """
        List of the ultimate added anime
        """
        res = self._scraper.get(f"{BASE_URL}")
        body = res.text
        soup = BeautifulSoup(body, 'lxml')
        elements = soup.select('div.BFluid aside.BFixed div.Emision div.Bod ul.ListSdbr li')
        response = []
        for element in elements:
           try:
                response.append({
                    'id': element.select_one('a')['href'][1:],
                    'title': element.select_one('a.fa-play-circle').contents[0],
                    'type': element.select_one('a span.Type').string,
                })
           except Exception:
               pass
        return response

    def allAnime(self,id=1):
        """
            get all animes
        """
        res = self._scraper.get(f"{ORDER_TITLE}{id}")
        body = res.text
        soup = BeautifulSoup(body, 'lxml')
        elements = soup.select('main.Main ul.ListAnimes li article.Anime')
        response = []
        for element in elements:
            try:
                response.append({
                    'id': element.select_one('a')['href'][1:],
                    'title': element.select_one('a h3.Title').string,
                    'image': element.select_one('a div.Image figure img')['src'],
                    'type': element.select_one('a div.Image span.Type').string,
                    'synopsis': element.select('div.Description p')[1].string,
                    'total': soup.select_one('main.Main div.NvCnAnm ul.pagination li:nth-last-of-type(2)').string
                })
            except Exception:
                pass
        return response

    def get_latest_episodes(self) -> List[EpisodeInfo]:
        """
        Get a list of new episodes released (possibly this last week).
        Return a list

        :rtype: list
        """

        response = self._scraper.get(BASE_URL)
        soup = BeautifulSoup(response.text, "lxml")

        elements = soup.select("ul.ListEpisodios li a")
        ret = []

        for element in elements:
            try:
                anime, _, id = element["href"].rpartition("-")

                ret.append(
                    EpisodeInfo(
                        id=id,
                        anime=removeprefix(anime, "/ver/"),
                        image_preview=f"{BASE_URL}{element.select_one('span.Image img').get('src')}",
                    )
                )
            except Exception as exc:
                raise AnimeFLVParseError(exc)

        return ret

    def get_latest_animes(self) -> List[AnimeInfo]:
        """
        Get a list of new animes released.
        Return a list

        :rtype: list
        """

        response = self._scraper.get(BASE_URL)
        soup = BeautifulSoup(response.text, "lxml")

        elements = soup.select("ul.ListAnimes li article")

        if elements is None:
            raise AnimeFLVParseError("Unable to get list of animes")

        return self._process_anime_list_info(elements)

    def getAnimeInfo(self, id):
        """
        Get information about specific anime.
        Return a dictionary.
        :param id: Anime id, like as 'anime/1590/nanatsu-no-taizai'.
        :rtype: dict
        """
        episodes, genres, extraInfo = self.__getAnimeEpisodesInfo__(id)
        data = []
        for info in extraInfo:
            try:
                data.append({
                    'title': info['title'],
                    'poster': info['poster'],
                    'synopsis': info['synopsis'],
                    'debut': info['debut'],
                    'type': info['type'],
                })
            except Exception:
                pass
        data.append({
            'id': id,
            'genres': genres or None,
            'episodes': episodes or None
        })

        return data

    def __getAnimeEpisodesInfo__(self, id):
        res = self._scraper.get(f"{ANIME_URL}/{id}")
        body = res.text
        soup = BeautifulSoup(body, 'lxml')
        elements = soup.select('body div.Wrapper div.Body div')
        extraInfo = []
        for element in elements:
            try:
                extraInfo.append({
                    'title': element.select_one('div.Ficha.fchlt div.Container h1.Title').string,
                    'poster': BASE_URL + element.select_one('div.Container div.BFluid aside.SidebarA div.AnimeCover div.Image figure img')['src'],
                    'synopsis': element.select_one('div.Container div.Sp20 main.Main section.WdgtCn div.Description p').string,
                    'debut': element.select_one("div.Container div.Sp20 aside.SidebarA p.AnmStts span.fa-tv").string,
                    'type': element.select_one("div.Ficha.fchlt div.Container span.Type").string,
                })
            except Exception:
                pass

        genres = []

        for element in soup.select('main.Main section.WdgtCn nav.Nvgnrs a'):
            if '=' in element['href']:
                genres.append(element['href'].split('=')[1])

        info_ids = []
        episodes_data = []
        episodes = []

        try:
            for script in soup.find_all('script'):
                contents = str(script)

                if 'var anime_info = [' in contents:
                    anime_info = contents.split('var anime_info = ')[1].split(';')[0]
                    info_ids.append(json.loads(anime_info))

                if 'var episodes = [' in contents:
                    data = contents.split('var episodes = ')[1].split(';')[0]
                    episodes_data.extend(json.loads(data))

            AnimeThumbnailsId = info_ids[0][0]
            animeId = info_ids[0][2]
            # nextEpisodeDate = info_ids[0][3] if len(info_ids[0]) > 4 else None

            for episode, id in episodes_data:
                episodes.append({
                    'episode': episode,
                    'id': f'{id}/{animeId}-{episode}',
                    'imagePreview': f'{BASE_EPISODE_IMG_URL}{AnimeThumbnailsId}/{episode}/th_3.jpg'
                })
        except Exception:
            pass

        return (episodes, genres, extraInfo)

    def _process_anime_list_info(self, elements: ResultSet) -> List[AnimeInfo]:
        ret = []

        for element in elements:
            try:
                ret.append(
                    AnimeInfo(
                        id=removeprefix(
                            element.select_one("div.Description a.Button")["href"][1:],
                            "anime/",
                        ),
                        title=element.select_one("a h3").string,
                        poster=(
                            element.select_one("a div.Image figure img").get(
                                "src", None
                            )
                            or element.select_one("a div.Image figure img")["data-cfsrc"]
                        ),
                        banner=(
                            element.select_one("a div.Image figure img").get(
                                "src", None
                            )
                            or element.select_one("a div.Image figure img")["data-cfsrc"]
                        )
                        .replace("covers", "banners")
                        .strip(),
                        type=element.select_one("div.Description p span.Type").string,
                        synopsis=(
                            element.select("div.Description p")[1].string.strip()
                            if element.select("div.Description p")[1].string
                            else None
                        ),
                        rating=element.select_one("div.Description p span.Vts").string,
                        debut=(
                            element.select_one("a span.Estreno").string.lower()
                            if element.select_one("a span.Estreno")
                            else None
                        ),
                    )
                )
            except Exception as exc:
                raise AnimeFLVParseError(exc)

        return ret
