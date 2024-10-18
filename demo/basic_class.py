import pydantic as pd


class BasicClass(pd.BaseModel):
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


class BasicMixedAnnotatedClass(BasicClass):
    my_parameter_4: str = pd.Field("" , description="This is my field parameter.", json_schema_extra={})
