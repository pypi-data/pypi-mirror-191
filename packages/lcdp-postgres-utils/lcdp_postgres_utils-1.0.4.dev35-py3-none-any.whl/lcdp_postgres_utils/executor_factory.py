from .executors import *


class ExecutorFactory:
    def __init__(self, engine_version="13"):
        self.engine_version = engine_version.split('.')[0]

    def build(self, database_name, endpoint, user_name, ssm_db_password_path):
        try:
            klass = globals()["Executor{0}".format(self.engine_version)]
            return klass(database_name, endpoint, user_name, ssm_db_password_path)
        except KeyError:
            raise Exception(f"Postgres engine {self.engine_version} is not supported, please provide an executor")
