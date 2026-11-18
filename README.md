# Merge Sort tối ưu với CUTOFF

**Sinh viên:** Phạm Hải Dương - MSV: 25021700  
**Môn:** Cấu trúc Dữ liệu và Giải thuật

---

## Giới thiệu

Dự án cài đặt và thực nghiệm thuật toán **Merge Sort tối ưu**: khi kích thước mảng con ≤ `CUTOFF`, chuyển sang dùng **Insertion Sort** thay vì tiếp tục đệ quy. 

Cả ba thuật toán đều cài đặt theo đúng giáo trình *Algorithms 4th Edition* (Sedgewick & Wayne). Qua thực nghiệm khảo sát, giá trị **CUTOFF = 8** được xác định là mốc tối ưu nhất (18.41 ms) và được sử dụng đồng nhất trong toàn bộ các phân tích so sánh diện rộng.

---

## 7 Kiểu dữ liệu thử nghiệm

1. **Random**: Phân bố ngẫu nhiên đều.
2. **Sorted**: Đã sắp xếp tăng dần hoàn toàn.
3. **Reversed**: Đã sắp xếp giảm dần (ngược chiều).
4. **Duplicates**: Chứa nhiều phần tử trùng lặp (chỉ 100 giá trị khác nhau).
5. **Partially Sorted (1%)**: Mảng tăng dần bị xáo trộn ngẫu nhiên 1% vị trí.
6. **Partially Sorted (5%)**: Mảng tăng dần bị xáo trộn ngẫu nhiên 5% vị trí.
7. **Partially Sorted (10%)**: Mảng tăng dần bị xáo trộn ngẫu nhiên 10% vị trí.

---

## Cấu trúc thư mục

```
optimized-merge-sort/
├── src/
│   ├── InsertionSort.java       # Thuật toán Insertion Sort
│   ├── MergeSort.java           # Thuật toán Merge Sort chuẩn
│   ├── OptimizedMergeSort.java  # Merge Sort với CUTOFF = 8
│   └── SortTest.java            # Bộ kiểm tra tính đúng đắn
├── benchmark/
│   └── BenchmarkRunner.java     # Đo thời gian trên 7 kiểu dữ liệu
├── results/
│   ├── raw_results.csv          # Toàn bộ số liệu đo thô
│   ├── summary.csv              # Bảng tóm tắt kết quả
│   └── cutoff_results.csv       # Kết quả khảo sát các giá trị CUTOFF
├── report/
│   ├── figures/                 # 4 biểu đồ kết quả
│   ├── BAO_CAO.pdf              # Báo cáo PDF chính thức
│   ├── plot_charts.py           # Script vẽ biểu đồ
│   └── generate_report.py       # Script xuất PDF
├── logs/
│   └── ai_conversation_log.md  # Nhật ký làm việc với AI
├── .gitignore
└── README.md
```

---

## Hướng dẫn chạy

### 1. Biên dịch
```bash
mkdir bin
javac -d bin src/InsertionSort.java src/MergeSort.java src/OptimizedMergeSort.java src/SortTest.java
javac -d bin -cp bin benchmark/BenchmarkRunner.java
```

### 2. Chạy kiểm tra tính đúng đắn (22 test case)
```bash
java -cp bin SortTest
```

### 3. Chạy benchmark đo thời gian (7 bộ dữ liệu)
```bash
java -cp bin BenchmarkRunner
```

### 4. Tạo biểu đồ và báo cáo PDF
```bash
python report/plot_charts.py
python report/generate_report.py
```

---

## Kết quả thực nghiệm chính

### 1. Khảo sát CUTOFF tối ưu (n = 100.000, ngẫu nhiên)
* Vùng CUTOFF hiệu quả nhất: **8 – 16**. Giá trị đạt thời gian thấp nhất là **CUTOFF = 8** (18.41 ms), được chọn làm chuẩn tối ưu cho thuật toán cải tiến trong toàn bộ bài toán.

### 2. Hiệu năng theo kiểu dữ liệu (n = 1.000.000, CUTOFF = 8)

| Kiểu dữ liệu | MergeSort (ms) | Optimized (ms) | Cải thiện (%) |
|---|---|---|---|
| **Gần sắp xếp (5%)** | 422.42 | 355.87 | **+15.8%** |
| **Gần sắp xếp (1%)** | 365.07 | 314.65 | **+13.8%** |
| **Gần sắp xếp (10%)** | 499.11 | 432.68 | **+13.3%** |
| **Đã sắp xếp (Sorted)** | 353.83 | 308.57 | **+12.8%** |
| **Trùng lặp (Duplicates)** | 342.37 | 304.99 | **+10.9%** |
| **Ngẫu nhiên (Random)** | 517.35 | 488.79 | **+5.5%** |
| **Ngược chiều (Reversed)** | 349.89 | 360.06 | -2.9% |

> Toàn bộ phân tích lý thuyết, bảng số liệu và 3 hình minh họa được trình bày trong file `report/BAO_CAO.pdf`.
