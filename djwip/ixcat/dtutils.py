'''
Utiltities for working with datetime values in SQL
'''


from datetime import datetime


def dt_slice(dt):
    ''' slice a datetime at second-level granularity '''
    return dt.timetuple()[:6]  # timestamp is granular to per-second level


def dt_trunc(dt):
    ''' trunctate a datetime to second-level granularity '''
    return datetime(*dt_slice(dt))


def dt_tostr(dt):
    ''' format a datetime to SQL query format '''
    return dt.strftime("'%Y-%m-%d %H:%M:%S'")


def dt_fromstr(s):
    ''' parse a SQL date string to a datetime '''
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def before(field, dt):
    ''' create a SQL 'before' clause for 'field' and 'dt' '''
    return str().join((field, ' < ', dt_tostr(dt_trunc(dt))))


def after(field, dt):
    ''' create a SQL 'after' clause for 'field' and 'dt' '''
    return str().join((field, ' > ', dt_tostr(dt_trunc(dt))))


def between(field, dtstart, dtend):
    ''' create a SQL 'between' clause for 'field' and 'dtstart'/'dtend' '''
    return str().join((field, ' between ', dt_tostr(dt_trunc(dtstart)),
                       ' and ', dt_tostr(dt_trunc(dtend))))


__all__ = [dt_slice, dt_trunc, dt_tostr, dt_fromstr, before, after, between]
