package com.mergesort.benchmark;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Random;

/**
 * DatasetGenerator produces deterministic, reproducible benchmark datasets
 * across four distinct input distributions:
 * 1. RANDOM: Uniformly distributed integers.
 * 2. SORTED: Already sorted in ascending order.
 * 3. REVERSED: Strictly sorted in descending order.
 * 4. DUPLICATES: Heavily duplicated elements (drawn from small range [0..9]).
 */
public class DatasetGenerator {

    public enum Distribution {
        RANDOM,
        SORTED,
        REVERSED,
        DUPLICATES
    }

    /**
     * Generates an array of Integer based on the specified distribution and random seed.
     *
     * @param size         the number of elements
     * @param distribution the input distribution type
     * @param seed         seed for pseudo-random number generator
     * @return an array of Integer elements
     */
    public static Integer[] generate(int size, Distribution distribution, long seed) {
        Random rng = new Random(seed);
        Integer[] arr = new Integer[size];

        switch (distribution) {
            case RANDOM:
                for (int i = 0; i < size; i++) {
                    // Range [-1,000,000, 1,000,000]
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
                    // Elements drawn from 10 distinct values [0..9]
                    arr[i] = rng.nextInt(10);
                }
                break;
        }

        return arr;
    }

    /**
     * Saves an array of Integers to a file, one number per line.
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
     * Pre-generates sample input files for inspection and academic documentation.
     */
    public static void main(String[] args) {
        System.out.println("Generating sample reference datasets in data/datasets/...");
        File outputDir = new File("data/datasets");
        if (!outputDir.exists()) {
            outputDir.mkdirs();
        }

        try {
            // 1. Tiny dataset
            Integer[] tiny = {5, 2, 9, 1, 5, 6};
            saveToFile(tiny, new File(outputDir, "tiny.txt"));

            // 2. 10k sample datasets
            int sampleSize = 10_000;
            saveToFile(generate(sampleSize, Distribution.RANDOM, 42L), new File(outputDir, "random_10k.txt"));
            saveToFile(generate(sampleSize, Distribution.SORTED, 42L), new File(outputDir, "sorted_10k.txt"));
            saveToFile(generate(sampleSize, Distribution.REVERSED, 42L), new File(outputDir, "reversed_10k.txt"));
            saveToFile(generate(sampleSize, Distribution.DUPLICATES, 42L), new File(outputDir, "duplicates_10k.txt"));

            System.out.println("Sample datasets generated successfully!");
        } catch (IOException e) {
            System.err.println("Error saving datasets: " + e.getMessage());
        }
    }
}
