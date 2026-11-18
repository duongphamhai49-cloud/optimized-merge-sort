package com.mergesort;

import java.util.Arrays;
import java.util.Random;

/**
 * Comprehensive Correctness and Unit Tests for:
 * - InsertionSort (full array and range [lo..hi])
 * - Standard MergeSort
 * - OptimizedMergeSort across diverse cutoff thresholds
 * 
 * Verifies correctness against java.util.Arrays.sort() oracle.
 * Tests edge cases: empty, single-element, all duplicates, negative numbers,
 * already-sorted, reverse-sorted, random, cutoff boundaries, and stability.
 */
public class SortCorrectnessTest {

    private static int testsRun = 0;
    private static int testsPassed = 0;

    public static void main(String[] args) {
        System.out.println("=================================================================");
        System.out.println("  RUNNING COMPREHENSIVE CORRECTNESS TESTS FOR MERGE SORT SUITE   ");
        System.out.println("=================================================================");

        // 1. Edge Case Tests
        testEmptyArray();
        testSingleElementArray();
        testTwoElementArrays();

        // 2. Data Characteristic Tests
        testAlreadySortedArray();
        testReverseSortedArray();
        testAllIdenticalElements();
        testManyDuplicates();
        testNegativeValues();
        testInterleavedValues();

        // 3. Cutoff Boundary Tests
        testCutoffBoundaryConditions();

        // 4. Randomized Oracle Verification
        testRandomArraysAgainstOracle();

        // 5. Insertion Sort Subarray Range Tests
        testInsertionSortSubarray();

        // 6. Stability Tests
        testStability();

        System.out.println("=================================================================");
        System.out.printf("  TEST SUMMARY: %d / %d tests passed successfully!%n", testsPassed, testsRun);
        System.out.println("=================================================================");

        if (testsPassed != testsRun) {
            System.err.println("SOME TESTS FAILED!");
            System.exit(1);
        }
    }

    private static void assertTrue(String testName, boolean condition) {
        testsRun++;
        if (condition) {
            testsPassed++;
            System.out.printf("  [PASS] %s%n", testName);
        } else {
            System.err.printf("  [FAIL] %s%n", testName);
            throw new AssertionError("Test failed: " + testName);
        }
    }

    private static void testEmptyArray() {
        Integer[] a1 = new Integer[0];
        Integer[] a2 = new Integer[0];
        Integer[] a3 = new Integer[0];

        InsertionSort.sort(a1);
        MergeSort.sort(a2);
        OptimizedMergeSort.sort(a3, 10);

        assertTrue("Empty array - InsertionSort", a1.length == 0);
        assertTrue("Empty array - MergeSort", a2.length == 0);
        assertTrue("Empty array - OptimizedMergeSort", a3.length == 0);
    }

    private static void testSingleElementArray() {
        Integer[] a1 = {42};
        Integer[] a2 = {42};
        Integer[] a3 = {42};

        InsertionSort.sort(a1);
        MergeSort.sort(a2);
        OptimizedMergeSort.sort(a3, 10);

        assertTrue("Single element - InsertionSort", a1[0] == 42);
        assertTrue("Single element - MergeSort", a2[0] == 42);
        assertTrue("Single element - OptimizedMergeSort", a3[0] == 42);
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

        assertTrue("Two elements inverted - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Two elements inverted - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Two elements inverted - OptimizedMergeSort", Arrays.equals(c3, exp));
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

        assertTrue("Already sorted - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Already sorted - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Already sorted - OptimizedMergeSort", Arrays.equals(c3, exp));
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

        assertTrue("Reverse sorted - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Reverse sorted - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Reverse sorted - OptimizedMergeSort", Arrays.equals(c3, exp));
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

        assertTrue("All identical elements - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("All identical elements - MergeSort", Arrays.equals(c2, exp));
        assertTrue("All identical elements - OptimizedMergeSort", Arrays.equals(c3, exp));
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

        assertTrue("Many duplicates - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Many duplicates - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Many duplicates - OptimizedMergeSort", Arrays.equals(c3, exp));
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

        assertTrue("Negative values - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Negative values - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Negative values - OptimizedMergeSort", Arrays.equals(c3, exp));
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

        assertTrue("Interleaved values - InsertionSort", Arrays.equals(c1, exp));
        assertTrue("Interleaved values - MergeSort", Arrays.equals(c2, exp));
        assertTrue("Interleaved values - OptimizedMergeSort", Arrays.equals(c3, exp));
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
            assertTrue("Cutoff boundary test (cutoff=" + cutoff + ")", Arrays.equals(copy, expected));
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
            assertTrue("MergeSort random array size " + size, Arrays.equals(mergeCopy, expected));

            Integer[] optCopyDefault = original.clone();
            OptimizedMergeSort.sort(optCopyDefault);
            assertTrue("OptimizedMergeSort default cutoff size " + size, Arrays.equals(optCopyDefault, expected));

            Integer[] optCopyCustom = original.clone();
            OptimizedMergeSort.sort(optCopyCustom, 16);
            assertTrue("OptimizedMergeSort cutoff 16 size " + size, Arrays.equals(optCopyCustom, expected));
        }
    }

    private static void testInsertionSortSubarray() {
        Integer[] arr = {9, 8, 7, 6, 5, 4, 3, 2, 1, 0};
        // Sort subarray index 2 to 6: elements {7, 6, 5, 4, 3} -> should become {3, 4, 5, 6, 7}
        InsertionSort.sort(arr, 2, 6);
        Integer[] expected = {9, 8, 3, 4, 5, 6, 7, 2, 1, 0};
        assertTrue("InsertionSort subarray [2..6]", Arrays.equals(arr, expected));
    }

    /**
     * Verifies stability: items with equal primary keys must retain original relative ordering.
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

        // Verify key ordering
        boolean keySorted = true;
        for (int i = 1; i < copy.length; i++) {
            if (copy[i].key < copy[i - 1].key) keySorted = false;
        }
        assertTrue("Stability - Keys sorted", keySorted);

        // Verify stability: for key == 1, original indices should be 2, 4, 7 in order
        int lastIdx1 = -1;
        boolean stable1 = true;
        for (Element e : copy) {
            if (e.key == 1) {
                if (e.originalIndex < lastIdx1) stable1 = false;
                lastIdx1 = e.originalIndex;
            }
        }
        assertTrue("Stability - Key 1 relative order preserved", stable1);
    }
}
