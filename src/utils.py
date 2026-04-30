import pandas as pd

def view_table(table, limit):
    query = f"""
        SELECT *
        FROM {table}
        LIMIT {limit}
    """
    return pd.read_sql_query(query, conn)

def remove_outliers_iqr(df, column, group_column):
  new_df = pd.DataFrame()
  for group_value in df[group_column].unique():
    group_df = df[df[group_column] == group_value]
    Q1 = group_df[column].quantile(0.25)
    Q3 = group_df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_group_df = group_df[(group_df[column] >= lower_bound) & (group_df[column] <= upper_bound)]
    new_df = pd.concat([new_df, filtered_group_df])
  return new_df

def remove_outliers_by_category(df, column, n_std=3):
    """Removes outliers based on standard deviation for specific categories."""
    new_df = df.copy()
    for category in df['category'].unique():
        category_data = df[df['category'] == category]
        mean = category_data[column].mean()
        std = category_data[column].std()
        lower_bound = mean - n_std * std
        upper_bound = mean + n_std * std
        
        # Filter out the outliers
        mask = (new_df['category'] == category) & ((new_df[column] < lower_bound) | (new_df[column] > upper_bound))
        new_df = new_df[~mask]
        
    return new_df
