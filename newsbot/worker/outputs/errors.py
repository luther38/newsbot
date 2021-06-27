class DiscordWebHookNotFound(Exception):
    """Raised when the output looks for a discord webhook in the DB but is unable to find any."""

class OutputResponseMessageIsInvalid(Exception):
    """Raised when the response message was not the expected status code."""