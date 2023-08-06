from enum import Enum

from sihodictapi import utils


class Google:
    class Lang(str, Enum):
        AF = 'af',
        '''afrikaans'''

        SQ = 'sq',
        '''albanian'''

        AM = 'am',
        '''amharic'''

        AR = 'ar',
        '''arabic'''

        HY = 'hy',
        '''armenian'''

        AZ = 'az',
        '''azerbaijani'''

        EU = 'eu',
        '''basque'''

        BE = 'be',
        '''belarusian'''

        BN = 'bn',
        '''bengali'''

        BS = 'bs',
        '''bosnian'''

        BG = 'bg',
        '''bulgarian'''

        CA = 'ca',
        '''catalan'''

        CEB = 'ceb',
        '''cebuano'''

        NY = 'ny',
        '''chichewa'''

        ZH_CN = 'zh-cn',
        '''chinese (simplified)'''

        ZH_TW = 'zh-tw',
        '''chinese (traditional)'''

        CO = 'co',
        '''corsican'''

        HR = 'hr',
        '''croatian'''

        CS = 'cs',
        '''czech'''

        DA = 'da',
        '''danish'''

        NL = 'nl',
        '''dutch'''

        EN = 'en',
        '''english'''

        EO = 'eo',
        '''esperanto'''

        ET = 'et',
        '''estonian'''

        TL = 'tl',
        '''filipino'''

        FI = 'fi',
        '''finnish'''

        FR = 'fr',
        '''french'''

        FY = 'fy',
        '''frisian'''

        GL = 'gl',
        '''galician'''

        KA = 'ka',
        '''georgian'''

        DE = 'de',
        '''german'''

        EL = 'el',
        '''greek'''

        GU = 'gu',
        '''gujarati'''

        HT = 'ht',
        '''haitian creole'''

        HA = 'ha',
        '''hausa'''

        HAW = 'haw',
        '''hawaiian'''

        IW = 'iw',
        '''hebrew'''

        HE = 'he',
        '''hebrew'''

        HI = 'hi',
        '''hindi'''

        HMN = 'hmn',
        '''hmong'''

        HU = 'hu',
        '''hungarian'''

        IS = 'is',
        '''icelandic'''

        IG = 'ig',
        '''igbo'''

        ID = 'id',
        '''indonesian'''

        GA = 'ga',
        '''irish'''

        IT = 'it',
        '''italian'''

        JA = 'ja',
        '''japanese'''

        JW = 'jw',
        '''javanese'''

        KN = 'kn',
        '''kannada'''

        KK = 'kk',
        '''kazakh'''

        KM = 'km',
        '''khmer'''

        KO = 'ko',
        '''korean'''

        KU = 'ku',
        '''kurdish (kurmanji)'''

        KY = 'ky',
        '''kyrgyz'''

        LO = 'lo',
        '''lao'''

        LA = 'la',
        '''latin'''

        LV = 'lv',
        '''latvian'''

        LT = 'lt',
        '''lithuanian'''

        LB = 'lb',
        '''luxembourgish'''

        MK = 'mk',
        '''macedonian'''

        MG = 'mg',
        '''malagasy'''

        MS = 'ms',
        '''malay'''

        ML = 'ml',
        '''malayalam'''

        MT = 'mt',
        '''maltese'''

        MI = 'mi',
        '''maori'''

        MR = 'mr',
        '''marathi'''

        MN = 'mn',
        '''mongolian'''

        MY = 'my',
        '''myanmar (burmese)'''

        NE = 'ne',
        '''nepali'''

        NO = 'no',
        '''norwegian'''

        OR = 'or',
        '''odia'''

        PS = 'ps',
        '''pashto'''

        FA = 'fa',
        '''persian'''

        PL = 'pl',
        '''polish'''

        PT = 'pt',
        '''portuguese'''

        PA = 'pa',
        '''punjabi'''

        RO = 'ro',
        '''romanian'''

        RU = 'ru',
        '''russian'''

        SM = 'sm',
        '''samoan'''

        GD = 'gd',
        '''scots gaelic'''

        SR = 'sr',
        '''serbian'''

        ST = 'st',
        '''sesotho'''

        SN = 'sn',
        '''shona'''

        SD = 'sd',
        '''sindhi'''

        SI = 'si',
        '''sinhala'''

        SK = 'sk',
        '''slovak'''

        SL = 'sl',
        '''slovenian'''

        SO = 'so',
        '''somali'''

        ES = 'es',
        '''spanish'''

        SU = 'su',
        '''sundanese'''

        SW = 'sw',
        '''swahili'''

        SV = 'sv',
        '''swedish'''

        TG = 'tg',
        '''tajik'''

        TA = 'ta',
        '''tamil'''

        TE = 'te',
        '''telugu'''

        TH = 'th',
        '''thai'''

        TR = 'tr',
        '''turkish'''

        UK = 'uk',
        '''ukrainian'''

        UR = 'ur',
        '''urdu'''

        UG = 'ug',
        '''uyghur'''

        UZ = 'uz',
        '''uzbek'''

        VI = 'vi',
        '''vietnamese'''

        CY = 'cy',
        '''welsh'''

        XH = 'xh',
        '''xhosa'''

        YI = 'yi',
        '''yiddish'''

        YO = 'yo',
        '''yoruba'''

        ZU = 'zu'
        '''zulu'''

    @classmethod
    def translate(cls, text: str, source_lang: Lang = None, target_lang: Lang = Lang.ZH_CN) -> dict:
        return utils.request_post('https://translate.google.com/translate_a/single', data={
            'client': 'at',
            'dt': ['t', 'ld', 'qca', 'rm', 'bd'],
            'dj': '1',
            "sl": source_lang or 'auto',
            "tl": target_lang,
            "q": text,
        }).json()
