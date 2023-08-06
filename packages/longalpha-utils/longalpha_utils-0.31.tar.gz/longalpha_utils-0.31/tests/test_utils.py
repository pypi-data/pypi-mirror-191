import os
import tempfile

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from longalpha_utils.utils import MinioWrapper, init_spark

load_dotenv()


def test_Minio():
    test_data = pd.DataFrame({"x": [1, 2]})
    mp = MinioWrapper(os.environ["MINIO_API"], os.environ["MINIO_ACCESS_KEY"], os.environ["MINIO_SECRET_KEY"])
    mp.put(test_data, "test", "test_data.parquet", file_format="parquet")
    mp.put(test_data, "test", "test_data.pkl", file_format="pickle")
    data1 = mp.get("test", "test_data.parquet", file_format="parquet")
    data2 = mp.get("test", "test_data.pkl", file_format="pickle")
    data3 = mp.get_latest("test", file_format="pickle")
    assert test_data.equals(data1)
    assert test_data.equals(data2)
    assert test_data.equals(data3)
    # test fput and fget
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "test_data.parquet")
        test_data.to_parquet(path)
        mp.fput(path, bucket_name="test", object_name="test_data.parquet")
        mp.fget(path, bucket_name="test", object_name="test_data.parquet")
        data4 = pd.read_parquet(path)
        assert test_data.equals(data4)


def test_init_spark():
    pdf = pd.DataFrame({"x": "alice", "y": 1}, index=[0])

    # connect minio
    # if you init spark with minio support, and then init with psql support, the psql connection will be broken
    # spark = init_spark(
    #     minio_endpoint=os.environ["MINIO_API"],
    #     minio_secret_key=os.environ["MINIO_SECRET_KEY"],
    #     minio_access_key=os.environ["MINIO_ACCESS_KEY"],
    # )
    # df = spark.createDataFrame(pdf)
    # df.write.mode("overwrite").save("s3a://test/test/")
    # assert spark.read.parquet("s3a://test/test/").toPandas().equals(pdf)
    # spark.stop()
    # connect postgres
    psql_engine = create_engine(
        f"postgresql://{os.environ['PSQL_USR']}:{os.environ['PSQL_PWD']}@{os.environ['PSQL_URL']}/test"
    )
    pdf.to_sql("test", con=psql_engine, if_exists="replace", index=False)
    spark = init_spark(connect_psql=True)
    df = (
        spark.read.format("jdbc")
        .option("url", f"jdbc:postgresql://{os.environ['PSQL_URL']}/test")
        .option("dbtable", "test")
        .option("user", os.environ["PSQL_USR"])
        .option("password", os.environ["PSQL_PWD"])
        .option("driver", "org.postgresql.Driver")
        .load()
    ).toPandas()
    assert df.equals(pdf)
    spark.stop()
