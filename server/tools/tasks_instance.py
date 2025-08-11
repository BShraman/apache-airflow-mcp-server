class AirflowTasksInstance:
    def __init__(self, client):
        """
        Initializes the AirflowTasksInstance with an HTTP client.

        Args:
            client: An asynchronous HTTP client with a method `api_request`
                    for making API calls to Airflow.
        """
        self.client = client

    async def get_task_instance(
        self,
        dag_id: str,
        dag_run_id: str,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "map_index"
    ):
        """
        Fetch task instances for a given DAG run.

        Args:
            dag_id (str): The DAG ID.
            dag_run_id (str): The DAG run ID (e.g., 'manual__2025-08-03T19:24:23.344927+00:00').
            limit (int): Maximum number of results to return.
            offset (int): Number of items to skip.
            order_by (str): Field to order results by (default: 'map_index').

        Returns:
            dict: List of task instances or error message.
        """
        from urllib.parse import quote

        encoded_dag_run_id = quote(dag_run_id, safe="")

        endpoint = f"dags/{dag_id}/dagRuns/{encoded_dag_run_id}/taskInstances"
        method = "get"
        params = {
            "limit": limit,
            "offset": offset,
            "order_by": order_by
        }

        response = await self.client.api_request(endpoint, method, params=params)

        return response

    async def clear_task_instance(
        self,
        dag_id: str,
        start_date: str,
        end_date: str,
        dry_run: bool = True,
        only_failed: bool = False,
        only_running: bool = False,
        reset_dag_runs: bool = True,
        task_ids: list = None,
        dag_run_id: str = None,
        include_upstream: bool = False,
        include_downstream: bool = False,
        include_future: bool = False,
        include_past: bool = False
    ):
        """
        Clear task instances for a DAG in a specified time range.

        Args:
            dag_id (str): DAG ID.
            start_date (str): ISO 8601 timestamp (e.g., "2025-08-11T01:01:45.016Z").
            end_date (str): ISO 8601 timestamp.
            dry_run (bool): If True, simulate only (default: True).
            only_failed (bool): Clear only failed tasks (default: False).
            only_running (bool): Clear only running tasks (default: False).
            reset_dag_runs (bool): If True, also clear DAG run state (default: True).
            task_ids (list): List of task IDs (can be flat list or nested).
            dag_run_id (str): Specific DAG run ID to target (optional).
            include_upstream (bool): Include upstream tasks (default: False).
            include_downstream (bool): Include downstream tasks (default: False).
            include_future (bool): Include future tasks (default: False).
            include_past (bool): Include past tasks (default: False).

        Returns:
            dict: API response.
        """
        endpoint = f"dags/{dag_id}/clearTaskInstances"
        method = "post"

        payload = {
            "dry_run": dry_run,
            "start_date": start_date,
            "end_date": end_date,
            "only_failed": only_failed,
            "only_running": only_running,
            "reset_dag_runs": reset_dag_runs,
            "task_ids": task_ids or [],
            "dag_run_id": dag_run_id,
            "include_upstream": include_upstream,
            "include_downstream": include_downstream,
            "include_future": include_future,
            "include_past": include_past
        }

        # Remove None values to avoid issues
        payload = {k: v for k, v in payload.items() if v is not None}

        response = await self.client.api_request(endpoint, method, json=payload)

        return response
