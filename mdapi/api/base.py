class APIBase:
    """
    The base class for all API classes.
    """

    def __init__(self, md, api):
        # If we import at the root level we have a circular import!
        from ..mdapi import APIHandler, MdAPI

        self.md: MdAPI = md
        self.api: APIHandler = api
