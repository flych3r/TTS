""" from https://github.com/keithito/tacotron """

import inflect
from num2words import num2words
import re

_inflect = inflect.engine()
_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
# _pounds_re = re.compile(r'£([0-9\,]*[0-9]+)')
# _dollars_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_reais_re = re.compile(r'R\$([0-9\.\,]*[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(º|ª)')
_number_re = re.compile(r'[0-9]+')


def _remove_commas(m):
    return m.group(1).replace(',', '')


def _expand_decimal_point(m):
    return m.group(1).replace('.', ' ponto ')


def _expand_reais(m):
    match = m.group(1)
    parts = match.split('.')
    if len(parts) > 2:
        return match + ' reais'  # Unexpected format
    reais = int(parts[0]) if parts[0] else 0
    centavos = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if reais and centavos:
        dollar_unit = 'real' if reais == 1 else 'reais'
        cent_unit = 'centavo' if centavos == 1 else 'centavos'
        return '%s %s e %s %s' % (reais, dollar_unit, centavos, cent_unit)
    elif reais:
        dollar_unit = 'real' if reais == 1 else 'reais'
        return '%s %s' % (reais, dollar_unit)
    elif centavos:
        cent_unit = 'centavo' if centavos == 1 else 'centavos'
        return '%s %s' % (centavos, cent_unit)
    else:
        return 'zero reais'


def _expand_ordinal(m):
    return _inflect.number_to_words(m.group(0))


def _expand_number(m):
    num = int(m.group(0))
    # if 1000 < num < 3000:
    #     if num == 2000:
    #         return 'two thousand'
    #     if 2000 < num < 2010:
    #         return 'two thousand ' + _inflect.number_to_words(num % 100)
    #     if num % 100 == 0:
    #         return _inflect.number_to_words(num // 100) + ' hundred'
    #     return _inflect.number_to_words(num,
    #                                     andword='',
    #                                     zero='oh',
    #                                     group=2).replace(', ', ' ')
    # return _inflect.number_to_words(num, andword='')
    return num2words(num, lang='pt_BR')


def normalize_numbers(text):
    text = re.sub(_comma_number_re, _remove_commas, text)
    text = re.sub(_reais_re, _expand_reais, text)
    text = re.sub(_decimal_number_re, _expand_decimal_point, text)
    text = re.sub(_ordinal_re, _expand_ordinal, text)
    text = re.sub(_number_re, _expand_number, text)
    return text
