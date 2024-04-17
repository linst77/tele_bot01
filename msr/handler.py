import telegram
import asyncio
import yaml
import requests
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

### singleton class for messanger
class Telegram( metaclass=Singleton):

    def __init__( self):
        # token difine from conf
        self.token = None
        self.secret = None
        self.token, self.secret = self.get_config()
        # self.bot = telegram.Bot(self.token)


    def get_config( self):

        with open( 'conf/messanger.yaml') as f:
            deployment_def = yaml.load(f, Loader=yaml.FullLoader)

        return ( deployment_def['token'], deployment_def['secret'])

    def send_message( self, text=None):
        # bot = telegram.Bot(self.token)

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.secret,
            "text": text
        }
        response = requests.post(url, payload)
        return response.json()

        #asyncio.run( self.bot.sendMessage(chat_id=self.secret, text=str( text)))

# master class
class MsrBot( Telegram):
    pass