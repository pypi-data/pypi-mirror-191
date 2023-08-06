import os
import tempfile
from io import BytesIO
from typing import List, Optional

import pandas as pd
from minio import Minio
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession


def max_pandas_display(pd: pd, max_row: int = 100) -> None:
    """
    set pandas print format to print all
    Args:
        pd: pandas object

    Returns: None

    """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", max_row)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.expand_frame_repr", False)


class MinioWrapper:
    def __init__(self, minio_url, minio_access_key, minio_secret_key):
        self.minio_client = Minio(
            endpoint=minio_url,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False,
        )

    def fput(
        self,
        file_path,
        bucket_name: str,
        object_name: str,
    ):
        self.minio_client.fput_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)

    def put(self, dataframe: pd.DataFrame, bucket_name: str, object_name: str, file_format: str) -> None:
        """
        put a pandas frame to parquet in s3

        Args:
            dataframe: a pandas dataframe
            bucket_name: Minio bucket_name
            object_name: path + file_name
            file_format: parquet or pickle


        Returns:

        """
        with tempfile.TemporaryDirectory() as temp_dir:
            path = os.path.join(temp_dir, object_name)
            if file_format == "parquet":
                dataframe.to_parquet(path)
            elif file_format == "pickle":
                dataframe.to_pickle(path)
            else:
                raise ValueError("Incorrect file format")
            self.fput(file_path=path, bucket_name=bucket_name, object_name=object_name)

    def fget(self, file_path: str, bucket_name: str, object_name: str):
        self.minio_client.fget_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)

    def get(
        self,
        bucket_name: str,
        object_name: str,
        file_format: str,
    ) -> pd.DataFrame:
        """
        get a parquet from s3 and read it into pandas dataframe
        Args:
            bucket_name: Minio bucket_name
            object_name: path + file_name
            file_format: parquet or pickle

        Returns: A pandas dataframe

        """
        file = self.minio_client.get_object(
            bucket_name,
            object_name,
        )
        read_file = {"parquet": pd.read_parquet, "pickle": pd.read_pickle}
        res = read_file[file_format](BytesIO(file.data))
        file.close()
        file.release_conn()
        return res

    def get_latest(self, bucket_name: str, file_format: str) -> pd.DataFrame:
        """
        get the latest parquet file and read it into pandas. Note that this does not include files in the
        sub-folders of the bucket.
        Args:
            bucket_name: bucket_name: Minio bucket_name
            file_format: parquet or pickle

        Returns: A pandas dataframe

        """
        objects = [i for i in self.minio_client.list_objects(bucket_name)]
        time_obj = {obj.last_modified: obj for obj in objects}
        latest_time = max([key for key in time_obj.keys() if key is not None])
        latest_obj = time_obj[latest_time]
        return self.get(bucket_name=bucket_name, object_name=latest_obj.object_name, file_format=file_format)

    def list(self, bucket_name: str) -> List[str]:
        return [i.object_name for i in self.minio_client.list_objects(bucket_name)]


def init_spark(
    spark_executor_memory: str = "30g",
    spark_driver_memory: str = "90g",
    connect_psql: bool = False,
    minio_endpoint: Optional[str] = None,
    minio_access_key: Optional[str] = None,
    minio_secret_key: Optional[str] = None,
) -> SparkSession:
    """
    get a spark instance. Note that we are not downloading jars here. We use spark.jars.packages to download jars.

    Args:
        minio_endpoint: minio_endpoint
        minio_access_key:  minio_access_key
        minio_secret_key:  minio_secret_key
        spark_executor_memory: size of spark_executor_memory
        spark_driver_memory: size of spark_driver_memory
        connect_psql: whether to connect to psql
    Returns:

    """
    if connect_psql and minio_endpoint is not None:
        raise ValueError("Cannot use both minio and psql")

    spark_conf = (
        SparkConf()
        .set("spark.executor.memory", spark_executor_memory)
        .set("spark.driver.memory", spark_driver_memory)
        .set("spark.sql.execution.arrow.pyspark.enabled", "true")
        .set("spark.ui.port", "4043")
    )
    if connect_psql:
        spark = (
            SparkSession.builder.config(conf=spark_conf).config(
                "spark.jars.packages", "org.postgresql:postgresql:42.5.2"
            )
            # .config("spark.jars", "/home/zhan/Projects/longalpha_utils/postgresql-42.5.2.jar")
            # .config("spark.driver.extraClassPath", "/home/zhan/Projects/longalpha_utils/postgresql-42.5.2.jar")
            # .config("spark.executor.extraClassPath", "/home/zhan/Projects/longalpha_utils/postgresql-42.5.2.jar")
            .getOrCreate()
        )
    else:
        spark = (
            SparkSession.builder.config(conf=spark_conf)
            .config(
                "spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.405"
            )
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.hadoop.fs.s3a.path.style.access ", "true")
            .getOrCreate()
        )
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", minio_endpoint)
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", minio_access_key)
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", minio_secret_key)
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
    return spark
