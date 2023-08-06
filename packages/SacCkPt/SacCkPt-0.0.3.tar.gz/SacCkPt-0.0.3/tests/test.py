import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "SacCkPt"))

from checkpoint import Checkpoint

def test_save_checkpoint_data_with_file():
    check = Checkpoint('file',file_path='C:/Users/user/Desktop/sacumen_trail/check1.env')
    assert  check.storage_medium == 'file'

def test_save_checkpoint_data_with_database():
    check = Checkpoint('database')
    assert  check.storage_medium=='database'

def test_save_checkpoint_data_with_filepath():
    check = Checkpoint('file',file_path='C:/Users/user/Desktop/sacumen_trail/check1.env')
    save = check.save_checkpoint_data(56)
    assert check.file_path




