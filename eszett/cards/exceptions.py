class CardNotFoundError(Exception):
    def __init__(self):
        Exception.__init__(self)
