from app.core.func import _get_name, _get_path
from graphene.types import Scalar
from bs4 import BeautifulSoup
from yarl import URL
import graphene


class Result(Scalar):

    @staticmethod
    def serialize(data):
        return data


class Data(graphene.ObjectType):

    url_string = graphene.String()
    data = graphene.List(Result)


class Google(graphene.ObjectType):
    """
    Схема для поика по Google
    """

    url = graphene.Field(Data, text=graphene.String(), num=graphene.Int())
    parser = graphene.Field(Data, html=graphene.String())

    def resolve_url(self, info, text, num):
        params = {
            'nl': "en",
            'q': text,
            'start': 0, # page * num
            'num': num,
        }

        url = URL("http://www.google.com/search").with_query(params)

        return Data(url_string=url)

    def resolve_parser(self, info, html):
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.findAll("div", attrs={"class": "g"})

        parse_data = [
            {"name": _get_name(li), "path": _get_path(li),}
                for li in divs
        ]

        return Data(data=parse_data)


class Yandex(graphene.ObjectType):
    """
    Схема для поика по Yandex
    """

    url = graphene.Field(Data, text=graphene.String(), num=graphene.Int())
    parser = graphene.Field(Data, html=graphene.String())

    def resolve_url(self, info, text, num):
        params = {
            "text": text,
            # "": num,
        }

        url = URL("https://yandex.ru/yandsearch").with_query(params)

        return Data(url_string=url)

    def resolve_parser(self, info, html):
        soup = BeautifulSoup(html, "html.parser")

        divs = soup.findAll("h2", attrs={"class": "organic__title-wrapper typo typo_text_l typo_line_m"})

        # parse_data = [
        #     {"name": _get_name(li), "path": _get_path(li),}
        #         for li in divs
        # ]

        return Data(data=parse_data)
