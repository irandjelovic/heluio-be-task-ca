class UserEmailDuplicateError(Exception):
    pass


class UserNotExistsError(Exception):
    pass


class ItemNotExistsError(Exception):
    pass


class ItemsNotEnoughError(Exception):
    pass


class ItemAlreadyAdded(Exception):
    pass
