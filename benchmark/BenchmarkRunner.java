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

    public static void main(String[] args) throws Exception {
        System.out.println("=== BAT DAU BENCHMARK CHUAN XAC VA DONG NHAT ===");
        new File("results").mkdirs();

        PrintWriter raw = new PrintWriter("results/raw_results.csv", "UTF-8");
        raw.println("size,type,algorithm,cutoff,rep,time_ms");

        // -------------------------------------------------------------
        // GIAI DOAN 1: KHAO SAT TIM CUTOFF TOI UU (n = 100.000, random)
        // Chay truoc khi heap bi day boi mang 1.000.000 phan tu
        // Dung trimmed mean (loai bo min va max) de triet tieu GC pause
        // -------------------------------------------------------------
        System.out.println("\n--- GIAI DOAN 1: KHAO SAT TIM CUTOFF TOI UU (n = 100.000, random) ---");
        PrintWriter cutWriter = new PrintWriter("results/cutoff_results.csv", "UTF-8");
        cutWriter.println("cutoff,time_ms");

        int n_cutoff = 100000;
        Integer[] base_cutoff = generate(n_cutoff, "random", 42);

        // Warm up JIT truoc khi do
        for (int w = 0; w < 10; w++) {
            Integer[] tmp = base_cutoff.clone();
            OptimizedMergeSort.sort(tmp, 16);
        }

        int bestCutoff = 16;
        double minTime = Double.MAX_VALUE;

        // Do tung cutoff voi 7 lan lap, loai bo 1 min va 1 max (tranh GC pause dot bien)
        for (int c : CUTOFFS) {
            System.gc();
            Thread.sleep(15);

            double[] times = new double[7];
            for (int r = 0; r < 7; r++) {
                Integer[] a = base_cutoff.clone();
                long t0 = System.nanoTime();
                OptimizedMergeSort.sort(a, c);
                times[r] = (System.nanoTime() - t0) / 1e6;
                raw.println(n_cutoff + ",random,OptimizedMergeSort," + c + "," + r + "," + times[r]);
            }

            Arrays.sort(times);
            // Trimmed mean: bo times[0] (min) va times[6] (max), tinh trung binh 5 lan con lai
            double sum = 0;
            for (int i = 1; i < 6; i++) sum += times[i];
            double avg = sum / 5.0;

            cutWriter.printf("%d,%.3f%n", c, avg);
            System.out.printf("  CUTOFF=%-3d  avg=%.3f ms%n", c, avg);

            if (avg < minTime) {
                minTime = avg;
                bestCutoff = c;
            }
        }
        cutWriter.close();
        System.out.printf("=> CUTOFF TOI UU TIM DUOC LA: %d (%.3f ms)%n%n", bestCutoff, minTime);

        // -------------------------------------------------------------
        // GIAI DOAN 2: SO SANH DIEN RONG DUNG CHINH bestCutoff VUA TIM DUOC
        // -------------------------------------------------------------
        System.out.println("--- GIAI DOAN 2: SO SANH MergeSort VS OptimizedMergeSort (CUTOFF = " + bestCutoff + ") ---");
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
                    OptimizedMergeSort.sort(tmp, bestCutoff);
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
                    OptimizedMergeSort.sort(b, bestCutoff);
                    optT[r] = (System.nanoTime() - t0) / 1e6;
                    raw.println(size + "," + type + ",OptimizedMergeSort," + bestCutoff + "," + r + "," + optT[r]);
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
        raw.close();

        System.out.println("\nHoan tat toan bo benchmark.");
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
