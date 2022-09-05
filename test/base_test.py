from os import path
def test_database():
    if not  path.exists("georgiaflow/api" + 'ufp.db'):
       
        assert("Created database failure")

