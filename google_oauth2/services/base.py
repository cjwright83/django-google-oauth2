class Service(object):
    def __init__(self, auth_session, context=None):
        if context is None:
            context = {}
        self.context = context
        self.auth_session = auth_session
        self.errors = []

    def process_api_calls(self):
        raise NotImplementedError('Service class requires implementation.')
