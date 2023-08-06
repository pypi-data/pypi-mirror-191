#!python
# cython: embedsignature=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False

from re import search, sub
from libc.string cimport strstr
from libc.time cimport tm

TZ_REGEXP = r'\s*[\+-][0-9]+$'

cpdef date2intWrapper(x, const char* fmt, bool skip_tz=False):
    if not skip_tz and strstr(fmt, '%M'):
        # This regex removes TZ information
        # example string: '2015-04-12T18:51:19-0500'
        temp = str(x)
        if search(TZ_REGEXP, temp):
            temp = sub(TZ_REGEXP, '', temp)

        return dateToInt(temp.encode(), fmt)

    else:
        return dateToInt(x.encode(), fmt)

cpdef date2intSafeWrapper(x, const char* fmt, bool skip_tz=False):
    if not skip_tz and strstr(fmt, '%M'):
        # This regex removes TZ information
        # example string: '2015-04-12T18:51:19-0500'
        temp = str(x)
        if search(TZ_REGEXP, temp):
            temp = sub(TZ_REGEXP, '', temp)

        return dateToIntSafe(temp.encode(), fmt)

    else:
        return dateToIntSafe(x.encode(), fmt)


cpdef object strptime(x, const char* fmt):
    cdef dr_tm tmb = strptime_c(x.encode(), fmt)
    return tm_to_datetime(<tm> tmb, tmb.tm_micro_sec)
