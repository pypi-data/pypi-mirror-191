class ValueObject:
    def __init__(self, value=None):
        self.value = value
        self.is_writable = True
        self.is_changeable = True
        self.is_unique = False
    
    def get_value(self):
        return self.value

    def __eq__(self, other):
        if other is None:
            return False
        if not hasattr(other, 'value'):
            return False
        return self.value == other.value

    def __str__(self) -> str:
        return self.value


    def __repr__(self) -> str:
        return str(self.value)


class U(ValueObject):
    pass


class UInt(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, int):
            raise ValueError('Value should be int type')
        super().__init__(value)


class UFloat(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, float):
            raise ValueError('Value should be float type')
        super().__init__(value)


class UStr(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, str):
            raise ValueError('Value should be str type')
        super().__init__(value)


class UDict(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, dict):
            raise ValueError('Value should be dict type')
