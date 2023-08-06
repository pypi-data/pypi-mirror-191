import pandas as pd

def pd_clean_up_columns(df) -> pd.DataFrame:
    # Drops all columns where all values are null/nan
    df_temp = df.dropna(how='all', axis=1)
    # Drops all columns which only contains 0's - multiple choice variables
    df_temp = df_temp.loc[:, (df_temp != 0).any(axis=0)]
    # Test of unique values in each column
    nb_unique = df_temp.apply(pd.Series.nunique) 
    static_cols = nb_unique[nb_unique==1].index # Cols containing only one value - though NANs as well
    columns_with_nan = df_temp.columns[df_temp.isna().any()].tolist()
    possible_cols = [col for col in static_cols if col not in columns_with_nan]

    # Close your eyes... this is ugly!
    remove_these_cols = []

    for col in possible_cols:
        if col.startswith('background__ptype') and col.endswith('t'):
            if possible_cols.count(col[:-1]) == 1:
                remove_these_cols.append(col[:-1])
                remove_these_cols.append(col)

    closed_ptypes = [col for col in df.columns if col.startswith('background__ptype') and col.endswith('c')]
    
    if closed_ptypes:
        remove_these_cols.extend(closed_ptypes)

    df2 = df_temp.drop(columns=remove_these_cols)
    return df2