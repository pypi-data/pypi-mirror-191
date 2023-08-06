from .utils import *
from .AntdInput import AntdInput
from .AntdTabs import AntdTabs
from .AntdTabPane import AntdTabPane
from .AntdButton import AntdButton
from .AntdRow import AntdRow
from .AntdCol import AntdCol
from .AntdSelect import AntdSelect
import dash
from dash import html
from dash import Input, Output, State
from dash.dependencies import ALL, MATCH
from dash.exceptions import PreventUpdate
from .dashCallbacks import dashCallbacks

class dashMultiSearch:
    def __init__(
        self,
        nrows=1,
        kws=[None],
        bools=['and'],
        domain_url=''
    ):
        self.n = nrows
        if len(kws) < nrows:
            to_add = nrows - len(kws)
            kws += [None] * to_add
        if len(bools) < nrows:
            to_add = nrows - len(bools)
            bools += ['and'] * to_add
        self.kws = kws
        self.bools = bools
        self.domain_url = domain_url

    @staticmethod
    def search_row(i=0, n=3, kw_input='', bool='and'):
        style0 = {'opacity': '0'}
        stylehide = {'display': 'None'}
        row = AntdRow(
            [
                AntdCol(
                    AntdSelect(
                        options=[
                            {'label': 'AND', 'value': 'and'},
                            {'label': 'OR', 'value': 'or'},
                            {'label': 'NOT', 'value': 'not'}
                        ],
                        value=bool,
                        className='w-100',
                        id={'type': 'boolean',
                            'index': 'boolean-input-{}'.format(i)},
                    ),
                    xl=2,
                    md=3,
                    sm=8,
                    xs=6,
                    style=style0 if i == 0 else {}
                ),
                AntdCol(
                    AntdInput(
                        id={'type': 'keyword',
                            'index': 'keyword-input-{}'.format(i)},
                        placeholder='Enter some keywords to start...' if i == 0 else '',
                        value=kw_input
                    ),
                    xl=19,
                    md=17,
                    sm=10,
                    xs=12,
                ),
                AntdCol(
                    html.Div(
                        [
                            AntdButton(
                                '+',
                                type='primary',
                                className='me-1',
                                id={'type': 'add-btn',
                                    'index': 'add-{}'.format(i)},
                                style=stylehide if i + 1 != n else {}
                            ),
                            AntdButton('-',
                                       id={'type': 'rem-btn',
                                           'index': 'rem-{}'.format(i)},
                                       type='primary',
                                       className='me-1',
                                       danger=True,
                                       style=stylehide if i == 0 else {}),
                        ],
                        className='justify-content-start'
                    ),
                    xl=3,
                    md=4,
                    sm=6,
                    xs=6
                )
            ],
            gutter=5,
            className='my-2'
        )
        return row

    @property
    def boxes(self):
        rows = []
        for i in range(self.n):
            rows.append(self.search_row(i, self.n, self.kws[i], self.bools[i]))
        return rows

    def add_drop(self, app, wrapper_id='advanced-search-group'):
        @app.callback(
            Output(wrapper_id, 'children'),
            [
                Input({'type': 'add-btn', 'index': ALL}, 'nClicks'),
                Input({'type': 'rem-btn', 'index': ALL}, 'nClicks'),
            ],
            [
                State({'type': 'boolean', 'index': ALL}, 'value'),
                State({'type': 'keyword', 'index': ALL}, 'value')
            ]
        )
        def update_av_search(add_clicks, rem_clicks, bools, kws):
            ctx = dashCallbacks(dash.callback_context)
            if ctx.triggered:
                if ctx.prop_ids[0].startswith('add-'):
                    n = len(bools)
                    bools += ['and']
                    kws += [None]
                    return dashMultiSearch(n + 1, kws, bools).boxes
                if ctx.prop_ids[0].startswith('rem-'):
                    rem_n = int(float(ctx.prop_ids[0].split('-')[1]))
                    bools = [bools[i] for i in range(len(bools)) if i != rem_n]
                    kws = [kws[i] for i in range(len(kws)) if i != rem_n]
                    return dashMultiSearch(len(bools), kws, bools).boxes
            raise PreventUpdate
