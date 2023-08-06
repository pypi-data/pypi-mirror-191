from libcpp.vector cimport vector


cdef extern from "histogram.hpp" nogil:
    cdef cppclass Bucket:
        Bucket(double, size_t)
        double centroid() const
        size_t count() const

    cdef cppclass Histogram:
        Histogram(size_t) except +ValueError
        void push(double)
        void push(const Bucket&)
        const vector[Bucket]& buckets() const
        size_t size() const


cpdef object histogram_from_values(size_t max_size, values)
cpdef object histogram_from_buckets(size_t max_size, buckets)
