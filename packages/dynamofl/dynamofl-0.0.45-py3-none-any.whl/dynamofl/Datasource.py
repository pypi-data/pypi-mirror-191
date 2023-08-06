from .Base import _Base

class _Datasource(_Base):
    def __init__(self, dfl, key):
        super().__init__(dfl.token, dfl.host)
        self.dfl = dfl
        self.key = key
        self.trainers = {}

    def add_trainer(self, key, train_callback, test_callback, default_hyper_params=None, description=None, model_path=None):
        params = {'key': key}
        if default_hyper_params is not None:
            params['defaultHyperParams'] = default_hyper_params
        if description is not None:
            params['description'] = description
        self._make_request('POST', f'/datasources/{self.key}/trainers', params=params)
        self.trainers[key] = {
            'train': train_callback,
            'test': test_callback,
        }

        if model_path is not None:
            self.trainers[key]['model_path'] = model_path

        self.dfl.initiate_project_participants(should_spawn_train=True, ds=self.key)