import lxml.html


class HTMLParser:
    """
    Base class for parsers that need to parse through HTML to get the requested
    information.
    """

    def __init__(self, html):
        self.html = lxml.html.fromstring(html)
