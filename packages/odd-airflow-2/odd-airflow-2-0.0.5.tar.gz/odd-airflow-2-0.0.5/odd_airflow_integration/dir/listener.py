import logging
import threading
from .airflow_odd_integrator import TaskWithIO, AirflowOddIntegrator, AirflowOddIntegratorException
from concurrent.futures import Executor
from airflow.hooks.base import BaseHook
from airflow.models.operator import Operator
from airflow.models.dag import DAG
from typing import TYPE_CHECKING, Callable, Optional, Dict, Any, Union
from airflow.listeners import hookimpl

if TYPE_CHECKING:
    from airflow.models import DagRun, TaskInstance

log = logging.getLogger("airflow")
# TODO: move task instance runs to executor
executor: Optional[Executor] = None

con = BaseHook.get_connection('odd')
host = con.host
port = con.port
url = f"{host}:{port}" if port is not None else host
integrator = AirflowOddIntegrator(url, con.get_password())


def execute_in_thread(target: Callable, kwargs=None):
    if kwargs is None:
        kwargs = {}
    thread = threading.Thread(target=target, kwargs=kwargs, daemon=True)
    thread.start()
    thread.join(timeout=1)


def task_has_io(task: Operator) -> bool:
    if len(task.inlets) > 0 or len(task.outlets) > 0:
        return True
    return False


def build_meta(obj: Union[Operator, DAG]) -> Dict[str, Any]:
    meta = {"Dag": obj.dag_id}
    if obj.doc_md is not None:
        meta.update({"Doc Md": obj.doc_md})
    if isinstance(obj, DAG):
        meta.update({"schedule": str(obj.schedule_interval)})
    return meta


@hookimpl
def on_dag_run_running(dag_run: "DagRun", msg: str):
    def on_dag_run():
        tasks = dag_run.dag.tasks
        tasks_with_io = [TaskWithIO(dag_run.dag_id, task.task_id, task.inlets, task.outlets, build_meta(task))
                         for task in tasks if
                         task_has_io(task)]
        reg_status = integrator.register_source()
        if reg_status != 200:
            log.error('odd source is not registered')
        else:
            if len(tasks_with_io) > 0:
                dag_status = integrator.push_dag_entity_with_tasks(dag_run.dag_id, tasks_with_io,
                                                                   dag_meta=build_meta(dag_run.dag))
                if dag_status != 200:
                    log.error('Dags are not sent')
                else:
                    pass
            else:
                pass

    execute_in_thread(on_dag_run)


@hookimpl
def on_task_instance_success(previous_state, task_instance: "TaskInstance", session):
    def on_task_success():
        run_status = integrator.push_task_run(task_instance.task.dag_id, task_instance.task_id,
                                              task_instance.start_date,
                                              task_instance.end_date
                                              )

        if run_status != 200:
            log.error('run is not sent')
            raise AirflowOddIntegratorException(str(run_status))
        else:
            pass

    execute_in_thread(on_task_success)


@hookimpl
def on_task_instance_failed(previous_state, task_instance: "TaskInstance", session):
    def on_task_failed():
        resp = integrator.push_task_run(task_instance.dag_id, task_instance.task_id,
                                        task_instance.start_date,
                                        task_instance.end_date,
                                        False,
                                        "Task Failed"
                                        )

    execute_in_thread(on_task_failed)
