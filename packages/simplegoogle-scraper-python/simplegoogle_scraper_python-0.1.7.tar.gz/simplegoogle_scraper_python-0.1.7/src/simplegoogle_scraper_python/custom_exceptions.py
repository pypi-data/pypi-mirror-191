class InvalidSearchqueryException(Exception):
    def __init__(self, message: str = "Search query not defined!"):
        self.message = message
        super().__init__(self.message)
