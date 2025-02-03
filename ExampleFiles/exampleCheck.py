import pandas as pd
import os


SumPromFolder1 = '/Users/divyakr/PythonCourseByGabor/project/ExampleFiles/SumPromRepeats' ## Path to your new SumPromRepeats Folder
SumPromFolder2 =  '/Users/divyakr/PythonCourseByGabor/project/SumPromRepeats' ## Path to my example SumPromRepeats Folder

files = sorted(os.listdir(SumPromFolder1))  
for f in files:
    file1 = os.path.join(SumPromFolder1, f)
    file2 = os.path.join(SumPromFolder2, f)

    df1 = pd.read_pickle(file1, compression="gzip")
    df2 = pd.read_pickle(file2, compression="gzip")

    if df1.equals(df2):
        print(f"{f}: Data is identical")
    else:
        print(f"{f}: Data is different")