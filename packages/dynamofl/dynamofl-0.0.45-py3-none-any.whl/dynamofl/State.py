from time import sleep
from importlib import import_module

from .Base import _Base
from .Project import _Project
from .Datasource import _Datasource

class _State(_Base):

    def __init__(self, token, host='https://api.dynamofl.com', metadata=None):
        super().__init__(token, host)

        self.project_participants = []
        self.datasources = {}
        self.instance_id = None
        self.metadata = metadata

    def _get_last_fed_model_round(self, current_round, is_complete):
        if is_complete:
            return current_round
        else:
            return current_round - 1

    def train_and_test_callback(self, datasource_key, project_info):
        project_key = project_info['key']
        project = _Project(self.token, self.host, project_key)

        # on some project round completed
        # get appropriate train, test methods
        for p in self.project_participants:
            if project_key == p['project_key'] and datasource_key == p['datasource_key']:
                trainer_key = p['trainer_key']
                hyper_param_values = p['hyper_param_values']
                break

        if trainer_key not in self.datasources[datasource_key].trainers and not project_info['hasDynamicTrainer']:
            return

        if project_info['hasDynamicTrainer']:
            mod = import_module(f'dynamic_trainers.{project_key}.train')
            train = getattr(mod, 'train')
            test = getattr(mod, 'test')
        else:    
            train = self.datasources[datasource_key].trainers[trainer_key]['train']
            test = self.datasources[datasource_key].trainers[trainer_key]['test']
        model_path = 'models'
        if 'model_path' in self.datasources[datasource_key].trainers.get(trainer_key, {}):
            model_path = self.datasources[datasource_key].trainers[trainer_key]['model_path']

        ext = project_info['modelType']
        current_round = project_info['currentRound']
        prev_round = self._get_last_fed_model_round(current_round, project_info['isComplete'])
        federated_model_path = get_federated_path(project_key, model_path, ext, datasource_key, prev_round)

        yes_stats = self._check_stats(project_info, datasource_key, prev_round)
        yes_submission = self._check_submissions(project_info, datasource_key, current_round)

        if not yes_submission or not yes_stats:
            # Pull
            print(f'>>> ({project_key}-{datasource_key}) Waiting to download round ({prev_round}) federated model...')
            project.pull_model(federated_model_path, round=prev_round, datasource_key=datasource_key, federated_model=True)

        # Test
        if not yes_stats:
            print(f'>>> ({project_key}-{datasource_key}) Running validation on round ({prev_round}) federated model...')
            test_res = test(datasource_key, federated_model_path, project_info)
            if test_res is not None:
                scores, num_samples = test_res
                print(scores)
                print(f'>>> ({project_key}-{datasource_key}) Uploading scores...')
                project.report_stats(scores, num_samples, prev_round, datasource_key)
                print('Done.')
            print()

        # Train and push
        if not yes_submission:
            new_model_path = get_trained_path(project_key, model_path, ext, datasource_key, current_round)

            print(f'>>> ({project_key}-{datasource_key}) Training weights on local model...')
            train_res = train(datasource_key, federated_model_path, new_model_path, project_info, hyper_param_values)

            print(f'>>> ({project_key}-{datasource_key}) Uploading round ({current_round}) trained model...')
            if train_res:
                project.push_model(new_model_path, datasource_key, params=train_res)
            else:
                project.push_model(new_model_path, datasource_key)
            print('Done.')
            print()

    def initiate_project_participants(self, should_fetch_bridges=False, should_spawn_train=False, ds=None):

        if should_fetch_bridges:
            if ds:
                datasources = [ds] # targeting specific datasource, we form an array with only one ds key
            else:
                datasources = self.datasources # all datasources as a dict
                self.project_participants = [] 

            for ds_key in datasources:
                j = self._make_request('GET', '/bridges', params={'datasourceKey': ds_key})
                for i in j['data']:
                    self.project_participants.append({
                        'project_key': i['projectKey'],
                        'datasource_key': i['datasourceKey'],
                        'trainer_key': i['trainerKey'],
                        'hyper_param_values': i['hyperParamValues'],
                        'labeled': i['isLabelled']
                    })
        if should_spawn_train:
            for p in self.project_participants:
                project_key = p['project_key']
                datasource_key = p['datasource_key']
                '''
                The first time attach_datasource() we might find 1 previous project for that ds1.
                So project_participants = [item1]
                The next time it is called it might also find 1 previous project for ds2
                So project_participants = [item1, item2]
                We only want create a thread for items that we haven't done so already
                '''
                # if threads_key in self.dfl.on_round_threads:
                #     continue
                if ds and ds != datasource_key:
                    continue

                info = self._make_request('GET', f'/projects/{project_key}')

                # todo
                # take this out and put logic on the server
                if info['isSemiSupervised']:
                    if (info['currentRound'] % 2 == 0 and p['labeled']) or (info['currentRound'] % 2 == 1 and not p['labeled']):
                        continue

                self.train_and_test_callback(datasource_key, info)

    # creates a new datasource in the api
    def attach_datasource(self, key, name=None, metadata=None):

        while not self.instance_id:
            sleep(0.1)

        params = { 'key': key, 'instanceId': self.instance_id }
        if name is not None:
            params['name'] = name
        if self.metadata is not None:
            params['metadata'] = self.metadata
        if metadata is not None:
            params['metadata'] = metadata

        found_datasources = self._make_request('GET', '/datasources', params={'key': key}, list=True)
        if len(found_datasources):
            self._make_request('POST', f'/datasources/{key}', params=params)
        else:
            self._make_request('POST', '/datasources', params=params)


        ds = _Datasource(self, key)
        self.datasources[key] = ds
        self.initiate_project_participants(should_fetch_bridges=True, ds=key)

        return ds

    def delete_datasource(self, key):
        return self._make_request('DELETE', f'/datasources/{key}')

    def delete_project(self, key):
        return self._make_request('DELETE', f'/projects/{key}')

    def get_user(self):
        return self._make_request('GET', '/user')

    def create_project(self, base_model_path, params, dynamic_trainer_path=None):
        j = self._make_request('POST', '/projects', params=params)

        project = _Project(self.token, self.host, j['key'])
        project.push_model(base_model_path, None)

        if dynamic_trainer_path:
            with open(dynamic_trainer_path, 'rb') as f:
                self._make_request('POST', f'/projects/{project.key}/files', files={'file': f})

        return project

    def get_project(self, project_key):
        j = self._make_request('GET', f'/projects/{project_key}')
        return _Project(self.token, self.host, j['key'])

    def get_projects(self):
        return self._make_request('GET', '/projects', list=True)

    def _check_submissions(self, project_info, datasource_key, round):
        params = {
            'owned': True,
            'datasource': datasource_key,
            'round': round
        }
        project_key = project_info['key']
        user_submissions = self._make_request('GET', f'/projects/{project_key}/submissions', params, list=True)
        # if sampled project, check if round reached full size
        if 'clientSampleSize' in project_info and project_info['clientSampleSize']:
            all_submissions = self._make_request('GET', f'/projects/{project_key}/submissions', { 'round': round }, list=True)
            if len(all_submissions) < project_info['clientSampleSize']:
                return False
            else:
                return True
        else:
            return len(user_submissions)

    def _check_stats(self, project_info, datasource_key, round):
        params = {
            'owned': True,
            'datasource': datasource_key,
            'round': round
        }
        project_key = project_info['key']
        user_stats = self._make_request('GET', f'/projects/{project_key}/stats', params, list=True)
        # if sampled project, check if round reached full size
        if 'clientSampleSize' in project_info and project_info['clientSampleSize']:
            all_stats = self._make_request('GET', f'/projects/{project_key}/stats', { 'round': round }, list=True)
            if len(all_stats) < project_info['clientSampleSize']:
                return False
            else:
                return True
        else:
            return len(user_stats)

def get_federated_path(project_key, base, ext, ds, round):
    return f'{base}/federated_model_{project_key}_{ds}_{round}.{ext}'

def get_trained_path(project_key, base, ext, ds, round):
    return f'{base}/trained_model_{project_key}_{ds}_{round}.{ext}'
