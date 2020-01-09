
import os
import pandas as pd
import logging
from configparser import ConfigParser
from pathlib import Path



# reads config file            
parser = ConfigParser()
try:
    parser.read(Path('dev.ini'))
except:
    print('File not Found')
else:
    folderName = parser.get('settings', 'root_file_location')
    log_file = parser.get('settings', 'log_file_location')


# creats logger    
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
LOG_FORMAT =logging.Formatter('%(name)s %(levelname)s %(asctime)s - %(message)s')
file_handler = logging.FileHandler(log_file, mode='w' )
file_handler.setFormatter(LOG_FORMAT)
logger.addHandler(file_handler)



# main function for searching .txt files
def getFiles(folderName):
    
    logger.info('create a list of directories and file in {0}'.format(folderName))
    
    # create a list of file and sub-folders 
    file_list = os.listdir(folderName)
    
    # create a dictionary to save file path and name
    file_names = {'path':[], 'name':[]}
    
    # Iterate over the list of files and folders
    for file_name in file_list:
        # Create full path
        fullPath = os.path.join(folderName, file_name)
        
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            file_names['path'] = file_names['path'] + getFiles(fullPath)['path']
            file_names['name'] = file_names['name'] + getFiles(fullPath)['name']
            
        # save the path if it is a .txt file
        elif file_name[-4:]=='.txt':
            file_names['path'].append(fullPath)
            file_names['name'].append(file_name)
                
    return file_names




# counts number of characters in each text file as the length of the file
def character_count(file_name):
    with open(file_name, 'r') as f:
        lines=0
        words=0
        characters=0
        for line in f:
            wordslist=line.split()
            lines=lines+1
            words=words+len(wordslist)
            characters += sum(len(word) for word in wordslist)
    return characters



dict_ = getFiles(folderName)
logger.info('Total number of {} files were detected'.format(len(dict_['path'])))


# adds 'date' and 'length' for each file
dict_['date'] = []
dict_['length'] = []
for i in range(len(dict_['path'])):
    dict_['length'].append(character_count(dict_['path'][i]))
    dict_['date'].append(os.path.getctime(dict_['path'][i])) 


# makes a dataframe in pandas
df = pd.DataFrame(dict_)
df['date'] = pd.to_datetime(df['date'], unit='s')

# sorts by names and date ascending and descending accordingly
df = df.sort_values(by=['name', 'date'], ascending=(True, False) )

# removes duplicate names and keep the last modified one
df = df.drop_duplicates(subset='name', keep='first')

# writes to a .csv file
out = df.to_csv(Path(os.path.abspath('export_to_csv.csv')), index=False)

# closes file logger
file_handler.close()

print('The output was saved on {}'.format(Path(os.path.abspath('export_to_csv.csv'))))
