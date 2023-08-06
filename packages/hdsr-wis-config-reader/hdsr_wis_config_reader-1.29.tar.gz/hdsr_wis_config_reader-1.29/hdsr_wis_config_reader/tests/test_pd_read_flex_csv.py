from hdsr_pygithub import GithubFileDownloader
from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader.utils import DatesColumns
from hdsr_wis_config_reader.utils import PdReadFlexibleCsv
from pathlib import Path

import datetime
import pandas as pd  # noqa pandas comes with geopandas
import pytest


date_fmt_Ymd__HMS = "%Y%m%d %H%M%S"
date_fmt_Y_m_d__H_M_S = "%Y-%m-%d %H:%M:%S"


def test_multi_separators_1():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_multi_separators_1.csv"
    assert csv_path.is_file()

    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=csv_path,
            try_separator=",",
            expected_columns=["series", "start", "end"],
            date_columns=[
                DatesColumns(column_name="start", date_format=date_fmt_Ymd__HMS),
                DatesColumns(column_name="end", date_format=date_fmt_Ymd__HMS),
            ],
        ).df


def test_multi_separators_2():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_multi_separators_2.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=csv_path,
            try_separator=",",
            expected_columns=["series", "start", "end"],
            date_columns=[
                DatesColumns(column_name="start", date_format=date_fmt_Ymd__HMS),
                DatesColumns(column_name="end", date_format=date_fmt_Ymd__HMS),
            ],
        ).df


def test_too_many_cells():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_too_many_cells.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=csv_path,
            try_separator=",",
            expected_columns=["series", "start", "end"],
            date_columns=[
                DatesColumns(column_name="start", date_format=date_fmt_Ymd__HMS),
                DatesColumns(column_name="end", date_format=date_fmt_Ymd__HMS),
            ],
        ).df


def test_too_little_cells():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_too_little_cells.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=csv_path,
            try_separator=",",
            expected_columns=["series", "start", "end"],
            date_columns=[
                DatesColumns(column_name="start", date_format=date_fmt_Ymd__HMS),
                DatesColumns(column_name="end", date_format=date_fmt_Ymd__HMS),
            ],
        ).df


def test_no_error_without_dates():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_comma_separated_utf8.csv"
    assert csv_path.is_file()

    # reader with sep argument
    reader = PdReadFlexibleCsv(path=csv_path, try_separator=",", expected_columns=["series", "start", "end"],)
    assert reader.used_separator is None
    assert isinstance(reader.df, pd.DataFrame)
    assert pd.api.types.is_string_dtype(reader.df["series"])
    assert pd.api.types.is_string_dtype(reader.df["start"])
    assert pd.api.types.is_string_dtype(reader.df["end"])
    assert reader.used_separator == ","
    assert reader.used_encoding == "utf-8"

    # reader without sep argument
    reader = PdReadFlexibleCsv(path=csv_path, expected_columns=["series", "start", "end"],)
    assert reader.used_separator is None
    assert isinstance(reader.df, pd.DataFrame)
    assert pd.api.types.is_string_dtype(reader.df["series"])
    assert pd.api.types.is_string_dtype(reader.df["start"])
    assert pd.api.types.is_string_dtype(reader.df["end"])
    assert reader.used_separator == ","
    assert reader.used_encoding == "utf-8"


