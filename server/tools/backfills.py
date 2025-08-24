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
    
    async def get_backfill(self, backfill_id: int):
        """
        Retrieve details of a specific backfill job by its ID.

        Sends a GET request to the `/backfills/{backfill_id}` endpoint to fetch
        information about the specified backfill job.

        Args:
            backfill_id (int): The unique identifier of the backfill job.

        Returns:
            dict or str: A dictionary containing backfill details if successful,
                         or an error message string if the request fails.
        """
        endpoint = f"backfills/{backfill_id}"
        method = 'get'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response 
         
        return response
    
    async def pause_backfill(self, backfill_id: int):
        """
        Pause a specific backfill job by its ID.

        Sends a POST request to the `/backfills/{backfill_id}/pause` endpoint
        to pause the specified backfill job.

        Args:
            backfill_id (int): The unique identifier of the backfill job to pause.

        Returns:
            dict or str: A dictionary containing the response from the API if successful,
                         or an error message string if the request fails.
        """
        endpoint = f"backfills/{backfill_id}/pause"
        method = 'put'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response 
        
        return response

    async def unpause_backfill(self, backfill_id: int): 
        """
        Unpause a specific backfill job by its ID.

        Sends a POST request to the `/backfills/{backfill_id}/unpause` endpoint
        to unpause the specified backfill job.

        Args:
            backfill_id (int): The unique identifier of the backfill job to unpause.

        Returns:
            dict or str: A dictionary containing the response from the API if successful,
                         or an error message string if the request fails.
        """
        endpoint = f"backfills/{backfill_id}/unpause"
        method = 'put'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response 
        
        return response
    
    async def cancel_backfill(self, backfill_id: int):
        """
        Cancel a specific backfill job by its ID.

        Sends a POST request to the `/backfills/{backfill_id}/cancel` endpoint
        to cancel the specified backfill job.

        Args:
            backfill_id (int): The unique identifier of the backfill job to cancel.

        Returns:
            dict or str: A dictionary containing the response from the API if successful,
                         or an error message string if the request fails.
        """
        endpoint = f"backfills/{backfill_id}/cancel"
        method = 'put'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response 
        
        return response
    
    async def backfill_dry_runs(self,
        dag_id: str,
        from_date: str,
        to_date: str,
        run_backwards: bool = False,
        reprocess_behavior: str = "none",
        max_active_runs: int = 10,
        dag_run_conf: dict = {},
        ):
        """
        Simulate a backfill operation and preview the resulting DAG runs.

        This method sends a POST request to the `/backfills/dry_run` endpoint to perform a dry run
        for the specified DAG and time range. It does not trigger any actual backfill jobs, but
        returns a list of DAG runs that would be created if the backfill were executed.

        Args:
            dag_id (str): The identifier of the DAG to simulate the backfill for.
            from_date (str): The start date of the backfill range (ISO 8601 format).
            to_date (str): The end date of the backfill range (ISO 8601 format).
            run_backwards (bool, optional): Whether to run tasks in reverse order. Defaults to False.
            reprocess_behavior (str, optional): Reprocessing behavior ('none', 'all', or 'failed'). Defaults to "none".
            max_active_runs (int, optional): Maximum number of concurrent runs. Defaults to 10.
            dag_run_conf (dict, optional): Optional configuration for the DAG run. Defaults to {}.

        Returns:
            list or str: A list of DAG run details that would be created by the backfill,
                 or an error message string if the request fails.
        """
        endpoint = "backfills/dry_run"
        method = 'post'

        payload = {
            "dag_id": dag_id,
            "from_date": from_date,
            "to_date": to_date,
            "run_backwards": False,
            "dag_run_conf": {},
            "reprocess_behavior": "none",
            "max_active_runs": 10
        }

        response = await self.client.api_request(endpoint, method, json=payload)

        if isinstance(response, str):
            return response 
        
        return response