import re

class RequestInvalidException(Exception):
    pass

class Request():
    def __init__(self, request):
        self.__raw_request = request
        self.__path = None
        self.__method = None
        self.__parse()
    
    def __parse(self):
        parts = self.__raw_request.split("\r\n")
        if len(parts) < 1 and len(parts[0].split(' ')) != 3:
            raise RequestInvalidException()
        method, path, params = re.search("(^[A-Z]+)\\s+(/[-a-zA-Z0-9_./=]+)(\?[-a-zA-Z0-9_.=&]*)?", parts[0]).groups()
        self.__path = path
        self.__params = params
        self.__method = method
    
    @property
    def path(self): 
        return self.__path
    
    @property
    def method(self): 
        return self.__method
    
    @property
    def args(self):
        if self.__params:
            values = [v.split("=") for v in self.__params[1:].split("&")]
            return {v[0]: v[1] for v in values}
        return {}

    def empty(self):
        return len(self.__raw_request) == 0
