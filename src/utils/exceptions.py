class Conflict(Exception):

    def __init__(self, *args, **kwargs):
        self.status = kwargs['status']
        del kwargs['status']
        super().__init__(*args, **kwargs)


class InvalidBody(Exception):

    def __init__(self, *args, **kwargs):
        self.status = kwargs['status']
        del kwargs['status']
        super().__init__(*args, **kwargs)
