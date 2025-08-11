class AirflowConnection:
    """A class to manage Airflow connections.

    Attributes:
        client: An instance of the Airflow client to interact with the Airflow API.
    """

    def __init__(self, client):
        self.client = client

    async def list_connection(self):
        """
        List all connections in Airflow.

        Sends a GET request to the Airflow `/connections` endpoint and retrieves
        a list of connections.

        Returns:
            list: A list of connection names as strings. If an error occurs, a string error message is returned.
        """
        endpoint = "connections"
        method = 'get'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response

        # Extract just the connection names from the response
        return response

    async def get_connection_details(self, conn_id: str):
        """
        Fetch detailed information for a specific Airflow connection.

        Sends a GET request to the `/connections/{conn_id}` endpoint to retrieve
        metadata and configuration related to the given connection.

        Args:
            conn_id (str): The connection identifier.

        Returns:
            dict: A dictionary containing connection details such as type, host, schema, etc.
                If an error occurs, a string error message is returned.
        """
        endpoint = f"connections/{conn_id}"
        method = 'get'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response

        return response

    async def create_connection(
        self,
        conn_id: str,
        conn_type: str,
        host: str,
        schema: str = "",
        login: str = "",
        password: str = "",
        port: int = 0,
        description: str = "",
        extra: str = ""
    ):
        """
        Create a new Airflow connection using the Stable REST API (v2).

        Args:
            conn_id (str): The connection identifier.
            conn_type (str): The type of the connection (e.g., 'mysql', 'postgres').
            host (str): The host for the connection.
            schema (str): The schema for the connection (optional).
            login (str): The login username (optional).
            password (str): The password (optional).
            port (int): The port number (optional).
            description (str): Optional description.
            extra (str): Optional extra configuration (as JSON string).

        Returns:
            dict: The created connection response or an error message.
        """
        endpoint = "connections"
        method = 'post'

        payload = {
            "connection_id": conn_id,
            "conn_type": conn_type,
            "host": host,
            "schema": schema,
            "login": login,
            "password": password,
            "port": port,
            "description": description,
            "extra": extra
        }

        response = await self.client.api_request(endpoint, method, json=payload)
        if isinstance(response, str):
            return response

        return {"message": f"Connection '{conn_id}' Created successfully."} 

    async def delete_connection(self, conn_id: str):
        """
        Delete an Airflow connection.

        Sends a DELETE request to the Airflow `/connections/{conn_id}` endpoint.

        Args:
            conn_id (str): The connection identifier to delete.

        Returns:
            dict: A confirmation message or an error message if the deletion fails.
        """
        endpoint = f"connections/{conn_id}"
        method = 'delete'

        response = await self.client.api_request(endpoint, method)

        if isinstance(response, str):
            return response

        return {"message": f"Connection '{conn_id}' deleted successfully."}

    async def update_connection(
        self,
        conn_id: str,
        conn_type: str,
        host: str,
        schema: str = "",
        login: str = "",
        password: str = "",
        port: int = 0,
        description: str = "",
        extra: str = ""
    ):
        """
        Update an existing Airflow connection.

        Sends a PATCH request to the Airflow `/connections/{conn_id}` endpoint with the updated details.

        Args:
            conn_id (str): The current connection ID to update.
            connection_id (str): The new connection ID (optional).
            conn_type (str): The type of the connection (optional).
            host (str): The host for the connection (optional).
            schema (str): The schema for the connection (optional).
            login (str): The login username (optional).
            password (str): The password (optional).
            port (int): The port number (optional).
            description (str): Description of the connection (optional).
            extra (str): Extra configuration as JSON string (optional).

        Returns:
            dict: A dictionary containing the updated connection details or an error message.
        """
        endpoint = f"connections/{conn_id}"
        method = 'patch'

        payload = {
            "connection_id": conn_id,
            "conn_type": conn_type,
            "host": host,
            "schema": schema,
            "login": login,
            "password": password,
            "port": port,
            "description": description,
            "extra": extra
        }

        # Remove keys with None values
        payload = {k: v for k, v in payload.items() if v is not None}

        response = await self.client.api_request(endpoint, method, json=payload)

        return response
