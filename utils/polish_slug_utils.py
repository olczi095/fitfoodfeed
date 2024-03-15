from django.utils.text import slugify


def convert_to_slug(text: str) -> str:
    """
    Converts polish signs into their ASCII substitutes,
    creates a valid slug from the input text.
    """
    text = text.lower()
    polish_signs_conversion = {
        'ą': 'a',
        'ć': 'c',
        'ę': 'e',
        'ł': 'l',
        'ń': 'n',
        'ó': 'o',
        'ś': 's',
        'ź': 'z',
        'ż': 'z'
    }
    text_without_polish_signs = ''

    for sign in text:
        if sign in polish_signs_conversion:
            text_without_polish_signs += polish_signs_conversion[sign]
        else:
            text_without_polish_signs += sign
    return slugify(text_without_polish_signs)
