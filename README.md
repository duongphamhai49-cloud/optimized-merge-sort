# Merge Sort tối ưu với Cutoff

**Sinh viên:** Phạm Hải Dương — MSV: 25021700  
**Ngành:** Khoa học Máy tính — Trường ĐH Công nghệ, ĐHQGHN  
**Môn:** Cấu trúc Dữ liệu và Giải thuật

---

## Giới thiệu

Dự án cài đặt và thực nghiệm thuật toán **Merge Sort tối ưu**: khi kích thước mảng con ≤ `cutoff`, chuyển sang dùng **Insertion Sort** thay vì tiếp tục đệ quy. Mục tiêu là tìm giá trị cutoff tốt nhất.

Cả ba thuật toán đều cài đặt theo giáo trình *Algorithms 4th Edition* (Sedgewick & Wayne).

---

## Cấu trúc thư mục

```
optimized-merge-sort/
├── src/
│   ├── InsertionSort.java       # Thuật toán Insertion Sort
│   ├── MergeSort.java           # Thuật toán Merge Sort chuẩn
│   ├── OptimizedMergeSort.java  # Merge Sort với cutoff
│   └── SortTest.java            # Bộ kiểm tra tính đúng đắn
├── benchmark/
│   └── BenchmarkRunner.java     # Chương trình đo thời gian
├── results/
│   ├── raw_results.csv          # Kết quả thô
│   ├── summary.csv              # Tóm tắt so sánh hai thuật toán
│   └── cutoff_results.csv       # Thời gian theo từng giá trị cutoff
├── report/
│   ├── figures/                 # Biểu đồ kết quả
│   ├── BAO_CAO.pdf              # Báo cáo chính
│   ├── plot_charts.py           # Script vẽ biểu đồ
│   └── generate_report.py       # Script tạo PDF
├── logs/
│   └── ai_conversation_log.md  # Nhật ký làm việc với AI
└── README.md
```

---

## Hướng dẫn chạy

### 1. Biên dịch

```bash
# Tạo thư mục bin
mkdir bin

# Biên dịch thuật toán
javac -d bin src/InsertionSort.java src/MergeSort.java src/OptimizedMergeSort.java src/SortTest.java

# Biên dịch benchmark
javac -d bin -cp bin benchmark/BenchmarkRunner.java
```

### 2. Chạy kiểm tra tính đúng đắn

```bash
java -cp bin SortTest
```

### 3. Chạy benchmark

```bash
java -cp bin BenchmarkRunner
```

Kết quả lưu tại `results/`.

### 4. Tạo biểu đồ và báo cáo PDF

```bash
python report/plot_charts.py
python report/generate_report.py
```

---

## Kết quả chính

| Cutoff tối ưu | n = 100.000, ngẫu nhiên |
|---|---|
| **10** | 19.5 ms (thấp nhất) |

| n | MergeSort | Optimized | Giảm |
|---|---|---|---|
| 1.000 | 0.54 ms | 0.22 ms | 58% |
| 100.000 | 24.4 ms | 25.8 ms | — |
| 500.000 | 312 ms | 236 ms | 24% |
| 1.000.000 | 620 ms | 540 ms | 13% |

Xem chi tiết trong `report/BAO_CAO.pdf`.
