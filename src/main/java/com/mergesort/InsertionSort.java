package com.mergesort;

/**
 * Insertion Sort implementation faithful to Algorithms 4th Edition
 * (Robert Sedgewick & Kevin Wayne), lecture slide 205.
 * 
 * Used both as a standalone elementary sorting algorithm and as the small-subarray
 * base-case optimizer for OptimizedMergeSort.
 */
public class InsertionSort {

    /**
     * Sorts the entire array using insertion sort.
     *
     * @param a the array of Comparable objects to sort
     */
    public static void sort(Comparable[] a) {
        if (a == null || a.length <= 1) {
            return;
        }
        sort(a, 0, a.length - 1);
    }

    /**
     * Sorts subarray a[lo..hi] using insertion sort.
     * Faithful to Algorithms 4th Edition inner loop mechanics.
     *
     * @param a  the array containing the subarray
     * @param lo the starting index of the subarray (inclusive)
     * @param hi the ending index of the subarray (inclusive)
     */
    public static void sort(Comparable[] a, int lo, int hi) {
        if (a == null || lo >= hi) {
            return;
        }
        for (int i = lo + 1; i <= hi; i++) {
            for (int j = i; j > lo && less(a[j], a[j - 1]); j--) {
                exch(a, j, j - 1);
            }
        }
    }

    /**
     * Helper comparison method: returns true if v < w.
     */
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }

    /**
     * Helper exchange method: swaps elements at index i and j.
     */
    private static void exch(Comparable[] a, int i, int j) {
        Comparable swap = a[i];
        a[i] = a[j];
        a[j] = swap;
    }
}
