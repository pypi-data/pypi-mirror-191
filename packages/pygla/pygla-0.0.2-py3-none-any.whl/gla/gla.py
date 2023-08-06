import argparse
from itertools import product

import pandas as pd

from gla.helper import save_output_excel
from gla.ref_map import CONST_VAL, COL_NAME, N_ELEMENT, D_AGG_CALCULATION, COLS_OPT


class PeerEvaluator:
    def __init__(self, finput, scale_type=None):

        self.scale_type = scale_type
        self.col_name = COL_NAME
        self.elements_to_extract = N_ELEMENT
        self.d_agg_calculation = D_AGG_CALCULATION
        self.cols_opt = COLS_OPT
        self.df_agg = []
        self.cal_score = []
        self.agg_df = []
        self.df = self.read_file_transform(finput)

    def extract_columns(self, df, columns, std_cols):
        """
        Extract specific columns from the dataframe, rename the columns and return the extracted dataframe.
        Parameters:
        - dcols (list): A list of column indices that need to be extracted from the dataframe
        - std_col (list): A list of column indices that will be included in the extracted dataframe along with dcols
        """
        column_indices = list(std_cols) + list(columns)
        extracted_df = df.iloc[:, column_indices]
        extracted_df.columns = self.col_name
        return extracted_df


    def collapse_cols_representation(self, df):
        """
        Extract specific columns from the dataframe, concatenate them, extract digits from the concatenated column and return the processed dataframe.
        Parameters:
        - cols (list): A list of column names in the dataframe
        """
        cols = df.columns
        start_indices = [i for i, col in enumerate(cols) if 'Peer Name' in col]
        end_indices = [i for i, col in enumerate(cols) if 'Justification for Peer' in col]
        end_indices = [x + 1 for x in end_indices]
        columns_to_int = [range(start, end) for start, end in zip(start_indices, end_indices)]
        std_cols = range(0, start_indices[0])
        all_df = [self.extract_columns(df, dcols, std_cols) for dcols in columns_to_int]
        df = pd.concat(all_df).reset_index(drop=True)
        for element in self.elements_to_extract:
            df[element] = df[element].str.extract(r'(\d+)')
        return df

    def read_file_transform(self, finput=None):
        """
        Read input file, process the dataframe and return the processed dataframe
        Parameters:
        - finput (str): The file name of the excel file that needs to be processed.

            Note:
    - The input dataframe should have the columns: name, group_name, peer_name, peer_student_id, research_information_gathering, creative_input, coperation_within_group, communication, contribution_quality, meeting_attendance, justification.
    - If the input dataframe is less than 13 columns, it is assumed that it is in the correct format for further processing.


        """
        df = pd.read_excel(finput)
        # cols = df.columns.tolist()
        return self.collapse_cols_representation(df) if df.shape[1]> 13 else df

    def convert_percentage_weightage(self):
        """
        Normalize the values of specific columns in the dataframe using a given scale and return the processed dataframe.
        The function has been tested for scale 5 and 7 and by default, the lowest point "Terrible (0)" will not yield any grade.
        Parameters:
        - scale_type (int): The type of scale to be used (5 or 7)
        """
        constant_val=1
        self.df[N_ELEMENT] = self.df[N_ELEMENT] - constant_val
        if self.scale_type not in (5, 7):
            raise ValueError('Please input a valid scale type: 5 or 7, to avoid normalization error')
        revise_max_val = 6 if self.scale_type == 7 else 4
        # df = self.df
        cols = pd.Index(CONST_VAL.keys())
        mi = pd.MultiIndex.from_product([['percentage_trans'], cols])
        self.df[mi] = self.df[cols] * pd.Series(CONST_VAL) / revise_max_val


    def aggregate_each_peers(self):

        df = self.df.copy(deep=True)
        col_to_sum = list(product(['percentage_trans'], self.elements_to_extract))
        df[('sum_percentage_all_elements')] = df[col_to_sum].sum(axis=1)
        df['row_const'] = 1  # Use to calculate the number of group members

        # Assign back the student ID
        df = df.reset_index().rename(columns={'index': 'std_id', 'peer_name': 'std_name'})

        df['dgroup_name'] = df['group_name']
        df = df.set_index(['group_name', 'std_id'])

        df_stats = self.group_stat(df)

        self.cal_score = self.calculate_factor(df, df_stats)

    def group_stat(self, df):
        """
       This function groups the dataframe by a specific column, performs aggregation and renames the column.

       Parameters:
       - df (pandas dataframe): The dataframe that needs to be processed

       Returns:
       - pandas dataframe: The processed dataframe

       """
        df_stat = df.groupby(level=0).agg({'row_const': 'sum',
                                           'sum_percentage_all_elements': 'sum'}).reset_index().rename(
            columns={'index': 'group_name'})
        return df_stat

    def calculate_factor(self, df, df_stat):
        """
        This function maps values of one dataframe column to another dataframe column based on a condition.

        Parameters:
        - df (pandas dataframe): The dataframe that needs to be processed
        - df_stat (pandas dataframe): The dataframe that will be used as a reference for the mapping

        Returns:
        - pandas dataframe: The processed dataframe
        """
        df_stat = df_stat.set_index('group_name')
        df = df.merge(df_stat, left_on='dgroup_name', right_index=True, how='left')
        df['nmember'] = df['row_const_y']
        df['group_summation'] = df['sum_percentage_all_elements_y']
        df['weightage'] = df['sum_percentage_all_elements_x'] / df['sum_percentage_all_elements_y'] * df['nmember']
        df = df.drop(
            columns=['sum_percentage_all_elements_x', 'sum_percentage_all_elements_y', 'row_const_y', 'row_const_x'])
        return df

    def re_arrange_justification(self):

        """
     This function processes the dataframe by creating a new column 'feedback', modifying the 'justification' column,
     setting the index, and converting the specific column to integer.

     Parameters:
     - df (pandas dataframe): The dataframe that needs to be processed
     - n_element (str): The name of the column that needs to be converted to integer

     Returns:
     - pandas dataframe: The processed dataframe

     """
        # df=self.df
        # n_element = self.n_element
        self.df["feedback"] = self.df["name"].str.cat(self.df["justification"], sep="-->")
        self.df["justification"] = "'" + self.df["justification"].astype(str) + "'"
        self.df = self.df.set_index(["peer_student_id", "assessor_student_id"])
        self.df = self.df.sort_index(ascending=True)
        self.df.index = pd.MultiIndex.from_tuples(self.df.index.tolist())
        self.df[self.elements_to_extract] = self.df[self.elements_to_extract].astype(int)
        self.df["justification_annom"] = self.df["justification"].astype(str)

        # self.agg_df = self.df.groupby(level=0).agg(D_AGG_CALCULATION)
        self.df = self.df.groupby(level=0).agg(D_AGG_CALCULATION)
        # self.df=df
        # return self.df

    def check_missing_infomation(self):
        """
            TODO:

            This function checks for missing information in the dataframe, specifically the student ID and peer ID. If any
            missing values are found, they will be dropped from the dataframe. This function also raises a warning for
            this serious issue.

            Parameters:
            - df (pandas dataframe): The dataframe to be checked for missing information

            Returns:
            - df (pandas dataframe): The dataframe with missing information removed
            """
        self.df = self.df.dropna()
        return self.df

    def process_dataframe(self):
        """
        Read input file, process the dataframe and return the final processed dataframe.
        Parameters:
        - finput (str): The file name of the excel file that needs to be processed.
        - scale_type (int): The type of scale to be used (5 or 7)
        """

        self.check_missing_infomation()
        self.re_arrange_justification()
        self.convert_percentage_weightage()
        self.aggregate_each_peers()


def create_parser():
    # fexcel = r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_assessment.xlsx'
    parser = argparse.ArgumentParser(description='Process peer assessment data')
    parser.add_argument('finput', type=str,help='file name of the excel file to be processed')
    parser.add_argument('foutput', type=str, default='individual_score.xlsx',help='file name of the excel file to be processed')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='include additional information in the output file')
    parser.add_argument('-f', '--fname', type=str, default='result.xlsx', help='output file name')
    parser.add_argument('-s', '--scale_type', type=int, default=5, choices=[5, 7], help='scale type for normalization')
    return parser




if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    PE = PeerEvaluator(finput=args.finput, scale_type=args.scale_type)
    PE.process_dataframe()
    save_output_excel(PE.cal_score, fname='output.xlsx', verbose=False)
