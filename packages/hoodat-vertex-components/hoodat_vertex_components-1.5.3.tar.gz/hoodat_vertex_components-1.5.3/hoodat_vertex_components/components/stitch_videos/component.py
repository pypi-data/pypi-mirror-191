from kfp.v2.dsl import component, Input, Output, Artifact, Dataset


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/stitch_videos",
    output_component_file="component.yaml",
)
def stitch_videos(
    input_videos: Input[Artifact],
    output_video: Output[Artifact],
    output_video_path: str,
):
    import os
    import ffmpeg
    from loguru import logger

    def concat_videos(input_videos_dir_path, output_path):
        videos = os.listdir(input_videos_dir_path)
        logger.info(f"videos: {videos}")
        ffmpeg_inputs = [
            ffmpeg.input(os.path.join(input_videos_dir_path, video)) for video in videos
        ]
        ffmpeg.concat(*ffmpeg_inputs).output(output_path).run()

    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    output_video.uri = output_video_path

    concat_videos(input_videos_dir_path=input_videos.path, output_path=output_video.uri)
