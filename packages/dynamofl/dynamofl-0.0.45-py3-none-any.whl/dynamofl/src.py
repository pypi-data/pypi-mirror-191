from .State import _State
from .MessageHandler import _MessageHandler

RETRY_AFTER = 5 # seconds

class DynamoFL():
    def __init__(self, token, host='https://api.dynamofl.com', metadata=None):
        self._state = _State(token, host, metadata)

        self._messagehandler = _MessageHandler(self._state, token, host)
        self._messagehandler.connect_to_ws()

    def attach_datasource(self, key, name=None, metadata=None):
        return self._state.attach_datasource(key, name, metadata)

    def delete_datasource(self, key):
        return self._state.delete_datasource(key)

    def delete_project(self, key):
        return self._state.delete_project(key)

    def get_user(self):
        return self._state.get_user()

    def create_project(self, base_model_path, params, dynamic_trainer_path=None):
        return self._state.create_project(base_model_path, params, dynamic_trainer_path)

    def get_project(self, project_key):
        return self._state.get_project(project_key)

    def get_projects(self):
        return self._state.get_project()
