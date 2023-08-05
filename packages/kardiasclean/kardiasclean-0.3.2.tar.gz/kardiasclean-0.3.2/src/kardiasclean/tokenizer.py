import pandas as pd
from .clean import clean_accents, clean_stopwords, clean_symbols, clean_tokenize
from .create import create_unique_list
from .normalize import normalize_from_tokens
from typing import List, Union


class Tokenizer:
    """
    Tokenizer class.

    Example:
        origin = Tokenizer(df[["patient_id", "state", "municipality", "altitude"]])
        origin.transform('state', 'municipality')
        state_df, municipality_df = origin.get_uniques('state', ['municipality', 'altitude'])
        print(origin.df)
    """

    def __init__(self, df: pd.DataFrame, token_suffix: str = "_token", keywords_suffix: str = "_kw") -> None:
        """Create a copy of a given dataframe for further transformation with the object methods."""
        self.df = df.copy()
        self.token_col = "{col}" + token_suffix
        self.kw_col = "{col}" + keywords_suffix

    def transform(self, *cols: str) -> None:
        """Apply all cleaning methods with the default values."""
        for col in cols:
            token = self.token_col.format(col=col)
            kw = self.kw_col.format(col=col)
            self.df[col] = clean_accents(self.df[col])
            self.df[col] = clean_symbols(self.df[col])
            self.df[kw] = clean_stopwords(self.df[col])
            self.df[token] = clean_tokenize(self.df[kw])

        for col in cols:
            token = self.token_col.format(col=col)
            unique_df = create_unique_list(self.df[[token, col]], self.df[token])
            self.df[col] = normalize_from_tokens(self.df[token], unique_df[token], unique_df[col])
        
    def get_uniques(self, *cols: Union[str, list]) -> List[pd.DataFrame]:
        """Use the Tokenizer's dataframe to get the unique values based on the arguments.
        If the argument is a string, use it along its token to create an unique list.
        If the argument is a list, use the first element with the token and include the
        with the max value found."""
        uniques = []
        for col in cols:
            if type(col) == str:
                token = self.token_col.format(col=col)
                columns = index = [token, col]
            else:
                token = self.token_col.format(col=col[0])
                columns = [token, *col]
                index = [token, col[0]]
            unique_df = self.df.groupby(index).max().reset_index()[columns]
            uniques.append(unique_df.rename(columns={token:"token"}))
        return uniques