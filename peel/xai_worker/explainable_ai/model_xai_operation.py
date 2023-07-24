from textwrap import dedent

from juicer.operation import Operation
from juicer.service.limonero_service import query_limonero
from juicer.service.tahiti_service import query_tahiti


class ModelXAIOperation(Operation):

    MODEL_PARAM = 'model'

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)
        self.parameters = parameters

        self.platform_type = None

        self.model = parameters.get(self.MODEL_PARAM)
        if not self.model:
            msg = 'Missing parameter model'
            raise ValueError(msg)

        self.has_code = any([len(named_outputs) > 0, self.contains_results()])
        self.output_model = named_outputs['model_out_port']

    def generate_code(self):

        limonero_config = self.parameters.get('configuration').get('juicer').get('services').get('limonero')
        url_a = limonero_config['url']
        token = str(limonero_config['auth_token'])

        model_data = query_limonero(url_a, '/models', token, self.model)
        parts = model_data['class_name'].split('.')
        self.platform_type = parts[0].upper()
        url = model_data['storage']['url']
        if url[-1] != '/':
            url += '/'

        path = '{}{}'.format(url, model_data['path'])

        tahiti_config = self.parameters.get('configuration').get('juicer').get('services').get('tahiti')
        urliti = tahiti_config['url']
        workflow_id = model_data['workflow_id']

        resp_tahiti = query_tahiti(base_url=urliti,
                                   item_path='/workflows',
                                   token=str(tahiti_config['auth_token']),
                                   item_id=workflow_id, qs=f'lang=pt')
        id_ds = None
        for task in resp_tahiti['tasks']:
            if 'data_source' in task['forms']:
                id_ds = task['forms']['data_source']['value']
                break

        data_source_used = query_limonero(url_a, '/datasources', token, id_ds)
        the_url = data_source_used['url']

        code = dedent("""
            platform_type = '{plat_type}'
            url = '{the_url}'            
            import pandas as pd
            pandas_df = pd.read_csv(url) 

            if platform_type == 'PYSPARK':            
                from {pkg} import {cls}
                {output} = [{cls}.load('{path}'), pandas_df]

            elif platform_type == 'SKLEARN':
                path = '{path}'
                fmp = path.split('/')
                fmt_ = '/'.join(fmp[1:])
                import pickle
                from pyarrow import fs as my_fs
                fs = my_fs.LocalFileSystem()
                exists = fs.get_file_info(fmt_).is_file
                if not exists:
                    raise ValueError('The file in this path dont exists')
                with fs.open_input_stream(fmt_) as stream:
                    rd = stream.readall()
                from {sk_class_path} import {sklearn_class}
                {output} = [pickle.loads(rd), pandas_df, url, fmt_]
            else:
                 raise ValueError('PEEL cant load this type of platform: {plat_type}!!')
        """.format(
            plat_type=self.platform_type,
            output=self.output_model,
            path=path,
            cls=parts[-1],
            the_url=the_url,
            sk_class_path='.'.join(parts[:2]),
            sklearn_class=parts[-1],
            pkg='.'.join(parts[:-1])
        ))
        return code

    def get_output_names(self, sep=','):
        return self.output_model


