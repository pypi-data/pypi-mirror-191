#ifndef DATETOINT_H
#define DATETOINT_H

#include <cstring>
#include <stdexcept>
#include <ctime>
#include "strptime.h"


time_t const secondsPerDay = 86400;

void inline validate_strptime(const char* result, const dr_tm* tmb, const char* fmt);


time_t inline dateToInt(const char* date, const char* fmt) {
	struct dr_tm tmb = {};
	tmb.tm_sec = 0;
	tmb.tm_min = 0;
	tmb.tm_hour = 0;
	tmb.tm_mday = 1;
	tmb.tm_mon = 0;
	tmb.tm_year = 0;
	tmb.tm_wday = 0;
	tmb.tm_isdst = 0;
	tmb.tm_micro_sec = 0;

    bool use_v2 = false;

    if (strncmp(fmt, "v2", 2) == 0) {
        use_v2 = true;
        fmt += 2;
    }

    const char* result = myStrptime(date, fmt, &tmb);
    validate_strptime(result, &tmb, fmt);

	time_t sec = timegm(&tmb);

    if (use_v2 && strstr(fmt, "%f"))
        return sec * 1000 + tmb.tm_micro_sec / 1000;
    else if (strstr(fmt, "%M"))
        // return the UNIX time
		return sec;
	else if (sec < 0 && sec % secondsPerDay != 0)
	    // ordinal with nonzero hours
	    return sec / secondsPerDay + 719162;
    else
        // return days after january 1 year 1
		return sec / secondsPerDay + 719163;
}

time_t inline dateToIntSafe(const char* date, const char* fmt) {
	struct dr_tm tmb = {};
	tmb.tm_sec = 0;
	tmb.tm_min = 0;
	tmb.tm_hour = 0;
	tmb.tm_mday = 1;
	tmb.tm_mon = 0;
	tmb.tm_year = 0;
	tmb.tm_wday = 0;
	tmb.tm_isdst = 0;
	tmb.tm_micro_sec = 0;

    bool use_v2 = false;

    if (strncmp(fmt, "v2", 2) == 0) {
        use_v2 = true;
        fmt += 2;
    }

    const char* result = myStrptime(date, fmt, &tmb);
    if (!result || strlen(result) > 0) return -1.0;
    if (tmb.tm_year < 1 - TM_YEAR_BASE && strstr(fmt, "%Y")) return -1.0;

    time_t sec = timegm(&tmb);

    if (use_v2 && strstr(fmt, "%f"))
        return sec * 1000 + tmb.tm_micro_sec / 1000;
    else if (strstr(fmt, "%M"))
        // return the UNIX time
		return sec;
	else if (sec < 0 && sec % secondsPerDay != 0)
	    // ordinal with nonzero hours
	    return sec / secondsPerDay + 719162;
    else
        // return days after january 1 year 1
		return sec / secondsPerDay + 719163;
}

dr_tm inline strptime_c(const char* date, const char* fmt) {
	struct dr_tm tmb = {};
	tmb.tm_sec = 0;
	tmb.tm_min = 0;
	tmb.tm_hour = 0;
	tmb.tm_mday = 1;
	tmb.tm_mon = 0;
	tmb.tm_year = 0;
	tmb.tm_wday = 0;
	tmb.tm_isdst = 0;
	tmb.tm_micro_sec = 0;

	const char* result = myStrptime(date, fmt, &tmb);
	validate_strptime(result, &tmb, fmt);
	return tmb;
}

void inline validate_strptime(const char* result, const dr_tm* tmb, const char* fmt) {
    if (!result || strlen(result) > 0)
		// if strptime fails
		throw std::invalid_argument("failed to read date from fmt");
	if (tmb->tm_year < 1 - TM_YEAR_BASE && strstr(fmt, "%Y"))
	    throw std::invalid_argument("year is out of range");
}

#endif
