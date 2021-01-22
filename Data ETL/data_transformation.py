import datetime

import pandas as pd


def format_columns(dtf):
    # format columns into better data types
    print("Formatting dataframe..........")
    # Fix id
    dtf = dtf[dtf.id.apply(lambda x: str(x).isnumeric())].set_index('id')

    # Convert Objects to Numeric
    dtf['term'] = dtf['term'].str.extract('(\\d+)').astype('float')
    dtf['emp_length'] = dtf['emp_length'].replace({'< 1 year': '0 years', '10+ years': '10 years'})
    dtf['emp_length'] = dtf['emp_length'].str.extract('(\\d+)').astype('float')

    # Format Date Columns
    filter_col = [col for col in dtf if col.endswith('_d')] + ['earliest_cr_line']
    dtf[filter_col] = dtf[filter_col].apply(pd.to_datetime)

    return dtf


def create_columns(dtf):
    # create a mean fico feature to remove the two other fico features and reduce feature space
    dtf['mean_fico'] = (dtf['fico_range_low'] + dtf['fico_range_high']) / 2
    print(dtf.head())
    return dtf


def save_split_data(dtf, name, clean_path):
    print("Saving Cleaned Data and Preparing for Database..........")
    dtf.head()
    # fully cleaned data is saved as a pkl file for efficient storage
    # incase there is ever something wrong with the database connect
    dtf.to_pickle(clean_path + '{}_clean_{}.pkl'.format(name, datetime.datetime.today().strftime('%y_%m_%d')))

    main_cols = ['funded_amnt_inv', 'term', 'int_rate', 'emp_length', 'out_prncp_inv', 'total_pymnt_inv',
                 'last_pymnt_amnt', 'mths_since_recent_inq', 'percent_bc_gt_75', 'mean_fico', 'sub_grade',
                 'home_ownership', 'loan_status', 'purpose', 'addr_state', 'issue_d', 'earliest_cr_line',
                 'last_pymnt_d', 'last_credit_pull_d']

    # split the two dataset into main and secondary
    df_1 = dtf[main_cols]
    df_2 = dtf.drop(df_1.columns, axis=1, errors='ignore')
    return df_1.reset_index(), df_2.reset_index()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
