# Count number of nans
def countNans(df):
    nan_count = df.isna().sum().sum()
    return nan_count


def showStats(original_df, actual_df):
    # Dataset information
    print("*************************")
    print("** DATASET INFORMATION **")
    print("")
    print("- Number of rows: " + str(len(actual_df)))
    print("")
    print("- Columns: " + actual_df.columns)

    print("")
    print("-------------------------")
    print("DATASET STATISTICS")
    print("")

    # NANS
    print("· Count of NANS in the raw dataset:")
    print(countNans(original_df))
    print(" ")

    # Removed rows
    print("· Number of removed rows:")
    print(len(original_df) - len(actual_df))
    print(" ")



def writeDF(df, route, name, output_format, index_format):
    if output_format == "csv" or output_format == "txt":
        df.to_csv(route + name + "." + output_format, index=index_format)
    elif output_format == "orc":
        df.to_orc(route + name + "." + output_format, index=index_format)
    elif output_format == "parquet":
        df.to_parquet(route + name + "." + output_format, index=index_format)
