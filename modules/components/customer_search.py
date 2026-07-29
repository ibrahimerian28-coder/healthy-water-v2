def search_customers(df, search):

    if not search:
        return df

    return df[
        df.astype(str)
        .apply(
            lambda x: x.str.contains(
                search,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    ]
