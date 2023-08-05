from enum import IntEnum, Enum

from sihodictapi import utils


class Moji:
    """Moji辞書"""

    g_os = 'PCWeb'
    g_ver = 'v4.4.2.20230116'
    _ApplicationId = 'E62VyFVLMiW7kvbtVq3p'
    _ClientVersion = 'js3.4.1'
    _InstallationId = 'e5272306-1a0e-402a-a659-6a12a21ff1e8'
    _SessionToken = None

    class DataType(IntEnum):
        """数据类型"""

        Word = 102
        '''词'''

        Example = 103
        '''例句'''

        Grammar = 106
        '''文法'''

        Sentence = 120
        '''句子'''

    search_types = [DataType.Word, DataType.Grammar, DataType.Example]
    '''支持搜索的DataType'''

    class VoiceId(str, Enum):
        """tts发音选择"""

        Female = 'f000'
        '''女生发音'''

        Male = 'm000'
        '''男生发音'''

    @classmethod
    def login(cls, email: str, password: str):
        """
        登录

        :param email: 邮箱
        :param password: 密码
        """
        cls._SessionToken = utils.request_post('https://api.mojidict.com/parse/functions/login', json={
            'email': email,
            'passwd': password,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId
        }).json().get('result').get('result').get('token')

    @classmethod
    def union_api(cls, *functions: dict) -> dict:
        """
        调用多个API

        :param functions: 每个结构为：{'name': API名, 'params': dict类型的参数列表}，可参考union_search方法
        """
        return utils.request_post('https://api.mojidict.com/parse/functions/union-api', json={
            'functions': functions,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def union_search(cls, text: str) -> dict:
        """
        综合搜索，包括：词、文法、例句、一道题

        :param text: 搜索关键词
        """
        return cls.union_api(
            {'name': 'search-all', 'params': {'text': text, 'types': cls.search_types}},
            {'name': 'mojitest-examV2-searchQuestion-v2', 'params': {'text': text, 'limit': 1, 'page': 1}}
        )

    @classmethod
    def search_all(cls, text: str, types: list = None) -> dict:
        """
        根据类型进行搜索搜索，默认搜索词、文法和例句

        :param text: 输入文本
        :param types: 搜搜类型
        :return:
        """
        if types:
            # 过滤不支持搜索的DataType
            types = [t for t in types if t in Moji.search_types]
        return utils.request_post('https://api.mojidict.com/parse/functions/search-all', json={
            'text': text,
            'types': types or cls.search_types,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def search_v3(cls, text: str) -> dict:
        """
        搜索词

        :param text: 输入文本
        """
        return utils.request_post('https://api.mojidict.com/parse/functions/search_v3', json={
            'langEnv': 'zh-CN_ja',
            'searchText': text,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def search_grammar(cls, text: str) -> dict:
        """
        搜索文法

        :param text: 输入文本
        """
        return utils.request_post('https://api.mojidict.com/parse/functions/search-grammar', json={
            'limit': 20,
            'text': text,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def search_example(cls, text: str) -> dict:
        """
        搜索例句

        :param text: 输入文本
        """
        return utils.request_post('https://api.mojidict.com/parse/functions/search-example', json={
            'limit': 20,
            'text': text,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def fetch_words(cls, *object_ids: str) -> dict:
        """
        根据ID获取词或文法的详细信息

        :param object_ids: ID列表
        :return:
        """
        return utils.request_post('https://api.mojidict.com/parse/functions/nlt-fetchManyLatestWords', json={
            'itemsJson': [{'objectId': object_id} for object_id in object_ids],
            'skipAccessories': False,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def fetch_example(cls, example_id: str) -> dict:
        """
        根据ID获取单个例句详细信息

        :param example_id: 例句ID
        """
        return utils.request_post('https://api.mojidict.com/parse/functions/nlt-fetchExample', json={
            'id': example_id,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def fetch_sentences(cls, *ids: str) -> dict:
        """
        根据ID获取句子详细信息

        :param ids: ID列表
        """
        return utils.request_post('https://api.mojidict.com/parse/functions/nlt-fetchManySentences', json={
            'ids': ids,
            'withExtra': True,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def tts_fetch(cls, tar_id: str, tar_type: DataType, voice_id: VoiceId = VoiceId.Female) -> dict:
        """
        获取tts发音

        :param tar_id: 数据ID
        :param tar_type: 数据类型
        :param voice_id: 发音类型
        """
        if tar_type is cls.DataType.Grammar:
            tar_type = cls.DataType.Word
        return utils.request_post('https://api.mojidict.com/parse/functions/tts-fetch', json={
            'tarId': tar_id,
            'tarType': tar_type,
            'voiceId': voice_id,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def word_click_search(cls, text: str):
        """
        在Moji页面中点词/划词时会发情的搜索请求

        :param text: 所选文本
        """
        return utils.request_post('https://api.mojidict.com/parse/functions/word-clickSearch', json={
            'langEnv': 'zh-CN_ja',
            'searchText': text,
            'g_os': cls.g_os,
            'g_ver': cls.g_ver,
            '_ApplicationId': cls._ApplicationId,
            '_ClientVersion': cls._ClientVersion,
            '_InstallationId': cls._InstallationId,
            '_SessionToken': cls._SessionToken,
        }).json()

    @classmethod
    def data_url(cls, tar_id: str, tar_type: DataType) -> str:
        """
        根据数据ID和数据类型获取其页面URL

        :param tar_id: 数据ID
        :param tar_type: 数据类型
        :return: 页面URL
        """
        if tar_type in [cls.DataType.Word, cls.DataType.Grammar]:
            return f'https://www.mojidict.com/details/{tar_id}'
        if tar_type is cls.DataType.Example:
            return f'https://www.mojidict.com/example/{tar_id}'
        if tar_type is cls.DataType.Sentence:
            return f'https://www.mojidict.com/sentence/{tar_id}'
