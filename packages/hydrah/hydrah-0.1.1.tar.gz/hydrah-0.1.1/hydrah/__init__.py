from typing import Any, List, TypeVar, Generic, Union, Optional
import datetime 

T = TypeVar("T")

class HydraData(Generic[T]):
    def __init__(self, data: T, message: str = ""):
        self.data = data
        self.message = message

    def parse(self) -> T:
        if self.message:
            raise Exception(self.message)
        return self.data
    
class HydraBaseValidator(Generic[T]):
    def parse(self, data: T) -> HydraData[T]:
        if not self.is_valid(data):
            return HydraData(data, self.get_error_message(data))
        return HydraData(data)

    def is_valid(self, data: T) -> bool:
        raise NotImplementedError

    def get_error_message(self, data: T) -> str:
        raise NotImplementedError

    def convert(self, data: T) -> T:
        raise data
    
    def optional(self) -> "HydraOptionalValidator[T]":
        return HydraOptionalValidator(self)

class HydraOptionalValidator(HydraBaseValidator[Optional[T]]):
    def __init__(self, validator: HydraBaseValidator[T]):
        self.validator = validator

    def is_valid(self, data: Optional[T]) -> bool:
        # if data is None:
        #     return True
        # return self.validator.is_valid(data)
        return data is None or self.validator.is_valid(data)

    def get_error_message(self, data: Optional[T]) -> str:
        if data is None:
            return ""
        return self.validator.get_error_message(data)

    def convert(self, data: Optional[T]) -> Optional[T]:
        if data is None:
            return None
        return self.validator.convert(data)

class HydraStringValidator(HydraBaseValidator[str]):
    def is_valid(self, data: str) -> bool:
        return isinstance(data, str)

    def get_error_message(self, data: str) -> str:
        return f"Expected string, but got {type(data).__name__}"

    def convert(self, data: Any) -> str:
        if isinstance(data, str):
            return data
        return str(data)

class HydraIntegerValidator(HydraBaseValidator[int]):
    def is_valid(self, data: int) -> bool:
        return isinstance(data, int)

    def get_error_message(self, data: int) -> str:
        return f"Expected integer, but got {type(data).__name__}"

    def convert(self, data: Any) -> int:
        if isinstance(data, int):
            return data
        try:
            return int(data)
        except ValueError:
            raise Exception(f"Expected number, but got {type(data).__name__}")

class HydraFloatValidator(HydraBaseValidator[float]):
    def is_valid(self, data: float) -> bool:
        return isinstance(data, float)

    def get_error_message(self, data: float) -> str:
        return f"Expected float, but got {type(data).__name__}"

    def convert(self, data: Any) -> float:
        if isinstance(data, float):
            return data
        try:
            return float(data)
        except ValueError:
            raise Exception(f"Expected number, but got {type(data).__name__}")

class HydraNumberValidator(HydraBaseValidator[float]):
    def is_valid(self, data: Union[float, int]) -> bool:
        return isinstance(data, float) or isinstance(data, int)

    def get_error_message(self, data: Union[float, int]) -> str:
        return f"Expected number, but got {type(data).__name__}"
    
    def convert(self, data: Any) -> float:
        if isinstance(data, float):
            return data
        try:
            return float(data)
        except ValueError:
            raise Exception(f"Expected number, but got {type(data).__name__}")

class HydraBooleanValidator(HydraBaseValidator[bool]):
    def is_valid(self, data: bool) -> bool:
        return isinstance(data, bool)

    def get_error_message(self, data: bool) -> str:
        return f"Expected boolean, but got {type(data).__name__}"
    
    def convert(self, data: Any) -> bool:
        # if data is null or undefined return false
        if not data:
            return False
        if isinstance(data, bool):
            return data
        if isinstance(data, str):
            if data.lower() == "true":
                return True
            if data.lower() == "false":
                return False
        return True

class HydraDatetimeValidator(HydraBaseValidator[datetime.datetime]):
    def is_valid(self, data: Union[str, datetime.datetime]) -> bool:
        data_ = data
        # try to pass the input through the converter
        try:
            if isinstance(data_, str):
                data_ = datetime.datetime.fromisoformat(data)
        except Exception:
            pass
        return isinstance(data_, datetime.datetime)

    def get_error_message(self, data: datetime.datetime) -> str:
        return f"Expected datetime, but got {type(data).__name__}"

    def convert(self, data: T) -> T:
        if isinstance(data, datetime.datetime):
            return data
        try:
            return datetime.datetime.fromisoformat(data)
        except ValueError:
            raise Exception(f"Expected datetime, but got {type(data).__name__}")

