import pandas as pd


# READ THE FILE
def readFile(file_format, file, separator, header):
    if file_format == "csv" or file_format == "txt":
        if header == "none":
            data_file = pd.read_csv(file, sep=separator, encoding='unicode_escape', header=None)
        else:
            data_file = pd.read_csv(file, sep=separator, encoding='unicode_escape')
    elif file_format == "parquet":
        data_file = pd.read_parquet(file)
    else:
        data_file = pd.read_orc(file)

    return data_file

#TREAT NUMERIC NANS
def numNans(df, type):
    if type == "drop":
        df = df.dropna()
    # Mean = the average value (the sum of all values divided by number of values)
    elif type == "mean":
        for col in df:
            if df.dtypes[col] == "int64" or df.dtypes[col] == "float64":
                mean = df[col].mean()
                df[col].fillna(mean, inplace=True)
    # Median = the value in the middle, after you have sorted all values ascending.
    elif type == "median":
        for col in df:
            if df.dtypes[col] == "int64" or df.dtypes[col] == "float64":
                mean = df[col].median()
                df[col].fillna(mean, inplace=True)
    # Mode = the value that appears most frequently.
    elif type == "mode":
        for col in df:
            if df.dtypes[col] == "int64" or df.dtypes[col] == "float64":
                mean = df[col].mode()
                df[col].fillna(mean, inplace=True)
    return df

#TREAT STRING NANS
def strNans(df):
    df = df.dropna()

    return df

#TREAT CAPS (upperCase, lowerCase)
def caps(df, type):
    for col in df:
        if df.dtypes[col] == "object":
            if type == "lower":
                df[col] = df[col].str.lower()
            else:
                df[col] = df[col].str.upper()

    return df

#TREAT UNQUOTED STRINGS
def removeWhites(df):
    for col in df:
        if df.dtypes[col] == "object":
            df[col] = df[col].str.replace(" ", "")

    return df

def quotes(df, method):
    for col in df:
        if df.dtypes[col] == "object":
            df[col] = df[col].str.replace('"', '')
            if method == "double":
                df[col] = df[col].apply(lambda x: '"' + str(x) + '"')
            elif method == "single":
                df[col] = df[col].apply(lambda x: "'" + str(x) + "'")
    return  df