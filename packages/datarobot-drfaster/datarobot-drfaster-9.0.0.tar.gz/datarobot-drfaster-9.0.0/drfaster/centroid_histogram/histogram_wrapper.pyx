import collections
from math import isnan

from cython.operator cimport dereference as deref


CentroidBucket = collections.namedtuple('CentroidBucket', ['centroid', 'count'])
CentroidHistogram = collections.namedtuple('CentroidHistogram', ['max_size', 'buckets'])


cpdef object histogram_from_values(size_t max_size, values):
    """Build a centroid histogram of a given size from an iterable of floating-point values."""

    # cython requires dynamic allocation for classes without a "default" constructor, and it does
    # not make sense to create a Histogram instance here without specifying the max_size value, so
    # dynamic allocation it is
    cdef:
        Histogram* h
        const vector[Bucket]* buckets
        size_t i
    h = new Histogram(max_size)
    try:
        for v in values:
            if v is not None and not isnan(v):
                # an explicit cast to float allows us to process both ints and floats
                # (and also allows Cython to figure out which of two overloaded methods to call)
                h.push(float(v))

        buckets = &h.buckets()
        return CentroidHistogram(
            max_size,
            [CentroidBucket(deref(buckets)[i].centroid(), deref(buckets)[i].count())
             for i in range(buckets.size())]
        )
    finally:
        del h


cpdef object histogram_from_buckets(size_t max_size, buckets):
    """Build a centroid histogram of a given size from an iterable of (centroid, count) pairs."""

    # cython requires dynamic allocation for classes without a "default" constructor, and it does
    # not make sense to create a Histogram instance here without specifying the max_size value, so
    # dynamic allocation it is
    cdef:
        Histogram* h
        const vector[Bucket]* new_buckets
        size_t i
    h = new Histogram(max_size)
    try:
        for b in buckets:
            h.push(Bucket(b[0], b[1]))

        new_buckets = &h.buckets()
        return CentroidHistogram(
            max_size,
            [CentroidBucket(deref(new_buckets)[i].centroid(), deref(new_buckets)[i].count())
             for i in range(new_buckets.size())]
        )
    finally:
        del h
