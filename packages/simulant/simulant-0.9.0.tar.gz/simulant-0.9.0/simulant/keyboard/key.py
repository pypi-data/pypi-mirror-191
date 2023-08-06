letters = {
    'а': 'Cyrillic_a',
    'б': 'Cyrillic_be',
    'в': 'Cyrillic_ve',
    'г': 'Cyrillic_ghe',
    'д': 'Cyrillic_de',
    'е': 'Cyrillic_ie',
    'ё': 'Cyrillic_io',
    'ж': 'Cyrillic_zhe',
    'з': 'Cyrillic_ze',
    'и': 'Cyrillic_i',
    'й': 'Cyrillic_shorti',
    'к': 'Cyrillic_ka',
    'л': 'Cyrillic_el',
    'м': 'Cyrillic_em',
    'н': 'Cyrillic_en',
    'о': 'Cyrillic_o',
    'п': 'Cyrillic_pe',
    'р': 'Cyrillic_er',
    'с': 'Cyrillic_es',
    'т': 'Cyrillic_te',
    'у': 'Cyrillic_u',
    'ф': 'Cyrillic_ef',
    'х': 'Cyrillic_ha',
    'ц': 'Cyrillic_tse',
    'ч': 'Cyrillic_che',
    'ш': 'Cyrillic_sha',
    'щ': 'Cyrillic_shcha',
    'ъ': 'Cyrillic_hardsign',
    'ы': 'Cyrillic_yeru',
    'ь': 'Cyrillic_softsign',
    'э': 'Cyrillic_e',
    'ю': 'Cyrillic_yu',
    'я': 'Cyrillic_ya',
}


class BaseKey(str):
    def __new__(cls, string):
        instance = super().__new__(cls, string)
        return instance

    def __add__(self, other):
        return f"{self}+{other}"


class Keys:
    F1 = BaseKey('F1')
    F2 = BaseKey('F2')
    F3 = BaseKey('F3')
    F4 = BaseKey('F4')
    F5 = BaseKey('F5')
    F6 = BaseKey('F6')
    F7 = BaseKey('F7')
    F8 = BaseKey('F8')
    F9 = BaseKey('F9')
    F10 = BaseKey('F10')
    F11 = BaseKey('F11')
    F12 = BaseKey('F12')

    ESC = BaseKey('Escape')
    ENTER = BaseKey('Return')
    TAB = BaseKey('Tab')

    RIGHT = BaseKey('Right')
    LEFT = BaseKey('Left')
    UP = BaseKey('Up')
    DOWN = BaseKey('Down')

    INSERT = BaseKey('Insert')
    DELETE = BaseKey('Delete')
    HOME = BaseKey('Home')
    END = BaseKey('End')
    PAGE_UP = BaseKey('Prior')
    PAGE_DOWN = BaseKey('Next')

    SHIFT = BaseKey('Shift_L')
    CTRL = BaseKey('ctrl')
    ALT = BaseKey('Alt_L')
    SPACE = BaseKey('space')


keys = Keys()
