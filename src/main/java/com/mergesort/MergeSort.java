package com.mergesort;

/**
 * Cài đặt thuật toán Sắp xếp trộn chuẩn (Standard Merge Sort) tuân thủ chặt chẽ
 * slide bài giảng môn học và giáo trình Algorithms 4th Edition (Sedgewick & Wayne),
 * slide 229-230.
 * 
 * Đặc điểm kỹ thuật:
 * - Cấp phát mảng phụ aux[] đúng một lần duy nhất ở hàm ngoài cùng.
 * - Quy trình trộn tại chỗ (in-place merge abstraction) với hai con trỏ i và j.
 * - Phân chia mảng theo phương pháp chia để trị đệ quy với điểm giữa mid.
 */
public class MergeSort {

    /**
     * Trộn hai nửa đã sắp xếp a[lo..mid] và a[mid+1..hi] bằng mảng phụ aux[].
     * Tái hiện chính xác mã nguồn slide 229.
     */
    private static void merge(Comparable[] a, Comparable[] aux, int lo, int mid, int hi) {
        // Sao chép sang mảng phụ aux[]
        for (int k = lo; k <= hi; k++) {
            aux[k] = a[k];
        }

        // Trộn ngược lại vào mảng chính a[]
        int i = lo, j = mid + 1;
        for (int k = lo; k <= hi; k++) {
            if      (i > mid)               a[k] = aux[j++];
            else if (j > hi)                a[k] = aux[i++];
            else if (less(aux[j], aux[i])) a[k] = aux[j++];
            else                            a[k] = aux[i++];
        }
    }

    /**
     * Hàm sắp xếp đệ quy chia đôi mảng và trộn.
     * Tái hiện chính xác mã nguồn slide 230.
     */
    private static void sort(Comparable[] a, Comparable[] aux, int lo, int hi) {
        if (hi <= lo) return;
        int mid = lo + (hi - lo) / 2;
        sort(a, aux, lo, mid);
        sort(a, aux, mid + 1, hi);
        merge(a, aux, lo, mid, hi);
    }

    /**
     * Phương thức public sắp xếp mảng bằng Merge Sort chuẩn.
     * Cấp phát mảng phụ aux[] một lần duy nhất để tối ưu hiệu năng.
     *
     * @param a mảng các đối tượng Comparable cần sắp xếp
     */
    public static void sort(Comparable[] a) {
        if (a == null || a.length <= 1) {
            return;
        }
        Comparable[] aux = new Comparable[a.length];
        sort(a, aux, 0, a.length - 1);
    }

    /**
     * Hàm so sánh phụ trợ: trả về true nếu v < w.
     */
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }
}