class HydraDateValidator(HydraBaseValidator[datetime.date]):
    def is_valid(self, data: Union[str, datetime.date]) -> bool:
        # try to pass the input through the converter
        try:
            data = self.convert(data)
        except Exception:
            pass
        return isinstance(data, datetime.date)

    def get_error_message(self, data: datetime.date) -> str:
        return f"Expected date, but got {type(data).__name__}"
    
    def convert(self, data: T) -> T:
        if isinstance(data, datetime.date):
            return data
        try:
            return datetime.date.fromisoformat(data)
        except ValueError:
            raise Exception(f"Expected date, but got {type(data).__name__}")

class HydraTimeValidator(HydraBaseValidator[datetime.time]):
    def is_valid(self, data: Union[str, datetime.time]) -> bool:
        # try to pass the input through the converter
        try:
            data = self.convert(data)
        except Exception:
            pass
        return isinstance(data, datetime.time)

    def get_error_message(self, data: datetime.time) -> str:
        return f"Expected time, but got {type(data).__name__}"
    
    def convert(self, data: T) -> T:
        if isinstance(data, datetime.time):
            return data
        try:
            return datetime.time.fromisoformat(data)
        except ValueError:
            raise Exception(f"Expected time, but got {type(data).__name__}")

class HydraNoneValidator(HydraBaseValidator[None]):
    def is_valid(self, data: None) -> bool:
        return data is None

    def get_error_message(self, data: None) -> str:
        return f"Expected None, but got {type(data).__name__}"
    
    def convert(self, data: T) -> T:
        return None

class HydraAnyValidator(HydraBaseValidator[object]):
    def is_valid(self, data: object) -> bool:
        return True

    def get_error_message(self, data: object) -> str:
        return ""
    
    def convert(self, data: T) -> T:
        return data

class HydraNeverValidator(HydraBaseValidator[object]):
    def is_valid(self, data: object) -> bool:
        return False

    def get_error_message(self, data: object) -> str:
        return f"Expected nothing, but got {type(data).__name__}"
    
class HydraListValidator(HydraBaseValidator[List[T]]):
    def __init__(self, item_validator: HydraBaseValidator[T]):
        self.item_validator = item_validator

    def is_valid(self, data: List[T]) -> bool:
        if not isinstance(data, list):
            return False
        for item in data:
            if not self.item_validator.is_valid(item):
                return False
        return True

    def get_error_message(self, data: List[T]) -> str:
        if not isinstance(data, list):
            return f"Expected list, but got {type(data).__name__}"
        for item in data:
            if not self.item_validator.is_valid(item):
                return self.item_validator.get_error_message(item)
        return ""


class HydraObjectValidator(HydraBaseValidator[dict]):
    def __init__(self, schema: dict):
        self.schema = schema

    def is_valid(self, data: dict) -> bool:
        if not isinstance(data, dict):
            return False
        for key, validator in self.schema.items():
            if isinstance(validator, HydraOptionalValidator):
                if key not in data:
                    continue
            if key not in data:
                return False
            if not validator.is_valid(data[key]):
                self.error_key = key
                return False
        return True
    
    def get_error_message(self, data: dict) -> str:
        return self.schema[self.error_key].get_error_message(data[self.error_key])

def coerce(data: Any, validator: HydraBaseValidator[T]) -> T:
    return validator.convert(data)


class h:
    @staticmethod
    def string() -> HydraStringValidator:
        return HydraStringValidator()

    @staticmethod
    def integer() -> HydraIntegerValidator:
        return HydraIntegerValidator()

    @staticmethod
    def number() -> HydraNumberValidator:
        return HydraNumberValidator()
    
    @staticmethod
    def float() -> HydraFloatValidator:
        return HydraFloatValidator()

    @staticmethod
    def boolean() -> HydraBooleanValidator:
        return HydraBooleanValidator()

    @staticmethod
    def list(item_validator: HydraBaseValidator[T]) -> HydraListValidator[T]:
        return HydraListValidator(item_validator)
    
    @staticmethod
    def object(schema: dict) -> HydraObjectValidator:
        return HydraObjectValidator(schema)
    
    @staticmethod
    def datetime() -> HydraDatetimeValidator:
        return HydraDatetimeValidator()

    @staticmethod
    def date() -> HydraDateValidator:
        return HydraDateValidator()

    @staticmethod
    def time() -> HydraTimeValidator:
        return HydraTimeValidator()
    
    @staticmethod
    def none() -> HydraNoneValidator:
        return HydraNoneValidator()

    @staticmethod
    def any() -> HydraAnyValidator:
        return HydraAnyValidator()
    
    @staticmethod
    def never() -> HydraNeverValidator:
        return HydraNeverValidator()

    @staticmethod
    def coerce(data: Any, validator: HydraBaseValidator[T]) -> T:
        return coerce(data, validator)
    
    @staticmethod
    def optional(validator: HydraBaseValidator[T]) -> HydraOptionalValidator[Optional[T]]:
        return HydraOptionalValidator(validator)