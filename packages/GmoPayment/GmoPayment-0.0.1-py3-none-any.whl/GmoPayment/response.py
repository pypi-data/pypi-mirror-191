import urllib.parse as urlparse


class Response:

    def __init__(self, response_text):
        self.data = self.decode(response_text)
        self.ok = bool('ErrCode' not in self.data)

    @staticmethod
    def decode(response_text):
        response_dict = urlparse.parse_qs(response_text)
        return {k: v[0] for k, v in response_dict.items()}

    def parse(self, ignores=[]):
        assert type(self.data) is dict
        assert type(ignores) is list

        result = {}
        for k, v in self.data.items():
            if k in ignores:
                continue

            for i2, v2 in enumerate(str(v).split('|')):
                if i2 not in result:
                    result[i2] = {}
                result[i2][k] = v2

        return list(result.values())

