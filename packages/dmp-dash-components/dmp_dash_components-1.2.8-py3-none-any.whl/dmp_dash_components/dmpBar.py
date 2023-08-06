from plotly.graph_objects import Figure, Bar
from .plotlyTemplate import *
from dash.dcc import Graph
from .utils import *

class dmpBar(Figure):
    def __init__(
            self,
            data=None,
            dimension='',
            value='',
            groupby=None,
            orientation='h',
            name=None,
            barmode='group',
            template='plotly_white+dmp',
            margin={'l': 20, 'r': 10, 't': 10, 'b': 10, 'pad': 5},
            width=None,
            barWidth=30,  # applies to horizontal bar only
            height=None,
            title=None,
            showLabels=True,
            xaxisTitle=None,
            yaxisTitle=None,
            *args,
            **kwargs):
        Figure.__init__(self, *args, **kwargs)
        if name is None:
            name = dimension.upper()
            if '_' in str(name):
                name = name.split('_')[1]
        data = dmpItem.sort_df_dimension(data, dimension, reverse=True)
        if groupby is None:
            barmode = 'group'
        if orientation == 'h':
            x, y = value, dimension
            if barWidth is not None:
                height = barWidth * data[x].nunique()
                if height < 120:
                    height = 120
            if data[x].nunique() == 1:
                height = 60
            if barmode == 'stack100':
                x = 'pert'
        else:
            y, x = value, dimension
            if barmode == 'stack100':
                y = 'pert'
        if groupby is None:
            data['pert'] = (data[value] / data[value].sum()) * 100
            data['text'] = data.apply(lambda x: '{} ({}%)'.format(
                x[value], Num(x['pert']).to_num()), axis=1)
            self.add_trace(
                Bar(
                    y=data[y], x=data[x], orientation=orientation,
                    name=name, text=data['text'], hovertemplate='%{text}'
                )
            )
        else:
            data['pert'] = 100 * data[value] / \
                data.groupby([dimension])[value].transform('sum')
            data['text'] = data.apply(lambda x: '{} ({}%)'.format(
                x[value], Num(x['pert']).to_num()), axis=1)
            group_list = data[groupby].unique().tolist()
            groups = List(group_list).sort(reverse=False)
            for group in groups:
                data_ = data[data[groupby] == group]
                self.add_trace(
                    Bar(
                        y=data_[y], x=data_[x],
                        orientation=orientation,
                        name=dmpItem.sort_group_name(group),
                        text=data_['text'],
                        hovertemplate='%{text}'
                    )
                )
        if 'stack' in barmode:
            self.update_layout(legend={'traceorder': 'normal'})
        self.update_layout(template=template, margin=margin, autosize=True)
        if width is not None:
            self.update_layout(width=width)
        if height is not None:
            self.update_layout(height=height)
        dim_list = data[dimension].unique().tolist()
        if orientation == 'h':
            gp_groups = List(dim_list).sort(reverse=True)
            gp_groups = [x.split(':')[0].strip() for x in gp_groups]
            self.update_xaxes(showticklabels=False, showgrid=False)
            self.update_yaxes(categoryorder='array', categoryarray=gp_groups)
        else:
            gp_groups = List(dim_list).sort(reverse=False)
            gp_groups = [x.split(':')[0].strip() for x in gp_groups]
            self.update_yaxes(showticklabels=False, showgrid=False)
            self.update_xaxes(categoryorder='array', categoryarray=gp_groups)
        if 'stack' in str(barmode):
            self.update_layout(barmode='stack')
            if orientation == 'h':
                self.update_layout(hovermode='y unified')
            else:
                self.update_layout(hovermode='x unified')
        if showLabels is False:
            self.update_traces(text=None)
        if xaxisTitle is not None:
            self.update_xaxes(title=xaxisTitle)
        if yaxisTitle is not None:
            self.update_yaxes(title=yaxisTitle)
        if title is not None:
            self.update_layout(title={'text': title,
                                      'xanchor': 'center',
                                      'yanchor': 'top',
                                      'x': 0.45 if groupby is not None else 0.5},
                               margin={'l': 20, 'r': 10,
                                       't': 35, 'b': 10, 'pad': 5},
                               title_font_family='sans-serif',
                               title_font_size=15,
                               )
        self.update_layout(hoverlabel=dict(bgcolor='#fff'))

    def graph(self, config=chart_config, className=None, style={}):
        return Graph(figure=self, config=chart_config, className=className, style=style)
