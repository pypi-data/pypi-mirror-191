from kfp.v2.dsl import component, Input, Artifact, OutputPath


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/video_in_database",
    output_component_file="component.yaml",
)
def video_in_database(
    secret_sql_conn: str, input_video: Input[Artifact], video_id: OutputPath(str)
):
    # Local imports
    from loguru import logger
    from pathlib import Path

    # Library imports
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from sqlalchemy.exc import IntegrityError
    from google.cloud import secretmanager

    # Hoodat utils imports
    from hoodat_utils import models

    ################################
    # Parse input video path
    ################################

    input_video_path = input_video.path
    logger.info(f"input_video_path: {input_video_path}")
    if "not_youtube" in input_video_path:
        VIDEO_TYPE_DB = "Not Youtube"
    elif "youtube" in input_video_path:
        VIDEO_TYPE_DB = "Youtube"
    logger.info(f"VIDEO_TYPE_DB: {VIDEO_TYPE_DB}")
    VIDEO_SAVE_NAME = input_video_path.split("/")[-1]
    logger.info(f"VIDEO_SAVE_NAME: {VIDEO_SAVE_NAME}")

    ################################
    # Helper functions
    ################################

    def create_sql_engine(secret_sql_conn: str):
        # Get db uri from secret manager
        secret_client = secretmanager.SecretManagerServiceClient()
        response = secret_client.access_secret_version(
            request={"name": secret_sql_conn}
        )
        SQLALCHEMY_DATABASE_URI = response.payload.data.decode("UTF-8")
        # Create connection to database
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        return engine

    def query_db(engine, query: str):
        # Run query
        result = pd.read_sql(sql=query, con=engine)
        # Return result
        return result

    # Check if file exists
    def check_file_exists(file_path):
        if file_path.startswith("gs://"):
            file_path = file_path.replace("gs://", "/gcs/")
        logger.info(f"Checking if file exists at {file_path}")
        if Path(file_path).exists():
            logger.info("File exists")
            return True
        else:
            logger.info("File does not exist")
            return False

    def save_string_to_file(string, save_path):
        logger.info(f"Creating parent directory of save_path {save_path}")
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Writing string {string} to save_path {save_path}")
        with open(save_path, "w") as f:
            f.write(str(string))
        logger.info("String written")

    def insert_video(engine, video_name, video_save_name, video_type):
        session = Session(engine)
        try:
            video = models.Video(
                user_id=1,
                video_name=video_name,
                save_name=video_save_name,
                video_type=video_type,
            )
            session.add(video)
            session.flush()
        except IntegrityError:
            logger.info("Record violated table constraints")
            session.rollback()
        else:
            logger.info("Adding row")
            session.commit()

    ################################
    # Main
    ################################

    # Check if file exists
    video_file_exists = check_file_exists(input_video_path)
    logger.info(f"video_file_exists: {video_file_exists}")
    if not video_file_exists:
        logger.info("Video file does not exist, exiting")
        SystemExit(1)
    else:
        # Create engine
        engine = create_sql_engine(secret_sql_conn=secret_sql_conn)
        # Check if file already in database
        query = f"""
            SELECT v.video_id
            FROM videos v
            WHERE v.video_type = '{VIDEO_TYPE_DB}'
            AND v.save_name = '{VIDEO_SAVE_NAME}'
        """
        logger.info(f"Running query: {query}")
        result = query_db(engine=engine, query=query)
        logger.info("Query result:")
        logger.info(result)
        if result.shape[0] > 1:
            logger.info("Query result has more than 1 row")
            SystemExit(1)
        if result.shape[1] > 1:
            logger.info("Query result has more than 1 column")
            SystemExit(1)
        if result.shape == (0, 1):
            logger.info("Query result is an empty data frame")
            # Insert video into database
            logger.info("Inserting video into database")
            insert_video(
                engine=engine,
                video_name=VIDEO_SAVE_NAME,
                video_save_name=VIDEO_SAVE_NAME,
                video_type=VIDEO_TYPE_DB,
            )
            result = query_db(engine=engine, query=query)
        save_string_to_file(string=result.iloc[0][0], save_path=video_id)
        logger.info(f"Data saved to {video_id}")
