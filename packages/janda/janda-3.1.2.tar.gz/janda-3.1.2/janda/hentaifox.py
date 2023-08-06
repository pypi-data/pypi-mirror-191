from janda.utils.client import *
from janda.utils.request import request

Janda = Api()


class Hentaifox(object):
    """Jandapress Hentaifox API

    Methods
    -------
    get : function
        Get doujin API from Id

    search : function
        Search for doujin wirh query and page number given

    get_random : function
        Get random doujin
    """

    def __init__(self, api_key: str = ""):
        """Initializes the Hentaifox.

        Parameters
        ----------
        api_key : str
            scathach.id API key (optional)
        """
        if api_key == "":
            self.api_key = None
        else:
            self.api_key = api_key
        self.specs = {"api_key": self.api_key}

    async def get(self, book: int) -> str:
        """Get hentaifox doujin book from Id

        example: https://hentaifox.com/gallery/88027/

        Parameters
        ----------
        book : int
            The id number of the doujin.

        Returns
        -------
        str
            reparsed json as string
        """

        self.book = str(book)
        data = await request(Janda.hentaifox + Janda.endpoint_book, self.book)
        return better_object(data)

    async def search(self, query: str, page: int = 1, sort: str = "latest") -> str:
        """Search hentaifox doujin with query and page number given

        example: https://hentaifox.com/search/?q=alter&sort=latest

        Parameters
        ----------
        query : str
            The query to search for

        page : int
            The page number to search

        sort : str
            The sort order to search: latest, popular

        Returns
        -------
        str
            reparsed json as string
        """

        self.query = query
        self.page = page
        self.sort = sort
        self.req = str(self.query + "&page=" +
                       str(self.page) + "&sort=" + self.sort)
        
        data = await request(Janda.hentaifox + Janda.endpoint_search, self.req)
        return better_object(data)

    async def get_random(self) -> str:
        """Get hentaifox random doujin

        Returns
        -------
        str
            reparsed json as string
        """

        data = await request(Janda.hentaifox + Janda.endpoint_random)
        return better_object(data)
