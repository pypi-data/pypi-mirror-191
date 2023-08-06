from make_cascade_file import (
    filter_cascades,
)


def test_filter_cascades_correct_rows():
    df = filter_cascades(cascade_ids="0,1")
    assert df.shape[0] == 2
    assert df["file"][1] == "haarcascade_frontalface_alt.xml"


def test_filter_cascades_empty_rows():
    df = filter_cascades(cascade_ids="")
    assert df is None


def test_filter_cascades_row_order():
    df = filter_cascades(cascade_ids="1,0,2")
    assert df.shape[0] == 3
    assert df["id"][1] == 1
    assert df["name"][1] == "frontalface_alt"
    assert df["file"][1] == "haarcascade_frontalface_alt.xml"


def test_filter_cascades_all_rows():
    df = filter_cascades(cascade_ids="0,1,2,3,4,5,6")
    assert df.shape[0] == 7
