import logging
import sqlite3 as sql
from pathlib import Path
from sqlite3 import Connection
from typing import Callable, Dict, List, Optional, Union

import pandas as pd
import swifter


class WildFireDataLoader:
    def __init__(
        self,
        datadir: Union[Path, str],
        start_date: str,
        end_date: str,
        truth_fields: List[str],
        input_fields: Optional[List[str]] = None,
        parallel_flag: bool = True,
    ):
        # Set up class variables
        self.datadir = Path(datadir)
        self.start_date = start_date
        self.end_date = end_date
        self.input_fields = input_fields
        self.truth_fields = truth_fields
        self.parallel_flag = parallel_flag
        self._df = None

        if self.parallel_flag:
            logging.debug("Setting up swifter for parallel processing.")
            swifter.set_defaults(
                npartitions=None,
                dask_threshold=1,
                scheduler="processes",
                progress_bar=False,
                progress_bar_desc=None,
                allow_dask_on_strings=False,
                force_parallel=False,
            )

    def _with_database(func: Callable):
        """A wrapper function designed to open an close a database connection,
        designed to reduce repeated code. This wrapper will open a connection to
        the database defined by the `datadir` class variable, execute a required
        function and will then disconnect from the database.

        Args:
            func (_type_): function to apply the wrapper to.
        """

        def wrapper(self, *args, **kwargs):
            # Connect to the SQLite database and set up class vars for the connection and cursor
            logging.debug("Opening database connection from: %s.", self.datadir)
            self.db_conn = sql.connect(self.datadir)
            self.cursor = self.db_conn.cursor()

            # Call the function with the database connection as an argument
            result = func(self, *args, **kwargs)

            # Close the connection to the database
            logging.debug("Closing database connection from: %s.", self.datadir)
            self.cursor.close()
            self.db_conn.close()

            # Return the result of the function call
            return result

        return wrapper

    def dataframe_wrapper(func: Callable):
        def wrapper(self, *args, **kwargs):
            if self._df is None:
                raise RuntimeError(
                    "Dataframe not loaded yet! You need to load one using a suitable method, such as load_dataframe_from_query, before using this method."
                )
            result = func(self, *args, **kwargs)

            return result

        return wrapper

    @_with_database
    def load_dataframe_from_query(self, query: str) -> pd.DataFrame:
        """Load in pandas DataFrame from a given SQL query. This will be applied to the SQL
        database provided in the class `basedir`.

        Args:
            query str: SQL query to be used to extract from the database.

        Returns:
            pd.DataFrame: A pandas dataframe reflecting the result of the query.
        """
        logging.debug("Reading query in as a pandas DataFrame...")
        df = pd.read_sql_query(query, self.db_conn)
        self._df = df
        return None

    @_with_database
    def extract_table_names(self) -> List[str]:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tns = self.cursor.fetchall()
        return [name[0] for name in tns]

    @_with_database
    def extract_colun_names_from_table(self, table_name: str, limit: int = 100) -> List[str]:
        self.cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        columns = [description[0] for description in self.cursor.description]
        return columns

    @dataframe_wrapper
    def to_pandas_df(self, datetime_cols: Optional[List[str]] = None) -> pd.DataFrame:
        if datetime_cols:
            logging.info("Processing pandas datetimes, this might take a few minutes...")
            for col in datetime_cols:
                if self.parallel_flag:
                    self._df[col] = self._df[col].swifter.apply(pd.to_datetime)
                else:
                    self._df[col] = pd.to_datetime(self._df[col])
        return self._df

    @dataframe_wrapper
    def save_dataframe_as_parquet(self, file_name:str = "export.parquet.gzip", save_path:Optional[Union[str,Path]]=None) -> None:
        """Save the loaded dataframe as a parquet file.

        Args:
            file_name (str, optional): Filename for saving. Defaults to "export.parquet.gzip".
            save_path (Optional[Union[str,Path]], optional): Path for saving. If not provided the `datadir` is used instead..
        """        
        if save_path is None:
            save_path = self.datadir.parents[0]
        
        output_file = Path(save_path) / file_name
        logging.info("Saving dataframe to: %s", output_file)     
        self._df.to_parquet(output_file, compression='gzip') 
