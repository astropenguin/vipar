# coding: utf-8

def append(db, newdata, N_max=10):
    '''append a new data to a database.

    Parameters
    ----------
    + db (dict): a vipar's database.
    + newdata (array): a new data to be appended to the database
    + N_max: maximum number of data that can be stored in the database.

    Returns
    ----------
    + None (NoneType): this function returns nothing.
    '''
    indices = [i for i in db.keys() if type(i)==int]
    N_data = len(indices)

    if N_data == 0:
        pass

    elif 0 < N_data < N_max:
        for i in range(N_data)[::-1]:
            db[i+1] = db.pop(i)

    else:
        for i in range(N_data-1)[::-1]:
            db[i+1] = db.pop(i)

    db[0] = newdata


def undo(db):
    '''rewind a database to the previous state.

    Parameters
    ----------
    + db (dict): a vipar's database.

    Returns
    ----------
    + None (NoneType): this function returns nothing.
    '''
    indices = [i for i in db.keys() if type(i)==int]
    N_data = len(indices)

    for i in range(N_data-1):
        db[i] = db.pop(i+1)


def record(db, newdata, label=None):
    '''append a new labeled data to a database.

    Parameters
    ----------
    + db (dict): a vipar's database.
    + newdata (array): a new data to be appended to the database
    + label (str): a label of the new data. if not spacified,
      string of current datetime (YYYYmmddHHMMSS) will be set.

    Returns
    ----------
    + None (NoneType): this function returns nothing.
    '''
    if label is None:
        label = datetime.now().strftime('%Y%m%d%H%M%S')

    assert type(label) == str
    db[label] = newdata
