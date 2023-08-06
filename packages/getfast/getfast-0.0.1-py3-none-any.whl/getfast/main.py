class GetFast:
    def __init__(self, key: str):
        self.key = key

    @staticmethod
    async def init(key: str = None):
        if key is None:
            key = os.environ.get("GETFAST_API_KEY")
        return GetFast(key)

    async def start(self):
        pass

    async def checkpoint(self):
        pass

    async def stop(self):
        pass
