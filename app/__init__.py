from aiohttp import web
from aiohttp_jinja2 import setup as setup_jinja2, render_template
from jinja2 import FileSystemLoader
from app.core.engine import Google, Yandex
from app.core.handler import AggregatorOfSearchEngines
import graphene, argparse


def _parse_argv(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H',
        '--host',
        type=str,
        default="127.0.0.1",
        help="host",
    )
    parser.add_argument(
        '-P',
        '--port',
        type=int,
        default=9091,
        help="port",
    )
    return parser.parse_args()


def run(argv):
    args = _parse_argv(argv)
    app = web.Application(middlewares=[main,])
    app.router.add_view("/search", AggregatorOfSearchEngines)
    app.on_startup.append(_create_scheme)
    setup_jinja2(
        app=app,
        loader=FileSystemLoader("app/static")
    )

    web.run_app(app, host=args.host, port=args.port)


async def _create_scheme(app):
    app["search_engines"] = {
        "google": graphene.Schema(Google),
        "yandex": graphene.Schema(Yandex),
    }


@web.middleware
async def main(request, handler):
    """
    Middleware для проверки параеметрова:
     - search_text текст запроса
     - search_num количество результатов
    """
    text = request.query.get("search_text")
    if not text:
        return render_template("html/home.html", request, {})

    try:
        num = int(request.query.get("search_num", 2))
    except ValueError:
        msg = {"error_msg": "Количество должно быть указано в цифрах",}
        return render_template("html/result.html", request, msg)

    request.text = text
    request.num = num
    return await handler(request)
