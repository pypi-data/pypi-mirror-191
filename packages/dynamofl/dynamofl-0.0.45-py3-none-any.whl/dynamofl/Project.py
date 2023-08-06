import os
import pathlib

import requests

from .Base import _Base


class _Project(_Base):
    def __init__(self, token, host, key):
        super().__init__(token, host)
        self.key = key

    def get_info(self):
        return self._make_request('GET', f'/projects/{self.key}')

    def update_rounds(self, rounds):
        return self._make_request('POST', f'/projects/{self.key}', params={'rounds': rounds})

    def update_schedule(self, schedule):
        return self._make_request('POST', f'/projects/{self.key}', params={'schedule': schedule})

    def update_paused(self, paused):
        return self._make_request('POST', f'/projects/{self.key}', params={'paused': paused})

    def update_auto_increment(self, auto_increment):
        return self._make_request('POST', f'/projects/{self.key}', params={'autoIncrement': auto_increment})

    def update_optimizer_params(self, optimizer_params):
        return self._make_request('POST', f'/projects/{self.key}', params={'optimizerParams': optimizer_params})

    def update_contributor(self, email, role):
        return self._make_request('POST', f'/projects/{self.key}/contributors/{email}', params={'role': role})

    def delete_project(self):
        return self._make_request('DELETE', f'/projects/{self.key}')

    def add_contributor(self, email, role='member'):
        return self._make_request('POST', f'/projects/{self.key}/contributors', params={'email': email, 'role': role})

    def delete_contributor(self, email):
        return self._make_request('DELETE', f'/projects/{self.key}/contributors', params={'email': email})

    def get_next_schedule(self):
        return self._make_request('GET', f'/projects/{self.key}/schedule')

    def increment_round(self):
        return self._make_request('POST', f'/projects/{self.key}/increment')

    def get_rounds(self):
        return self._make_request('GET', f'/projects/{self.key}/rounds', list=True)

    def get_round(self, round):
        return self._make_request('GET', f'/projects/{self.key}/rounds/{round}')

    def get_stats(self, round=None, datasource_key=None):
        params = {}
        if round is not None:
            params['round'] = round
        if datasource_key is not None:
            params['datasource'] = datasource_key
        return self._make_request('GET', f'/projects/{self.key}/stats', params, list=True)

    def get_stats_avg(self):
        return self._make_request('GET', f'/projects/{self.key}/stats/avg')

    def get_submissions(self, datasource_key=None, round=None, owned=None):
        params = {}
        if round is not None:
            params['round'] = round
        if datasource_key is not None:
            params['datasource'] = datasource_key
        if owned is not None:
            params['owned'] = owned
        return self._make_request('GET', f'/projects/{self.key}/submissions', params, list=True)

    def upload_optimizer(self, path):
        with open(path, 'rb') as f:
            self._make_request('POST', f'/projects/{self.key}/optimizers', files={'optimizer': f})

    def report_stats(self, scores, num_samples, round, datasource_key):
        return self._make_request('POST', f'/projects/{self.key}/stats', params={
            'round': round,
            'scores': scores,
            'numPoints': num_samples,
            'datasource': datasource_key
        })

    def push_model(self, path, datasource_key, params=None):
        if params is not None:
            self._make_request('POST', f'/projects/{self.key}/models/{datasource_key}/params', params={'params': params})

        if datasource_key is None:
            url = f'/projects/{self.key}/models'
        else:
            url = f'/projects/{self.key}/models/{datasource_key}'
        with open(path, 'rb') as f:
            file_name = os.path.basename(path)
            params = {
                'filename':  file_name,
                'datasourceKey': datasource_key
            }
            upload_url = self._make_request('GET', f'/projects/{self.key}/models/presigned-url', params=params)['url']
            r = requests.put(upload_url, data=f.read())
            if not r.ok:
                print(r.text)
            r.raise_for_status()

            try:
                self._make_request('POST', url, print_error=False)
            except Exception as e:
                if str(e).find('Model will not be uploaded.'):
                    print('Model not sampled.')
                else:
                    raise e
            

    def pull_model(self, filepath, datasource_key=None, round=None, federated_model=None):
        params = {
            'usePresignedUrl': True
        }
        if round is not None:
            params['round'] = round
        if federated_model is not None:
            params['federatedModel'] = federated_model

        if datasource_key is None:
            url = f'/projects/{self.key}/models'
        else:
            url = f'/projects/{self.key}/models/{datasource_key}'
        download_url = self._make_request('GET', url, params=params)['url']
        directory = os.path.dirname(filepath)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        r = requests.get(download_url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=None): 
                f.write(chunk)

    def add_datasource_and_trainer(self, datasource_key, trainer_key, hyper_param_values={}, labeled=True):
        return self._make_request('POST', '/bridges', params={
            'projectKey': self.key,
            'datasourceKey': datasource_key,
            'trainerKey': trainer_key,
            'hyperParamValues': hyper_param_values,
            'labeled': labeled
        })
 