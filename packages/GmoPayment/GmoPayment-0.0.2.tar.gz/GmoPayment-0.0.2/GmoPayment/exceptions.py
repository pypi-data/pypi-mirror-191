from .errors import Error


class GMOPGException(Exception):
    pass


class ResponseError(GMOPGException):

    def __init__(self, response):
        self.error = self.parse(response.data)

    def __str__(self):
        return "Response contains Error: " + repr(self.error)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def parse(response):
        dict_list = [Error(i).to_dict() for i in response['ErrInfo'].split('|')]
        return {k: v for dic in dict_list for k, v in dic.items()}
