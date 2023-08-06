from airflow.plugins_manager import AirflowPlugin
import listener


class OddPlugin(AirflowPlugin):
    name = "OddPlugin"
    listeners = [listener]
