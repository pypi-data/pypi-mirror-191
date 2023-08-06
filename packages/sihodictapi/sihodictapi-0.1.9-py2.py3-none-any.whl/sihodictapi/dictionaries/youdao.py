from enum import Enum

from sihodictapi import utils


class Youdao:
    """网易有道"""

    class SupportLanguage(str, Enum):
        """支持的语言列表"""

        English = 'en'
        '''中英'''

        French = 'fr'
        '''中法'''

        Korean = 'ko'
        '''中韩'''

        Japanese = 'ja'
        '''中日'''

    @classmethod
    def dict_search(cls, text: str, language: SupportLanguage = SupportLanguage.English) -> dict:
        """
        词典查词

        :param text: 输入文本
        :param language: 语言，默认为中英，支持语言列表见SupportLanguage
        """
        S = "web"
        k = "webdict"
        time = len(text + k) % 10
        x = "Mk6hqtUp33DGGtoS63tTJbMUYjRrG1Lu"
        r = text + k

        resp = utils.request_post(url='https://dict.youdao.com/jsonapi_s?doctype=json&jsonversion=4',
                                  data={
                                      'q': text,
                                      'le': language,
                                      't': time,
                                      'client': S,
                                      'sign': utils.md5(S + text + str(time) + x + utils.md5(r)),
                                      'keyfrom': k
                                  })
        return resp.json()

    @classmethod
    def suggest(cls, text: str, language: SupportLanguage = SupportLanguage.English) -> dict:
        """
        词典查词建议

        :param text: 输入文本
        :param language: 语言，默认为中英，支持语言列表见SupportLanguage
        """
        return utils.request_get(url='https://dict.youdao.com/suggest',
                                 params={
                                     'num': 5,
                                     'ver': '3.0',
                                     'doctype': 'json',
                                     'cache': False,
                                     'le': language,
                                     'q': text
                                 }).content.decode('utf-8')
