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

j = 22  # for console purposes - number of volunteers/users
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

            # average daily steps, as we only have one day's observations we only need to sum. division used for scale
            tempGraphDF.insert(1, 'ADS', tempGraphDF['Steps'].sum()/1000)
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
                # renaming activities
                conditions = [finalDF['Activity'] == 0, finalDF['Activity'] == 1, finalDF['Activity'] == 2,
                              finalDF['Activity'] == 3, finalDF['Activity'] == 4, finalDF['Activity'] == 5,
                              finalDF['Activity'] == 6, finalDF['Activity'] == 7, finalDF['Activity'] == 8,
                              finalDF['Activity'] == 9, finalDF['Activity'] == 10, finalDF['Activity'] == 11,
                              finalDF['Activity'] == 12]
                choices = ['sleeping', 'sleeping', 'laying', 'sitting', 'm-light', 'm-medium', 'm-heavy', 'eating',
                           'su-small', 'su-large', 'caffeine', 'smoking', 'alcohol']
                finalDF['Activity'] = np.select(conditions, choices, default=np.nan)
                # classifying time ranges
                conditions = [(finalDF.time >= '05:00') & (finalDF.time < '11:00'),
                              ((finalDF.time >= '11:00') & (finalDF.time < '15:00')),
                              ((finalDF.time >= '15:00') & (finalDF.time < '22:00')),
                              ((finalDF.time >= '22:00') & (finalDF.time <= '23:59')),
                              (finalDF.time < '05:00')]
                choices = ['Morning', 'Noon', 'Evening', 'Night', 'Night']
                finalDF['time'] = np.select(conditions, choices, default=np.nan)
                # reducing inclinometer columns - off is nan so that it is ignored by the model
                finalDF.insert(4, 'Inc', np.nan)
                conditions = [finalDF['Inclinometer Off'] == 1, finalDF['Inclinometer Lying'] == 1,
                              finalDF['Inclinometer Sitting'] == 1, finalDF['Inclinometer Standing'] == 1]
                choices = [np.nan, 'Lying', 'Sitting', 'Standing']
                finalDF['Inc'] = np.select(conditions, choices, default=np.nan)
                # columns to delete
                cols = ['Unnamed: 0', 'Start', 'End', 'Gender', 'day', 'Inclinometer Off', 'Inclinometer Standing',
                        'Inclinometer Sitting', 'Inclinometer Lying', 'Day']
                finalDF.drop(finalDF[cols], axis=1, inplace=True)
                # the ID column is deleted twice, let's retrieve it and set it as dataframe index
                finalDF.insert(0, 'ID', i)
                finalDF.set_index('ID', inplace=True)
                finalDF.rename(columns={'time': 'TOD'}, errors="raise", inplace=True)
                finalDF.drop_duplicates(inplace=True)
                #  dataframe rearrangement
                print(finalDF)
                finalDF = finalDF[['Age', 'Height', 'Weight', 'ADS', 'Activity', 'Inc', 'TOD', 'HR']]
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