def test_no_error_with_dates():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_colon_separated.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=csv_path,
            try_separator=",",
            expected_columns=["series", "start", "end"],
            date_columns=[
                DatesColumns(column_name="start", date_format=date_fmt_Y_m_d__H_M_S),
                DatesColumns(column_name="end", date_format=date_fmt_Y_m_d__H_M_S),
            ],
        ).df

    # reader with sep argument
    reader = PdReadFlexibleCsv(
        path=csv_path,
        try_separator=";",
        expected_columns=["series", "start", "end"],
        date_columns=[
            DatesColumns(column_name="start", date_format=date_fmt_Y_m_d__H_M_S),
            DatesColumns(column_name="end", date_format=date_fmt_Y_m_d__H_M_S),
        ],
    )
    assert not reader.used_separator
    assert isinstance(reader.df, pd.DataFrame)
    assert reader.used_separator == ";"
    assert pd.api.types.is_string_dtype(reader.df["series"])
    assert pd.api.types.is_datetime64_any_dtype(reader.df["start"])
    assert pd.api.types.is_datetime64_any_dtype(reader.df["end"])

    # reader without sep argument
    reader = PdReadFlexibleCsv(
        path=csv_path,
        expected_columns=["series", "start", "end"],
        date_columns=[
            DatesColumns(column_name="start", date_format=date_fmt_Y_m_d__H_M_S),
            DatesColumns(column_name="end", date_format=date_fmt_Y_m_d__H_M_S),
        ],
    )
    assert not reader.used_separator
    assert isinstance(reader.df, pd.DataFrame)
    assert reader.used_separator == ";"
    assert pd.api.types.is_string_dtype(reader.df["series"])
    assert pd.api.types.is_datetime64_any_dtype(reader.df["start"])
    assert pd.api.types.is_datetime64_any_dtype(reader.df["end"])


def test_multi_separators_2_with_dates():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_multi_separators_2.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=csv_path,
            try_separator=",",
            expected_columns=["series", "start", "end"],
            date_columns=[
                DatesColumns(column_name="start", date_format=date_fmt_Ymd__HMS),
                DatesColumns(column_name="end", date_format=date_fmt_Ymd__HMS),
            ],
        ).df


def test_no_error_but_wrong_expected_columns():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_comma_separated_utf8.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=csv_path,
            try_separator=",",
            expected_columns=["series", "start", "column_does_not_exist"],
            date_columns=[
                DatesColumns(column_name="start", date_format=date_fmt_Ymd__HMS),
                DatesColumns(column_name="end", date_format=date_fmt_Ymd__HMS),
            ],
        ).df


def test_github_file():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_comma_separated_utf8.csv"
    assert csv_path.is_file()

    github_downloader = GithubFileDownloader(
        allowed_period_no_updates=datetime.timedelta(weeks=52 * 10),
        target_file=constants.GITHUB_STARTENDDATE_CAW_OPPERVLAKTEWATER_SHORT,
        branch_name=constants.GITHUB_STARTENDDATE_BRANCH_NAME,
        repo_name=constants.GITHUB_STARTENDDATE_REPO_NAME,
        repo_organisation=constants.GITHUB_ORGANISATION_NAME,
    )

    assert isinstance(github_downloader.get_download_url(), str)
    reader = PdReadFlexibleCsv(
        path=github_downloader.get_download_url(),
        try_separator=",",
        expected_columns=["series", "start", "end"],
        date_columns=[
            DatesColumns(column_name="start", date_format=date_fmt_Y_m_d__H_M_S),
            DatesColumns(column_name="end", date_format=date_fmt_Y_m_d__H_M_S),
        ],
    )
    assert not reader.used_separator
    assert isinstance(reader.df, pd.DataFrame)
    assert reader.used_separator == ","

    assert isinstance(github_downloader.target_file, Path)
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=github_downloader.target_file,
            try_separator=",",
            expected_columns=["series", "start", "end"],
            date_columns=[
                DatesColumns(column_name="start", date_format=date_fmt_Y_m_d__H_M_S),
                DatesColumns(column_name="end", date_format=date_fmt_Y_m_d__H_M_S),
            ],
        ).df


def test_no_utf8():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_parameters_no_utf8_but_ansi.csv"
    assert csv_path.is_file()
    df = PdReadFlexibleCsv(path=csv_path).df
    assert isinstance(df, pd.DataFrame)


def test_only_3header_no_data():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_only_3header_no_data.csv"
    assert csv_path.is_file()
    df = PdReadFlexibleCsv(path=csv_path).df
    assert isinstance(df, pd.DataFrame)
    assert sorted(df.columns) == ["column1", "column2", "column3"]
    assert df.empty


