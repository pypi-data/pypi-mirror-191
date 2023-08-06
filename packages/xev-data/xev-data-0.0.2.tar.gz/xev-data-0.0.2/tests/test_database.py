#!/usr/env/bin python3
######## Globals ########
TESTDATA = "test_database.hdf5"
TESTALIAS = "test_alias.hdf5"
TESTGROUP1 = "test_group1"
TESTGROUP2 = "test_group2"
TESTGROUP3 = "test_group3"
TESTDATA_NAME1 = "test1"
TESTDATA_NAME2 = "test2"
TESTDATA_NAME3 = "test3"
TESTDATA_NAME4 = "test4"
TESTDATA_NAME5 = "test5"

######## Imports ########
from xdata import Database
import numpy as np

######## Functions ########

def test_group():
    # Create a new database
    db = Database(TESTDATA)
    # test list_items when no items are present
    items = db.list_items()
    # Assert database is empty
    assert len(items) == 0
    # Create some groups
    db.create_group(TESTGROUP1)
    db.create_group(TESTGROUP2)
    db.create_group(TESTGROUP3)
    db.dset_set(TESTDATA_NAME1, np.arange(10))
    db.dset_set(TESTGROUP1 + "/" +  TESTDATA_NAME2, np.arange(11))

    #### List tests ####
    # List items again
    items = db.list_items()
    assert (len(items) == 4)
    # List only groups
    groups = db.list_items(kind="group")
    assert(len(groups) == 3)
    # List only dsets
    dsets = db.list_items(kind="dset")
    assert(len(dsets) == 1)
    # List items in group
    groupitems = db.list_items(path=TESTGROUP1)
    assert(len(groupitems) == 1)

    #### Group tests ####
    # Initialize fresh database object pointing at a group
    db = Database(TESTDATA, group=TESTGROUP1)
    # List items in that group
    groupitems = db.list_items()
    assert(len(groupitems) == 1)
    # Global path
    assert(len(db.list_items(path="/" +TESTGROUP1)) == 1)
    # Change group
    db.change_group(group='/')
    # Assert items again
    items = db.list_items()
    assert (len(items) == 4)
    # Change back
    db.change_group(TESTGROUP1)
    # Assert groupitems again
    groupitems = db.list_items()
    assert(len(groupitems) == 1)

def test_kind():
    db = Database(TESTDATA)
    assert(db.kind(TESTGROUP1) == "group")
    assert(db.kind(TESTDATA_NAME1) == "dset")

def test_exists():
    db = Database(TESTDATA)
    assert db.exists(TESTDATA_NAME1)
    assert not (db.exists("A pink elephant"))

def test_visit():
    db = Database(TESTDATA)
    print("Visiting with print")
    db.visit()

def test_scan():
    db = Database(TESTDATA)
    db.scan()

def test_dset():
    db = Database(TESTDATA)
    data = np.eye(10)
    dtype = data.dtype
    shape = data.shape
    size = data.size
    db.dset_init(TESTDATA_NAME3, shape, dtype)
    db.dset_set(TESTDATA_NAME3, data)
    assert db.dset_size(TESTDATA_NAME3) == size
    assert db.dset_compression(TESTDATA_NAME3) == None
    assert db.dset_shape(TESTDATA_NAME3) == shape
    assert db.dset_dtype(TESTDATA_NAME3) == dtype
    assert np.allclose(db.dset_value(TESTDATA_NAME3), data)
    assert db.dset_sum(TESTDATA_NAME3) == np.sum(data)
    assert db.dset_min(TESTDATA_NAME3) == np.min(data)
    assert db.dset_max(TESTDATA_NAME3) == np.max(data)
    db.dset_set(TESTDATA_NAME4, data, compression="gzip")
    assert db.dset_compression(TESTDATA_NAME4) == "gzip"
    return

def test_attrs():
    db = Database(TESTDATA)
    assert db.attr_exists(TESTDATA_NAME3, "min")
    assert db.attr_exists(TESTDATA_NAME3, "max")
    assert db.attr_exists(TESTDATA_NAME3, "sum")
    attr_list = db.attr_list(TESTDATA_NAME3)
    assert "min" in attr_list
    assert "max" in attr_list
    assert "sum" in attr_list
    attr_dict = db.attr_dict(TESTDATA_NAME3)
    for item in attr_list:
        assert not(attr_dict[item] is None)
    db.attr_set_dict(TESTDATA_NAME4, attr_dict)
    attr_dict = db.attr_dict(TESTDATA_NAME4)
    for item in attr_list:
        assert not(attr_dict[item] is None)
    return 

def test_fields():
    return

def test_shard():
    return

def test_merge():
    return

def test_rm():
    return

def test_copy():
    return

def test_recompress():
    return


######## Main ########
def main():
    # Working tests
    test_group()
    test_kind()
    test_exists()
    test_dset()
    test_attrs()
    # Tests yet to be implemented
    test_fields()
    test_shard()
    test_merge()
    test_rm()
    test_copy()
    test_recompress()
    #test_visit()
    #test_scan()
    return

######## Execution ########
if __name__ == "__main__":
    main()
