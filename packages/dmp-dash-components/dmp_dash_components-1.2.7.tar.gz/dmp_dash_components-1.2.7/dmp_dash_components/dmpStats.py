import pandas as pd
from .utils import *
from .dashTable import dashTable

class dmpStats:
    def __init__(self,
                 variable,
                 num_var=None,
                 stra_var=None,
                 data=None,
                 tlines=None,
                 django=False,
                 dtypes=None
                 ):
        self.variable = variable
        self.num_var = num_var
        self.stra_var = stra_var
        self.data = data
        self.django = django
        self.dtypes = dtypes

    @property
    def clean_data(self):
        data = self.data
        if self.django:
            vari = self.variable.variable
            vari_type = self.variable.variable_type
        else:
            vari = self.variable
            vari_type = self.dtypes[vari]
        num_vari = self.num_var.variable if self.django and self.num_var else self.num_var
        stra_vari = self.stra_var.variable if self.django and self.stra_var else self.stra_var
        data = data[['subjectid'] + [x for x in data.columns if x in [vari, num_vari, stra_vari]]]
        if vari_type in [4, 5, 6]:
            data = data.dropna(subset=[vari])
            data = data[data[vari].apply(lambda x: Num(x).is_num)]
        if self.num_var is not None:
            data = data.dropna(subset=[vari, num_vari])
            data = data[data[num_vari].apply(lambda x: NAcheck(x).notna)]
            data = data[data[num_vari].apply(lambda x: Num(x).is_num)]
        if self.stra_var is not None and vari_type in [1, 2, 3]:
            data = data[~((data[vari] == '9999: Unknown') & (data[stra_vari] == '9999: Unknown'))]
        return data

    @property
    def mixed_vari(self):
        data = self.data
        vari = self.variable.variable if self.django else self.variable
        data = data.dropna(subset=[vari])
        num_count = len(data[data[vari].apply(lambda x: Num(x).is_num)])
        text_count = len(data[~data[vari].apply(lambda x: Num(x).is_num)])
        text_des = dict(data[~data[vari].apply(lambda x: Num(x).is_num)][vari].value_counts())
        text_des = ', '.join(['{}: {}'.format(k, v) for k, v in text_des.items()])
        template = 'This variable contains mixed values - No. of numeric values: {}, No. of non-numeric values: {} ({})'
        return template.format(num_count, text_count, text_des)

    @property
    def des_table(self):
        vari = self.variable.variable if self.django else self.variable
        variType = self.variable.variable_type if self.django else self.dtypes[vari]
        if variType in [1, 2, 3]:
            return self.cat_table
        else:
            return self.num_table

    @property
    def fig(self):
        column_mapping={
            'Count': {'className': 'text-center'},
            'Min': {'className': 'text-center'},
            'Q1': {'className': 'text-center'},
            'Median': {'className': 'text-center'},
            'Q3': {'className': 'text-center'},
            'Max': {'className': 'text-center'},
            'Mean': {'className': 'text-center'},
            'Variable': {'className': 'text-start'},
            'Category': {'className': 'text-start'},
        }
        cols = list(self.des_table.columns)
        if cols[0] not in column_mapping:
            column_mapping.update(
                {cols[0]: {'className': 'text-start'}}
            )
        for i in range(1, len(cols)):
            if cols[i] not in column_mapping:
                column_mapping.update(
                    {cols[i]: {'className': 'text-center'}}
                )
        t = dashTable(
            data=self.des_table,
            column_mapping=column_mapping
        )
        return t

    @property
    def cat_table(self):
        vari = self.variable.variable if self.django else self.variable
        stra_vari = self.stra_var.variable if self.django and self.stra_var else self.stra_var
        data = self.data.copy()
        if self.stra_var is None:
            data = data[data[vari] != '9999: Unknown']
            data = data[vari].value_counts().to_frame('Count').reset_index()
            data['index'] = data['index'].apply(lambda x: dmpItem.sort_group_name(x))
            data.columns = [dmpItem.sort_vari_code(vari), 'Count']
            data['Count'] = data.Count.apply(lambda x: '{} ({}%)'.format(x, round(x / data.Count.sum() * 100, 2)))
        else:
            for col in data.columns:
                data[col] = data[col].apply(lambda x: pd.NA if x == '9999: Unknown' else x)
            data = data.dropna(how='all', subset=[vari, stra_vari])
            data = data.fillna('9999: Unknown')
            data = pd.crosstab(data[vari], data[stra_vari]).reset_index()
            data[vari] = data[vari].apply(lambda x: dmpItem.sort_group_name(x))
            cols = pd.Series(data.columns)
            cols = cols.apply(lambda x: dmpItem.sort_vari_code(x) if ':' not in x else dmpItem.sort_group_name(x))
            data.columns = cols
        return data

    @property
    def num_table(self):
        cols = {'count': 'Count', 'min': 'Min', '25%': 'Q1',
                '50%': 'Median', '75%': 'Q3', 'max': 'Max', 'mean': 'Mean'}
        con1, con2 = self.stra_var is not None, self.num_var is not None
        if self.django:
            vari = self.variable.variable
            variType = self.variable.variable_type
        else:
            vari = self.variable
            variType = self.dtypes[vari]

        conNum = variType in [4, 5, 6]
        data = self.clean_data
        if conNum:
            data[vari] = data[vari].astype(float)
        if con1:
            stra_vari = self.stra_var.variable if self.django else self.stra_var
        if con2:
            num_vari = self.num_var.variable if self.django else self.num_var
            data[num_vari] = data[num_vari].astype(float)
        if conNum:
            if not con1 and not con2:
                des = dict(data[vari].astype(float).describe())
                des = pd.DataFrame({'vari': des.keys(), 'value': des.values()}).set_index('vari').T
                des = des[list(cols.keys())]
            if con1 and not con2:
                des = data.groupby(stra_vari)[vari].describe().reset_index()
                des = des[[stra_vari] + list(cols.keys())]
                des.columns = [''] + list(des.columns[1:])
                try:
                    des['int'] = des[''].apply(lambda x: float(x.split(': ')[0]))
                    des = des.sort_values(by=['int'])
                    des[''] = des[''].apply(lambda x: x.split(': ')[1].strip())
                except:
                    des = des.sort_values(by=[''])
            if con2 and not con1:
                des = data[[vari, num_vari]].describe().T.reset_index()
                des = des.rename(columns={'index': 'Variable'})
                if all(['_' in x for x in des.Variable.unique().tolist()]):
                    des.Variable = des.Variable.apply(lambda x: x.split('_')[1].strip().upper())
                des = des[['Variable'] + list(cols.keys())]
            if con1 and con2:
                des = []
                for v in [vari, num_vari]:
                    des_ = data.groupby(stra_vari)[v].describe().reset_index()
                    des_.insert(0, 'Variable', v.replace('sp_', '').replace('gt_', '').upper())
                    des.append(des_[['Variable', stra_vari] + list(cols.keys())])
                des = pd.concat(des)
                des = des.rename(columns={stra_vari: 'Category'})
                try:
                    des['int'] = des['Category'].apply(lambda x: float(x.split(': ')[0]))
                    des = des.sort_values(by=['Variable', 'int'])
                    des['Category'] = des['Category'].apply(lambda x: x.split(': ')[1].strip())
                except:
                    des = des.sort_values(by=['Variable', 'Category'])
            des = des.rename(columns=cols)
            for vari in cols.values():
                if vari != 'Count':
                    des[vari] = des[vari].apply(lambda x: Num.round(x,2))
                else:
                    des[vari] = des[vari].astype(int)
            des = des.drop(columns=['int']) if 'int' in des.columns else des
            return des
