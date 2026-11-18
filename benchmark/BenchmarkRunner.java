package com.mergesort.benchmark;

import com.mergesort.MergeSort;
import com.mergesort.OptimizedMergeSort;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;

/**
 * BenchmarkRunner executes empirical measurements of MergeSort vs OptimizedMergeSort.
 * 
 * Adheres to rigorous empirical benchmarking methodology:
 * 1. Warm-up phase to eliminate JVM cold-start and JIT compilation jitter.
 * 2. High-precision timing via System.nanoTime().
 * 3. Fresh array cloned for each trial, data generation excluded from timing.
 * 4. Outside-timing verification of sorting correctness.
 * 5. Full preservation of raw trial data and aggregated statistics.
 */
public class BenchmarkRunner {

    private static final int TRIALS = 10;
    private static final int WARMUP_ITERATIONS = 8;
    private static final int WARMUP_SIZE = 50_000;

    // Tested cutoff thresholds specified by academic assignment
    public static final int[] CUTOFFS = { 1, 2, 4, 6, 7, 8, 10, 12, 16, 20, 24, 32, 48, 64 };

    // Tested input sizes
    public static final int[] SIZES = { 1_000, 10_000, 100_000, 500_000, 1_000_000 };

    // Tested distributions
    public static final DatasetGenerator.Distribution[] DISTRIBUTIONS = {
        DatasetGenerator.Distribution.RANDOM,
        DatasetGenerator.Distribution.SORTED,
        DatasetGenerator.Distribution.REVERSED,
        DatasetGenerator.Distribution.DUPLICATES
    };

