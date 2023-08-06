#ifndef HISTOGRAM_HPP
#define HISTOGRAM_HPP

#include <algorithm>
#include <tuple>
#include <vector>


class Bucket {
    public:
        Bucket(double centroid, size_t count)
            : _count(count)
            , _centroid(centroid)
        {}

        Bucket(const Bucket& lhs, const Bucket& rhs)
            : _count(lhs._count + rhs._count)
            , _centroid((lhs._count * lhs._centroid + rhs._count * rhs._centroid) / _count)
        {}

        bool operator<(const Bucket& other) const {
            return std::tie(this->_centroid, this->_count) < std::tie(other._centroid, other._count);
        }

        double centroid() const {
            return this->_centroid;
        }

        size_t count() const {
            return this->_count;
        }

    private:
        size_t _count;
        double _centroid;
};


class Histogram {
    public:
        // create a new fixed-size histogram
        Histogram(size_t max_size) : _max_size(max_size) {
            if (max_size < 1) {
                throw std::length_error("histogram size must be >= 1");
            }

            // reserve enough slots in the vector, so that inserts do not cause memory reallocations
            // (there can be at most (max_size + 1) buckets in the vector at a time; after that
            // the algorithm finds and merges two closest buckets to keep the histogram size fixed)
            this->_buckets.reserve(max_size + 1);
        }

        // return the size of the histogram
        size_t size() const {
            return _max_size;
        }

        // return the vector of histogram buckets. Note, that constant reference is returned, so
        // that it's not possible to modify this vector directly. push() must be used instead
        const std::vector<Bucket>& buckets() const {
            return this->_buckets;
        }

        // add a new bucket to the histogram
        void push(const Bucket& bucket) {
            // buckets are stored in the sorted order, that allows us to use the binary search
            // algorithm to determine the position, where a new bucket should go
            auto position = std::upper_bound(this->_buckets.begin(), this->_buckets.end(), bucket);
            // insertion to an arbitrary position in the buckets vector is O(M) (where M is the
            // maximum size of the histogram), but M is a constant that is fixed at histogram
            // creation time
            this->_buckets.insert(position, bucket);

            // if a new insertion exceeds histogram's capacity, we need to find and combine
            // two closest (by centroids) buckets
            if (this->_buckets.size() > this->_max_size) {
                combine();
            }
        }

        // a convenience function to add new floating-point values to the histogram
        void push(double value) {
            push(Bucket(value, 1));
        }


    private:
        const size_t _max_size;
        std::vector<Bucket> _buckets;

        // find and merge two closest buckets (by centroid)
        void combine() {
            // for each pair of adjacent buckets use the following sorting key to find the minimum:
            // 1) consider the gap between centroids first; if it's a tie, then
            // 2) consider the total count; if it's still a tie, then
            // 3) consider the value of the left centroid; if it's still a tie, then
            // 4) prefer the buckets closer to the end of the vector (negated index)
            auto merge_index = 0;
            auto merge_tuple = std::make_tuple(
                this->_buckets[1].centroid() - this->_buckets[0].centroid(),
                this->_buckets[1].count() + this->_buckets[0].count(),
                this->_buckets[0].centroid(),
                0
            );
            for (size_t i = 2; i < this->_buckets.size(); ++i) {
                auto candidate_tuple = std::make_tuple(
                    this->_buckets[i].centroid() - this->_buckets[i - 1].centroid(),
                    this->_buckets[i].count() + this->_buckets[i - 1].count(),
                    this->_buckets[i - 1].centroid(),
                    -(i - 1)
                );
                if (candidate_tuple < merge_tuple) {
                    merge_index = i - 1;
                    merge_tuple = candidate_tuple;
                }
            }

            // replace the "left" bucket of a pair with the result of the merge and pop the "right"
            // one from the vector by the means of erase(), shifting all elements to the right by
            // 1 position. erase() is O(M) (where M is a constant fixed at histogram creation time).
            this->_buckets[merge_index] = Bucket(
                this->_buckets[merge_index],
                this->_buckets[merge_index + 1]
            );
            this->_buckets.erase(this->_buckets.begin() + (merge_index + 1));
        }
};

#endif
