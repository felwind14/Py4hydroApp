from pcraster import * 

def col2map(x,y,id,datatype,clone):
    """Function to place a point selected manually QGIS and construct the location map

    Args:
        x (_type_): _description_
        y (_type_): _description_
        id (_type_): _description_
        datatype (_type_): _description_
        clone (_type_): _description_

    Returns:
        _type_: _description_
    """    
    with open('data/flocation.txt', 'w') as f:
        f.write(str(x) + ' ' + str(y) + ' ' + str(id))
    cmd = 'col2map -{0} data/flocation.txt data/flocation.map --clone {1}'.format(datatype,clone)
    print(cmd)
    os.system(cmd)
    Map = readmap('data/flocation.map')
    return Map

def main():
    print(os.getcwd())
    x = 288880.648
    y = 5675880.258
    id = 1
    datatype = 'N'
    clone = 'data/fstream8.map'
    aguila(clone)

    Outlet = col2map(x,y,id,datatype,clone)
    aguila(Outlet)

if __name__== "__main__":
    main()