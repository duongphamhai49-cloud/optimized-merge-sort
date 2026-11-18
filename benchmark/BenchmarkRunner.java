package com.mergesort.benchmark;

import com.mergesort.MergeSort;
import com.mergesort.OptimizedMergeSort;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;

/**
 * BenchmarkRunner thực hiện đo đạc và phân tích thực nghiệm thuật toán (Algorithm Analysis).
 * So sánh giữa MergeSort chuẩn và MergeSort cải tiến Cutoff.
 * 
 * Tuân thủ phương pháp luận thực nghiệm khoa học nghiêm ngặt:
 * 1. Làm nóng máy ảo (JVM Warm-up) để khử sai số khởi động lạnh và ổn định JIT compiler.
 * 2. Đo đạc chính xác bằng System.nanoTime().
 * 3. Cấp phát mảng mới cho từng lượt chạy; loại bỏ thao tác sinh dữ liệu khỏi vùng bấm giờ.
 * 4. Kiểm tra tính đúng đắn bên ngoài vùng bấm giờ.
 * 5. Lưu trữ toàn bộ 3.000 phép đo thô và thống kê tổng hợp.
 */
public class BenchmarkRunner {

    private static final int TRIALS = 10;
    private static final int WARMUP_ITERATIONS = 8;
    private static final int WARMUP_SIZE = 50_000;

    // Dải giá trị CUTOFF khảo sát theo yêu cầu đề bài
    public static final int[] CUTOFFS = { 1, 2, 4, 6, 7, 8, 10, 12, 16, 20, 24, 32, 48, 64 };

    // Kích thước mảng N thử nghiệm
    public static final int[] SIZES = { 1_000, 10_000, 100_000, 500_000, 1_000_000 };

    // Các dạng phân bố dữ liệu
    public static final DatasetGenerator.Distribution[] DISTRIBUTIONS = {
        DatasetGenerator.Distribution.RANDOM,
        DatasetGenerator.Distribution.SORTED,
        DatasetGenerator.Distribution.REVERSED,
        DatasetGenerator.Distribution.DUPLICATES
    };

