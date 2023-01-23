import os
import json

from enum import Enum
from typing import Dict, Optional
import time

from pydantic import BaseModel, ValidationError
import jwt
import httpx

from utils.tools.configManager import ConfigReader, BASE_DIR
from utils.tools.singletonType import SingletonType


class PushType(str, Enum):
    alert = 'alert'
    background = 'background'


class TokenInfo(BaseModel):
    token: str
    timestamp: float


class AppleAPNsHelper(metaclass=SingletonType):
    def __init__(self):
        config = ConfigReader()
        self._base_url = config.get_config('AppleServiceConfig', 'baseUrl')

        self.auth_key_id = config.get_config('AuthKeyConfig', 'KeyId')
        self.team_id = config.get_config('AuthKeyConfig', 'TeamId')
        self.app_id = config.get_config('AuthKeyConfig', 'AppId')

        with open(str(BASE_DIR) + config.get_config('AuthKeyConfig', 'KeyPath'), 'r') as f:
            self.auth_key = f.read()

        self.apns_token_save_path = str(BASE_DIR) + config.get_config('AuthKeyConfig', 'TokenSavePath')

        if os.path.exists(self.apns_token_save_path):
            with open(self.apns_token_save_path, 'r') as f:
                temp = json.loads(f.read())
                try:
                    self._token_info = TokenInfo(**temp)
                except ValidationError:
                    self._token_info = None
        else:
            self._token_info = None

    def _creat_token(self) -> TokenInfo:
        timestamp = time.time()
        local_token = jwt.encode(
            {
                'iss': self.team_id,
                'iat': int(timestamp)
            },
            self.auth_key,
            algorithm='ES256',
            headers={
                'alg': 'ES256',
                'kid': self.auth_key_id,
            }
        )
        return TokenInfo(token=local_token, timestamp=timestamp)

    @property
    def token(self) -> str:
        token_info: Optional[TokenInfo] = self._token_info
        if token_info is None or (time.time() - token_info.timestamp) >= 3600:
            self._token_info = self._creat_token()
            token_info = self._token_info
            with open(self.apns_token_save_path, 'w') as f:
                f.write(self._token_info.json())
        return token_info.token

    async def send_message(self,
                           device_id: str, data: Dict, push_type: PushType = PushType.alert, priority: int = 10,
                           expiration: int = 0):
        url = self._base_url + device_id
        async with httpx.AsyncClient(http2=True) as client:

            headers = {
                'authorization': 'bearer {0}'.format(self.token),
                'apns-push-type': push_type.value,
                'apns-expiration': str(expiration),
                'apns-priority': str(priority),
                'apns-topic': self.app_id
            }
            res = await client.post(url, json=data, headers=headers)
            print(res.content)
