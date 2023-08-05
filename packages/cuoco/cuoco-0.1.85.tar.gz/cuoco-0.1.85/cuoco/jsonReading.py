import sys


# Check json file for unaccepted values
def checkJSONFormat(json_file, cols, col_types):
    accepted_inputForm = ["csv", "parquet", "orc", "txt"]
    accepted_outputForm = ["csv", "parquet", "orc", "txt"]
    accepted_header = ["yes", "none"]
    accepted_numNans = ["drop", "yes", "mean", "mode", "median"]
    accepted_strNans = ["yes", "no"]
    accepted_caps = ["no", "lower", "upper"]
    accepted_balanceData = ["yes", "no"]
    accepted_normalize = ["max_abs", "min_max", "z_score", "no"]
    accepted_balanceMethod = ["random", "smote"]
    accepted_index = ["True", "False"]
    # accepted_quotation = ["double", "single", "none"]

    if json_file['input_format'] not in accepted_inputForm:
        print("ERROR in JSON: input_format is not an accepted value")
        sys.exit(1)
    elif json_file['output_format'] not in accepted_outputForm:
        print("ERROR in JSON: output_format is not an accepted value")
        sys.exit(1)
    elif json_file['header'] not in accepted_header:
        print("ERROR in JSON: header is not an accepted value")
        sys.exit(1)
    elif json_file['num_nans'] not in accepted_numNans:
        print("ERROR in JSON: num_nans is not an accepted value")
        sys.exit(1)
    elif json_file['str_nans'] not in accepted_strNans:
        print("ERROR in JSON: str_nans is not an accepted value")
        sys.exit(1)
    elif json_file['caps'] not in accepted_caps:
        print("ERROR in JSON: caps is not an accepted value")
        sys.exit(1)
    elif json_file['normalize_method'] not in accepted_normalize:
        print("ERROR in JSON: normalize_method is not an accepted value")
        sys.exit(1)
    elif json_file['balance_data'] not in accepted_balanceData:
        print("ERROR in JSON: balance_data is not an accepted value")
        sys.exit(1)
    elif json_file['balance_data'] == "yes" and "object" in col_types:
        print("ERROR in JSON: cant apply numerical oversampling methods to a dataframe with string type columns")
        sys.exit(1)
    elif json_file['balance_params']["balance_method"] not in accepted_balanceMethod \
            and json_file['balance_data'] == "yes":
        print("ERROR in JSON: balance_method is not an accepted value")
        sys.exit(1)
    elif json_file['balance_params']["y_col"] not in cols and json_file['balance_data'] == "yes":
        print("ERROR in JSON: the column you want to use as y_col doesn't exist on the dataset")
        sys.exit(1)
    elif json_file['index'] not in accepted_index:
        print("ERROR in JSON: index is not an accepted value")
        sys.exit(1)
