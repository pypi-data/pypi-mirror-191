from kfp.components import func_to_container_op
from kfp.v2.dsl import component, Input, Output, Artifact, Dataset


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/video_to_frames",
    output_component_file="component.yaml",
)
def video_to_frames(
    input_video: Input[Artifact],
    output_frames_df: Output[Dataset],
    output_frames_dir: Output[Artifact],
    output_frames_df_path: str = None,
    output_frames_dir_path: str = None,
    every_n_frames: int = 1,
):
    """Converts a video to frames.

    Args:
        input_video (Input[Artifact]): The video to convert to frames.
        output_frames_df (Output[Dataset]): The destination of the CSV file containing the frame numbers and timestamps.
        output_frames_dir (Output[Artifact]): The destination of the directory containing the frames.
        every_n_frames (int): The number of frames to skip between each frame saved.
    """
    import os
    import cv2
    from loguru import logger
    from math import floor

    ################################
    # Helper functions
    ################################

    def setup_output_path(output_path):
        if output_path.startswith("gs://"):
            output_path_gs = output_path
            output_path_local = output_path.replace("gs://", "/gcs/")
        elif output_path.startswith("/gcs/"):
            output_path_gs = output_path.replace("/gcs/", "gs://")
            output_path_local = output_path
        else:
            raise ValueError("output_path should start with either gs:// or /gcs/")
        return output_path_gs, output_path_local

    def write_row(file_, *columns):
        print(*columns, sep="\t", end="\n", file=file_)

    ################################
    # Main
    ################################

    if output_frames_df_path:
        output_frames_df.path = output_frames_df_path
    if output_frames_dir_path:
        output_frames_dir.path = output_frames_dir_path

    # Setup input and output paths
    input_video_gs, input_video_local = setup_output_path(input_video.path)
    output_frames_df_gs, output_frames_df_local = setup_output_path(
        output_frames_df.path
    )
    output_frames_dir_gs, output_frames_dir_local = setup_output_path(
        output_frames_dir.path
    )

    # Read the video file
    source = input_video_local
    save_dir_root = output_frames_dir_local
    if every_n_frames == 1:
        save_dir = f"{save_dir_root}/clean_complete"
    elif every_n_frames == 30:
        save_dir = f"{save_dir_root}/clean"
    else:
        raise ValueError("every_n_frames must be 1 or 30")
    vidcap = cv2.VideoCapture(source)
    vidcap_metrics = {
        "num_frames": int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": vidcap.get(cv2.CAP_PROP_FPS),
    }
    logger.info(f"source: {source}")
    logger.info(f"frames: {vidcap_metrics['num_frames']}")
    logger.info(f"width: {vidcap_metrics['width']}")
    logger.info(f"height: {vidcap_metrics['height']}")
    logger.info(f"fps: {vidcap_metrics['fps']}")
    vidcap_metrics["num_frames_to_save"] = floor(
        float(vidcap_metrics["num_frames"]) / float(every_n_frames)
    )
    logger.info("vidcap_metrics: " + str(vidcap_metrics))
    success, image = vidcap.read()
    logger.info("Success: " + str(success))
    # Initialise the count that will increase with each frame
    count = 0
    # If the video is read successfully
    if success:
        save_dir_exists = os.path.isdir(save_dir)
        logger.info("Directory already exists: " + str(save_dir_exists))
        if not save_dir_exists:
            os.makedirs(save_dir)
        frames_list = os.listdir(save_dir)
        if len(frames_list) == vidcap_metrics["num_frames"]:
            logger.info("Frames already saved")
            success = False
        else:
            logger.info(f"Saving output to: {save_dir}")
            save_path = f"{save_dir}/f{str(count)}.jpg"
            cv2.imwrite(save_path, image)  # save frame as JPEG file
            with open(output_frames_df_local, "a+") as f:
                write_row(f, "frame_number")
                write_row(f, count)
    while success:
        # Read the next frame
        try:
            # Increase count
            count += 1
            success, image = vidcap.read()
            if count % (every_n_frames * 100) == 0:
                logger.info("Saving frame: " + str(count))
            if count % every_n_frames == 0:
                save_path = f"{save_dir}/f{str(count)}.jpg"
                cv2.imwrite(save_path, image)  # save frame as JPEG file
                with open(output_frames_df_local, "a+") as f:
                    write_row(f, count)
        except Exception as e:
            logger.info("Error in image capture on frame {0}".format(count))
            logger.info(e)
    num_frames_saved = len(os.listdir(save_dir))
    logger.info("Total frames saved: " + str(num_frames_saved))
    logger.info("Finished getting frames")
    logger.info(f"num_frames_to_save: {vidcap_metrics['num_frames_to_save']}")
    logger.info(f"num_frames_saved: {num_frames_saved}")
    success = num_frames_saved == vidcap_metrics["num_frames_to_save"]
    logger.info(f"All frames successfully saved: {success}")
    if not success:
        raise ValueError("Not all frames were successfully saved")
