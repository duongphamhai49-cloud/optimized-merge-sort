package com.mergesort.benchmark;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Random;

/**
 * DatasetGenerator tạo ra các tập dữ liệu thực nghiệm xác định, có thể tái lập 100%
 * trên 4 dạng phân bố dữ liệu:
 * 1. RANDOM: Số nguyên ngẫu nhiên phân bố đều.
 * 2. SORTED: Mảng đã được sắp xếp tăng dần sẵn.
 * 3. REVERSED: Mảng nghịch đảo giảm dần hoàn toàn.
 * 4. DUPLICATES: Mảng chứa nhiều phần tử trùng lặp (tập giá trị nhỏ [0..9]).
 */
public class DatasetGenerator {

    public enum Distribution {
        RANDOM,
        SORTED,
        REVERSED,
        DUPLICATES
    }

    /**
     * Sinh mảng Integer dựa theo dạng phân bố và seed ngẫu nhiên xác định.
     *
     * @param size         số lượng phần tử
     * @param distribution dạng phân bố dữ liệu
     * @param seed         seed khởi tạo bộ sinh số giả ngẫu nhiên
     * @return mảng Integer tương ứng
     */
    public static Integer[] generate(int size, Distribution distribution, long seed) {
        Random rng = new Random(seed);
        Integer[] arr = new Integer[size];

        switch (distribution) {
            case RANDOM:
                for (int i = 0; i < size; i++) {
                    // Dải giá trị [-1.000.000, 1.000.000]
                    arr[i] = rng.nextInt(2_000_001) - 1_000_000;
                }
                break;

            case SORTED:
                for (int i = 0; i < size; i++) {
                    arr[i] = i;
                }
                break;

            case REVERSED:
                for (int i = 0; i < size; i++) {
                    arr[i] = size - i;
                }
                break;

            case DUPLICATES:
                for (int i = 0; i < size; i++) {
                    // Lấy ngẫu nhiên từ 10 giá trị khác nhau [0..9]
                    arr[i] = rng.nextInt(10);
                }
                break;
        }

        return arr;
    }

    /**
     * Lưu mảng Integer vào tệp tin văn bản, mỗi phần tử trên một dòng.
     */
    public static void saveToFile(Integer[] arr, File file) throws IOException {
        File parent = file.getParentFile();
        if (parent != null && !parent.exists()) {
            parent.mkdirs();
        }
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
            for (Integer val : arr) {
                writer.write(val.toString());
                writer.newLine();
            }
        }
    }

    /**
     * Tiền sinh các tệp dữ liệu mẫu để lưu trữ và kiểm tra tài liệu.
     */
    public static void main(String[] args) {
        System.out.println("Đang sinh các tập dữ liệu mẫu trong data/datasets/...");
        File outputDir = new File("data/datasets");
        if (!outputDir.exists()) {
            outputDir.mkdirs();
        }

        try {
            // 1. Tập dữ liệu nhỏ (tiny)
            Integer[] tiny = {5, 2, 9, 1, 5, 6};
            saveToFile(tiny, new File(outputDir, "tiny.txt"));

            // 2. Các tập dữ liệu mẫu 10.000 phần tử
            int sampleSize = 10_000;
            saveToFile(generate(sampleSize, Distribution.RANDOM, 42L), new File(outputDir, "random_10k.txt"));
            saveToFile(generate(sampleSize, Distribution.SORTED, 42L), new File(outputDir, "sorted_10k.txt"));
            saveToFile(generate(sampleSize, Distribution.REVERSED, 42L), new File(outputDir, "reversed_10k.txt"));
            saveToFile(generate(sampleSize, Distribution.DUPLICATES, 42L), new File(outputDir, "duplicates_10k.txt"));

            System.out.println("Đã sinh toàn bộ tập dữ liệu mẫu thành công!");
        } catch (IOException e) {
            System.err.println("Lỗi khi ghi tệp dữ liệu: " + e.getMessage());
        }
    }
}
