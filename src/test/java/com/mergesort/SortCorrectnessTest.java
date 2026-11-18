package com.mergesort;

import java.util.Arrays;
import java.util.Random;

/**
 * Bộ kiểm thử tính đúng đắn toàn diện (Unit Correctness Tests):
 * - InsertionSort (toàn mảng và đoạn con [lo..hi])
 * - MergeSort chuẩn
 * - OptimizedMergeSort trên đa dạng các ngưỡng cutoff
 * 
 * Đối chứng tính đúng đắn với oracle java.util.Arrays.sort().
 * Kiểm tra các trường hợp biên: mảng rỗng, 1 phần tử, trùng lặp hoàn toàn, số âm,
 * đã sắp xếp, nghịch đảo, ngẫu nhiên, các biên cutoff và tính ổn định (stability).
 */
public class SortCorrectnessTest {

    private static int testsRun = 0;
    private static int testsPassed = 0;

    public static void main(String[] args) {
        System.out.println("=================================================================");
        System.out.println("  BẮT ĐẦU CHẠY BỘ KIỂM THỬ ĐÚNG ĐẮN TOÀN DIỆN CHO MERGE SORT     ");
        System.out.println("=================================================================");

        // 1. Kiểm thử trường hợp biên
        testEmptyArray();
        testSingleElementArray();
        testTwoElementArrays();

        // 2. Kiểm thử đặc tính dữ liệu
        testAlreadySortedArray();
        testReverseSortedArray();
        testAllIdenticalElements();
        testManyDuplicates();
        testNegativeValues();
        testInterleavedValues();

        // 3. Kiểm thử các ngưỡng biên Cutoff
        testCutoffBoundaryConditions();

        // 4. Đối chứng ngẫu nhiên với Oracle Arrays.sort()
        testRandomArraysAgainstOracle();

        // 5. Kiểm thử sắp xếp đoạn con Insertion Sort
        testInsertionSortSubarray();

        // 6. Kiểm thử tính ổn định (Stability)
        testStability();

        System.out.println("=================================================================");
        System.out.printf("  TỔNG KẾT KIỂM THỬ: %d / %d bài test VƯỢT QUA thành công!%n", testsPassed, testsRun);
        System.out.println("=================================================================");

        if (testsPassed != testsRun) {
            System.err.println("CÓ BÀI TEST BỊ THẤT BẠI!");
            System.exit(1);
        }
    }

    private static void assertTrue(String testName, boolean condition) {
        testsRun++;
        if (condition) {
            testsPassed++;
            System.out.printf("  [PASS - ĐẠT] %s%n", testName);
        } else {
            System.err.printf("  [FAIL - LỖI] %s%n", testName);
            throw new AssertionError("Kiểm thử thất bại: " + testName);
        }
    }

    private static void testEmptyArray() {
        Integer[] a1 = new Integer[0];
        Integer[] a2 = new Integer[0];
        Integer[] a3 = new Integer[0];

        InsertionSort.sort(a1);
        MergeSort.sort(a2);
        OptimizedMergeSort.sort(a3, 10);

        assertTrue("Mảng rỗng - InsertionSort", a1.length == 0);
        assertTrue("Mảng rỗng - MergeSort", a2.length == 0);
        assertTrue("Mảng rỗng - OptimizedMergeSort", a3.length == 0);
    }

    private static void testSingleElementArray() {
        Integer[] a1 = {42};
        Integer[] a2 = {42};
        Integer[] a3 = {42};

        InsertionSort.sort(a1);
        MergeSort.sort(a2);
        OptimizedMergeSort.sort(a3, 10);

        assertTrue("Mảng 1 phần tử - InsertionSort", a1[0] == 42);
        assertTrue("Mảng 1 phần tử - MergeSort", a2[0] == 42);
        assertTrue("Mảng 1 phần tử - OptimizedMergeSort", a3[0] == 42);
    }

