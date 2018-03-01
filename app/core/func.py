from urllib.parse import unquote
import re


def _get_name(li):
    a = li.find("a")
    if a:
        return a.text.strip()


def _get_path(li):
    a = li.find("a")
    if not a:
        return

    path = a.get("href")

    # если есть url
    if path.startswith("/url?"):
        m = re.match('/url\?(url|q)=(.+?)&', path)
        if m and len(m.groups()) == 2:
            return unquote(m.group(2))
