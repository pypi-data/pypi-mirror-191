from .utils import *
import pandas as pd


class DBQuery:
    def __init__(
            self,
            host='localhost',
            db_name='postgres',
            db_user='postgres',
            db_password='123456'):
        self.host = host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.postgres_url = 'postgresql://{}:{}@{}:5432/{}'.format(
            db_user, db_password, host, db_name)

    @staticmethod
    def check_cat(t_, v, ttype='dict', sep=', '):
        try:
            t = t_.split(sep)
            t = {x.split(': ')[0].strip(): x.split(': ')[
                0].strip() + ': ' + x.split(': ')[1].strip() for x in t}
            t = {k: v for k, v in t.items() if k not in [
                '9999', '999', '99', 99, 999, 9999]}
            if ttype == 'dict':
                return {int(float(k)): v for k, v in t.items()}
            else:
                return ' | '.join(t.values())
        except:
            print('ERROR!!!!!!!', v, t_)
            return pd.NA

    @staticmethod
    def handle_data(data, dd):
        data = data.fillna(9999)
        for i in range(len(dd)):
            row = dd.iloc[i]
            v = row.variable
            vartype = row.variable_type
            if vartype == 1:
                cat = DBQuery.check_cat(
                    row.categories, v, ttype='dict', sep=' | ')
                cat.update({9999: '9999: Unknown'})
                data[v] = data[v].astype(int).map(cat)
            elif vartype == 3:
                data[v] = data[v].apply(lambda x: str(Num(x).to_num()))
            elif vartype == 4:
                data[v] = data[v].apply(lambda x: Num(x).to_num()).astype(int)
            elif vartype == 5:
                data[v] = data[v].apply(lambda x: Num(x).to_num())
            elif vartype == 6:
                data[v] = data[v].apply(lambda x: Num(x).to_num())
        for col in data.columns:
            data[col] = data[col].apply(
                lambda x: pd.NA if NAcheck(x).isna else x)
        data = data.drop_duplicates()
        return data

    def retrieve_omics(self, sids, schema='omics'):
        table_name = 'data'
        columns = ['subjectid'] + sids
        data = pd.read_sql_table(
            table_name=table_name, con=self.postgres_url, schema=schema, columns=columns)
        data['sum'] = data.sum(axis=1)
        data = data[data['sum'] > 0].drop(columns=['sum'])
        return data

    def retrieve_table(self, table_name, schema, columns=[]):
        if not columns:
            data = pd.read_sql_table(
                table_name=table_name, con=self.postgres_url, schema=schema)
        else:
            data = pd.read_sql_table(
                table_name=table_name,
                con=self.postgres_url,
                schema=schema,
                columns=columns
            )
        return data

    def retrieve_dd(
        self, variables=[], table_name='dd',
        schema='cataloge', columns=['variable', 'description', 'variable_type'],
    ):
        data = pd.read_sql_table(
            table_name=table_name,
            con=self.postgres_url,
            schema=schema,
            columns=columns
        )
        if variables:
            data = data[data.variable.isin(variables)]
        return data

    def retrieve_varType(
        self, variables=[], table_name='dd',
        schema='cataloge', columns=['variable', 'description', 'variable_type'],
    ):
        data = pd.read_sql_table(
            table_name=table_name,
            con=self.postgres_url,
            schema=schema,
            columns=columns
        )
        if variables:
            data = data[data.variable.isin(variables)]
        return dict(zip(data.variable, data.variable_type))

    def retrieve_tp_dt(self, label_type='short'):
        tps = self.retrieve_table('timepoint', schema='base')
        if label_type == 'short':
            return dict(zip(tps.id, tps.label_short))
        elif label_type == 'full':
            return dict(zip(tps.id, tps.label_full))

    def retrieve_topic_dt(self):
        topics = self.retrieve_table('topics', schema='cataloge', columns=['topic_id', 'topic'])
        return dict(zip(topics.topic_id, topics.topic))

    def retrieve_omcis_samples(self, sids=[]):
        omics = self.retrieve_table('omic', schema='base')
        omics_samples = self.retrieve_table('samples', schema='omics')
        tps = self.retrieve_table('timepoint', schema='base')
        fmcs = self.retrieve_table('fmc', schema='base')

        omics_samples['omic_id'] = omics_samples.sid.apply(
            lambda x: x[:8].upper())
        omics_samples = omics_samples.drop(columns=['index'])
        omics = omics.drop(columns=['index'])

        omics = omics.merge(omics_samples, on='omic_id', how='right')
        omics['fmc_icon'] = omics.fmc.map(dict(zip(fmcs.id, fmcs.icon)))
        omics.sample_type = omics.fmc_icon + ' ' + omics.sample_type
        omics = omics.drop(columns=['level_0', 'platform_id', 'fmc_icon'])
        min_, max_ = omics.subject_count.min(), omics.subject_count.max()
        omics['color'] = omics.subject_count.apply(
            lambda x: getColor.continuous(x, min_, max_))
        colors = dict(zip(omics.sid, omics.color))
        gp = ['omic_id', 'category_id', 'sample_id', 'fmc',
              'category_type', 'sample_type', 'platform']
        omics.subject_count = omics.apply(lambda x: {'id': {'index': x.sid, 'type': 'omic-subject-count'},
                                                     'type': 'Button', 'text': x.subject_count,
                                                     'className': 'w-100',
                                                     'style': x.color
                                                     }, axis=1)
        if sids:
            omics = omics[omics.sid.isin(sids)]
        omics = omics.pivot(index=gp, columns=[
                            'tp_id'], values=['subject_count'])
        for col in omics.columns:
            omics[col] = omics[col].apply(lambda x: '' if pd.isna(x) else x)
        omics = omics.reset_index()
        cols = pd.Series(omics.columns.tolist()).apply(
            lambda x: x[0] if x[0] and x[0] != 'subject_count' else x[1])
        cols = cols.map(dict(zip(tps.id, tps.label_short))).fillna(cols)
        omics.columns = cols
        omics = omics.sort_values(by=['category_id', 'fmc'])
        return omics

    def retrieve_data(self, variables, schema='data', django=False, dropna=False, dropnaCat=False):
        if django is True:
            tables = list(set([x.table for x in variables]))
            dd = pd.DataFrame(variables.values(
                'variable', 'variable_type', 'categories'))
        else:
            dd = pd.read_sql_table(table_name='dd', con=self.postgres_url, schema='cataloge',
                                   columns=['variable', 'table', 'variable_type', 'categories'])
            dd = dd[dd.variable.isin(variables)]
            tables = dd.table.unique().tolist()
        dfs = []
        for t in tables:
            table_name = t.split('_', 1)[1]
            if django is True:
                columns = ['subjectid'] + \
                    [x.variable for x in variables.filter(table=t)]
            else:
                columns = ['subjectid'] + dd[dd.table == t].variable.tolist()
            df = pd.read_sql_table(table_name=table_name,
                                   con=self.postgres_url,
                                   schema=schema,
                                   columns=columns)
            df.subjectid = df.subjectid.astype(str)
            if table_name.startswith('gt'):
                df['family_id'] = df.subjectid.str[:9]
            else:
                df['family_id'] = df.subjectid.str[:5].tolist()
            dfs.append(df)
        data = dfs[0]
        if len(dfs) > 0:
            for i in range(1, len(dfs)):
                data = data.merge(dfs[i], on='family_id', how='outer')
                data.insert(0, 'subjectid',
                            data.subjectid_x.fillna(data.subjectid_y))
                data = data.drop(columns=['subjectid_x', 'subjectid_y'])
        if dd is not None:
            data = DBQuery.handle_data(data, dd)
        if dropna is True:
            for col in data.columns:
                data[col] = data[col].apply(
                    lambda x: pd.NA if NAcheck(x).isna else x)
            data = data.dropna()
        if dropnaCat is True:
            data = data.replace('9999: Unknown', pd.NA)
            data = data.dropna()
        return data
