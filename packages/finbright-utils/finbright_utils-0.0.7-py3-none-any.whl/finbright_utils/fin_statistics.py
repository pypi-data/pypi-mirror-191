import pandas as pd
from statsmodels.tsa.stattools import coint
from finbright_utils import resample
from .constants.errors import LenghtNotMatch


def correlation(X1: pd.Series, X2: pd.Series) -> int:
    """_summary_

    Args:
        data (pd.DataFrame): A close price dataframe of two coins

    Returns:
        int: correlation coeffiecient between close prices of two coins
    """
    if len(X1) == len(X2):

        corr_coefficient = X1.corr(X2)

        return round(corr_coefficient, 2)

    else:
        raise (LenghtNotMatch)


def cointegration(X1: pd.Series, X2: pd.Series) -> int:
    """_summary_

    Args:
        data (pd.DataFrame): A close price dataframe of two coins

    Returns:
        int: cointegation coeffiecient between close prices of two coins
    """
    if len(X1) == len(X2):

        score, pvalue, _ = coint(X1, X2)
        coint_score = 1 - pvalue

        return round(coint_score, 2)

    else:
        raise (LenghtNotMatch)
