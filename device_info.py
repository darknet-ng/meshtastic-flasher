class DeviceInfo:
    _shared_data = {}

    @classmethod
    def set_data(cls, key, value):
        cls._shared_data[key] = value

    @classmethod
    def get_data(cls, key):
        return cls._shared_data.get(key)
