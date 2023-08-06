import os
import argparse
from pathlib import Path
import pandas as pd


def filter_cascades(cascade_ids):
    print(f"cascade_ids: {cascade_ids}")
    if cascade_ids == "":
        return None
    else:
        cascade_ids = [int(x) for x in cascade_ids.split(",")]
        file_path = os.path.join(os.path.dirname(__file__), "cascades.csv")
        cascades = pd.read_csv(file_path)
        filtered_cascades = cascades[cascades["id"].isin(cascade_ids)]
        print(filtered_cascades)
        return filtered_cascades


def write_cascade_df(df, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_path",
        type=str,
        help="File to save cascades to",
        required=True,
    )
    parser.add_argument(
        "--cascade_ids",
        type=str,
        help="List of IDs to filter the cascade file down to of the format '1,2,3'",
        required=True,
    )
    parser.add_argument(
        "--cascade_dataframe",
        type=str,
        help="Another file to save cascades to",
        required=True,
    )
    args = parser.parse_args()
    df = filter_cascades(args.cascade_ids)
    write_cascade_df(
        df,
        output_path=args.output_path,
    )
    write_cascade_df(
        df,
        output_path=args.cascade_dataframe,
    )
