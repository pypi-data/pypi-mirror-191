from airflow.plugins_manager import AirflowPlugin
from .dir import listener


class OddPlugin(AirflowPlugin):
    name = "OddPlugin"
    listeners = [listener]
