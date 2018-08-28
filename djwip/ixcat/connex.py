# connection extensions

def set_cfgvar(conn, var, val):
    q = 'set session {}={}'.format(var, val)
    return conn.query(q).fetchall()

def get_cfgvar(conn, var):
    q = "show variables like '{}'".format(var)
    return conn.query(q).fetchall()[0][1])

def set_slow_make(conn, howslow=600):
    set_cfgvar(conn, 'net_read_timeout', howslow)

