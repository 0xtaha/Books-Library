class ValidationError(Exception):
    def __init__(self, message="ValidationError"):
        self.message = message
        super().__init__(self.message)

class ParameterError(Exception):
    def __init__(self, message="ParameterError: Bad parameters "):
        self.message = message
        super().__init__(self.message)


class NoOperation(Exception):
    def __init__(self, message="NoOperation"):
        self.message = message
        super().__init__(self.message)


class AlreadyExists(Exception):
    def __init__(self, message="AlreadyExists: Resource already exists"):
        self.message = message
        super().__init__(self.message)


class DBsavingError(Exception):
    def __init__(
        self,
        message="DBsavingError: Something went wrong while saving to database",
    ):
        self.message = message
        super().__init__(self.message)


class DBError(Exception):
    def __init__(
        self,
        message="DBError: Something went wrong while reading from database",
    ):
        self.message = message
        super().__init__(self.message)

class NotFound(Exception):
    def __init__(self, message="ContentNotFound: Cannot find resource"):
        self.message = message
        super().__init__(self.message)

class IOPermissionError(Exception):
    def __init__(self, message="IOPermissionError"):
        self.message = message
        super().__init__(self.message)
