# This module is part of mydstools.
# Please refer to https://github.com/antobzzll/dstoolbox

import numpy as np
import pandas as pd
import re


def clean_col_names(df_columns: pd.Index, wlen: int = 0) -> list:
    """
    Method for cleaning column names of a `pandas.DataFrame`.

    Args:
        df_columns (pd.Index): dataframe's dirty column names.
        wlen (int, optional): length of cleaned words. Defaults to 0.

    Raises:
        ValueError: if `df_columns` is not a `pd.Index`.

    Returns:
        list: list of new column names to be assigned to `df.columns`.
    """

    # usage:
    # df.columns = utilities.clean_col_names(df.columns)

    try:
        df_columns = df_columns.to_list()
    except AttributeError:
        raise ValueError(
            "Invalid argument type. `df_columns` takes a "
            "`pandas.Index` type.") from None
    else:
        def _fix(target: str):
            target = target.lower().split()
            res = []
            for elem in target:
                elem = re.sub(r'[^\w]', '', elem)
                
                if elem:
                    if wlen > 0:
                        res.append(elem[:wlen])
                    else:
                        res.append(elem)
            return '_'.join(res)

        return list(map(_fix, df_columns))


def currency_to_float(
        target: str | list | tuple | pd.Series
        ) -> str | list | tuple | pd.Series:
    """Automatically cleans a currency containing variable and prepares it 
    for analysis by transforming it to `float` type. 
    Target variable of type `str`, `list`, `tuple`, or `pandas.Series`.

    Args:
        target (str | list | tuple | pandas.Series): target variable.

    Returns:
        [str | list | tuple | pandas.Series]: cleaned target variable.
    """
    symbols = ['$', '€', '£', '¥', '₣', '₹', 'د.ك', 'د.إ', '﷼', '₻', '₽',
               '₾', '₺', '₼', '₸', '₴', '₷', '฿', '원', '₫', '₮', '₯',
               '₱', '₳', '₵', '₲', '₪', '₰']

    codes = ['AFN', 'ALL', 'DZD', 'USD', 'EUR', 'AOA', 'XCD', 'ARS', 'AMD',
             'AWG', 'AUD', 'AZN', 'BSD', 'BHD', 'BDT', 'BBD', 'BYN', 'BZD',
             'XOF', 'BMD', 'BTN', 'INR', 'BOB', 'BOV', 'BAM', 'BWP', 'NOK',
             'BRL', 'BND', 'BGN', 'BIF', 'CVE', 'KHR', 'XAF', 'CAD', 'KYD',
             'CLF', 'CLP', 'CNY', 'COP', 'COU', 'KMF', 'CDF', 'NZD', 'CRC',
             'HRK', 'CUC', 'CUP', 'ANG', 'CZK', 'DKK', 'DJF', 'DOP', 'EGP',
             'SVC', 'ERN', 'ETB', 'FKP', 'FJD', 'XPF', 'GMD', 'GEL', 'GHS',
             'GIP', 'GTQ', 'GBP', 'GNF', 'GYD', 'HTG', 'HNL', 'HKD', 'HUF',
             'ISK', 'IDR', 'XDR', 'IRR', 'IQD', 'ILS', 'JMD', 'JPY', 'JOD',
             'KZT', 'KES', 'KPW', 'KRW', 'KWD', 'KGS', 'LAK', 'LBP', 'LSL',
             'ZAR', 'LRD', 'LYD', 'CHF', 'MOP', 'MGA', 'MWK', 'MYR', 'MVR',
             'MRU', 'MUR', 'XUA', 'MXN', 'MXV', 'MDL', 'MNT', 'MAD', 'MZN',
             'MMK', 'NAD', 'NPR', 'NIO', 'NGN', 'OMR', 'PKR', 'PAB', 'PGK',
             'PYG', 'PEN', 'PHP', 'PLN', 'QAR', 'MKD', 'RON', 'RUB', 'RWF',
             'SHP', 'WST', 'STN', 'SAR', 'RSD', 'SCR', 'SLE', 'SGD', 'XSU',
             'SBD', 'SOS', 'SSP', 'LKR', 'SDG', 'SRD', 'SZL', 'SEK', 'CHE',
             'CHW', 'SYP', 'TWD', 'TJS', 'TZS', 'THB', 'TOP', 'TTD', 'TND',
             'TRY', 'TMT', 'UGX', 'UAH', 'AED', 'USN', 'UYI', 'UYU', 'UZS',
             'VUV', 'VEF', 'VED', 'VND', 'YER', 'ZMW', 'ZWL']

    currencies = symbols + codes

    def _fix(string: str):
        
        # value and currency definitions
        if type(string) == float:
            raise ValueError(f"{string} not a string")
        
        string = string.split()
        if len(string) == 1:
            for c in currencies:
                if c in string[0].upper(): # check if symbols
                    currency = c
                    value = string[0].upper().replace(currency, '')
            if not 'value' in locals():
                currency = ''
                value = string[0]
        else:
            if string[1].upper() in currencies:
                currency = string[1].upper()
                value = string[0]
            elif string[0].upper() in currencies:
                currency = string[0].upper()
                value = string[1]
            else:
                currency = None
                value = string[0]

        # commas and dots manipulations
        first_comma_pos = re.search(r'[,]', value)
        first_dot_pos = re.search(r'[.]', value)

        if all(ele is not None for ele in [first_comma_pos, first_dot_pos]):
            # if both commas and dots have been found
            if first_comma_pos.span()[0] < first_dot_pos.span()[0]:
                value = value.replace(',', '')
            else:
                value = value.replace('.', '')
                value = value.replace(',', '.')
            ret_float = float(value)
            
        elif not any(ele is not None for ele in [first_comma_pos,
                                                 first_dot_pos]):
            ret_float = float(value)
            
        else:
            if len(re.findall(r'[.]', value)) == 1:
                ret_float = float(value)
            elif len(re.findall(r'[,]', value)) == 1:
                value = value.replace(',', '.')
                try:
                    ret_float = float(value)
                except ValueError:
                    ret_float = np.nan
            else:
                ret_float = np.nan

        # final return
        return ret_float, currency


    if type(target) is str:
        return _fix(target)
    else:
        values = []
        currs = []

        if type(target) is list:
            for t in target:
                v, c = _fix(t)
                values.append(v)
                currs.append(c)
            return values, currs
       
        elif type(target) is tuple:
            for t in target:
                v, c = _fix(t)
                values.append(v)
                currs.append(c)
            return tuple(values), tuple(currs)

        elif type(target) is pd.Series:
            for _, t in target.items():
                v, c = _fix(t)
                values.append(v)
                currs.append(c)
            return pd.Series(values), pd.Series(currs)