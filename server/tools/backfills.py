class AirflowBackfills:
    """
    Resource class to interact with Airflow backfills via the Airflow REST API.

    Args:
        client: An asynchronous HTTP client with a method `api_request`
                for making API calls to Airflow.
    """
    def __init__(self, client):
        self.client = client

    async def list_backfills(self,dag_id: str):
        """
        Retrieves and summarizes backfill runs for a specific DAG.

        Sends a GET request to the Airflow `/backfills` endpoint and filters the results
        for the given `dag_id`. If any backfills are found, it returns a human-readable
        summary including DAG run IDs, states, and time ranges.

        Args:
            dag_id (str): The identifier of the DAG for which to list backfills.

        Returns:
            str: A formatted string summarizing the backfills for the DAG.
                If no backfills are found, a message stating that is returned.
                If an error occurs during the request, the error message is returned.
        """

        endpoint = "backfills"
        method = 'get'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response 

        backfills = response.get("backfills", [])
        total = response.get("total_entries", 0)

        if not backfills:
            return f"No backfills found for DAG '{dag_id}'."

        lines = [f"Found {total} backfills for DAG '{dag_id}':\n"]
        for b in backfills:
            dag_run_id = b.get("dag_run_id", "unknown")
            state = b.get("state", "unknown")
            start_date = b.get("start_date", "N/A")
            end_date = b.get("end_date", "N/A")
            lines.append(f"- Run ID: {dag_run_id}, State: {state}, Start: {start_date}, End: {end_date}")

        return "\n".join(lines)
    
    async def create_backfill(self,
        dag_id: str,
        from_date: str,
        to_date: str,
        run_backwards: bool = False,
        reprocess_behavior: str = "none",
        max_active_runs: int = 10,
        dag_run_conf: dict = {},
    ):
        """ 
        Trigger a backfill job for a given DAG.

        Time fields (`from_date`, `to_date`) must be in ISO 8601 format.
        To use CST, include the `-06:00` offset. Example:

            "2025-08-08T09:00:00-06:00"

        Args:
            dag_id (str): DAG to backfill.
            from_date (str): Start time (ISO 8601, CST or UTC).
            to_date (str): End time (ISO 8601, CST or UTC).
            run_backwards (bool): Run tasks in reverse order.
            reprocess_behavior (str): 'none', 'all', or 'failed'.
            max_active_runs (int): Max concurrent runs.
            dag_run_conf (dict): Optional config for DAG run.

        Returns:
            dict or str: Airflow API response or error.
        """
        endpoint = "backfills"
        method = "post"

        payload = {
            "dag_id": dag_id,
            "from_date": from_date,
            "to_date": to_date,
            "run_backwards": run_backwards,
            "dag_run_conf": dag_run_conf,
            "reprocess_behavior": reprocess_behavior,
            "max_active_runs": max_active_runs
        }

        response = await self.client.api_request(endpoint, method, json=payload)

        return response
