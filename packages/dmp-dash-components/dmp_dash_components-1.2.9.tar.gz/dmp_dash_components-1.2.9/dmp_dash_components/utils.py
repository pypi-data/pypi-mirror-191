from decimal import Decimal, ROUND_HALF_UP
from pandas import isna as pd_isna
from pandas import DataFrame
from numpy import floor

class Text:
    def __init__(self, text, truncN=300):
        self.text = text
        self.truncN = truncN
    @property
    def truncated(self):
        if len(self.text) > self.truncN:
            return self.text[:self.truncN] + '...'
        else:
            return self.text

class NAcheck:
    def __init__(self, object):
        self.object = object

    @staticmethod
    def value_isna(object):
        if pd_isna(object):
            return True
        elif object in [None, '', [], {}, 'None', 9999, '9999']:
            return True
        else:
            try:
                if float(object) == 9999:
                    return True
            except:
                return False
    @property
    def isna(self):
        is_na = False
        if type(self.object) == list:
            ob = [x for x in self.object if not self.value_isna(x)]
        if self.value_isna(self.object):
            is_na = True
        return is_na

    @property
    def notna(self):
        return not self.isna


class Num:
    def __init__(self, n):
        self.num = n

    @staticmethod
    def round(n, d=2):
        n = Decimal(str(n)).quantize(
            Decimal('0.'.ljust(2 + d, '0')), rounding=ROUND_HALF_UP)
        return n

    def to_num(self, round_n=2):
        """
        Convert strings to integers of floats (round_n decimals)
        """
        try:
            if int(float(self.num)) == float(self.num):
                return int(float(self.num))
            else:
                return self.round(float(self.num), d=round_n)
        except:
            return self.num

    @property
    def is_num(self):
        """
        Check if the object is a number
        """
        try:
            x = int(float(self.num))
            return True
        except:
            return False


class List:
    def __init__(self, ls):
        self.ls = ls

    def reverse(self):
        """
        Reverse a list
        """
        lst_new = []
        for i in range(1, len(self.ls) + 1):
            lst_new.append(self.ls[-i])
        return lst_new

    def sort(self, reverse=False):
        """
        Sort a list.. If integer code exist, sort by the codes instead
        """
        if all([':' in str(x) for x in self.ls]):
            ls = DataFrame({'lst': self.ls})
            try:
                ls['num'] = ls['lst'].apply(lambda x: float(x.split(':')[0]))
                ls = ls.sort_values(by=['num'])
            except:
                ls = ls.sort_values(by=['lst'])
            ls = ls['lst'].tolist()
        else:
            ls = self.ls
            ls.sort()
        if reverse is True:
            ls = List(ls).reverse()
        return ls


class dmpItem:
    def sort_group_name(string):
        if ':' in str(string):
            return string.split(':')[1].strip()
        else:
            if type(string) == str:
                return string.title()
            else:
                return string

    def sort_vari_code(string):
        if '_' in string:
            return string.split('_')[1].upper()
        else:
            return string

    def sort_df_dimension(df, dimension, reverse=False):
        df = df.sort_values(by=[dimension])
        if all([':' in str(x) for x in df[dimension].unique().tolist()]):
            try:
                df['sortD'] = df[dimension].apply(
                    lambda x: int(float(x.split(':')[0])))
                df = df.sort_values(['sortD'], ascending=not reverse)
                df[dimension] = df[dimension].apply(
                    lambda x: x.split(':')[1].strip())
            except:
                pass
        return df


class getColor:
    def continuous(
        n, min_, max_,
        corMapCont=['#dedbea', '#d2ccec', '#c5bded', '#b7aeee',
                    '#a99fef', '#9a90f0', '#8a82f0', '#7874f1', '#6366f1']):
        corMapCont = List(corMapCont).reverse()
        n_cat = len(corMapCont) - 1
        if n == 0:
            c = 'transparent|#3e4265'
        elif min_ == max_:
            c = 'transparent|#3e4265'
        else:
            n_ = int(floor((n - min_) / (max_ - min_) * n_cat))
            if n_ > 4:
                c = corMapCont[n_] + '|#3e4265'
            else:
                c = corMapCont[n_] + '|#fff'
        return {'background-color': c.split('|')[0], 'color': c.split('|')[1]}

echartsToolbox = {
    'show': True,
    'feature': {
        'saveAsImage': {
            'title': 'Save as Image',
            'iconStyle': {
                'color': '#3178b4',
                'borderColor': '#3178b4'
            },
            'name': 'Image',
            'icon': 'path://M414.72,112.64h-49.152l-27.136-40.96c-10.24-15.36-28.16-24.576-46.592-24.576H179.2c-18.432,0-36.352,9.216-46.592,24.576l-27.136,40.96H56.32C25.088,112.64,0,137.728,0,168.96v198.656c0,31.232,25.088,56.32,56.32,56.32h358.4c31.232,0,56.32-25.088,56.32-56.32V168.96C471.04,137.728,445.952,112.64,414.72,112.64z M235.52,377.856c-70.144,0-126.976-56.832-126.976-126.976c0-70.144,56.832-126.464,126.976-126.464s126.976,56.832,126.976,126.976C362.496,321.024,305.664,377.856,235.52,377.856z M407.552,192c-0.512,0-1.024,0-2.048,0h-20.48c-9.216-0.512-16.384-8.192-15.872-17.408c0.512-8.704,7.168-15.36,15.872-15.872h20.48c9.216-0.512,16.896,6.656,17.408,15.872C423.424,183.808,416.768,191.488,407.552,192z',
        },
    },
    'top': 10,
    'right': '15%'
}
