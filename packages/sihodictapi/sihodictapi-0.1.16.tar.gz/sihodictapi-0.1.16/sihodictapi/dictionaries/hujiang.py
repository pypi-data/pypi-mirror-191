from enum import Enum

from bs4 import BeautifulSoup

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

    cookies = {'HJ_UID': '0', 'HJ_SID': '0'}

    @classmethod
    def translate(cls, text: str, from_lang: Lang, to_lang: Lang) -> dict:
        """
        沪江小D翻译(应该是用的百度翻译，而且翻译结果不完整，不建议用)
        :param text: 输入文本
        :param from_lang: 源语言
        :param to_lang: 目标语言
        """
        return utils.request_post(f"https://dict.hjenglish.com/v10/dict/translation/{from_lang}/{to_lang}", data={
            'content': text
        }, cookies=cls.cookies).json()

    @classmethod
    def dict_search_jp(cls, text: str, search_type: str = 'jc') -> dict:
        """
        沪江小D查词-日语（由 https://dict.hjenglish.com/jp/ 网页HTML生成）

        :param text: 输入文本
        :param search_type: 'jc'(日→中) 或 'cj'(中→日)
        """
        if search_type not in ['jc', 'cj']:
            raise Exception('search_type值无效')
        url = f'https://dict.hjenglish.com/jp/{search_type}/{text}'
        content = utils.request_get(url, cookies=cls.cookies).content.decode()
        result = {
            'text': text,
            'search_type': search_type
        }
        if '抱歉，没有找到你查的单词结果' in content:
            result['results'] = []
            return result
        soup = BeautifulSoup(content, 'html.parser')
        word_details_content = soup.find('section', attrs={'class': 'word-details-content'})
        word_details_panes = word_details_content.findAll('div', attrs={'class': 'word-details-pane'})
        words = []
        for details_pane in word_details_panes:
            word_text = details_pane.find('div', attrs={'class': 'word-text'}).find('h2').text
            pronounces = details_pane.find('div', attrs={'class': 'pronounces'}).findAll('span')
            spell = pronounces[0].text[1:-1]
            audio = pronounces[-1].attrs.get('data-src')
            word_info = {
                'spell': spell,
                'audio': audio,
            }
            if len(pronounces) > 3:
                word_info['accent'] = pronounces[2].text
            simple = []
            simple_div = details_pane.find('div', attrs={'class': 'simple'})
            simple_titles = [title.text for title in simple_div.findAll('h2')]
            simple_paraphrases = simple_div.findAll('ul')
            if simple_paraphrases:
                if not simple_titles:
                    simple_titles = ['【】'] * len(simple_paraphrases)
                for title, paraphrases in zip(simple_titles, simple_paraphrases):
                    simple.append({
                        'title': title[1:-1],
                        'paraphrases': [paraphrase.text[2:] for paraphrase in paraphrases.findAll('li')]
                    })
            else:
                simple_definition = simple_div.find('span', attrs={'class': 'simple-definition'})
                if simple_definition:
                    simple.append({
                        'title': '',
                        'paraphrases': simple_definition.text.replace('\n', '').replace(' ', '').split('；')
                    })
            details = []
            detail_groups = details_pane.find('section', attrs={'class': 'detail-groups'})
            if detail_groups:
                for dl in detail_groups.findAll('dl'):
                    category = dl.find('dt').text.strip()
                    paraphrases = []
                    for dd in dl.findAll('dd'):
                        p = dd.find('h3').findAll('p')
                        if len(p) > 1:
                            paraphrase_ja = p[0].text.strip()
                            paraphrase_zh = p[1].text.strip()
                        else:
                            paraphrase_ja = ''
                            paraphrase_zh = p[0].text.strip()
                        examples = []
                        for li in dd.find('ul').findAll('li'):
                            p = li.findAll('p')
                            example = p[0].text.strip()
                            trans = p[1].text.strip()
                            examples.append({'example': example, 'trans': trans})
                        paraphrases.append(
                            {'paraphrase_ja': paraphrase_ja, 'paraphrase_zh': paraphrase_zh, 'examples': examples})
                    details.append({'category': category, 'paraphrases': paraphrases})
            words.append({
                'word_text': word_text,
                'word_info': word_info,
                'simple': simple,
                'details': details
            })
        result['results'] = words
        return result