    public static void main(String[] args) {
        System.out.println("==========================================================================");
        System.out.println("  THỰC NGHIỆM ĐO ĐẠC VÀ ĐÁNH GIÁ NGƯỠNG CUTOFF TỐI ƯU CHO MERGESORT      ");
        System.out.println("  Dựa trên nền tảng giáo trình Algorithms 4th Edition (Sedgewick & Wayne) ");
        System.out.println("==========================================================================");

        File resultsDir = new File("data/results");
        if (!resultsDir.exists()) {
            resultsDir.mkdirs();
        }

        File rawCsvFile = new File(resultsDir, "raw_benchmark_results.csv");
        File summaryCsvFile = new File(resultsDir, "summary_statistics.csv");

        // Làm nóng JVM
        System.out.println("\n[Giai đoạn 1] Đang khởi động làm nóng JVM (" + WARMUP_ITERATIONS + " vòng lặp mồi)...");
        performWarmUp();
        System.out.println("[Giai đoạn 1] Khởi động JVM hoàn tất. JIT Compiler đã đạt trạng thái ổn định.\n");

        System.out.println("[Giai đoạn 2] Bắt đầu thực thi ma trận đo đạc thực nghiệm...");

        try (PrintWriter rawWriter = new PrintWriter(new FileWriter(rawCsvFile));
             PrintWriter summaryWriter = new PrintWriter(new FileWriter(summaryCsvFile))) {

            // Header CSV
            rawWriter.println("RunId,Size,Distribution,Algorithm,Cutoff,Trial,TimeNs,TimeMs");
            summaryWriter.println("Size,Distribution,Algorithm,Cutoff,Trials,MeanMs,MedianMs,StdDevMs,MinMs,MaxMs");

            int runId = 1;

            for (DatasetGenerator.Distribution dist : DISTRIBUTIONS) {
                System.out.println("\n==========================================================================");
                System.out.printf("  DẠNG PHÂN BỐ: %-15s (Số lần lặp mỗi cấu hình: %d)%n", dist, TRIALS);
                System.out.println("==========================================================================");

                for (int size : SIZES) {
                    System.out.printf("%n--- Kích thước N = %,d (%s) ---%n", size, dist);
                    System.out.printf("%-18s | %-8s | %-12s | %-12s | %-12s | %-12s%n",
                            "Thuật toán", "CUTOFF", "TB (ms)", "Trung vị (ms)", "Độ lệch (ms)", "Nhỏ nhất (ms)");
                    System.out.println("--------------------------------------------------------------------------------");

                    // 1. MergeSort chuẩn làm mốc đối chứng
                    BenchmarkStats stdStats = runBenchmark(size, dist, 0, false, rawWriter, runId);
                    runId += TRIALS;
                    System.out.printf("%-18s | %-8s | %-12.4f | %-12.4f | %-12.4f | %-12.4f%n",
                            "MergeSort chuẩn", "Không", stdStats.mean, stdStats.median, stdStats.stdDev, stdStats.min);
                    writeSummary(summaryWriter, size, dist.name(), "StandardMergeSort", 0, stdStats);

                    // 2. MergeSort cải tiến trên tất cả các ngưỡng Cutoff
                    for (int cutoff : CUTOFFS) {
                        BenchmarkStats optStats = runBenchmark(size, dist, cutoff, true, rawWriter, runId);
                        runId += TRIALS;
                        System.out.printf("%-18s | %-8d | %-12.4f | %-12.4f | %-12.4f | %-12.4f%n",
                                "Optimized Merge", cutoff, optStats.mean, optStats.median, optStats.stdDev, optStats.min);
                        writeSummary(summaryWriter, size, dist.name(), "OptimizedMergeSort", cutoff, optStats);
                    }

                    rawWriter.flush();
                    summaryWriter.flush();

                    System.gc();
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException ignored) {}
                }
            }

            System.out.println("\n==========================================================================");
            System.out.println("  THỰC NGHIỆM ĐO ĐẠC HOÀN THÀNH XUẤT SẮC!                                ");
            System.out.println("  Dữ liệu thô được lưu tại:        " + rawCsvFile.getAbsolutePath());
            System.out.println("  Thống kê tổng hợp được lưu tại:  " + summaryCsvFile.getAbsolutePath());
            System.out.println("==========================================================================");

        } catch (IOException e) {
            System.err.println("Lỗi nghiêm trọng trong quá trình đo đạc: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static BenchmarkStats runBenchmark(int size, DatasetGenerator.Distribution dist, int cutoff,
                                               boolean isOptimized, PrintWriter rawWriter, int startRunId) {
        double[] timesMs = new double[TRIALS];
        long[] timesNs = new long[TRIALS];

        String algoName = isOptimized ? "OptimizedMergeSort" : "StandardMergeSort";

        for (int t = 0; t < TRIALS; t++) {
            long seed = 100_000L * (t + 1) + size;
            Integer[] original = DatasetGenerator.generate(size, dist, seed);
            Integer[] copy = Arrays.copyOf(original, original.length);

            // VÙNG ĐO THỜI GIAN ĐỘC LẬP
            long start = System.nanoTime();
            if (isOptimized) {
                OptimizedMergeSort.sort(copy, cutoff);
            } else {
                MergeSort.sort(copy);
            }
            long elapsedNs = System.nanoTime() - start;
            // KẾT THÚC VÙNG ĐO THỜI GIAN

            if (!isSorted(copy)) {
                throw new IllegalStateException("Thuật toán sắp xếp sai! Kích thước: " + size +
                        ", Cutoff: " + cutoff + ", Dạng: " + dist);
            }

            timesNs[t] = elapsedNs;
            timesMs[t] = elapsedNs / 1_000_000.0;

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
