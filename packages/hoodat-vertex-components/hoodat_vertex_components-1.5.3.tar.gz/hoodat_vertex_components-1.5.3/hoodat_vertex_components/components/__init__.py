"""
Hoodat components
"""
import os

try:
    from kfp.v2.components import load_component_from_file
except ImportError:
    from kfp.components import load_component_from_file

__all__ = [
    "AddPyOp",
    "MakeCascadeFileOp",
    "PyscenedetectOp",
    "BytetrackFromVideoOp",
    "VideoToFramesOp",
    "HaarFromFramesOp",
    "StitchVideosOp",
    "QueryDatabaseOutputDataOp",
    "QueryDatabaseOutputStringOp",
    "VideoInDatabaseOp",
]

AddPyOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "add_py/component.yaml")
)

MakeCascadeFileOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "make_cascade_file/component.yaml")
)

BytetrackFromVideoOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "bytetrack_from_video/component.yaml")
)

PyscenedetectOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "pyscenedetect/component.yaml")
)

VideoToFramesOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "video_to_frames/component.yaml")
)

HaarFromFramesOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "haar_from_frames/component.yaml")
)

StitchVideosOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "stitch_videos/component.yaml")
)

QueryDatabaseOutputDataOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "query_database_output_data/component.yaml")
)

QueryDatabaseOutputStringOp = load_component_from_file(
    os.path.join(
        os.path.dirname(__file__), "query_database_output_string/component.yaml"
    )
)

VideoInDatabaseOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "video_in_database/component.yaml")
)
