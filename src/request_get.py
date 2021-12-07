import requests

from requests.exceptions import HTTPError, InvalidURL, ConnectionError
from src.exceptions import url_invalida_ou_indisponivel, indisponibilidade_temporaria


class RequestGet:
    def __init__(self) -> None:
        self.headers = {
            'user-agent': (
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
            )
        }

    def obtem_response(self, url: str) -> bytes:
        try:
            response = requests.get(url, headers=self.headers)
        except HTTPError or InvalidURL or ConnectionError:
            url_invalida_ou_indisponivel()
        if response.status_code >= 500:
            indisponibilidade_temporaria()
        return response.content
