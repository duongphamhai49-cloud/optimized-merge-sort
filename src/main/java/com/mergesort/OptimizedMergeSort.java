package com.mergesort;

/**
 * Optimized Merge Sort with small subarray cutoff optimization,
 * based on Algorithms 4th Edition (Robert Sedgewick & Kevin Wayne), slide 238.
 * 
 * When subarray length <= cutoff (i.e. hi <= lo + cutoff - 1),
 * the algorithm switches directly to Insertion Sort, bypassing recursive function call overhead
 * and auxiliary array copy overhead on tiny subarrays.
 */
public class OptimizedMergeSort {

    /**
     * Default cutoff threshold recommended in modern editions of Algorithms 4th Edition.
     */
    public static final int DEFAULT_CUTOFF = 10;

    /**
     * Merges two sorted subarrays a[lo..mid] and a[mid+1..hi] using auxiliary array aux[].
     * Preserves the lecture-based merge procedure from slide 229.
     */
    private static void merge(Comparable[] a, Comparable[] aux, int lo, int mid, int hi) {
        // Copy to auxiliary array aux[]
        for (int k = lo; k <= hi; k++) {
            aux[k] = a[k];
        }

        // Merge back to a[]
        int i = lo, j = mid + 1;
        for (int k = lo; k <= hi; k++) {
            if      (i > mid)               a[k] = aux[j++];
            else if (j > hi)                a[k] = aux[i++];
            else if (less(aux[j], aux[i])) a[k] = aux[j++];
            else                            a[k] = aux[i++];
        }
    }

    /**
     * Recursive sort helper with cutoff threshold.
     * Slide 238 implementation:
     * if (hi <= lo + CUTOFF - 1) {
     *     Insertion.sort(a, lo, hi);
     *     return;
     * }
     */
    private static void sort(Comparable[] a, Comparable[] aux, int lo, int hi, int cutoff) {
        // Cutoff optimization: for subarrays of length <= cutoff, switch to Insertion Sort
        if (hi <= lo + cutoff - 1) {
            InsertionSort.sort(a, lo, hi);
            return;
        }

        int mid = lo + (hi - lo) / 2;
        sort(a, aux, lo, mid, cutoff);
        sort(a, aux, mid + 1, hi, cutoff);
        merge(a, aux, lo, mid, hi);
    }

    /**
     * Sorts array with a specified cutoff threshold.
     *
     * @param a      the array of Comparable elements
     * @param cutoff the subarray length threshold below which Insertion Sort is used
     */
    public static void sort(Comparable[] a, int cutoff) {
        if (a == null || a.length <= 1) {
            return;
        }
        // If cutoff < 1, fall back to standard cutoff = 1 (standard base case: length <= 1)
        int effectiveCutoff = Math.max(1, cutoff);
        Comparable[] aux = new Comparable[a.length];
        sort(a, aux, 0, a.length - 1, effectiveCutoff);
    }

    /**
     * Sorts array with default cutoff threshold (10).
     *
     * @param a the array of Comparable elements
     */
    public static void sort(Comparable[] a) {
        sort(a, DEFAULT_CUTOFF);
    }

    /**
     * Helper comparison method: returns true if v < w.
     */
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }
}
