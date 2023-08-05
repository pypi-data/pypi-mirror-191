from imblearn.over_sampling import RandomOverSampler, SMOTE


# Function for data normalization
def normalize(col, df, method):
    if method == "max_bas":
        df[col] = df[col] / df[col].abs().max()
    elif method == "min_max":
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    elif method == "z_score":
        df[col] = (df[col] - df[col].mean()) / df[col].std()

    return df


# Function to manage oversampling method
def oversampling(df, method, ycol):
    global oversampling_method

    # Establish X and Y columns for the operation
    x = df.drop(ycol, axis=1)
    y = df[ycol]

    if method == "random":
        oversampling_method = RandomOverSampler(sampling_strategy='minority')
    elif method == "smote":
        oversampling_method = SMOTE(sampling_strategy='minority')

    # Execute imblearn random oversampling method
    x_ov, y_ov = oversampling_method.fit_resample(x, y)
    x_ov[ycol] = y_ov



    return x_ov