    private static void testTwoElementArrays() {
        Integer[] pairs = {20, 10};
        Integer[] exp = {10, 20};

        Integer[] c1 = pairs.clone();
        Integer[] c2 = pairs.clone();
        Integer[] c3 = pairs.clone();

        InsertionSort.sort(c1);
        MergeSort.sort(c2);
        OptimizedMergeSort.sort(c3, 2);

        assertTrue("Mảng 2 phần tử nghịch đảo - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Mảng 2 phần tử nghịch đảo - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Mảng 2 phần tử nghịch đảo - OptimizedMergeSort", Arrays.equals(c3, exp));
    }

    private static void testAlreadySortedArray() {
        Integer[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        Integer[] exp = arr.clone();

        Integer[] c1 = arr.clone();
        Integer[] c2 = arr.clone();
        Integer[] c3 = arr.clone();

        InsertionSort.sort(c1);
        MergeSort.sort(c2);
        OptimizedMergeSort.sort(c3, 4);

        assertTrue("Mảng đã sắp xếp - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Mảng đã sắp xếp - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Mảng đã sắp xếp - OptimizedMergeSort", Arrays.equals(c3, exp));
    }

    private static void testReverseSortedArray() {
        Integer[] arr = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
        Integer[] exp = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        Integer[] c1 = arr.clone();
        Integer[] c2 = arr.clone();
        Integer[] c3 = arr.clone();

        InsertionSort.sort(c1);
        MergeSort.sort(c2);
        OptimizedMergeSort.sort(c3, 4);

        assertTrue("Mảng nghịch đảo hoàn toàn - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Mảng nghịch đảo hoàn toàn - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Mảng nghịch đảo hoàn toàn - OptimizedMergeSort", Arrays.equals(c3, exp));
    }

    private static void testAllIdenticalElements() {
        Integer[] arr = {7, 7, 7, 7, 7, 7, 7, 7};
        Integer[] exp = arr.clone();

        Integer[] c1 = arr.clone();
        Integer[] c2 = arr.clone();
        Integer[] c3 = arr.clone();

        InsertionSort.sort(c1);
        MergeSort.sort(c2);
        OptimizedMergeSort.sort(c3, 4);

        assertTrue("Mảng toàn bộ phần tử giống nhau - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Mảng toàn bộ phần tử giống nhau - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Mảng toàn bộ phần tử giống nhau - OptimizedMergeSort", Arrays.equals(c3, exp));
    }

    private static void testManyDuplicates() {
        Integer[] arr = {3, 1, 2, 3, 1, 2, 3, 3, 1, 2, 1, 3};
        Integer[] exp = arr.clone();
        Arrays.sort(exp);

        Integer[] c1 = arr.clone();
        Integer[] c2 = arr.clone();
        Integer[] c3 = arr.clone();

        InsertionSort.sort(c1);
        MergeSort.sort(c2);
        OptimizedMergeSort.sort(c3, 5);

        assertTrue("Mảng nhiều phần tử trùng lặp - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Mảng nhiều phần tử trùng lặp - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Mảng nhiều phần tử trùng lặp - OptimizedMergeSort", Arrays.equals(c3, exp));
    }

    private static void testNegativeValues() {
        Integer[] arr = {-5, 12, -100, 0, 45, -3, 8, -5, 0};
        Integer[] exp = arr.clone();
        Arrays.sort(exp);

        Integer[] c1 = arr.clone();
        Integer[] c2 = arr.clone();
        Integer[] c3 = arr.clone();

        InsertionSort.sort(c1);
        MergeSort.sort(c2);
        OptimizedMergeSort.sort(c3, 3);

        assertTrue("Mảng chứa số âm và số không - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Mảng chứa số âm và số không - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Mảng chứa số âm và số không - OptimizedMergeSort", Arrays.equals(c3, exp));
    }

    private static void testInterleavedValues() {
        Integer[] arr = {100, -100, 50, -50, 25, -25, 12, -12, 6, -6, 0};
        Integer[] exp = arr.clone();
        Arrays.sort(exp);

        Integer[] c1 = arr.clone();
        Integer[] c2 = arr.clone();
        Integer[] c3 = arr.clone();

        InsertionSort.sort(c1);
        MergeSort.sort(c2);
        OptimizedMergeSort.sort(c3, 4);

        assertTrue("Mảng số âm dương đan xen - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Mảng số âm dương đan xen - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Mảng số âm dương đan xen - OptimizedMergeSort", Arrays.equals(c3, exp));
    }

    private static void testCutoffBoundaryConditions() {
        int[] cutoffs = {1, 2, 4, 6, 7, 8, 10, 12, 16, 20, 24, 32, 48, 64, 100, 1000};
        Random rng = new Random(2026);
        int size = 150;
        Integer[] original = new Integer[size];
        for (int i = 0; i < size; i++) {
            original[i] = rng.nextInt(1000) - 500;
        }

        Integer[] expected = original.clone();
        Arrays.sort(expected);

        for (int cutoff : cutoffs) {
            Integer[] copy = original.clone();
            OptimizedMergeSort.sort(copy, cutoff);
            assertTrue("Kiểm thử biên Cutoff (cutoff=" + cutoff + ")", Arrays.equals(copy, expected));
        }
    }

    private static void testRandomArraysAgainstOracle() {
        int[] sizes = {5, 13, 37, 64, 128, 512, 2048, 10000};
        Random rng = new Random(1337);

        for (int size : sizes) {
            Integer[] original = new Integer[size];
            for (int i = 0; i < size; i++) {
                original[i] = rng.nextInt(100000);
            }

            Integer[] expected = original.clone();
            Arrays.sort(expected);

            Integer[] mergeCopy = original.clone();
            MergeSort.sort(mergeCopy);
            assertTrue("MergeSort mảng ngẫu nhiên kích thước " + size, Arrays.equals(mergeCopy, expected));

            Integer[] optCopyDefault = original.clone();
            OptimizedMergeSort.sort(optCopyDefault);
            assertTrue("OptimizedMergeSort cutoff mặc định kích thước " + size, Arrays.equals(optCopyDefault, expected));

            Integer[] optCopyCustom = original.clone();
            OptimizedMergeSort.sort(optCopyCustom, 16);
            assertTrue("OptimizedMergeSort cutoff 16 kích thước " + size, Arrays.equals(optCopyCustom, expected));
        }
    }

    private static void testInsertionSortSubarray() {
        Integer[] arr = {9, 8, 7, 6, 5, 4, 3, 2, 1, 0};
        // Sắp xếp đoạn con từ chỉ số 2 đến 6
        InsertionSort.sort(arr, 2, 6);
        Integer[] expected = {9, 8, 3, 4, 5, 6, 7, 2, 1, 0};
        assertTrue("InsertionSort trên đoạn con [2..6]", Arrays.equals(arr, expected));
    }

    /**
     * Kiểm thử tính ổn định (Stability): các phần tử có khóa bằng nhau phải giữ nguyên thứ tự ban đầu.
     */
    private static void testStability() {
        class Element implements Comparable<Element> {
            final int key;
            final int originalIndex;

            Element(int key, int originalIndex) {
                this.key = key;
                this.originalIndex = originalIndex;
            }

            @Override
            public int compareTo(Element o) {
                return Integer.compare(this.key, o.key);
            }
        }

        Element[] items = {
            new Element(3, 1),
            new Element(1, 2),
            new Element(2, 3),
            new Element(1, 4),
            new Element(3, 5),
            new Element(2, 6),
            new Element(1, 7)
        };

        Element[] copy = items.clone();
        OptimizedMergeSort.sort(copy, 4);

        // Kiểm tra các khóa có được sắp xếp không
        boolean keySorted = true;
        for (int i = 1; i < copy.length; i++) {
            if (copy[i].key < copy[i - 1].key) keySorted = false;
        }
        assertTrue("Tính ổn định - Khóa chính được sắp xếp", keySorted);

        // Kiểm tra tính ổn định: với key == 1, thứ tự ban đầu phải là 2, 4, 7
        int lastIdx1 = -1;
        boolean stable1 = true;
        for (Element e : copy) {
            if (e.key == 1) {
                if (e.originalIndex < lastIdx1) stable1 = false;
                lastIdx1 = e.originalIndex;
            }
        }
        assertTrue("Tính ổn định - Thứ tự tương đối của các phần tử bằng nhau được bảo toàn", stable1);
    }
}
