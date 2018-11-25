from django.http import QueryDict
from rest_framework import parsers
from rest_framework.utils import json


class MultipartJsonParser(parsers.MultiPartParser):
    # https://stackoverflow.com/a/50514022/8897256

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}

        # find the data field and parse it
        data = json.loads(result.data["data"])

        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        return parsers.DataAndFiles(qdict, result.files)