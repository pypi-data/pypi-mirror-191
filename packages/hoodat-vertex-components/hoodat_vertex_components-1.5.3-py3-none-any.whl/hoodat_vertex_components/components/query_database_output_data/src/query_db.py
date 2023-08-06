# Local imports
import logging
import argparse
from pathlib import Path

# Library imports
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from google.cloud import secretmanager


def query_db(secret_sql_conn: str, query: str):
    # Get db uri from secret manager
    secret_client = secretmanager.SecretManagerServiceClient()
    response = secret_client.access_secret_version(request={"name": secret_sql_conn})
    SQLALCHEMY_DATABASE_URI = response.payload.data.decode("UTF-8")
    # Create connection to database
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    # session = Session(engine)
    # Run query
    result = pd.read_sql(sql=query, con=engine)
    # Return result
    return result


def save_df_to_file(df, save_path):
    print("Creating parent directory of save_path")
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(save_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--secret_sql_conn", type=str)
    parser.add_argument("--query", type=str)
    parser.add_argument("--query_result", type=str)
    args = parser.parse_args()
    result = query_db(secret_sql_conn=args.secret_sql_conn, query=args.query)
    print(result)
    save_df_to_file(df=result, save_path=args.query_result)
    print(f"Data saved to {args.query_result}")
