from collections import namedtuple


QUERY = namedtuple(
    typename="QUERY",
    field_names=(
        "get_url",
        "parse_html",
    ),
)(
    get_url=(
        "query GetURLPath($text: String!, $num: Int!) {"
            " url(text: $text, num: $num) {"
                " urlString"
            " }"
        " }"
    ),
    parse_html=(
        "query ParseHTML($html: String!) {"
            " parser(html: $html) {"
                " data"
            " }"
        " }"
    ),
)
