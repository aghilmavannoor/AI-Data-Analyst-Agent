import pandas as pd


def analyze_data(df, operation, column=None):
    """
    Perform common data-analysis operations.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data.

    operation : str
        Analysis operation to perform.

    column : str, optional
        Column on which to perform the operation.
    """

    operation = operation.lower().strip()

    # --------------------------------------
    # SUM
    # --------------------------------------

    if operation == "sum":

        if column is None:
            raise ValueError("Column is required for sum.")

        return df[column].sum()


    # --------------------------------------
    # AVERAGE
    # --------------------------------------

    elif operation in ["average", "mean"]:

        if column is None:
            raise ValueError("Column is required for average.")

        return df[column].mean()


    # --------------------------------------
    # MINIMUM
    # --------------------------------------

    elif operation == "min":

        if column is None:
            raise ValueError("Column is required for minimum.")

        return df[column].min()


    # --------------------------------------
    # MAXIMUM
    # --------------------------------------

    elif operation == "max":

        if column is None:
            raise ValueError("Column is required for maximum.")

        return df[column].max()


    # --------------------------------------
    # COUNT
    # --------------------------------------

    elif operation == "count":

        return len(df)


    # --------------------------------------
    # DESCRIBE
    # --------------------------------------

    elif operation == "describe":

        return df.describe()


    # --------------------------------------
    # SORT
    # --------------------------------------

    elif operation == "sort":

        if column is None:
            raise ValueError("Column is required for sorting.")

        return df.sort_values(
            by=column,
            ascending=False
        )


    # --------------------------------------
    # UNKNOWN OPERATION
    # --------------------------------------

    else:

        raise ValueError(
            f"Unsupported operation: {operation}"
        )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    data = {
        "category": [
            "Laptop",
            "Smartphone",
            "Tablet"
        ],
        "revenue": [
            172440000,
            68090000,
            22290000
        ]
    }

    df = pd.DataFrame(data)

    print("\nOriginal Data:")
    print(df)

    print("\nTotal Revenue:")

    total = analyze_data(
        df,
        "sum",
        "revenue"
    )

    print(total)

    print("\nAverage Revenue:")

    average = analyze_data(
        df,
        "average",
        "revenue"
    )

    print(average)

    print("\nMaximum Revenue:")

    maximum = analyze_data(
        df,
        "max",
        "revenue"
    )

    print(maximum)