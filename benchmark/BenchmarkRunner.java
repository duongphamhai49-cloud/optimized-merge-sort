import java.io.*;
import java.util.*;

public class BenchmarkRunner {

    static final int WARMUP = 3;
    static final int REPS   = 5;
    static final int[] SIZES   = {1000, 10000, 100000, 500000, 1000000};
    static final int[] CUTOFFS = {1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64};
    static final String[] TYPES = {
        "random", 
        "sorted", 
        "reversed", 
        "duplicates", 
        "partially_sorted_1pct", 
        "partially_sorted_5pct", 
        "partially_sorted_10pct"
    };

    // Gia tri CUTOFF duoc chon de so sanh dien rong
    static final int CHOSEN_CUTOFF = 16;

    public static void main(String[] args) throws Exception {
        System.out.println("Bat dau benchmark (CUTOFF = " + CHOSEN_CUTOFF + ", 7 bo du lieu)...\n");
        new File("results").mkdirs();

        PrintWriter raw = new PrintWriter("results/raw_results.csv", "UTF-8");
        raw.println("size,type,algorithm,cutoff,rep,time_ms");

        // Phan 1: So sanh MergeSort vs OptimizedMergeSort (CUTOFF = 16) tren ca 7 kieu du lieu
        System.out.println("--- So sanh MergeSort vs OptimizedMergeSort (CUTOFF = " + CHOSEN_CUTOFF + ") ---");
        PrintWriter sumWriter = new PrintWriter("results/summary.csv", "UTF-8");
        sumWriter.println("size,type,merge_ms,optimized_ms,speedup_pct");

        for (int size : SIZES) {
            for (String type : TYPES) {
                double[] mergeT = new double[REPS];
                double[] optT   = new double[REPS];

                Integer[] data = generate(size, type, 0);

                // Warm up
                for (int w = 0; w < WARMUP; w++) {
                    Integer[] tmp = data.clone();
                    MergeSort.sort(tmp);
                    tmp = data.clone();
                    OptimizedMergeSort.sort(tmp, CHOSEN_CUTOFF);
                }

                // Do thuc te
                for (int r = 0; r < REPS; r++) {
                    Integer[] a = data.clone();
                    long t0 = System.nanoTime();
                    MergeSort.sort(a);
                    mergeT[r] = (System.nanoTime() - t0) / 1e6;
                    raw.println(size + "," + type + ",MergeSort,-1," + r + "," + mergeT[r]);

                    Integer[] b = data.clone();
                    t0 = System.nanoTime();
                    OptimizedMergeSort.sort(b, CHOSEN_CUTOFF);
                    optT[r] = (System.nanoTime() - t0) / 1e6;
                    raw.println(size + "," + type + ",OptimizedMergeSort," + CHOSEN_CUTOFF + "," + r + "," + optT[r]);
                }

                double avgM = mean(mergeT);
                double avgO = mean(optT);
                double speedup = (avgM - avgO) / avgM * 100.0;
                sumWriter.printf("%d,%s,%.3f,%.3f,%.1f%n", size, type, avgM, avgO, speedup);
                System.out.printf("  n=%-8d  %-24s  Merge=%.2fms  Opt=%.2fms  Speedup=%.1f%%%n",
                        size, type, avgM, avgO, speedup);
            }
        }
        sumWriter.close();

        // Phan 2: Tim CUTOFF toi uu tren n=100000 (random)
        System.out.println("\n--- Khao sat cac gia tri CUTOFF (n=100000, random) ---");
        PrintWriter cutWriter = new PrintWriter("results/cutoff_results.csv", "UTF-8");
        cutWriter.println("cutoff,time_ms");

        int n = 100000;
        Integer[] base = generate(n, "random", 42);
        for (int cutoff : CUTOFFS) {
            double[] times = new double[REPS];

            for (int w = 0; w < WARMUP; w++) {
                Integer[] tmp = base.clone();
                OptimizedMergeSort.sort(tmp, cutoff);
            }

            for (int r = 0; r < REPS; r++) {
                Integer[] a = base.clone();
                long t0 = System.nanoTime();
                OptimizedMergeSort.sort(a, cutoff);
                times[r] = (System.nanoTime() - t0) / 1e6;
                raw.println(n + ",random,OptimizedMergeSort," + cutoff + "," + r + "," + times[r]);
            }

            double avg = mean(times);
            cutWriter.printf("%d,%.3f%n", cutoff, avg);
            System.out.printf("  CUTOFF=%-3d  avg=%.3f ms%n", cutoff, avg);
        }
        cutWriter.close();
        raw.close();

        System.out.println("\nHoan tat. Ket qua luu tai: results/");
    }

    static Integer[] generate(int n, String type, long seed) {
        Random rng = new Random(seed == 0 ? 123456 : seed);
        Integer[] a = new Integer[n];
        switch (type) {
            case "random":
                for (int i = 0; i < n; i++) a[i] = rng.nextInt(1000000);
                break;
            case "sorted":
                for (int i = 0; i < n; i++) a[i] = i;
                break;
            case "reversed":
                for (int i = 0; i < n; i++) a[i] = n - i;
                break;
            case "duplicates":
                for (int i = 0; i < n; i++) a[i] = rng.nextInt(100);
                break;
            case "partially_sorted_1pct": {
                for (int i = 0; i < n; i++) a[i] = i;
                int swaps = Math.max(1, (int)(n * 0.01));
                for (int i = 0; i < swaps; i++) {
                    int i1 = rng.nextInt(n), i2 = rng.nextInt(n);
                    int t = a[i1]; a[i1] = a[i2]; a[i2] = t;
                }
                break;
            }
            case "partially_sorted_5pct": {
                for (int i = 0; i < n; i++) a[i] = i;
                int swaps = Math.max(1, (int)(n * 0.05));
                for (int i = 0; i < swaps; i++) {
                    int i1 = rng.nextInt(n), i2 = rng.nextInt(n);
                    int t = a[i1]; a[i1] = a[i2]; a[i2] = t;
                }
                break;
            }
            case "partially_sorted_10pct": {
                for (int i = 0; i < n; i++) a[i] = i;
                int swaps = Math.max(1, (int)(n * 0.10));
                for (int i = 0; i < swaps; i++) {
                    int i1 = rng.nextInt(n), i2 = rng.nextInt(n);
                    int t = a[i1]; a[i1] = a[i2]; a[i2] = t;
                }
                break;
            }
        }
        return a;
    }

    static double mean(double[] arr) {
        double s = 0;
        for (double v : arr) s += v;
        return s / arr.length;
    }
}
