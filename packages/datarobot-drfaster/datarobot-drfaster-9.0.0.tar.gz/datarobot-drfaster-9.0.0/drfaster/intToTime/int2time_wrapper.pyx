#!python
# cython: embedsignature=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
from collections import namedtuple

from libcpp cimport bool
from libc.time cimport gmtime, tm, time_t
from libc.string cimport strstr, strncmp
from cpython.datetime cimport (datetime_new, import_datetime, datetime_year,
                               datetime_month, datetime_day, datetime_hour,
                               datetime_minute, datetime_second)
from cython.operator cimport dereference as deref

cdef extern from "<time.h>" nogil:
    long timegm(tm *tm)

    tm *gmtime_r(const time_t *, tm *)


import_datetime()


struct_time = namedtuple('struct_time', ['tm_year', 'tm_mon', 'tm_mday',
                                         'tm_hour', 'tm_min', 'tm_sec',
                                         'tm_wday', 'tm_yday', 'tm_isdst',
                                         'tm_milli_sec'])


cpdef inline object int2time(long x, const char* fmt):
    """
    Converts an integer (ordinal) representation into its corresponding time.
    Converts to GMT timezone.
    """
    cdef tm t
    cdef tm *ptr
    cdef int millis = 0
    cdef bool use_v2 = False

    if strncmp(fmt, 'v2', 2) == 0:
        fmt += 2
        use_v2 = True

    if use_v2 and strstr(fmt, '%f'):
        ptr = int2time_tm(x / 1000, fmt, &t)
        millis = x % 1000
    else:
        ptr = int2time_tm(x, fmt, &t)

    if ptr == NULL:
        raise ValueError('gmtime failed due to invalid input')

    return struct_time(deref(ptr).tm_year + 1900,
                       deref(ptr).tm_mon + 1,
                       deref(ptr).tm_mday,
                       deref(ptr).tm_hour,
                       deref(ptr).tm_min,
                       deref(ptr).tm_sec,
                       (deref(ptr).tm_wday + 6) % 7,
                       deref(ptr).tm_yday + 1,
                       deref(ptr).tm_isdst,
                       millis)


cpdef inline object fromordinal(long x):
    """
    Convert from days from 1/1/1 to seconds from epoch
    3652059 is datetime.date.max.toordinal()
    """
    if x < 1:
        raise ValueError('ordinal must be >= 1')
    cdef tm t
    cdef tm *ptr
    ptr = fromordinal_tm(x, &t)
    if ptr == NULL:
        raise ValueError('gmtime failed due to invalid input')
    return tm_to_datetime(deref(ptr))


cpdef inline object utcfromtimestamp(double x):
    """Convert from seconds from epoch to datetime object"""
    cdef long seconds = <long> x
    cdef int microseconds
    if x > 0:
        microseconds = <int> (((x - seconds) * 1e6) + 0.5)  # 1e6 microseconds in second
    else:
        microseconds = <int> (((x - seconds) * 1e6) - 0.5)
        if microseconds != 0:
            seconds -= 1
            microseconds += 1000000
    if microseconds > 999999:
        microseconds = 999999
    cdef tm t
    cdef tm *ptr
    ptr = gmtime_r(&seconds, &t)
    if ptr == NULL:
        raise ValueError('gmtime failed due to invalid input')
    return tm_to_datetime(deref(ptr), microseconds)


cpdef inline long totimestamp(object dt):
    """
    Parameters
    ----------
    dt : datetime
    
    Returns
    -------
    Seconds since 1/1/1 for dt
    """
    cdef tm t = datetime_to_tm(dt)
    return timegm(&t)


cdef object tm_to_datetime(const tm& t, int microseconds = 0):
    """Convert struct tm to datetime object"""
    return datetime_new(t.tm_year + 1900,
                        t.tm_mon + 1,
                        t.tm_mday,
                        t.tm_hour,
                        t.tm_min,
                        t.tm_sec,
                        microseconds,
                        None)  # tzinfo


cdef inline tm* fromordinal_tm(long x, tm*t) nogil:
    """
    Convert from days from 1/1/1 to seconds from epoch
    719163 is the number of days from 1/1/1 to epoch inclusive
    86400 is the number of seconds in a day
    """
    x = (x - 719163) * 86400
    return gmtime_r(&x, t)


cdef inline tm* int2time_tm(long x, const char* fmt, tm*t) nogil:
    """
    Converts an integer (ordinal) representation into its corresponding time
    represented by a C struct tm.
    
    Converts to GMT timezone.
    """
    if strstr(fmt, '%M'):
        return gmtime_r(&x, t)
    else:
        return fromordinal_tm(x, t)


cdef inline tm datetime_to_tm(object dt):
    """
    Note that this returns the C struct tm, not the dr_tm
    However, this is not a problem if we are not dealing with milliseconds
    
    Parameters
    ----------
    dt : datetime
    
    Returns
    -------
    Struct tm for dt
    """
    cdef tm t
    t.tm_year = datetime_year(dt) - 1900
    t.tm_mon = datetime_month(dt) - 1
    t.tm_mday = datetime_day(dt)
    t.tm_hour = datetime_hour(dt)
    t.tm_min = datetime_minute(dt)
    t.tm_sec = datetime_second(dt)
    return t
