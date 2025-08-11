class AirflowDAGs:
    """
    A utility class to manage Airflow DAGs via the Airflow REST API.

    Provides asynchronous methods to trigger DAG runs, delete DAGs,
    and pause or unpause one or all DAGs.

    Args:
        client: An HTTP client instance with an async method `api_request`
                to communicate with the Airflow REST API.
    """
    def __init__(self, client):
        self.client = client

    async def get_dags_list(self) -> list:
        """
        Fetch all available Airflow DAGs via the Airflow REST API.

        Sends a GET request to the `/dags` endpoint and retrieves a list of DAGs.
        Returns only the DAG IDs, omitting other metadata.

        Returns:
            list: A list of DAG IDs as strings. If an error occurs, a string error message is returned.
        """
        endpoint = "dags"
        method = 'get'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response

        # Extract just the dag_id values from the response
        return [dag["dag_id"] for dag in response.get("dags", [])]
    
    async def get_dag_details(self,dag_id) -> list:
        """
        Fetch detailed information for a specific Airflow DAG.

        Sends a GET request to the `/dags/{dag_id}/details` endpoint to retrieve
        metadata and configuration related to the given DAG.

        Args:
            dag_id (str): The DAG identifier.

        Returns:
            dict: A dictionary containing DAG details such as schedule, tasks, owners, etc.
                If an error occurs, a string error message is returned.
        """
        endpoint = f"dags/{dag_id}/details"
        method = 'get'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response 

        return response
    
    async def get_dag_runs(self, dag_id: str):
        """
        Fetch all runs for a specific DAG.

        Sends a GET request to the `/dags/{dag_id}/dagRuns` endpoint to retrieve
        all runs associated with the specified DAG.

        Args:
            dag_id (str): The identifier of the DAG.

        Returns:
            list: A list of dictionaries containing details of each DAG run.
                  If an error occurs, a string error message is returned.
        """
        endpoint = f"dags/{dag_id}/dagRuns"
        method = 'get'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response

        return response.get("dag_runs", [])

    async def trigger_dag(self, dag_id: str):
        """
        Trigger a DAG run for the specified DAG ID.

        Sends a POST request to the `/dags/{dag_id}/dagRuns` endpoint with
        the current UTC logical date to initiate a new DAG run.

        Args:
            dag_id (str): The identifier of the DAG to trigger.

        Returns:
            dict or str: The response from Airflow API if successful;
                         otherwise, an error message string.
        """
        from datetime import datetime, timezone

        endpoint = f"dags/{dag_id}/dagRuns"
        method = 'post'

        logical_date = datetime.now(timezone.utc).isoformat()

        payload = { "logical_date": logical_date }

        response = await self.client.api_request(endpoint, method, json=payload)

        if isinstance(response, str):
            return response 

        return response
    
    async def clear_dag_run(self, dag_id: str, dag_run_id: str, dry_run: bool = True, only_failed: bool = False):
        """
        Clear a specific DAG run in Airflow.

        Args:
            dag_id (str): The DAG ID.
            dag_run_id (str): The DAG run ID to clear (e.g., 'scheduled__2025-08-10T00:00:00+00:00').
            dry_run (bool): If True, only simulate the clear operation (default: True).
            only_failed (bool): If True, only clear failed task instances (default: False).

        Returns:
            dict: The API response or error.
        """
        # Encode the DAG run ID properly for URL
        from urllib.parse import quote

        encoded_dag_run_id = quote(dag_run_id, safe='')

        endpoint = f"dags/{dag_id}/dagRuns/{encoded_dag_run_id}/clear"
        method = "post"

        payload = {
            "dry_run": dry_run,
            "only_failed": only_failed
        }

        response = await self.client.api_request(endpoint, method, json=payload)

        return response

    async def delete_dag(self, dag_id: str):
        """
        Delete a DAG from Airflow by its DAG ID.

        Sends a DELETE request to the `/dags/{dag_id}` endpoint.

        Args:
            dag_id (str): The identifier of the DAG to delete.

        Returns:
            dict or str: The response from Airflow API if successful;
                         otherwise, an error message string.
        """
        endpoint = f"dags/{dag_id}"
        method = 'delete'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response 

        return response
    
    async def pause_dags(self, dag_id: str, pause: bool):
        """
        Pause or unpause a single DAG by updating its `is_paused` status.

        Sends a PATCH request to the `/dags/{dag_id}` endpoint with the
        pause flag.

        Args:
            dag_id (str): The identifier of the DAG to pause/unpause.
            pause (bool): True to pause the DAG, False to unpause.

        Returns:
            dict: A dictionary containing the `dag_id` and the result of the API call.
        """
        endpoint = f"dags/{dag_id}"
        payload = {"is_paused": pause}

        return {
            "dag_id": dag_id,
            "result": await self.client.api_request(endpoint, "patch", json=payload)
        }

    async def pause_all_dags(self, pause: bool = True):
        """
        Pause or unpause all DAGs concurrently.

        Fetches the list of all DAGs, then issues PATCH requests in parallel
        to update their `is_paused` status.

        Args:
            pause (bool, optional): True to pause all DAGs, False to unpause.
                                    Defaults to True.

        Returns:
            list: A list of results or exceptions from each concurrent PATCH request.
                  If fetching DAGs fails, returns an error string.
        """
        import asyncio
        
        # Step 1: Get all DAGs
        response = await self.client.api_request("dags", "get")
        if isinstance(response, str):
            return f"Failed to get DAGs: {response}"

        dags = response.get("dags", [])
        if not dags:
            return "No DAGs found."

        # Step 2: Prepare concurrent PATCH tasks
        tasks = [self.pause_dags(dag["dag_id"], pause) for dag in dags]

        # Step 3: Run all PATCH requests in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return results


