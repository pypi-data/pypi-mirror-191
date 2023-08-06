"""C++ implementation of Ben-Haim / Tom-Tov centroid histograms.

A centroid histogram is a fixed-size histogram that consists of M (centroid, count) pairs
(i.e. buckets). Each pair represents a certain number of observations and is stored as an
average value and a count. When a new value is inserted into the histogram, it's added as
a (value, 1) bucket into the sorted list of pairs at the appropriate position based on its
value. If there are (M + 1) entries after the insert, then the closest pair of buckets
(based on their centroid values) is merged and replaced with a new one to keep the histogram
size unchaged.

A centroid histogram is used to get accurate estimates of the quantiles and counts of observed
values below a threshold.

The performance critical part of building histograms from a sequence of floating-point values
and merging buckets from existing histograms is implemented in C++ for the sake of efficiency.

See this paper for more details:

http://www.jmlr.org/papers/volume11/ben-haim10a/ben-haim10a.pdf

Examples of usage:

    >>> from drfaster.centroid_histogram import histogram_from_values
    >>> # build a histogram of size 5 from a list of floats
    >>> h = histogram_from_values(5, [1.0, 2.0, 4.0, 5.0, 3.0, 2.0, 7.0, 9.0, 8.0])
    >>> # instead of a list, one can pass an arbitrary iterable producing floating-point values
    >>> import random
    >>> h = histogram_from_values(5, (random.random() * 1000 for _ in range(1000)))
    >>> # NaN's and None's are filtered out
    >>> h = histogram_from_values(5, [1.0, None, 4.0, 5.0, float('nan'), 2.0, 7.0, 9.0, 8.0])

    >>> from drfaster.centroid_histogram import histogram_from_buckets
    >>> # histogram_from_buckets() can be used for merging buckets of existing histograms
    >>> import itertools
    >>> h1 = histogram_from_values(5, [1.0, 2.0, 4.0, 5.0, 3.0, 2.0, 7.0, 9.0, 8.0])
    >>> h2 = histogram_from_values(5, [7.0, 1.4, 2.9, 3.5, 7.8, 10.1, 2.0, 4.3, 2.1])
    >>> h = histogram_from_buckets(5, itertools.chain(h1.buckets, h2.buckets))
"""

__all__ = (
    'histogram_from_buckets',
    'histogram_from_values',
)


from drfaster.centroid_histogram.histogram_wrapper import (
    histogram_from_buckets,
    histogram_from_values,
)
