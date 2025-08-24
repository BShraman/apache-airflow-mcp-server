class RegisterTools:
    def __init__(self, mcp):
        from services.airflow_client import AirflowClient
        from tools.dags import AirflowDAGs
        from tools.backfills import AirflowBackfills
        from tools.assets import AirflowAssets
        from tools.connections import AirflowConnection
        from tools.tasks_instance import AirflowTasksInstance
        from tools.pool import AirflowPool

        self.client = AirflowClient()
        self.dags = AirflowDAGs(self.client)
        self.backfills = AirflowBackfills(self.client)
        self.assets = AirflowAssets(self.client)
        self.connection = AirflowConnection(self.client)
        self.tasks_instance = AirflowTasksInstance(self.client)
        self.pools = AirflowPool(self.client)

        self.mcp = mcp

    #-------------------------------- Dags Registration ----------------------------------#
    def _dags(self):
        @self.mcp.tool("get_dags_list")
        async def get_dags_list():
            """Get the list of all the Dags (see tools.get_dags_list for details)."""
            return await self.dags.get_dags_list()
        
        @self.mcp.tool("get_dag_details")
        async def get_dag_details(dag_id: str):
            """Get details of a specific DAG (see tools.get_dag_details for details)."""
            return await self.dags.get_dag_details(dag_id)
        
        @self.mcp.tool("get_dag_runs")
        async def get_dag_runs(dag_id: str):
            """Get all runs for a specific DAG (see tools.get_dag_runs for details)."""
            return await self.dags.get_dag_runs(dag_id)

        @self.mcp.tool("trigger_dag")
        async def trigger_dag(dag_id: str):
            """Triggers a DAG run (see tools.trigger_dag for details)."""
            return await self.dags.trigger_dag(dag_id)
        
        @self.mcp.tool("clear_dag_run")
        async def clear_dag_run(dag_id: str, dag_run_id: str, dry_run: bool = True, only_failed: bool = False):
            """Clears a specific DAG run (see tools.clear_dag_run for details)."""
            return await self.dags.clear_dag_run(dag_id, dag_run_id, dry_run, only_failed)

        @self.mcp.tool("delete_dag")
        async def delete_dag(dag_id: str):
            """Deletes a DAG from Airflow (see tools.delete_dag for details)."""
            return await self.dags.delete_dag(dag_id)

        @self.mcp.tool("pause_all_dags")
        async def pause_all_dags():
            """Pauses all DAGs in Airflow (see tools.pause_all_dags for details)."""
            return await self.dags.pause_all_dags(pause=True)
        
        # @self.mcp.tool("unpause_all_dags")
        # async def unpause_all_dags():
        #     """Unpauses all DAGs in Airflow (see tools.unpause_all_dags for details)."""
        #     return await self.dags.pause_all_dags(pause=False)
        
        @self.mcp.tool("delete_dags_runs")
        async def delete_dags_runs(dag_id: str, dag_run_id:str):
            """Deletes all runs for a specific DAG (see tools.delete_dags_runs for details)."""
            return await self.dags.delete_dags_runs(dag_id,dag_run_id)
        
        @self.mcp.tool("get_dag_version")
        async def get_dag_version(dag_id: str):
            """Get the version of a specific DAG (see tools.get_dag_version for details)."""
            return await self.dags.get_dag_version(dag_id)
        
    #-------------------------------- Tasks Registration --------------------------------------#
    def _tasks_instance(self):
        @self.mcp.tool("get_task_instance")
        async def get_task_instance(dag_id: str,run_id: str):
            """Get a specific task instance (see tools.get_task_instance for details)."""
            return await self.tasks_instance.get_task_instance(dag_id, run_id)

        @self.mcp.tool("clear_task_instance")
        async def clear_task_instance(dag_id: str, dag_run_id:str, start_date: str, end_date: str):
            """Clears a specific task instance (see tools.clear_task_instance for details)."""
            return await self.tasks_instance.clear_task_instance(dag_id, dag_run_id, start_date)

    #-------------------------------- Backfills Registration ----------------------------------#
    def _backfills(self):
        @self.mcp.tool("list_backfills")
        async def list_backfills(dag_id: str):
            """List backfills for a specific DAG (see tools.list_backfills for details)."""
            return await self.backfills.list_backfills(dag_id)
        
        @self.mcp.tool("create_backfill")
        async def create_backfill(
            dag_id: str,
            from_date: str,
            to_date: str,
            run_backwards: bool = False,
            reprocess_behavior: str = "none",
            max_active_runs: int = 10,
            dag_run_conf: dict = {},
            ):
            """Creates a backfill for a specific DAG (see tools.create_backfill for details)."""
            return await self.backfills.create_backfill(
                dag_id, from_date, to_date, run_backwards, reprocess_behavior, max_active_runs, dag_run_conf
            )
        
        @self.mcp.tool("get_backfill")
        async def get_backfill(backfill_id: int):
            """Get details of a specific backfill (see tools.get_backfill for details)."""
            return await self.backfills.get_backfill(backfill_id)
        
        @self.mcp.tool("pause_backfill")
        async def pause_backfill(backfill_id: int):
            """Pause a specific backfill (see tools.pause_backfill for details)."""
            return await self.backfills.pause_backfill(backfill_id)
        
        @self.mcp.tool("unpause_backfill")
        async def unpause_backfill(backfill_id: int):
            """Unpause a specific backfill (see tools.unpause_backfill for details)."""
            return await self.backfills.unpause_backfill(backfill_id)
        
        @self.mcp.tool("cancel_backfill")
        async def cancel_backfill(backfill_id: int):
            """Cancel a specific backfill (see tools.cancel_backfill for details)."""
            return await self.backfills.cancel_backfill(backfill_id)
        
        @self.mcp.tool("backfill_dry_runs")
        async def backfill_dry_runs(
            dag_id: str,
            from_date: str,
            to_date: str,
            run_backwards: bool = False,
            reprocess_behavior: str = "none",
            max_active_runs: int = 10,
            dag_run_conf: dict = {},
            ):
            """Simulates a backfill for a specific DAG without executing tasks (see tools.backfill_dry_runs for details)."""
            return await self.backfills.backfill_dry_runs(
                dag_id, from_date, to_date, run_backwards, reprocess_behavior, max_active_runs, dag_run_conf
            )
        
    #-------------------------------- Assets Registration -------------------------------------#
    def _assets(self):
        @self.mcp.tool("get_assets")
        async def get_assets():
            """Fetch all Airflow assets (see tools.get_assets for details)."""
            return await self.assets.get_assets()
        
        @self.mcp.tool("get_asset_aliases")
        async def get_asset_aliases():
            """Fetch all Airflow asset aliases (see tools.get_asset_aliases for details)."""
            return await self.assets.get_asset_aliases()
        
        @self.mcp.tool("get_asset_events")
        async def get_asset_events():
            """Fetch all Airflow asset events (see tools.get_asset_events for details)."""
            return await self.assets.get_asset_events()
        
        @self.mcp.tool("create_asset_event")
        async def create_asset_event(asset_id: int):
            """Create an Airflow asset event (see tools.create_asset_event for details)."""
            return await self.assets.create_asset_events(asset_id)
        
        @self.mcp.tool("get_asset_queued_events")
        async def get_asset_queued_events(asset_id: int):
            """Fetch queued events for a specific asset (see tools.get_asset_queued_events for details)."""
            return await self.assets.get_asset_queued_events(asset_id)
        
        @self.mcp.tool("get_dag_asset_queued_events")
        async def get_dag_asset_queued_events(dag_id: str):
            """Fetch queued events for all assets associated with a specific DAG (see tools.get_dag_asset_queued_events for details)."""
            return await self.assets.get_dag_asset_queued_events(dag_id)
        
        @self.mcp.tool("delete_asset_event")
        async def delete_asset_event(event_id: int):
            """Delete a specific asset event (see tools.delete_asset_event for details)."""
            return await self.assets.delete_asset_event(event_id)
        
        @self.mcp.tool("delete_dag_asset_events")
        async def delete_dag_asset_events(dag_id: str):
            """Delete all asset events associated with a specific DAG (see tools.delete_dag_asset_events for details)."""
            return await self.assets.delete_dag_asset_events(dag_id)
        
    #-------------------------------- Connection Registration ----------------------------------#
    def _connections(self):
        @self.mcp.tool("list_connections")
        async def list_connections():
            """List all Airflow connections (see tools.list_connections for details)."""
            return await self.connection.list_connection()

        @self.mcp.tool("get_connection_details")
        async def get_connection_details(conn_id: str):
            """Get details of a specific Airflow connection (see tools.get_connection_details for details)."""
            return await self.connection.get_connection_details(conn_id)

        @self.mcp.tool("create_connection")
        async def create_connection(conn_id: str, conn_type: str, host: str, schema: str = "", login: str = "", password: str = "", port: int = 0):
            """Create a new Airflow connection (see tools.create_connection for details)."""
            return await self.connection.create_connection(conn_id, conn_type, host, schema, login, password, port)
        
        @self.mcp.tool("update_connection")
        async def update_connection(conn_id: str, conn_type: str, host: str, schema: str = "", login: str = "", password: str = "", port: int = 0):
            """Update an existing Airflow connection (see tools.update_connection for details)."""
            return await self.connection.update_connection(conn_id, conn_type, host, schema, login, password, port)

        @self.mcp.tool("delete_connection")
        async def delete_connection(conn_id: str):
            """Delete an Airflow connection (see tools.delete_connection for details)."""
            return await self.connection.delete_connection(conn_id)
        
    #-------------------------------- Pools Registration ----------------------------------#
    def _pools(self):
        @self.mcp.tool("get_pools")
        async def get_pools():
            """Fetch all Airflow pools (see tools.get_pools for details)."""
            return await self.pools.get_pools()
        
        @self.mcp.tool("create_pool")
        async def create_pool(name: str, slots: int, description: str = ""):
            """Create a new Airflow pool (see tools.create_pool for details)."""
            return await self.pools.create_pool(name, slots, description)
        
        @self.mcp.tool("update_pool")
        async def update_pool(name: str, slots: int, description: str = ""):
            """Update an existing Airflow pool (see tools.update_pool for details)."""
            return await self.pools.update_pool(name, slots, description)
        
        @self.mcp.tool("delete_pool")
        async def delete_pool(name: str):
            """Delete an Airflow pool (see tools.delete_pool for details)."""
            return await self.pools.delete_pool(name)
        
