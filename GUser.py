class Master:

    def __init__(self):
        self.__name = ''
        self.__sex = ''
        self.__password = ''
        self.__user_type = ''

    def getName(self) -> str:
        return self.__name

    def getSex(self) -> str:
        return self.__sex

    def getPassword(self) -> str:
        return self.__password

    def getUser_type(self) -> int:
        return self.__user_type

    def setName(self, name: str = ''):
        self.__name = name

    def setSex(self, sex: str = ''):
        self.__sex = sex

    def setPassword(self, password: str):
        self.__password = password

    def setUser_type(self, user_type: int):
        self.__user_type = user_type


class GroupLeader(Master):
    def __init__(self):
        super().__init__()
        self.__student_number = ''
        self.__group_number = ''
        self.__qq_number = ''

    def getStudent_number(self) -> str:
        return self.__student_number

    def getGroup_number(self) -> str:
        return self.__group_number

    def getQQ_number(self) -> str:
        return self.__qq_number

    def setStudent_number(self, student_number: str = ''):
        self.__student_number = student_number

    def setGroup_number(self, group_number: str = ''):
        self.__group_number = group_number

    def setQQ_number(self, qq_number: str = ''):
        self.__qq_number = qq_number
