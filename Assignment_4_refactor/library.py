import pandas as pd
import numpy as np

def render_table(data, title, transpose=False, change_indexing_id=False, new_index="S/N", should_display=True):
    df = pd.DataFrame(data).style.set_caption(title)
    if change_indexing_id:
        df.set_index(new_index, inplace=True)
    if should_display:
        display(df)
    return df

def render_multi_index_2D_table(data, outer_column_1, outer_column_2, inner_1, inner_2, unique_key, should_display=True):
    df = pd.DataFrame(data)

    # create a MultiIndex for liquid and gas columns
    columns = pd.MultiIndex.from_product([[outer_column_1, outer_column_2], [inner_1, inner_2]], names=['', ''])

    # create a new DataFrame with the desired columns and index
    new_df = pd.DataFrame(columns=columns, index=df.index)

    # fill in the values for the new DataFrame
    for i, row in df.iterrows():
        new_df.loc[i, (outer_column_1, inner_1)] = row[outer_column_1][inner_1]
        new_df.loc[i, (outer_column_1, inner_2)] = row[outer_column_1][inner_2]
        new_df.loc[i, (outer_column_2, inner_1)] = row[outer_column_2][inner_1]
        new_df.loc[i, (outer_column_2, inner_2)] = row[outer_column_2][inner_2]

    # add the component column back to the new DataFrame
    new_df.insert(0, unique_key, df[unique_key])

    # display the new DataFrame
    if should_display:
        display(new_df)
    return new_df