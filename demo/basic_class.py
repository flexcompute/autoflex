import pydantic


class BasicClass(pydantic.BaseModel):
    my_parameter_1: int = 1
    my_parameter_2: str = 2
    my_parameter_3: float = 3.0

    def my_method(self):
        """
        This is my method.
        """
        pass

    @classmethod
    def my_class_method(cls):
        """
        This is my class method.
        """
        pass

    @staticmethod
    def my_static_method():
        """
        This is my static method.
        """
        pass
