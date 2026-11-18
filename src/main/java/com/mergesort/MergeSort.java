package com.mergesort;

/**
 * Standard Merge Sort implementation strictly adhering to the lecture materials
 * from Algorithms 4th Edition (Robert Sedgewick & Kevin Wayne), lecture slides 229-230.
 * 
 * Features:
 * - Single auxiliary array allocation prior to recursion to avoid memory thrashing.
 * - In-place merge abstraction with left pointer i and right pointer j.
 * - Classic divide-and-conquer recursive structure with midpoint calculation.
 */
public class MergeSort {

    /**
     * Merges two sorted subarrays a[lo..mid] and a[mid+1..hi] using auxiliary array aux[].
     * Exactly reproduces slide 229 merge procedure.
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
     * Recursive sort helper dividing the range and merging.
     * Slide 230 implementation.
     */
    private static void sort(Comparable[] a, Comparable[] aux, int lo, int hi) {
        if (hi <= lo) return;
        int mid = lo + (hi - lo) / 2;
        sort(a, aux, lo, mid);
        sort(a, aux, mid + 1, hi);
        merge(a, aux, lo, mid, hi);
    }

    /**
     * Sorts the array using standard Merge Sort.
     * Allocates auxiliary array once.
     *
     * @param a the array of Comparable elements to sort
     */
    public static void sort(Comparable[] a) {
        if (a == null || a.length <= 1) {
            return;
        }
        Comparable[] aux = new Comparable[a.length];
        sort(a, aux, 0, a.length - 1);
    }

    /**
     * Helper comparison method: returns true if v < w.
     */
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }
}
