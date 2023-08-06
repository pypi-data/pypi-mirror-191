from libcpp cimport bool
from ..intToTime.int2time_wrapper cimport tm_to_datetime

cdef extern from '../dateToInt/strptime.h' nogil:
    cdef struct dr_tm:
        int  tm_micro_sec
        int  tm_sec
        int  tm_min
        int  tm_hour
        int  tm_mday
        int  tm_mon
        int  tm_year
        int  tm_wday
        int  tm_yday
        int  tm_isdst
        char *tm_zone
        long tm_gmtoff

cdef extern from "PosixFctns.hpp" nogil:
    long dateToInt(const char* date, const char* fmt) except +ValueError
    long dateToIntSafe(const char* date, const char* fmt)
    dr_tm strptime_c(const char* date, const char* fmt) except +ValueError

cpdef date2intWrapper(x, const char* fmt, bool skip_tz=*)
cpdef date2intSafeWrapper(x, const char* fmt, bool skip_tz=*)
cpdef object strptime(x, const char* fmt)
