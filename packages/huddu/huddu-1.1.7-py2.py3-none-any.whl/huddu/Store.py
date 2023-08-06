from typing import Union

from ._exceptions import StoreException
from ._sessions import Session
from .utils import get_headers_from_one_string_token


class Store:
    def __init__(
            self,
            token: str,
            base_url: str = "https://store.huddu.io",
    ) -> None:
        """
        This class provides a simple way to interface with the **Store API** in python
        The endpoint for the store api is: https://store.huddu.io
        :param token:
        :param base_url:
        """

        self.session = Session(
            headers=get_headers_from_one_string_token(token),
            base_url=base_url,
        )

    def put(
            self, id: str, data: Union[list, str, dict, int], safe: bool = True
    ) -> None:
        """
        The put method allows you to add data to your store.
        if safe is True (which it is by default), it will first check if an entry with the same name exists
        :param id:
        :param data:
        :param safe:
        :return:
        """
        if safe:
            if self.get(id):
                raise StoreException("Another entry with the same id already exists")

        self.session.request(
            "POST", "/documents", data={"items": [{"id": id, "data": str(data)}]}
        )

    def list(self, limit: int = 25, skip: int = 0) -> list:
        """
        Returns a list of entries
        :return:
        """

        documents = self.session.request(
            "GET", "/documents", params={"skip": skip, "limit": limit}
        )

        res = []
        for i in documents["data"]:
            try:
                res.append(eval(i["data"]))
            except Exception:
                res.append(i["data"])
        return res

    def update(self, id: str, data: str) -> None:
        """
        Updates an entry by id

        :param id:
        :param data:
        :return:
        """
        self.put(id, data, safe=False)

    def delete(self, id: str) -> None:
        """
        Delete an entry by id
        :param id:
        :return:
        """
        self.session.request("DELETE", "/documents", data={"ids": [id]})

    def get(self, id: str):
        """
        Retrieve an entry by id
        :param id:
        :return:
        """
        res = self.session.request("GET", "/documents", params={"ids": id})["data"]

        if len(res) == 0:
            return None

        try:
            res = eval(res[0]["data"])
        except Exception:
            res = res[0]["data"]
        return res
