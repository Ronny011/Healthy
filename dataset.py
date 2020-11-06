import pandas as pd
import pandasql as ps
import numpy as np
import os

# initializing dataframes
dataset = pd.DataFrame()
# directory path for scanning
path = 'dataset'
# user index and counter
i = 0
j = 22  # for console purposes
# recursively scanning the path top-down
for root, dirs, files in os.walk(path):
    # initializing temporary dataframes
    tempUserDF = pd.DataFrame()
    tempActivDF = pd.DataFrame()
    tempGraphDF = pd.DataFrame()

    # file array
    for file in files:
        # a full directory path is needed
        directory = os.path.join(root, file)
        # index assignment - by directory numbering
        i = str(root)[13:]

        # activity file
        if directory.endswith('Activity.csv'):
            tempActivDF = pd.read_csv(directory)
            tempActivDF['Unnamed: 0'] = i

        # info file
        elif directory.endswith('user_info.csv'):
            # temporary dataframe from a specific user
            tempUserDF = pd.read_csv(directory)
            # setting index to dataframe
            tempUserDF['Unnamed: 0'] = i

        elif directory.endswith('Actigraph.csv'):
            tempGraphDF = pd.read_csv(directory)
            # dropping unneeded columns
            tempGraphDF.drop(columns=['Axis1', 'Axis2', 'Axis3', 'Vector Magnitude'], inplace=True)
            # column reduction
            # first we add the new column - Inc for all inclinometer values
            tempGraphDF.insert(2, 'Inc', -1)

            # setting the conditions - if that column has 1 or 0...
            conditions = [tempGraphDF['Inclinometer Off'] == 1,
                          (tempGraphDF['Inclinometer Lying'] == 1),
                          (tempGraphDF['Inclinometer Sitting'] == 1),
                          (tempGraphDF['Inclinometer Standing'] == 1)]
            # ...then insert a corresponding indicator
            choices = ['0', '1', '2', '3']  # off, lying, sitting, standing
            tempGraphDF['Inc'] = np.select(conditions, choices, default=np.nan)

            # we can now drop the old columns
            tempGraphDF.drop(columns=['Inclinometer Off', 'Inclinometer Lying',
                                      'Inclinometer Sitting', 'Inclinometer Standing'], inplace=True)
            # adding the average daily steps - if the entire table has only 1 day
            tempGraphDF.insert(1, 'ADS', tempGraphDF['Steps'].sum())
            tempGraphDF.drop(columns=['Steps'], inplace=True)
            # filtering outliers and empty hr
            tempGraphDF = tempGraphDF[(tempGraphDF.HR >= 49) & (tempGraphDF.HR <= 200) & (tempGraphDF.HR != np.nan)]
            tempGraphDF['Unnamed: 0'] = i

            # if the dataframes are not empty
        if (len(tempUserDF) != 0) & (len(tempActivDF) != 0):
            # merging the activity and user info dataframes
            tempUsrActv = tempActivDF.merge(tempUserDF, 'right', 'Unnamed: 0')

            if len(tempGraphDF) != 0:
                # query to join all dataframes
                sqlcode = '''
                select *
                from tempGraphDF
                join tempUsrActv
                on tempGraphDF.day = tempUsrActv.Day
                and tempGraphDF.time between tempUsrActv.Start and tempUsrActv.End
                '''
                # implementing the query
                finalDF = ps.sqldf(sqlcode, locals())

                conditions = [(finalDF.time >= '05:00') & (finalDF.time < '11:00'),
                              ((finalDF.time >= '11:00') & (finalDF.time < '15:00')),
                              ((finalDF.time >= '15:00') & (finalDF.time < '22:00')),
                              ((finalDF.time >= '22:00') & (finalDF.time <= '23:59')),
                              (finalDF.time < '05:00')]
                choices = ['1', '2', '3', '0', '0']
                finalDF['time'] = np.select(conditions, choices, default=np.nan)

                cols = [4, 6, 8, 9, 10]
                finalDF.drop(finalDF.columns[cols], axis=1, inplace=True)
                # the ID column is deleted twice, let's retrieve it
                finalDF.insert(0, 'ID', i)
                finalDF.rename({'time': 'TOD'})
                print('user', i, 'dataframe generated')
                dataset = pd.concat([dataset, finalDF])
                j -= 1
                print('')
                print('Added to main dataframe')
                print('')
                print(j, 'users left')

print('')
print('Exporting...')
dataset.to_csv("Dataset.csv")
print('')
print('Done!')

