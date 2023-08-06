import pandas as pd
from .utils import *
from random import randint
import json
from dash import html, Input, Output
from feffery_utils_components import FefferyExecuteJs, FefferyExternalJs


class dmpWordCloud:
    def __init__(self,
                 text,
                 id='',
                 truncN=400,
                 sep='|',
                 input_type='list',
                 style={'height': '360px', 'width': '100%'}):
        self.text = text
        self.truncN = truncN
        self.sep = sep
        self.input_type = input_type
        self.colors = ["#6366f1", "#f52080", "#a056f3", "#ff7075", "#fcce25",
                       "#1ac7c2", "#48a7f0", "#fc8b4e", "#7ca7eb", "#f768a1",
                       "#4e79a7", "#f28e2c", "#e15759", "#76b7b2", "#59a14f",
                       "#edc949", "#af7aa1", "#ff9da7", "#9c755f", "#bab0ab"]
        self.style = style
        self.id = id

    @property
    def gen_words(self):
        text = [Text(x.strip()).truncated for x in self.text.split(self.sep)]
        text = pd.DataFrame([x.split(' ') for x in text])
        text.columns = ['source', 'target']
        words = pd.Series(text.source.tolist() + text.target.tolist()
                          ).value_counts().to_frame('freq').reset_index()
        words.columns = ['name', 'freq']
        nodes = [tuple(x) for x in words[['name', 'freq']].values.tolist()]
        if self.input_type == 'dict':
            nodes = words[['name', 'freq']].rename(columns={'freq': 'value'})
            nodes = nodes.to_dict('records')
        nodes = [{
            'name': x[0],
            'value': x[1],
            'textStyle': {'color': self.colors[randint(0, 19)]}
        } for x in nodes]
        nodes = json.dumps(nodes)
        return nodes

    def fig(self):
        wrapper = html.Div(
            [
                FefferyExecuteJs(
                    id='{}-js'.format(self.id),
                    jsString="""
                    buildWC("{}", {})
                    """.format(self.id, str(self.gen_words))
                ),
                html.Div(
                    id=self.id,
                    style=self.style
                )
            ]
        )
        return wrapper
