class AirflowAssets:
    """Class to manage Airflow assets."""

    def __init__(self, client):
        self.client = client

    async def get_assets(self) -> list:
        """
        Fetch all Airflow assets via the Airflow REST API.

        Sends a GET request to the `/assets` endpoint and extracts the asset names.
        Assets can represent datasets, code packages, or other resources linked to DAGs.

        Returns:
            list: A list of asset names as strings. If an error occurs, a string error message is returned.
        """
        endpoint = "assets" 
        method = 'get'

        response = await self.client.api_request(endpoint, method)
        if isinstance(response, str):
            return response
        
        # Extract just the name values from the response
        return [asset["name"] for asset in response.get("assets", [])]
    
    async def get_asset_aliases(self) -> dict:
        """
        Returns a mapping of asset aliases to their actual names.

        This is useful for translating user-friendly names to the names used in Airflow.

        Returns:
            dict: A dictionary mapping aliases to actual asset names.
        """
        endpoint = "assets" 
        method = 'get'

        response = await self.client.api_request(endpoint, method)
        if isinstance(response, str):
            return response
        
        #return [asset["name"] for asset in response.get("assets", [])]
        return response
    
    async def get_asset_events(self) -> list:
        """
        Fetch all Airflow asset events via the Airflow REST API.
        Sends a GET request to the `/assets/events` endpoint to retrieve events related to assets.
        Returns:
            list: A list of asset event details. If an error occurs, a string error message is returned.
        """
        endpoint = "assets/events" 
        method = 'get'

        response = await self.client.api_request(endpoint, method)
        if isinstance(response, str):
            return response
        
        return response
    
    async def create_asset_events(self, asset_id:int ) -> str:
        """
        Creates an asset event in Airflow via the Airflow REST API.
        Sends a POST request to the `/assets/events` endpoint to create a new asset event.
        Returns:
            str: A success message or an error message if the operation fails.
        """
        endpoint = "assets/events" 
        method = 'post'
        payload = {
            "asset_id": asset_id,
            "extra": {
                "additionalProp1": {}
            }
        }

        response = await self.client.api_request(endpoint, method, json=payload)
        if isinstance(response, str):
            return response

        return response
    
    async def get_asset_queued_events(self, asset_id:int) -> list:
        """
        Fetch queued events for a specific asset via the Airflow REST API.
        Sends a GET request to the `/assets/{asset_id}/events/queued` endpoint to retrieve queued events.
        Returns:
            list: A list of queued asset event details. If an error occurs, a string error message is returned.
        """
        endpoint = f"assets/{asset_id}/queuedEvents"
        method = 'get'

        response = await self.client.api_request(endpoint, method)
        if isinstance(response, str):
            return response

        return response
    
    async def get_dag_asset_queued_events(self, dag_id:str) -> list:
        """
        Fetch queued events for all assets associated with a specific DAG via the Airflow REST API.
        Sends a GET request to the `/dags/{dag_id}/assets/queuedEvents` endpoint to retrieve queued events.
        Returns:
            list: A list of queued asset event details for the specified DAG. If an error occurs, a string error message is returned.
        """
        endpoint = f"dags/{dag_id}/assets/queuedEvents"
        method = 'get'

        response = await self.client.api_request(endpoint, method)
        if isinstance(response, str):
            return response

        return response
    
    async def delete_asset_event(self, event_id:int) -> str:
        """
        Deletes a specific asset event via the Airflow REST API.
        Sends a DELETE request to the `/assets/events/{event_id}` endpoint to remove the specified asset event.
        Returns:
            str: A success message or an error message if the operation fails.
        """
        endpoint = f"assets/{event_id}/queuedEvents"
        method = 'delete'

        response = await self.client.api_request(endpoint, method)
        if isinstance(response, str):
            return response

        return response
    
    async def delete_dag_asset_events(self, dag_id:str) -> str:
        """
        Deletes all asset events associated with a specific DAG via the Airflow REST API.
        Sends a DELETE request to the `/dags/{dag_id}/assets/events` endpoint to remove all asset events for the specified DAG.
        Returns:
            str: A success message or an error message if the operation fails.
        """
        endpoint = f"dags/{dag_id}/assets/queuedEvents"
        method = 'delete'

        response = await self.client.api_request(endpoint, method)
        if isinstance(response, str):
            return response

        return response