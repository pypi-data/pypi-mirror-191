import os
import json
import threading
import websocket
import requests
import shutil
import pathlib
import zipfile

from .Base import _Base, _check_for_error

RETRY_AFTER = 5 # seconds

class _MessageHandler(_Base):

    def __init__(self, state, token, host):
        super().__init__(token, host)

        self.wshost = self.host.replace('http', 'ws', 1)
        self.state = state

        self.ws = websocket.WebSocketApp(
            self.wshost,
            on_open=self._on_open,
            on_message=self._on_message,
            on_close=self._on_close,
            on_error=self._on_error
        )

        self.handlers = {
            'client-info': self.client_info,
            'new-project': self.new_project,
            'project-complete': self.project_complete,
            'round-complete': self.round_complete,
            'hyperparams-updated': self.hyperparams_updated,
            'dynamic-trainer': self.dynamic_trainer,
            'round-error': self.round_error,
        }

    def connect_to_ws(self):
        t = threading.Thread(target=self.ws.run_forever, kwargs={'reconnect': RETRY_AFTER})
        t.daemon = False
        t.start()

    def _on_open(self, ws):
        print('>>> Connection to DynamoFL established.')
        self.ws.send('{ "action": "auth", "token": "' + self.token + '" }')

    def _on_message(self, ws, res):
        j = json.loads(res)

        project_key = None
        if 'data' in j and 'project' in j['data'] and 'key' in j['data']['project']:
            project_key = j['data']['project']['key']

        if j['event'] in self.handlers:
            self.handlers[j['event']](j, project_key)

    def _on_close(self, ws, close_status_code, close_msg):
        print('Connection closed')
        print(close_msg)

    def _on_error(self, ws, error):
        print('Connection error:')
        print(error)
        print(f'Will attempt to reconnect every {RETRY_AFTER} seconds...')

    """
    Message Handlers
    """

    def client_info(self, j, _):
        self.state.instance_id = j['data']['id']
        self.state.initiate_project_participants(should_fetch_bridges=True, should_spawn_train=True)

    def new_project(self, j, _):
        project_key = j['data']['projectKey']
        datasource_key = j['data']['datasourceKey']
        trainer_key = j['data']['trainerKey']
        hyper_param_values = j['data']['hyperParamValues']
        not_sampled = False
        if 'notSampled' in j['data']:
            not_sampled = j['data']['notSampled']

        self.state.project_participants.append({
            'project_key': project_key,
            'datasource_key': datasource_key,
            'trainer_key': trainer_key,
            'hyper_param_values': hyper_param_values
        })

        if not_sampled:
            return

        info = self._make_request('GET', f'/projects/{project_key}')
        self.state.train_and_test_callback(datasource_key, info)

    def project_complete(self, _, project_key):
        self.state.project_participants = list(filter(lambda x : x['project_key'] != project_key, self.state.project_participants))

    def round_complete(self, j, project_key):
        samples = []
        if 'samples' in j['data']:
            samples = j['data']['samples']

        for p in self.state.project_participants:
            if project_key == p['project_key']:
                if not len(samples) or p['datasource_key'] in samples:
                    self.state.train_and_test_callback(p['datasource_key'], j['data']['project'])

    def hyperparams_updated(self, j, project_key):
        for p in self.state.project_participants:
            if project_key == p['project_key'] and p['datasource_key'] == j['data']['datasourceKey']:
                p['hyper_param_values'] = j['data']['hyperParamValues']

    def dynamic_trainer(self, j, project_key):
        if os.path.isdir(f'dynamic_trainers/{project_key}'):
            return

        filename = j['data']['filename']

        url = f'{self._get_route()}/projects/{project_key}/files/{filename}'
        r = requests.get(url, headers=self._get_headers())
        _check_for_error(r)

        filepath = f'dynamic_trainers/{project_key}_{filename}'

        directory = os.path.dirname(filepath)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            parent_dir_name = zip_ref.namelist()[0][:-1]
            zip_ref.extractall(directory)
        shutil.move(directory + '/' + parent_dir_name, directory + '/' + project_key)
        os.remove(filepath)

    def round_error(self, j, project_key):
        for p in self.state.project_participants:
            print('Federation error occured:\n  ' + j['data']['errorMessage'])
