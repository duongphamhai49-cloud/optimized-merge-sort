# Merge Sort tối ưu với CUTOFF

**Sinh viên:** Phạm Hải Dương — MSV: 25021700  
**Môn:** Cấu trúc Dữ liệu và Giải thuật

---

## Giới thiệu

Dự án cài đặt và thực nghiệm thuật toán **Merge Sort tối ưu**: khi kích thước mảng con ≤ `CUTOFF`, chuyển sang dùng **Insertion Sort** thay vì tiếp tục đệ quy. 

Cả ba thuật toán đều cài đặt theo đúng giáo trình *Algorithms 4th Edition* (Sedgewick & Wayne). Qua thực nghiệm khảo sát, giá trị **CUTOFF = 16** được xác định là mốc tối ưu nhất và được sử dụng đồng nhất trong toàn bộ các phân tích so sánh tiếp theo.

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
│   ├── OptimizedMergeSort.java  # Merge Sort với CUTOFF = 16
│   └── SortTest.java            # Bộ kiểm tra tính đúng đắn (22/22 tests PASS)
├── benchmark/
│   └── BenchmarkRunner.java     # Đo thời gian trên 7 kiểu dữ liệu (CUTOFF = 16)
├── results/
│   ├── raw_results.csv          # Toàn bộ số liệu đo thô
│   ├── summary.csv              # Bảng tóm tắt kết quả
│   └── cutoff_results.csv       # Kết quả khảo sát các giá trị CUTOFF
├── report/
│   ├── figures/                 # 4 biểu đồ kết quả (.png không title, tiếng Việt)
│   ├── BAO_CAO.pdf              # Báo cáo PDF chính thức (2 trang gọn gàng)
│   ├── plot_charts.py           # Script vẽ biểu đồ (CUTOFF = 16)
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
* Vùng CUTOFF hiệu quả nhất: **8 – 16** (loại bỏ từ 3 đến 4 tầng đệ quy nhị phân dưới cùng). Mốc **CUTOFF = 16** được chọn làm chuẩn tối ưu cho thuật toán cải tiến.

### 2. Hiệu năng theo kiểu dữ liệu (n = 1.000.000, CUTOFF = 16)

| Kiểu dữ liệu | MergeSort (ms) | Optimized (ms) | Cải thiện (%) |
|---|---|---|---|
| **Đã sắp xếp (Sorted)** | 324.83 | 259.17 | **+20.2%** |
| **Gần sắp xếp (1%)** | 331.65 | 275.66 | **+16.9%** |
| **Gần sắp xếp (5%)** | 370.48 | 314.45 | **+15.1%** |
| **Gần sắp xếp (10%)** | 405.06 | 349.66 | **+13.7%** |
| **Trùng lặp (Duplicates)** | 320.73 | 306.28 | **+4.5%** |
| **Ngẫu nhiên (Random)** | 574.79 | 573.94 | **+0.1%** |
| **Ngược chiều (Reversed)** | 327.90 | 367.05 | -11.9% |

> Toàn bộ phân tích lý thuyết, bảng số liệu và 3 hình minh họa được trình bày trong file `report/BAO_CAO.pdf`.
