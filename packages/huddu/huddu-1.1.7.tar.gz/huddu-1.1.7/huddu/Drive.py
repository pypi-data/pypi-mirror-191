from ._exceptions import DriveException
from ._sessions import Session
from .utils import get_headers_from_one_string_token


class Drive:
    def __init__(
            self,
            token: str,
            base_url: str = "https://drive.huddu.io",
    ) -> None:
        """
        This class provides a simple way to interface with the **Store API** in python
        The endpoint for the drive api is: https://drive.huddu.io
        :param token:
        :param base_url:
        """
        self.session = Session(
            headers=get_headers_from_one_string_token(token),
            base_url=base_url,
        )

    def upload(
            self, name: str, data: str = "", path: str = None, safe: bool = True, chunk_size: int = int(1e7)
    ) -> None:
        """
        Upload a file with name by specifying one of data or path
        If safe is True (which it is by default). Files with the same name won't be overridden
        :param name:
        :param data:
        :param path:
        :param safe:
        :param chunk_size:
        :return:
        """
        if safe:
            if self.read(name):  # check for first chunk
                raise DriveException("Another entry with the same id already exists")

        file_data = data
        if path:
            file_data = open(path).read()

        if not file_data:
            raise DriveException("One of data or path has to be specified")
        if chunk_size > 1e7:
            print("It's not recommended to use a chunk size of more than 1e7 bytes")

        file_items = [
            file_data[i: i + chunk_size] for i in range(0, len(file_data), chunk_size)
        ]

        for i in range(0, len(file_items)):
            self.session.request(
                "POST",
                "/upload",
                data={
                    "name": f"{name}__chunk__{i}",
                    "data": file_items[i],
                },
            )

    def delete(self, name: str) -> None:
        """
        Delete a file by name
        :param name:
        :return:
        """
        has_more = True
        run = 0

        while has_more:
            try:
                self.session.request("DELETE", f"/{name}__chunk__{run}")
                run += 1
            except Exception:
                has_more = False

    def read_iterator(self, name: str):
        """
        Iterate over a file by name
        :param name:
        :return:
        """
        has_more = True
        run = 0

        while has_more:
            try:
                yield self.session.request("GET", f"/{name}__chunk__{run}")["data"]
                run += 1
            except Exception:
                has_more = False

    def read(self, name: str):
        """
        Read the entire file by name
        :param name:
        :return:
        """
        response = ""
        for i in self.read_iterator(name):
            response += i

        return response
