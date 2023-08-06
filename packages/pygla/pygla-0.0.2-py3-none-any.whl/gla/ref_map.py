
LEN_COLS_MQUIZ=13

COLS_OPT = [
    ['std_name',
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
]

D_AGG_CALCULATION = {
    "peer_name": "first",
    "group_name": "first",
    "research_information_gathering": "mean",
    "creative_input": "mean",
    "cooperation_within_group": "mean",
    "communication": "mean",
    "contribution_quality": "mean",
    "meeting_attendance": "mean",
    "feedback": "\n".join,
    "justification_annom": "\n".join
}

REMAP_VALUES = {
    "Terrible (0)": "0",
    "Very Poor (1)": "1",
    "Poor (2)": "2",
    "Adequate (3)": "3",
    "Good (4)": "4",
    "Very Good (5)": "5",
    "Excellent (6)": "6"
}

COL_NAME = [
    "id", "start_time", "completion_time", "email", "name", "assessor_student_id", "group_name",
    "peer_name", "peer_student_id", "research_information_gathering", "creative_input",
    "cooperation_within_group", "communication", "contribution_quality", "meeting_attendance", "justification"
]

# ['id','start_time','completion_time','email','name','group_name','peer_name',
#  'peer_student_id','research_information_gathering','creative_input',
#  'cooperation_within_group','communication','contribution_quality',
#  'meeting_attendance','justification']

N_ELEMENT = [
    "research_information_gathering", "creative_input", "cooperation_within_group",
    "communication", "contribution_quality", "meeting_attendance"
]

CONST_VAL = {
    "research_information_gathering": 15,
    "creative_input": 20,
    "cooperation_within_group": 15,
    "communication": 15,
    "contribution_quality": 20,
    "meeting_attendance": 15
}