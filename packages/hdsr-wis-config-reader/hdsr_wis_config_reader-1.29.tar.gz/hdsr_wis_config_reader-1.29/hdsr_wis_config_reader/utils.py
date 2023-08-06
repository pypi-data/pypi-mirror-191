from hdsr_wis_config_reader import constants
from pathlib import Path
from typing import List
from typing import Union

import logging
import numpy as np  # noqa numpy comes with geopandas
import pandas as pd  # noqa pandas comes with geopandas
import re


logger = logging.getLogger(__name__)


class DatesColumns:
    def __init__(self, column_name: str, date_format: str, errors: str = "raise"):
        self.column_name = column_name
        self.date_format = date_format
        self.errors = errors
        assert self.column_name
        assert all([isinstance(x, str) and x for x in (column_name, date_format, errors)])
        assert errors in ("raise", "coerce", "ignore")


class PdReadFlexibleCsv:
    def __init__(
        self,
        path: Union[str, Path],
        try_separator: str = None,
        expected_columns: List[str] = None,
        date_columns: List[DatesColumns] = None,
    ):
        self.is_http_file = None
        self._used_separator = None
        self._used_encoding = None
        self.path_str = self._get_path(path=path)
        self.date_columns = date_columns
        self.separators = self.__get_separators(sep=try_separator)
        self.expected_columns = expected_columns
        self._df = None

    @property
    def used_encoding(self) -> str:
        return self._used_encoding

    @property
    def used_separator(self) -> str:
        return self._used_separator

    def _get_path(self, path: Union[str, Path]) -> str:
        if isinstance(path, str) and ("http" in path or Path(path).is_file()):
            self.is_http_file = True
            return path
        elif isinstance(path, Path) and path.is_file():
            self.is_http_file = False
            return path.as_posix()
        raise AssertionError(
            "path must be a pathlib.Path (existing file) or a str (an url containing 'http'). "
            "In case you use e.g. GithubFileDownloader, then use get_download_url() instead of target_file"
        )

    @staticmethod
    def __get_separators(sep: str = None) -> List[str]:
        if sep:
            assert isinstance(sep, str), f"sep {sep} must be of type string"
            return [sep]
        return [",", ";"]

    @staticmethod
    def __trim_all_string_columns(df):
        """Trim whitespace from ends of each value across all series in dataframe."""
        return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    def __fixed_by_quotechar(self, line: str, used_separator: str, too_many_sep: int):
        """Pandas quotechar denotes the start and end of a quoted item. Quoted items can include the delimiter and
        it will be ignored. The default quotechar is double quote (so pd.read_csv(quotechar='"').
        So this csv row (with sep=',') has 3 columns: 21000101,"Groenraven-Oost, zuidelijk deel",HPIM0129.jpg

        To find quotes in a string we use regex pattern:
            '"([^"]*)"'
        The pattern can be broken down as follows:
            " - matches a double quote.
            ( - start of a capturing group, used to capture the matched string.
            [^"]* - matches zero or more characters that are not a double quote.
            ) - end of the capturing group.
            " - matches the closing double quote.
        So, the entire pattern matches a string that starts and ends with double quotes, and can contain any
        characters in between except a double quote.
        """
        quotechar = constants.PANDAS_DEFAULT_QUOTECHAR
        pattern = f"{quotechar}([^{quotechar}]*){quotechar}"
        quotes = re.findall(pattern=pattern, string=line)
        nr_sep_in_quotes = 0
        for quote in quotes:
            nr_sep_in_quotes += quote.count(used_separator)
        if too_many_sep == nr_sep_in_quotes:
            return True
        msg = f"line contains {too_many_sep} too many separator and has no quotes with default quote_char ({quotechar})"
        logger.warning(msg)
        return True if too_many_sep == nr_sep_in_quotes else False

    def __check_separators_per_row(self, used_separator: str, df: pd.DataFrame) -> None:
        if self.is_http_file:
            # loop trough csv line by line is not possible with github file (in buffer). Avoid downloading!
            return
        nr_expected_separators_per_row = len(df.columns) - 1
        with open(self.path_str) as tmp_file:
            for index, line in enumerate(tmp_file):
                nr_separators_found = line.count(used_separator)
                if nr_separators_found == nr_expected_separators_per_row:
                    continue
                if nr_separators_found > nr_expected_separators_per_row:
                    too_many_sep = nr_separators_found - nr_expected_separators_per_row
                    if self.__fixed_by_quotechar(line=line, used_separator=used_separator, too_many_sep=too_many_sep):
                        continue
                raise AssertionError(
                    f"csv error in {self.path_str} as line nr {index+1} has unexpected nr separators "
                    f"{nr_separators_found} (expected={nr_expected_separators_per_row})"
                )

    @staticmethod
    def __check_sep_not_in_other_columns(df: pd.DataFrame, used_separator: str, default_error_msg: str) -> None:
        """
        We want to avoid that this:
            col_a,col_b,col_c
            text1,text2,text3
            text1;text2;text3
            text1,text2,text3
        becomes:
            col_a               col_b               col_c
            text1               text2               text3
            text1;text2;text3   None                None
            text1               text2               text3
        """
        has_df_no_nan = df.isnull().sum().sum() == 0
        if has_df_no_nan:
            return

        df_nr_nans_per_row = df.isnull().sum(axis=1)
        df_wrong_rows = df[df_nr_nans_per_row == len(df.columns) - 1]
        if not df_wrong_rows.empty:
            raise AssertionError(f"{default_error_msg}.  df_wrong_rows={df_wrong_rows}")

        all_possible_separators = [",", ";"]
        df_rows_with_nan = df[df_nr_nans_per_row != 0]
        for possible_wrong_separator in all_possible_separators:
            if possible_wrong_separator == used_separator:
                continue
            for col in df_rows_with_nan.columns:
                try:
                    df_wrong_rows = df_rows_with_nan[df_rows_with_nan[col].str.contains(possible_wrong_separator)]
                except Exception:  # noqa
                    continue
                if not df_wrong_rows.empty:
                    row_indices = df_wrong_rows.index.to_list()
                    err = f"row(s) {row_indices} contain empty cell(s) AND a separator other than {used_separator}"
                    raise AssertionError(f"{default_error_msg}, err={err}")

    @property
    def df(self) -> pd.DataFrame:
        if self._df is not None:
            return self._df
        default_error_msg = (
            f"could not read csv {self.path_str} with separators={self.separators}, "
            f"expected columns={self.expected_columns}"
        )
        for separator in self.separators:
            df = self._csv_to_df(separator=separator)
            if len(df.columns) == 1:
                continue
            if df.empty and len(df.columns) in (0, 1):
                continue
            if self.expected_columns:
                for expected_column in self.expected_columns:
                    assert (
                        expected_column in df.columns
                    ), f"expected_column '{expected_column}' must be in {df.columns}, file={self.path_str}"
            df = self.__trim_all_string_columns(df=df)
            self.__check_separators_per_row(used_separator=separator, df=df)
            self._used_separator = separator
            self._df = df
            return self._df
        raise AssertionError(default_error_msg)  # raise since no success

    def _csv_to_df(self, separator: str, encoding: str = None) -> pd.DataFrame:
        encoding = encoding if encoding else "utf-8"
        try:
            df = pd.read_csv(filepath_or_buffer=self.path_str, sep=separator, engine="python", encoding=encoding)
            if self.date_columns:
                # convert 'None' to pd.NaN (we require this for the __check_sep_not_in_other_columns()
                for x in self.date_columns:
                    df[x.column_name] = pd.to_datetime(
                        arg=df[x.column_name], format=x.date_format, errors=x.errors, exact=True
                    )
            self._used_encoding = encoding
            return df
        except pd.errors.EmptyDataError:
            logger.warning(f"{self.path_str} is empty")
            return pd.DataFrame(data=None)
        except pd.errors.ParserError as err:
            logger.debug(f"could not parse csv {self.path_str} with separator {separator}, err={err}")
            return pd.DataFrame(data=None)
        except KeyError as err:
            logger.debug(f"could not parse csv {self.path_str} with separator {separator}, err={err}")
            return pd.DataFrame(data=None)
        except UnicodeDecodeError as err:
            with open(self.path_str) as tmp_file:
                df = self._csv_to_df(separator=separator, encoding=tmp_file.encoding)
                if not df.empty:
                    logger.warning(
                        f"found encoding {tmp_file.encoding} (instead of utf-8) for {self.path_str}, err={err}"
                    )
                self._used_encoding = tmp_file.encoding
                return df
        except Exception as err:
            raise AssertionError(f"unexpected error when opening {self.path_str}, err={err}")