def test_only_2header_no_data():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_only_2header_no_data.csv"
    assert csv_path.is_file()
    df = PdReadFlexibleCsv(path=csv_path).df
    assert isinstance(df, pd.DataFrame)
    assert sorted(df.columns) == ["column1", "column2"]
    assert df.empty


def test_only_1header_no_data():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_only_1header_no_data.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(path=csv_path).df  # noqa


def test_empty():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_empty.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(path=csv_path).df  # noqa


def test_no_error_ansi():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_comma_separated_ansi.csv"
    assert csv_path.is_file()
    with open(csv_path) as tmp_file:
        file_encoding = tmp_file.encoding
        assert file_encoding == "cp1252"

    reader = PdReadFlexibleCsv(path=csv_path)
    assert reader.used_encoding is None
    df = reader.df  # noqa
    assert reader.used_encoding == "utf-8"


def test_date_columns():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_comma_separated_utf8.csv"
    expected_first_start_value = pd.Timestamp("2018-03-27 01:45:36")

    # this works (with date_format)
    df = PdReadFlexibleCsv(  # noqa
        path=csv_path,
        try_separator=",",
        expected_columns=["series", "start", "end"],
        date_columns=[
            DatesColumns(column_name="start", date_format=date_fmt_Y_m_d__H_M_S),
            DatesColumns(column_name="end", date_format=date_fmt_Y_m_d__H_M_S),
        ],
    ).df
    assert not df.empty
    # 0,3247_ES1,2018-03-27 01:45:36,2018-04-11 01:45:36
    assert df.iloc[0]["start"] == expected_first_start_value

    # this also works (added wrong date_format but we ignore errors)
    df = PdReadFlexibleCsv(  # noqa
        path=csv_path,
        try_separator=",",
        expected_columns=["series", "start", "end"],
        date_columns=[
            DatesColumns(column_name="start", date_format="%Y%m%d", errors="ignore"),
            DatesColumns(column_name="end", date_format="%Y%m%d", errors="ignore"),
        ],
    ).df
    assert not df.empty
    assert df.iloc[0]["start"] == str(expected_first_start_value)

    # this also works (added wrong date_format but we coerce errors)
    df = PdReadFlexibleCsv(  # noqa
        path=csv_path,
        try_separator=",",
        expected_columns=["series", "start", "end"],
        date_columns=[
            DatesColumns(column_name="start", date_format="%Y%m%d", errors="coerce"),
            DatesColumns(column_name="end", date_format="%Y%m%d", errors="coerce"),
        ],
    ).df
    assert not df.empty
    assert pd.isna(df.iloc[0]["start"])

    with pytest.raises(AssertionError):
        df = PdReadFlexibleCsv(  # noqa
            path=csv_path,
            try_separator=",",
            expected_columns=["series", "start", "end"],
            date_columns=[
                DatesColumns(column_name="start", date_format="%Y%m%d", errors="raise"),
                DatesColumns(column_name="end", date_format="%Y%m%d", errors="raise"),
            ],
        ).df


def test_extra_commas_in_string():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error_extra_comma_in_string.csv"

    # this works (with date_format)
    reader = PdReadFlexibleCsv(  # noqa
        path=csv_path,
        try_separator=",",
        date_columns=[
            DatesColumns(column_name="START", date_format=date_fmt_Y_m_d__H_M_S),
            DatesColumns(column_name="EIND", date_format=date_fmt_Y_m_d__H_M_S),
        ],
    )

    df = reader.df

    expected_cols = sorted(
        [
            "LOC_ID",
            "LOC_NAME",
            "X",
            "Y",
            "STATUS",
            "REF_NIVO",
            "RAYON",
            "INTERVAL",
            "START",
            "EIND",
            "PEILBESLUI",
            "FOTO_ID",
            "GPGIDENT",
            "GAFCODE",
            "RBGID",
        ]
    )
    assert sorted(df.columns) == expected_cols