    public static void main(String[] args) {
        System.out.println("==========================================================================");
        System.out.println("  EMPIRICAL BENCHMARK: MERGE SORT CUTOFF OPTIMIZATION EVALUATION         ");
        System.out.println("  Algorithms 4th Edition (Sedgewick & Wayne) Foundation                  ");
        System.out.println("==========================================================================");

        File resultsDir = new File("data/results");
        if (!resultsDir.exists()) {
            resultsDir.mkdirs();
        }

        File rawCsvFile = new File(resultsDir, "raw_benchmark_results.csv");
        File summaryCsvFile = new File(resultsDir, "summary_statistics.csv");

        // Warm-up JVM
        System.out.println("\n[Phase 1] Performing JVM JIT warm-up (" + WARMUP_ITERATIONS + " iterations)...");
        performWarmUp();
        System.out.println("[Phase 1] JVM Warm-up complete. Steady-state compilation reached.\n");

        System.out.println("[Phase 2] Executing rigorous benchmark matrix...");

        try (PrintWriter rawWriter = new PrintWriter(new FileWriter(rawCsvFile));
             PrintWriter summaryWriter = new PrintWriter(new FileWriter(summaryCsvFile))) {

            // CSV Headers
            rawWriter.println("RunId,Size,Distribution,Algorithm,Cutoff,Trial,TimeNs,TimeMs");
            summaryWriter.println("Size,Distribution,Algorithm,Cutoff,Trials,MeanMs,MedianMs,StdDevMs,MinMs,MaxMs");

            int runId = 1;

            for (DatasetGenerator.Distribution dist : DISTRIBUTIONS) {
                System.out.println("\n==========================================================================");
                System.out.printf("  DISTRIBUTION: %-15s (Trials per config: %d)%n", dist, TRIALS);
                System.out.println("==========================================================================");

                for (int size : SIZES) {
                    System.out.printf("%n--- Size N = %,d (%s) ---%n", size, dist);
                    System.out.printf("%-18s | %-8s | %-12s | %-12s | %-12s | %-12s%n",
                            "Algorithm", "Cutoff", "Mean (ms)", "Median (ms)", "StdDev (ms)", "Min (ms)");
                    System.out.println("--------------------------------------------------------------------------------");

                    // 1. Standard MergeSort baseline (Cutoff 0)
                    BenchmarkStats stdStats = runBenchmark(size, dist, 0, false, rawWriter, runId);
                    runId += TRIALS;
                    System.out.printf("%-18s | %-8s | %-12.4f | %-12.4f | %-12.4f | %-12.4f%n",
                            "Standard Merge", "N/A", stdStats.mean, stdStats.median, stdStats.stdDev, stdStats.min);
                    writeSummary(summaryWriter, size, dist.name(), "StandardMergeSort", 0, stdStats);

                    // 2. Optimized MergeSort across all cutoff thresholds
                    for (int cutoff : CUTOFFS) {
                        BenchmarkStats optStats = runBenchmark(size, dist, cutoff, true, rawWriter, runId);
                        runId += TRIALS;
                        System.out.printf("%-18s | %-8d | %-12.4f | %-12.4f | %-12.4f | %-12.4f%n",
                                "Optimized Merge", cutoff, optStats.mean, optStats.median, optStats.stdDev, optStats.min);
                        writeSummary(summaryWriter, size, dist.name(), "OptimizedMergeSort", cutoff, optStats);
                    }

                    // Flush results after each size configuration
                    rawWriter.flush();
                    summaryWriter.flush();

                    // Hint GC to avoid mid-measurement collection
                    System.gc();
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException ignored) {}
                }
            }

            System.out.println("\n==========================================================================");
            System.out.println("  BENCHMARK EXECUTION COMPLETED SUCCESSFULLY!                            ");
            System.out.println("  Raw results preserved in:     " + rawCsvFile.getAbsolutePath());
            System.out.println("  Summary statistics stored in: " + summaryCsvFile.getAbsolutePath());
            System.out.println("==========================================================================");

        } catch (IOException e) {
            System.err.println("Fatal error during benchmark execution: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static BenchmarkStats runBenchmark(int size, DatasetGenerator.Distribution dist, int cutoff,
                                               boolean isOptimized, PrintWriter rawWriter, int startRunId) {
        double[] timesMs = new double[TRIALS];
        long[] timesNs = new long[TRIALS];

        String algoName = isOptimized ? "OptimizedMergeSort" : "StandardMergeSort";

        for (int t = 0; t < TRIALS; t++) {
            // Generate deterministic input using fixed seed per trial
            long seed = 100_000L * (t + 1) + size;
            Integer[] original = DatasetGenerator.generate(size, dist, seed);
            Integer[] copy = Arrays.copyOf(original, original.length);

            // TIMED EXECUTION REGION
            long start = System.nanoTime();
            if (isOptimized) {
                OptimizedMergeSort.sort(copy, cutoff);
            } else {
                MergeSort.sort(copy);
            }
            long elapsedNs = System.nanoTime() - start;
            // END TIMED EXECUTION REGION

            // Verify correctness outside timed region
            if (!isSorted(copy)) {
                throw new IllegalStateException("Algorithm failed to sort correctly! Size: " + size +
                        ", Cutoff: " + cutoff + ", Distribution: " + dist);
            }

            timesNs[t] = elapsedNs;
            timesMs[t] = elapsedNs / 1_000_000.0;

            // Record raw measurement
            rawWriter.printf("%d,%d,%s,%s,%d,%d,%d,%.6f%n",
                    (startRunId + t), size, dist.name(), algoName, cutoff, (t + 1), elapsedNs, timesMs[t]);
        }

        return computeStats(timesMs);
    }

    private static boolean isSorted(Comparable[] a) {
        for (int i = 1; i < a.length; i++) {
            if (a[i].compareTo(a[i - 1]) < 0) {
                return false;
            }
        }
        return true;
    }

    private static void performWarmUp() {
        for (int i = 0; i < WARMUP_ITERATIONS; i++) {
            Integer[] a1 = DatasetGenerator.generate(WARMUP_SIZE, DatasetGenerator.Distribution.RANDOM, 999L + i);
            Integer[] a2 = Arrays.copyOf(a1, a1.length);
            MergeSort.sort(a1);
            OptimizedMergeSort.sort(a2, 10);
        }
    }

    private static BenchmarkStats computeStats(double[] values) {
        int n = values.length;
        double sum = 0.0;
        double min = Double.MAX_VALUE;
        double max = Double.MIN_VALUE;

        for (double v : values) {
            sum += v;
            if (v < min) min = v;
            if (v > max) max = v;
        }

        double mean = sum / n;

        double sumSqDiff = 0.0;
        for (double v : values) {
            sumSqDiff += (v - mean) * (v - mean);
        }
        double stdDev = (n > 1) ? Math.sqrt(sumSqDiff / (n - 1)) : 0.0;

        double[] sorted = values.clone();
        Arrays.sort(sorted);
        double median;
        if (n % 2 == 0) {
            median = (sorted[n / 2 - 1] + sorted[n / 2]) / 2.0;
        } else {
            median = sorted[n / 2];
        }

        return new BenchmarkStats(mean, median, stdDev, min, max, n);
    }

    private static void writeSummary(PrintWriter writer, int size, String dist, String algo, int cutoff, BenchmarkStats stats) {
        writer.printf("%d,%s,%s,%d,%d,%.6f,%.6f,%.6f,%.6f,%.6f%n",
                size, dist, algo, cutoff, stats.trials, stats.mean, stats.median, stats.stdDev, stats.min, stats.max);
    }

    public static class BenchmarkStats {
        public final double mean;
        public final double median;
        public final double stdDev;
        public final double min;
        public final double max;
        public final int trials;

        public BenchmarkStats(double mean, double median, double stdDev, double min, double max, int trials) {
            this.mean = mean;
            this.median = median;
            this.stdDev = stdDev;
            this.min = min;
            this.max = max;
            this.trials = trials;
        }
    }
}
