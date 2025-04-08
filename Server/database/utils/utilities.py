class Messages:
    _logger = None

    @classmethod
    def set_logger(cls, logger):
        cls._logger = logger

    class Complete:
        @staticmethod
        def connection(db_path):
            Messages._logger.log(f"✅ Connection to database '{db_path}' was successful.")

        @staticmethod
        def close_connection(db_path):
            Messages._logger.log(f"✅ Connection to database '{db_path}' was successful close.")

        @staticmethod
        def create_db(db_path):
            Messages._logger.log(f"✅ Database {db_path} has been created.")

        @staticmethod
        def delete_db(db_path):
            Messages._logger.log(f"✅ Database {db_path} has been deleted.")

        @staticmethod
        def db_load_config():
            Messages._logger.log(f"✅ Database config loaded successfully.")

        @staticmethod
        def table_load_config():
            Messages._logger.log(f"✅ Tables config loaded successfully.")

        @staticmethod
        def table_load_queries(table_name):
            Messages._logger.log(f"✅ Queries for table '{table_name}' loaded successfully.")

        @staticmethod
        def table_initialized(table_name):
            Messages._logger.log(f"✅ Table '{table_name}' initialized with queries successfully.")

        @staticmethod
        def table_creating(table_name):
            Messages._logger.log(f"✅ Table '{table_name}' created successfully.")

        @staticmethod
        def table_droping(table_name):
            Messages._logger.log(f"✅ Table '{table_name}' dropped successfully.")

    class Error:
        @staticmethod
        def try_action(exception):
            Messages._logger.log(f"❌ An error occurred: '{exception}'.")

        @staticmethod
        def connection(db_path):
            Messages._logger.log(f"❌ Connection to database '{db_path}' was not successful.")

        @staticmethod
        def miss_connection(db_path):
            Messages._logger.log(f"❌ No connection to database '{db_path}' exists.")

        @staticmethod
        def db_path():
            Messages._logger.log("❌ Invalid database path configuration.")

        @staticmethod
        def create_db(db_path):
            Messages._logger.log(f"❌ Failed to create database '{db_path}'.")

        @staticmethod
        def delete_db(db_path):
            Messages._logger.log(f"❌ Failed to delete database '{db_path}'.")

        @staticmethod
        def db_already_exist(db_path):
            Messages._logger.log(f"❌ Database '{db_path}' already exists.")

        @staticmethod
        def db_file_found(db_path):
            Messages._logger.log(f"❌ Database file '{db_path}' not found.")

        @staticmethod
        def db_load_config():
            Messages._logger.log("❌ Failed to load database config.")
            raise Exception("The Database Config was not uploaded.")

        @staticmethod
        def table_load_config():
            Messages._logger.log("❌ Failed to load tables config.")
            raise Exception("The Tables Config was not uploaded.")

        @staticmethod
        def table_load_queries(table_name):
            Messages._logger.log(f"❌ Failed to load queries for table '{table_name}'.")
            raise Exception(f"Queries for table '{table_name}' was not uploaded.")

        @staticmethod
        def table_found(table_name):
            Messages._logger.log(f"❌ Table '{table_name}' not found in configuration.")

        @staticmethod
        def table_already_exist(table_name):
            Messages._logger.log(f"❌ Table '{table_name}' already exists.")

        @staticmethod
        def connection_already_established(db_path):
            Messages._logger.log(f"❌ Connection to database '{db_path}' already established.")

        @staticmethod
        def table_initialized(table_name):
            Messages._logger.log(f"❌ Failed to initialize table '{table_name}'.")

        @staticmethod
        def table_creating(table_name):
            Messages._logger.log(f"❌ Failed to create table '{table_name}'.")

        @staticmethod
        def table_droping(table_name):
            Messages._logger.log(f"❌ Failed to drop table '{table_name}'.")

        @staticmethod
        def data_inserting(table_name):
            Messages._logger.log(f"❌ Failed to insert data into table '{table_name}'.")

        @staticmethod
        def data_updating(table_name):
            Messages._logger.log(f"❌ Failed to update data in table '{table_name}'.")

        @staticmethod
        def data_deleting(table_name):
            Messages._logger.log(f"❌ Failed to delete data from table '{table_name}'.")

        @staticmethod
        def data_fetching(table_name):
            Messages._logger.log(f"❌ Failed to fetch data from table '{table_name}'.")