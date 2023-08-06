from odd_models.models import (
    DataTransformer,
    DataEntity,
    DataEntityType,
    DataEntityList,
    DataTransformerRun,
    JobRunStatus,
    DataEntityGroup
)

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from odd_models.integrator import OddIntegrator
import datetime

import logging


@dataclass
class TaskWithIO:
    dag_id: str
    task_id: str
    input_oddrns: Optional[List[str]]
    output_oddrns: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]


logger = logging.getLogger("AirflowOddIntegrator")


class AirflowOddIntegratorException(Exception):
    def __init__(self, message):
        super().__init__(message)


class AirflowOddIntegrator(OddIntegrator):
    def __create_dag_entity(self, dag_id: str, tasks_oddrns: List[str], metadata: Dict[str, Any] = None):
        de = DataEntity(
            oddrn=f"{self.source_oddrn}/dags/{dag_id}",
            name=dag_id,
            type=DataEntityType.DAG,
            data_entity_group=DataEntityGroup(
                entities_list=tasks_oddrns
            ),
        )
        if metadata is not None:
            de.metadata = self.create_metadata_extension_list(metadata)
        return de

    service_name = 'airflow'

    def __create_task_entity(self,
                             dag_id: str,
                             task_id: str,
                             inputs_oddrn_list: List[str] = None,
                             outputs_oddrn_list: List[str] = None,
                             metadata: Dict[str, Any] = None
                             ):
        de = DataEntity(
            oddrn=f"{self.source_oddrn}/dags/{dag_id}/tasks/{task_id}",
            name=task_id,
            type=DataEntityType.JOB,
            data_transformer=DataTransformer(
                inputs=inputs_oddrn_list,
                outputs=outputs_oddrn_list
            )

        )
        if metadata is not None:
            de.metadata = self.create_metadata_extension_list(metadata)
        return de

    def __create_task_run_entity(self,
                                 dag_id: str, task_id: str, start_time: datetime, end_time: datetime,
                                 success: bool = True, error_message: str = ""
                                 ):
        return DataEntity(
            name=f"task_run-{end_time}",
            oddrn=f"{self.source_oddrn}/dags/{dag_id}/tasks/{task_id}/runs/{end_time}",
            type=DataEntityType.JOB_RUN,
            data_transformer_run=DataTransformerRun(
                transformer_oddrn=f"{self.source_oddrn}/dags/{dag_id}/tasks/{task_id}",
                start_time=start_time,
                end_time=end_time,
                status_reason=error_message,
                status=JobRunStatus.SUCCESS if success else JobRunStatus.FAILED,
            ),
        )

    def push_dag_entity_with_tasks(self, dag_id: str, tasks_with_io: List[TaskWithIO], dag_meta: Dict[str, Any] = None) \
            -> int:
        tasks_ents = [self.__create_task_entity(task.dag_id, task.task_id, task.input_oddrns, task.output_oddrns,
                                                task.metadata)
                      for task in tasks_with_io]
        dag_entity = self.__create_dag_entity(dag_id, [task_entity.oddrn for task_entity in tasks_ents],
                                              metadata=dag_meta)
        odd_request = DataEntityList(
            items=[*tasks_ents, dag_entity], data_source_oddrn=self.source_oddrn
        )
        resp = self.platform_client.post_data_entity_list(
            odd_request
        )
        return resp.status_code

    def push_task_run(self,
                      dag_id: str, task_id: str, start_time: datetime, end_time: datetime,
                      success: bool = True, error_message: str = ""
                      ) -> int:
        run_entity = self.__create_task_run_entity(dag_id, task_id, start_time, end_time, success, error_message)

        odd_request = DataEntityList(
            items=[run_entity], data_source_oddrn=self.source_oddrn
        )
        resp = self.platform_client.post_data_entity_list(
            odd_request
        )
        return resp.status_code
