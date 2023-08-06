from plotly.graph_objects import Figure, Box
from .utils import *
from .plotlyTemplate import *
from feffery_utils_components import FefferyExecuteJs, FefferyExternalJs
import json
from dash import html

subColor = ["#4e79a7", "#f28e2c", "#e15759", "#76b7b2", "#59a14f",
            "#edc949", "#af7aa1", "#ff9da7", "#9c755f", "#bab0ab"]
colorway = ["#6366f1", "#f52080", "#a056f3", "#ff7075", "#fcce25",
            "#1ac7c2", "#48a7f0", "#fc8b4e", "#7ca7eb", "#f768a1"]
corMapCont = ['#dedbea', '#d2ccec', '#c5bded', '#b7aeee',
              '#a99fef', '#9a90f0', '#8a82f0', '#7874f1', '#6366f1']
colorway = colorway + corMapCont[1:] + subColor


class dmpHeatMap:
    def __init__(self,
                 data=None,
                 x='tp_id',
                 y='sample_type',
                 value='count',
                 labels={},
                 style={'height': '500px', 'width': '100%'},
                 id='',
                 title='Number of Subjects',
                 overview_data=False):
        self.data = data
        self.title = title
        self.x = x
        self.y = y
        self.labels = labels
        self.value = value
        self.overview_data = overview_data
        self.id = id
        self.style = style

    @staticmethod
    def getValues(df, col='sample_type'):
        rowLen = range(len(df))
        colLen = len(df.columns)
        df_ = df[list(df.columns)]
        df_[col] = rowLen
        df_.columns = ['t'] + list(range(df_.shape[1] - 1))
        dt = df_.to_dict()
        rowI = list(dt['t'].keys())
        rowI.sort()
        colI = [x for x in list(dt.keys()) if x != 't']
        result = []
        for r in rowI:
            for c in colI:
                result.append([c, len(df) - r - 1, dt[c][r]])
        return result

    @property
    def count_table(self):
        if self.overview_data is False:
            df_summary, x, y, vari = self.data, self.x, self.y, self.value
            df_summary = df_summary[[self.y, self.x, self.value]]
            max_ = df_summary[self.value].max()
            min_ = df_summary[self.value].min()
            df_summary = df_summary.pivot(
                index=[y], columns=[x], values=self.value)
        else:
            x, y, vari = self.x, self.y, self.value
            max_ = self.data[self.value].max()
            min_ = self.data[self.value].min()
            df_summary = self.data.pivot(
                index=[y], columns=[x], values=self.value)
        df_summary = df_summary.reset_index().fillna(0).sort_values(by=y)
        for col in df_summary.columns:
            if col != y:
                if self.value in ['mean', 'median']:
                    df_summary[col] = df_summary[col].apply(lambda x: float(Num.round(x, 2)))
                else:
                    df_summary[col] = df_summary[col].astype(int)
        if self.x not in self.labels:
            x = [x for x in df_summary.columns if x != y]
        else:
            x = [self.labels[self.x][i] for i in df_summary.columns if i != y]
        df_summary = df_summary.replace(0, '-')
        if self.y not in self.labels:
            y = List(df_summary[y].tolist()).reverse()
        else:
            y = List(df_summary[y].tolist()).reverse()
            y = [self.labels[self.y][x] for x in y]
        value = self.getValues(df_summary, col=y)
        return x, y, value, min_, max_

    @property
    def graph(self):
        fig = html.Div(
            [
                html.Div(
                    id=self.id,
                    style=self.style
                ),
                FefferyExecuteJs(
                    jsString="""
                    var o = echarts.init(document.getElementById("%s"));
                    o.setOption(%s), window.onresize = function() {
                    o.resize()
                    }
                    """%(self.id, str(self.options))
                )
            ],
        )
        return fig
    @property
    def options(self):
        x, y, values, min_, max_ = self.count_table
        option = {
            'tooltip': {
                'position': 'top',
            },
            'toolbox': echartsToolbox,
            'grid': {
                'top': 50,
                'left': '4%',
                'right': '4%',
                'bottom': '8%',
                'height': '88%',
                'containLabel': True
            },
            'xAxis': {
                'type': 'category',
                'data': x,
                'axisLabel': {'rotate': -55},
                'position': 'top',
                'axisLine': {'show': True},
                'axisTick': {'show': True, 'interval': 0},
                'splitArea': {
                    'show': True
                }
            },
            'yAxis': {
                'type': 'category',
                'data': y,
                'axisTick': {'show': True, 'interval': 0},
                'splitArea': {
                    'show': True,
                    'areaStyle': {'color': ['#f1f2f7', '#fff']}
                }
            },
            'visualMap': {
                'type': 'continuous',
                'min': min_,
                'max': max_,
                'show': False,
                'precision': 5,
                'inRange': {
                    'color': corMapCont
                },
            },
            'series': [
                {
                    'name': self.title,
                    'type': 'heatmap',
                    'data': values,
                    'label': {
                        'show': True,
                    },
                    'emphasis': {
                        'itemStyle': {
                            'shadowBlur': 10,
                            'shadowColor': 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        }
        option = json.dumps(option)
        return option
