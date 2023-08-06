# sac_httpadaptor_kd
Python based Checkpoint.

## Project description

This python package provides a checkpoint class which allow you to save and load the state of your streaming data as a checkpoint.



## Installation

Using Python package manager you can install this module by using below command:

pip install CkPt

```bash
  pip install CkPt
```
    
## Usage/Examples

Class Checkpoint takes number of arguments as shown below. If not provided keep it blank.


User must provide anyone storage_medium at a time amongst file or database without fail:
1) If user wants to store the checkpoint data in the file, he has to provide the storage medium as file along with file path and include file storage type like
a. JSON (*.json)
b. Text (*.txt)
c. Environment (.env)
for referrence:
check = Checkpoint('file',file_path='C:/Users/user/Desktop/check1.txt')
or 
check2 = Checkpoint('file',file_path='C:/Users/user/Desktop/check2.json')
or
check3 = Checkpoint('file',file_path='C:/Users/user/Desktop/check3.env')

2) If user wants to store the checkpoint data in the database then user must specify the storage medium as "database" along with the dbconnection
for referrence:
check = Checkpoint('database',db_conn='C:/Users/user/Desktop/check1.db')



#imports
from CkPt.checkpoint import Checkpoint

obj = Checkpoint('storage_medium' , filepath="", db_conn="")


result = obj.save_checkpoint_data(checkpoint_data)
result = obj.get_last_checkpoint()

