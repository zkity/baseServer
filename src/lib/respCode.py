from enum import Enum

class RespCode(Enum):

    # user login 1
    LOGIN_OK = 11
    LOGIN_PARAM_ERR = 12
    LOGIN_PASS_ERR = 13
    LOGIN_USER_ERR = 14

    # user changePass 2
    CHANGE_PASS_OK = 21
    CHANGE_PASS_ORA_ERR = 22
    CHANGE_PASS_USER_ERR = 23
    CHANGE_PASS_NEW_ERR = 24

    # hi sayHi 3
    HI_OK = 31
    HI_ERR = 32
    HELLO_OK = 33
    HELLO_ERR = 34

    # file upload 4
    UPLOAD_FILE_OK = 41
    UPLOAD_FILE_ERR = 42
    UPLOAD_NAME_ERR = 43
    UPLOAD_TYPE_ERR = 44

    # file download 5
    DOWNLOAD_OK = 51
    DOWNLOAD_FILE_ERR = 52
