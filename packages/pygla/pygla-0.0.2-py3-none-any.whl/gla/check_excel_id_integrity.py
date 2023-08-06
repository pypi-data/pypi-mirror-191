
import pandas as pd
'''
To check if the student ID is duplicated or not

'''

def read_file(finput=None):

    """
    This function reads in a file and performs data transformations to filter and group the data.

    Parameters:

    finput (str, optional): The location and name of the excel file. Default is None
    Returns:

    pandas dataframe: The processed dataframe
    """
    df=pd.read_excel(finput)
    df = df.filter(regex='Peers Student.*')
    indices_s = df.columns.get_indexer(df.columns[df.columns.str.contains('Peers Student')])

    all_df=[]
    for dcols in indices_s :
        dd=df.iloc[:,[dcols-1,dcols]]
        dd.columns=['peer_name','std_id']
        all_df.append(dd)

    df1 = pd.concat(all_df).reset_index(drop=True)
    df1=df1.dropna()
    newdf1 = df1.groupby(['peer_name','std_id']).first()
    newdf1=newdf1.reset_index()


    return newdf1.drop_duplicates( "std_id" , keep='first')




fexcel=r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_assessment.xlsx'
df=read_file(fexcel)

h=1