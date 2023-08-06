import re
from enum import Enum

from sihodictapi import utils


class Iciba:
    """金山词霸"""

    Auto = 'auto'
    '''自动检测'''

    Chinese = 'zh'
    '''中文'''

    English = 'en'
    '''英语'''

    French = 'fr'
    '''法语'''

    Japanese = 'ja'
    '''日语'''

    Korean = 'ko'
    '''韩语'''

    German = 'de'
    '''德语'''

    Spanish = 'es'
    '''西班牙语'''

    class Domain(Enum):
        """翻译领域"""

        Common = None
        '''通用领域'''

        Biomedicine = 1
        '''生物医药'''

    support_languages = ['sq', 'ar', 'am', 'acu', 'agr', 'ake', 'amu', 'az', 'ga', 'et', 'ee', 'ojb', 'om', 'or', 'os',
                         'tpi', 'bsn', 'ba', 'eu', 'be', 'mww', 'ber', 'bg', 'is', 'bi', 'bem', 'pl', 'bs', 'fa', 'pot',
                         'br', 'cha', 'cv', 'tn', 'ts', 'tt', 'da', 'de', 'tet', 'dv', 'dik', 'ru', 'djk', 'fr', 'fo',
                         'fil', 'fj', 'fi', 'fy', 'km', 'quw', 'kg', 'jy', 'gu', 'ka', 'kk', 'ht', 'ko', 'ha', 'me',
                         'ky', 'quc', 'gbi', 'gl', 'ca', 'cs', 'kn', 'kek', 'cni', 'cop', 'kbh', 'co', 'otq', 'hr',
                         'ku', 'kab', 'cjp', 'cak', 'la', 'lv', 'lo', 'rn', 'lt', 'ln', 'lg', 'dop', 'lb', 'rw', 'ro',
                         'rmn', 'mg', 'mt', 'gv', 'mr', 'ml', 'ms', 'mhr', 'mam', 'mk', 'mi', 'mn', 'bn', 'my', 'nhg',
                         'af', 'xh', 'zu', 'ne', 'nl', 'no', 'pap', 'pck', 'pa', 'pt', 'ps', 'ny', 'tw', 'chr', 'ja',
                         'sv', 'sm', 'sr', 'crs', 'st', 'sg', 'si', 'mrj', 'eo', 'jiv', 'sk', 'sl', 'sw', 'gd', 'so',
                         'ceb', 'tg', 'ty', 'te', 'ta', 'th', 'to', 'tig', 'tmh', 'tr', 'tk', 'chq', 'wal', 'war', 'uy',
                         'cy', 've', 'wol', 'udm', 'ur', 'uk', 'uz', 'ppk', 'usp', 'es', 'he', 'shi', 'el', 'haw', 'sd',
                         'hu', 'sn', 'syc', 'hy', 'jac', 'ace', 'ig', 'it', 'yi', 'hi', 'su', 'id', 'jv', 'en', 'yua',
                         'yo', 'vi', 'yue', 'ti', 'dje', 'zh', 'cht', 'dz']
    '''支持的语言列表'''

    @classmethod
    def translate(cls, text: str, from_lang: str = Auto, to_lang: str = Chinese,
                  domain: Domain = Domain.Common) -> dict:
        """
        翻译

        :param text: 输入文本
        :param from_lang: 源语言(默认为自动检测)
        :param to_lang: 翻译为(默认为中文)
        :param domain: 领域(默认为通用领域)
        """
        if from_lang not in cls.support_languages:
            from_lang = cls.Auto
        if to_lang not in cls.support_languages:
            to_lang = cls.Chinese
        sign = utils.md5('6key_web_fanyi' + 'ifanyiweb8hc9s98e' + re.compile('(^\s*)|(\s*$)').sub('', text))[:16]
        return utils.request_post(
            f'http://ifanyi.iciba.com/index.php?c=trans&m=fy&client=6&auth_user=key_web_fanyi&sign={sign}', data={
                'from': from_lang,
                'to': to_lang,
                'q': text,
                'headerDomain': domain.value
            }).json()
