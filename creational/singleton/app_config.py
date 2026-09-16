class AppConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        self.debug = False
        self.api_key = None
        self._initialized = True  # 한번 초기화되면 그 이후엔 초기화 하지 않기 위한 장치
