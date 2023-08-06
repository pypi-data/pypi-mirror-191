from enum import Enum

from sihodictapi import utils


class Hujiang:
    """沪江小D"""

    class Lang(str, Enum):
        CN = 'cn'
        '''中文(简体)'''

        CHT = 'cht'
        '''中文(繁体)'''

        EN = 'en'
        '''英文'''

        JP = 'jp'
        '''日语'''

        KR = 'kr'
        '''韩语'''

        FR = 'fr'
        '''法语'''

        DE = 'de'
        '''德语'''

        ES = 'es'
        '''西班牙语'''

        TH = 'th'
        '''泰语'''

        RU = 'ru'
        '''俄语'''

        PT = 'pt'
        '''葡萄牙语'''

    cookies = {
        'HJ_UID': '0'
    }

    @classmethod
    def translate(cls, text: str, from_lang: Lang, to_lang: Lang) -> dict:
        return utils.request_post(f"https://dict.hjenglish.com/v10/dict/translation/{from_lang}/{to_lang}", data={
            'content': text
        }, cookies=cls.cookies).json()
