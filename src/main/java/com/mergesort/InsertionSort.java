package com.mergesort;

/**
 * Cài đặt thuật toán Sắp xếp chèn (Insertion Sort) bám sát nội dung bài giảng
 * giáo trình Algorithms 4th Edition (Robert Sedgewick & Kevin Wayne), slide 205.
 * 
 * Hỗ trợ sắp xếp toàn bộ mảng hoặc sắp xếp đoạn con a[lo..hi] làm cơ sở
 * tối ưu cho thuật toán Merge Sort cải tiến.
 */
public class InsertionSort {

    /**
     * Sắp xếp toàn bộ mảng a bằng thuật toán Insertion Sort.
     *
     * @param a mảng các đối tượng Comparable cần sắp xếp
     */
    public static void sort(Comparable[] a) {
        if (a == null || a.length <= 1) {
            return;
        }
        sort(a, 0, a.length - 1);
    }

    /**
     * Sắp xếp đoạn con a[lo..hi] bằng thuật toán Insertion Sort.
     * Cài đặt bám sát slide 205 với cơ chế ngắt sớm khi phần tử đã đúng thứ tự.
     *
     * @param a  mảng chứa đoạn con
     * @param lo chỉ số bắt đầu (bao gồm)
     * @param hi chỉ số kết thúc (bao gồm)
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
     * Hàm phụ trợ so sánh: trả về true nếu v < w.
     */
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }

    /**
     * Hàm phụ trợ đổi chỗ: hoán đổi hai phần tử tại vị trí i và j.
     */
    private static void exch(Comparable[] a, int i, int j) {
        Comparable swap = a[i];
        a[i] = a[j];
        a[j] = swap;
    }
}
