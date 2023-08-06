



def save_output_excel(df, fname='result.xlsx', verbose=False):
    """
    This function saves the processed dataframe to an excel file. The location and name of the file can be specified
    by providing the 'fname' parameter. The function also has an option to remove certain columns from the dataframe
    before saving, by setting the 'verbose' parameter to False.

    Parameters:
    - df (pandas dataframe): The dataframe that needs to be saved
    - fname (str, optional): The location and name of the excel file. Default is 'result.xlsx'
    - verbose (bool, optional): A flag to indicate if certain columns should be removed from the dataframe before saving.
                                Default is False

    Returns:
    - None
    """
    columns_to_keep=['std_name',
                     'research_information_gathering',
                     'creative_input',
                     'cooperation_within_group',
                     'communication',
                     'contribution_quality',
                     'meeting_attendance',
                     'dgroup_name',
                     'nmember',
                     'weightage',
                     'justification_annom',
                     'feedback'
                     ]


    if not verbose:
        df = df.loc[:, columns_to_keep]
    # Move 'justification_annom' and 'feedback' to the last columns
    cols = df.columns.tolist()
    cols = [col for col in cols if col not in ['justification_annom', 'feedback']] + ['justification_annom', 'feedback']
    df = df[cols]
    df.to_excel(fname, index=False)

