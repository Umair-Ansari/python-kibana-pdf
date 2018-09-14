class Response(object):

    def __init__(self):
        self.codes = [200, 400, 500]
        self.messages = ["Success", "Invalid Url", "Server Error"]

    def get_response(self, code, message):
        return dict(code=self.codes[code], message=self.messages[message])

    def get_code(self, code):
        return self.codes[code]


