class AirflowPool():
    """
    A class to represent an Airflow Pool.
    This class provides methods to manage and interact with Airflow Pools.
    """
    def __init__(self, client):
        self.client = client

    async def get_pools(self) -> list:
        """
        Fetch all available Airflow Pools via the Airflow REST API.

        Sends a GET request to the `/pools` endpoint and retrieves a list of Pools.

        Returns:
            list: A list of Pools as dictionaries. If an error occurs, a string error message is returned.
        """
        endpoint = "pools"
        method = 'get'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response

        return response.get("pools", [])
    
    async def create_pool(self, name: str, slots: int, description: str = "") -> dict | str:
        """
        Create a new Airflow Pool via the Airflow REST API.

        Sends a POST request to the `/pools` endpoint with the provided pool details.

        Args:
            name (str): The name of the new Pool.
            slots (int): The number of slots for the Pool.
            description (str, optional): A description for the Pool. Defaults to an empty string.

        Returns:
            dict: The created Pool as a dictionary. If an error occurs, a string error message is returned.
        """
        endpoint = "pools"
        method = 'post'
        payload = {
            "name": name,
            "slots": slots,
            "description": description
        }

        response = await self.client.api_request(endpoint, method, json=payload)

        if isinstance(response, str):
            return response

        return response
    
    async def update_pool(self, name: str, slots: int, description: str = "") -> dict | str:
        """
        Update an existing Airflow Pool via the Airflow REST API.

        Sends a PATCH request to the `/pools/{name}` endpoint with the updated pool details.

        Args:
            name (str): The name of the Pool to update.
            slots (int): The new number of slots for the Pool.
            description (str, optional): A new description for the Pool. Defaults to an empty string.

        Returns:
            dict: The updated Pool as a dictionary. If an error occurs, a string error message is returned.
        """
        endpoint = f"pools/{name}"
        method = 'patch'
        payload = {
            "pool": name,
            "slots": slots,
            "description": description,
            "include_deferred": True
        }

        response = await self.client.api_request(endpoint, method, json=payload)

        if isinstance(response, str):
            return response

        return response
    
    async def delete_pool(self, name: str) -> dict | str:
        """
        Delete an existing Airflow Pool via the Airflow REST API.

        Sends a DELETE request to the `/pools/{name}` endpoint to delete the specified pool.

        Args:
            name (str): The name of the Pool to delete.

        Returns:
            dict: A confirmation message as a dictionary. If an error occurs, a string error message is returned.
        """
        endpoint = f"pools/{name}"
        method = 'delete'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response

        return response