import time
from enum import Enum
from urllib import parse

from sihodictapi import utils


class Foxit:
    """
    福昕翻译
    https://fanyi.pdf365.cn/free
    """

    class Lang(str, Enum):
        EN = 'en',
        '''英语'''

        CN = 'zh-CN',
        '''中文'''

        CHT = 'cht',
        '''中文繁体'''

        JA = 'ja',
        '''日语'''

        KO = 'ko',
        '''韩语'''

        FR = 'fr',
        '''法语'''

        ES = 'es',
        '''西班牙语'''

        IT = 'it',
        '''意大利语'''

        DE = 'de',
        '''德语'''

        TR = 'tr',
        '''土耳其语'''

        RU = 'ru',
        '''俄语'''

        PT = 'pt',
        '''葡萄牙语'''

        VI = 'vi',
        '''越南语'''

        ID = 'id',
        '''印尼语'''

        TH = 'th',
        '''泰语'''

        MS = 'ms',
        '''马来西亚语'''

        AR = 'ar',
        '''阿拉伯语'''

        EL = 'el',
        '''希腊语'''

        BUL = 'bul',
        '''保加利亚语'''

        FIN = 'fin',
        '''芬兰语'''

        SLO = 'slo',
        '''斯洛文尼亚语'''

        NL = 'nl',
        '''荷兰语'''

        CS = 'cs',
        '''捷克语'''

        SWE = 'swe',
        '''瑞典语'''

        PL = 'pl',
        '''波兰语'''

        DAN = 'dan',
        '''丹麦语'''

        ROM = 'rom',
        '''罗马尼亚语'''

        HU = 'hu',
        '''匈牙利语'''

    @classmethod
    def translate(cls, text: str, from_lang: Lang = None, target_lang: Lang = Lang.CN) -> dict:
        timestamp = int(time.time()) * 1000
        sign = utils.md5(str(timestamp) + 'FOXIT_YEE_TRANSLATE')
        response = utils.request_post('https://fanyi.pdf365.cn/api/wordTranslateResult', data={
            'plateform': 'web',
            'orginL': from_lang or 'auto',
            'targetL': target_lang or cls.Lang.CN,
            'text': parse.quote(text),
            'timestamp': timestamp,
            'sign': sign
        })
        return response.json()
