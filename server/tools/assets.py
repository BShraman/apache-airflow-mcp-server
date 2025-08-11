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