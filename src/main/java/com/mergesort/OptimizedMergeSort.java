package com.mergesort;

/**
 * Cài đặt thuật toán Sắp xếp trộn cải tiến (Optimized Merge Sort) với ngưỡng CUTOFF
 * chuyển đổi sang Insertion Sort cho các mảng con kích thước nhỏ, bám sát slide 238
 * giáo trình Algorithms 4th Edition (Robert Sedgewick & Kevin Wayne).
 * 
 * Khi kích thước mảng con <= cutoff (hi <= lo + cutoff - 1), giải thuật chuyển trực tiếp
 * sang Insertion Sort, triệt tiêu chi phí gọi hàm đệ quy và sao chép mảng phụ trên các đoạn mảng nhỏ.
 */
public class OptimizedMergeSort {

    /**
     * Ngưỡng Cutoff mặc định được khuyến nghị trong ấn bản mới của giáo trình.
     */
    public static final int DEFAULT_CUTOFF = 10;

    /**
     * Trộn hai nửa đã sắp xếp a[lo..mid] và a[mid+1..hi] bằng mảng phụ aux[].
     * Giữ nguyên quy trình trộn chuẩn theo slide 229.
     */
    private static void merge(Comparable[] a, Comparable[] aux, int lo, int mid, int hi) {
        // Sao chép sang mảng phụ aux[]
        for (int k = lo; k <= hi; k++) {
            aux[k] = a[k];
        }

        // Trộn vào mảng chính a[]
        int i = lo, j = mid + 1;
        for (int k = lo; k <= hi; k++) {
            if      (i > mid)               a[k] = aux[j++];
            else if (j > hi)                a[k] = aux[i++];
            else if (less(aux[j], aux[i])) a[k] = aux[j++];
            else                            a[k] = aux[i++];
        }
    }

    /**
     * Hàm sắp xếp đệ quy tích hợp ngưỡng Cutoff.
     * Cài đặt bám sát slide 238:
     * if (hi <= lo + CUTOFF - 1) {
     *     Insertion.sort(a, lo, hi);
     *     return;
     * }
     */
    private static void sort(Comparable[] a, Comparable[] aux, int lo, int hi, int cutoff) {
        // Cải tiến Cutoff: Nếu độ dài mảng con <= cutoff, dùng Insertion Sort
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
     * Sắp xếp mảng với ngưỡng Cutoff tùy chọn.
     *
     * @param a      mảng cần sắp xếp
     * @param cutoff ngưỡng chuyển đổi sang Insertion Sort
     */
    public static void sort(Comparable[] a, int cutoff) {
        if (a == null || a.length <= 1) {
            return;
        }
        int effectiveCutoff = Math.max(1, cutoff);
        Comparable[] aux = new Comparable[a.length];
        sort(a, aux, 0, a.length - 1, effectiveCutoff);
    }

    /**
     * Sắp xếp mảng với ngưỡng Cutoff mặc định (10).
     *
     * @param a mảng cần sắp xếp
     */
    public static void sort(Comparable[] a) {
        sort(a, DEFAULT_CUTOFF);
    }

    /**
     * Hàm so sánh phụ trợ: trả về true nếu v < w.
     */
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }
}
