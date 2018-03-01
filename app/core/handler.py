from aiohttp import web, ClientSession
from aiohttp_jinja2 import render_template
from app.core.queries import QUERY
import traceback


class AggregatorOfSearchEngines(web.View):

    async def get(self):
        engines, result = (
            "google",
            # "yandex",
        ), {}

        for schema in engines:
            try:
                # получаем url для запроса в поисковую машину
                url = self._execute(
                    schema,
                    QUERY.get_url,
                    {"text": self.request.text, "num": self.request.num,},
                )["url"]["urlString"]

                # делаем запрос
                html = await self._make_request(url)

                # парсим ответ
                data = self._execute(
                    schema,
                    QUERY.parse_html,
                    {"html": html,},
                )
                data = data["parser"]["data"]

            except Exception as e:
                traceback.print_exc()

            else:
                # в случае успеха добавляем данные
                result[schema] = data

        context = {"schemes": [result,]}
        template = "html/result.html"

        return render_template(template, self.request, context)

    def _execute(self, schema, query, variable_values={}):
        schema = self.request.app["search_engines"].get(schema)
        result = schema.execute(
            query,
            variable_values=variable_values,
        )

        return result.data

    async def _make_request(self, url):
        headers = {
            "User-Agent": "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101",
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.text()

        return text
