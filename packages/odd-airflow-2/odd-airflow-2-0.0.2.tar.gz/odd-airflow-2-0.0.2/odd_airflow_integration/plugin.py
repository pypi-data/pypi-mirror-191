from airflow.plugins_manager import AirflowPlugin
from odd_airflow_integration import listener


class OddPlugin(AirflowPlugin):
    name = "OddPlugin"
    listeners = [listener]
