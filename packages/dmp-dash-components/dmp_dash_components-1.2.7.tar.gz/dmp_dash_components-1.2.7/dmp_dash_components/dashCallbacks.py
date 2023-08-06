class dashCallbacks:
    def __init__(self, ctx_content):
        self.inputs_list = ctx_content.inputs_list
        self.triggered = ctx_content.triggered
        self.states_list = ctx_content.states_list
        self.outputs_list = ctx_content.outputs_list

    @property
    def input_ids(self):
        ids = []
        for x in self.inputs_list:
            if type(x) == dict:
                if type(x['id']) == dict:
                    ids.append(x['id']['index'])
                else:
                    ids.append(x['id'])
            elif type(x) == list:
                for y in x:
                    if type(y['id']) == dict:
                        ids.append(y['id']['index'])
                    else:
                        ids.append(y['id'])
        return ids

    @property
    def prop_ids(self):
        ids = []
        if self.triggered:
            ids = [x['prop_id'] for x in self.triggered]
        ids = [self.get_id(x) for x in ids]
        return ids

    @property
    def prop_dt(self):
        ids = self.prop_ids
        return dict(zip(ids, [x['value'] for x in self.triggered]))

    @property
    def state_dt(self):
        dts = []
        for state in self.states_list:
            ids = [self.get_id(x['id']) for x in state]
            values = [x['value'] for x in state]
            dts.append(dict(zip(ids, values)))
        return dts

    @staticmethod
    def get_id(id_text):
        id = id_text
        if type(id) == str:
            if '{' in id:
                id = id.split('","t')[0].split('":"')[1]
        elif type(id) == dict:
            if id.get('index'):
                id = id['index']
        return id

    @staticmethod
    def sort_options(options, ids):
        option_list = []
        for op in options:
            try:
                option_list.append([x['value'] for x in op])
            except:
                option_list.append(op)
        options = dict(zip(ids, option_list))
        return options

    @staticmethod
    def keyenter(key_press):
        keyEnter = False
        if key_press is not None:
            if key_press.get('key') == 'Enter':
                keyEnter = True
        return keyEnter
