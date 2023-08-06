from libc.time cimport tm

cpdef inline int2time(long x, const char* fmt)
""""
Converts an integer (ordinal) representation into its corresponding time.
Converts to GMT timezone.

"""


cpdef inline fromordinal(long x)
"""
Convert from days from 1/1/1 to seconds from epoch
719163 is the number of days from 1/1/1 to epoch inclusive
86400 is the number of seconds in a day

"""


cpdef inline object utcfromtimestamp(double x)
"""Convert from seconds from epoch to datetime object"""


cpdef inline long totimestamp(dt)
"""
Parameters
----------
dt : datetime

Returns
-------
Seconds since 1/1/1 for dt
"""


cdef object tm_to_datetime(const tm& t, int microseconds=*)
"""Convert struct tm to datetime object"""


cdef inline tm* fromordinal_tm(long x, tm* t) nogil
"""
Convert from days from 1/1/1 to seconds from epoch
719163 is the number of days from 1/1/1 to epoch inclusive
86400 is the number of seconds in a day
"""


cdef inline tm* int2time_tm(long x, const char* fmt, tm* t) nogil
"""
Converts an integer (ordinal) representation into its corresponding time
represented by a C struct tm.

Converts to GMT timezone.
"""


cdef inline tm datetime_to_tm(object dt)
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
