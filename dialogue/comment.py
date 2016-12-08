class Comment:
    """
    :ivar comment string
    """

    def __init__(self, comment=None):

        if not isinstance(comment, str) or comment is None:
            raise Exception('Comment must be a string')
        self.comment = comment


