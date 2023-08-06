class user:
    __name__ = ''
    def __init__(self,name) -> None:
        self.__name__ = name
    def set_namm(self,name):
        self.__name__ = name
    def get_name(self):
        return self.__name__
        