class DataframeActions:
    @staticmethod
    def df1_rows_not_in_df2(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """
        df1 = pd.DataFrame(data = {'col1' : [1, 2, 3, 4, 5, 3], 'col2' : [10, 11, 12, 13, 14, 10]})
        df2 = pd.DataFrame(data = {'col1' : [1, 2, 3, 4], 'col2' : [10, 11, 12, 16]})
        df_all = df1.merge(df2.drop_duplicates(), how='outer', indicator=True)
        ------------------------
           col1  col2      _merge
        0     1    10        both
        1     2    11        both
        2     3    12        both
        3     4    13   left_only
        4     5    14   left_only
        5     3    10   left_only
        6     4    16  right_only
        ------------------------
        """
        df_all = df1.merge(df2.drop_duplicates(), how="outer", indicator=True)
        return df_all[df_all["_merge"] == "right_only"]

    @classmethod
    def is_equal_dataframes(
        cls, df1: pd.DataFrame, df2: pd.DataFrame, do_raise: bool = True, check_index: bool = False
    ) -> bool:
        assert isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame)
        # ensure ordered dfs (index and column)
        df1 = df1.sort_index().sort_index(axis=1)
        df2 = df2.sort_index().sort_index(axis=1)

        if not check_index:
            df1 = df1.reset_index(inplace=False, drop=True)
            df2 = df2.reset_index(inplace=False, drop=True)

        if df1.equals(df2):
            return True

        try:
            assert sorted(df2.columns) == sorted(df1.columns)
            df1_too_few_rows = cls.df1_rows_not_in_df2(df1=df1, df2=df2)
            df2_too_many_rows = cls.df1_rows_not_in_df2(df1=df2, df2=df1)
            assert df1_too_few_rows.empty, f"{len(df1_too_few_rows)} df1 rows not in df2"
            assert df2_too_many_rows.empty, f"{len(df2_too_many_rows)} df2 rows not in df1"
        except AssertionError as err:
            if do_raise:
                logger.error(err)
                raise

        try:
            pd.testing.assert_frame_equal(left=df2, right=df1)
            return True
        except Exception as err:
            logger.debug(err)
            return False
