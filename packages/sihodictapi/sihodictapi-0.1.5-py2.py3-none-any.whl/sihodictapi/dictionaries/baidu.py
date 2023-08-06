from sihodictapi import utils


class Baidu:
    """百度翻译"""

    langList = {
        'zh': '中文', 'jp': '日语', 'jpka': '日语假名', 'th': '泰语', 'fra': '法语', 'en': '英语', 'spa': '西班牙语', 'kor': '韩语',
        'tr': '土耳其语', 'vie': '越南语', 'ms': '马来语', 'de': '德语', 'ru': '俄语', 'ir': '伊朗语', 'ara': '阿拉伯语', 'est': '爱沙尼亚语',
        'be': '白俄罗斯语', 'bul': '保加利亚语', 'hi': '印地语', 'is': '冰岛语', 'pl': '波兰语', 'fa': '波斯语', 'dan': '丹麦语', 'tl': '菲律宾语',
        'fin': '芬兰语', 'nl': '荷兰语', 'ca': '加泰罗尼亚语', 'cs': '捷克语', 'hr': '克罗地亚语', 'lv': '拉脱维亚语', 'lt': '立陶宛语',
        'rom': '罗马尼亚语', 'af': '南非语', 'no': '挪威语', 'pt_BR': '巴西语', 'pt': '葡萄牙语', 'swe': '瑞典语', 'sr': '塞尔维亚语',
        'eo': '世界语', 'sk': '斯洛伐克语', 'slo': '斯洛文尼亚语', 'sw': '斯瓦希里语', 'uk': '乌克兰语', 'iw': '希伯来语', 'el': '希腊语',
        'hu': '匈牙利语', 'hy': '亚美尼亚语', 'it': '意大利语', 'id': '印尼语', 'sq': '阿尔巴尼亚语', 'am': '阿姆哈拉语', 'as': '阿萨姆语',
        'az': '阿塞拜疆语', 'eu': '巴斯克语', 'bn': '孟加拉语', 'bs': '波斯尼亚语', 'gl': '加利西亚语', 'ka': '格鲁吉亚语', 'gu': '古吉拉特语',
        'ha': '豪萨语', 'ig': '伊博语', 'iu': '因纽特语', 'ga': '爱尔兰语', 'zu': '祖鲁语', 'kn': '卡纳达语', 'kk': '哈萨克语', 'ky': '吉尔吉斯语',
        'lb': '卢森堡语', 'mk': '马其顿语', 'mt': '马耳他语', 'mi': '毛利语', 'mr': '马拉提语', 'ne': '尼泊尔语', 'or': '奥利亚语', 'pa': '旁遮普语',
        'qu': '凯楚亚语', 'tn': '塞茨瓦纳语', 'si': '僧加罗语', 'ta': '泰米尔语', 'tt': '塔塔尔语', 'te': '泰卢固语', 'ur': '乌尔都语',
        'uz': '乌兹别克语', 'cy': '威尔士语', 'yo': '约鲁巴语', 'yue': '粤语', 'wyw': '文言文', 'cht': '中文繁体'
    }
    '''语言列表'''

    @classmethod
    def lang_detect(cls, text):
        """
        语言识别

        :param text: 输入文本
        :return: 识别结果，语言列表见langList
        """
        return utils.request_post('https://fanyi.baidu.com/langdetect', json={'query': text}).json()

    @classmethod
    def translate(cls, text: str, from_lang=None, to_lang=None) -> dict:
        """
        翻译(只支持翻译单行文本)

        :param text: 输入文本
        :param from_lang: 源语言，默认通过lang_detect方法自动识别，语言列表见langList
        :param to_lang: 目标语言，默认若源语言为非中文则目标语言为中文，否则目标语言为英文，语言列表见langList
        """
        if not from_lang:
            from_lang = cls.lang_detect(text).get('lan')
        if not to_lang:
            # 非中文->中文, 中文(也可能是日文)->英文
            to_lang = 'zh' if from_lang != 'zh' else 'en'
        return utils.request_post('https://fanyi.baidu.com/transapi', json={
            'from': from_lang,
            'to': to_lang,
            'query': text,
            'source': 'txt'
        }).json()
