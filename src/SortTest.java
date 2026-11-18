import java.util.Arrays;
import java.util.Random;

public class SortTest {

    static int passed = 0, failed = 0;

    public static void main(String[] args) {
        testMergeSort();
        testOptimizedMergeSort();
        System.out.println("\nKet qua: " + passed + " passed, " + failed + " failed.");
    }

    static void check(String name, Integer[] arr) {
        Integer[] expected = arr.clone();
        Arrays.sort(expected);

        Integer[] a1 = arr.clone();
        MergeSort.sort(a1);

        Integer[] a2 = arr.clone();
        OptimizedMergeSort.sort(a2, 8);

        boolean ok1 = Arrays.equals(a1, expected);
        boolean ok2 = Arrays.equals(a2, expected);

        if (ok1 && ok2) {
            System.out.println("  PASS: " + name);
            passed++;
        } else {
            System.out.println("  FAIL: " + name);
            if (!ok1) System.out.println("    MergeSort sai");
            if (!ok2) System.out.println("    OptimizedMergeSort sai");
            failed++;
        }
    }

    static void testMergeSort() {
        System.out.println("=== Kiem tra MergeSort ===");

        check("Mang rong", new Integer[]{});
        check("1 phan tu", new Integer[]{42});
        check("2 phan tu - da sap xep", new Integer[]{1, 2});
        check("2 phan tu - nguoc", new Integer[]{2, 1});
        check("Da sap xep tang dan", new Integer[]{1, 2, 3, 4, 5});
        check("Sap xep nguoc", new Integer[]{5, 4, 3, 2, 1});
        check("Co phan tu trung lap", new Integer[]{3, 1, 4, 1, 5, 9, 2, 6, 5, 3});
        check("Tat ca bang nhau", new Integer[]{7, 7, 7, 7, 7});
        check("So am", new Integer[]{-3, -1, -4, -1, -5, -9});
        check("Am va duong", new Integer[]{-5, 3, -2, 8, 0, -1, 4});

        Random rng = new Random(42);
        Integer[] rand100 = new Integer[100];
        for (int i = 0; i < 100; i++) rand100[i] = rng.nextInt(1000);
        check("Ngau nhien 100 phan tu", rand100);

        Integer[] rand1000 = new Integer[1000];
        for (int i = 0; i < 1000; i++) rand1000[i] = rng.nextInt(10000);
        check("Ngau nhien 1000 phan tu", rand1000);
    }

    static void testOptimizedMergeSort() {
        System.out.println("\n=== Kiem tra OptimizedMergeSort (cac gia tri cutoff) ===");

        int[] cutoffs = {1, 4, 8, 16, 32};
        for (int c : cutoffs) {
            Integer[] arr = {9, 3, 7, 1, 5, 8, 2, 6, 4, 0};
            Integer[] expected = arr.clone();
            Arrays.sort(expected);
            OptimizedMergeSort.sort(arr, c);
            boolean ok = Arrays.equals(arr, expected);
            System.out.println("  PASS cutoff=" + c + ": " + (ok ? "PASS" : "FAIL"));
            if (ok) passed++; else failed++;
        }

        // Bien bien vung bien cutoff
        Integer[] exact = new Integer[8];
        for (int i = 0; i < 8; i++) exact[i] = 8 - i;
        check("Dung bang cutoff (n=8, cutoff=8)", exact);

        Integer[] overCutoff = new Integer[9];
        for (int i = 0; i < 9; i++) overCutoff[i] = 9 - i;
        check("Vuot cutoff (n=9, cutoff=8)", overCutoff);
    }
}

