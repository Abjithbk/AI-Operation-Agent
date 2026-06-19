class Config:
    API_URL = 'http://localhost:8000/api'
    API_KEY=None

    @classmethod
    def init(cls,api_key:str,api_url:str = None):
        cls.API_KEY = api_key
        if api_url:
            cls.API_URL = api_url