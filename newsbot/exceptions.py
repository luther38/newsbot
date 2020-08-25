class NewsBotException(Exception):
    """
    This is the base class that all exceptions orignate from.
    """

    pass


class UnableToFindContent(NewsBotException):
    """
    Used when failure to return results from a scrape request.
    """

    pass

