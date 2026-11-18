# Merge Sort tối ưu với CUTOFF

**Sinh viên:** Phạm Hải Dương - MSV: 25021700  
**Môn:** Cấu trúc Dữ liệu và Giải thuật

---

## 1. Giới thiệu và Bối cảnh Lý thuyết

Trong phân tích thuật toán, **Merge Sort** đạt độ phức tạp lý thuyết tối ưu là $O(N \log N)$ trong mọi trường hợp. Tuy nhiên, khi mảng con bị chia nhỏ đến kích thước rất bé ($N \le 1$), chi phí quản lý đệ quy (call stack) và thao tác sao chép sang mảng phụ `aux[]` tạo ra overhead đáng kể.

Kỹ thuật **CUTOFF** giải quyết vấn đề này bằng cách chuyển sang **Insertion Sort** khi kích thước đoạn con nhỏ hơn hoặc bằng một ngưỡng xác định ($hi \le lo + CUTOFF - 1$). Trong giáo trình kinh điển *Algorithms, 4th Edition*, GS. Robert Sedgewick từng đề xuất ngưỡng $CUTOFF = 7$ (ở các ấn bản cũ) và $CUTOFF = 10$ hoặc trong khoảng $8 \le CUTOFF \le 16$ (ở các ấn bản mới).

Dự án này thực nghiệm khảo sát và xác định ngưỡng **CUTOFF tối ưu** trên môi trường phần cứng thực tế, đồng thời đối chiếu hiệu năng giữa thuật toán nguyên bản và thuật toán cải tiến trên **7 kiểu phân bố dữ liệu** với kích thước lên tới 1.000.000 phần tử.

---

## 2. Đặc tả Môi trường Thực Nghiệm

Toàn bộ các phép đo được thực hiện trực tiếp trên hệ thống phần cứng và phần mềm sau:
* **Bộ xử lý (CPU):** 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz (4 Cores, 8 Threads)
* **Bộ nhớ trong (RAM):** 8 GB
* **Hệ điều hành:** Microsoft Windows 11 (64-bit)
* **Môi trường Java:** OpenJDK 21.0.11 LTS
* **Môi trường phân tích & vẽ biểu đồ:** Python 3.13 (Pandas, Matplotlib, ReportLab)

---

## 3. Phương pháp Thực Nghiệm (Algorithm Analysis)

Để đảm bảo kết quả đo lường khách quan, chính xác và có tính tái lập (reproducibility), quy trình đo tuân thủ các nguyên tắc khoa học:
1. **Khử sai số khởi động lạnh (JVM Warm-up):** Thực hiện các chu kỳ chạy mồi trước khi bấm giờ để trình biên dịch JIT (Just-In-Time) của JVM hoàn tất tối ưu mã máy.
2. **Khử nhiễu Garbage Collection (Trimmed Mean):** Khi khảo sát CUTOFF, mỗi mốc được đo 7 lần độc lập. Sử dụng phương pháp *Trimmed Mean* (tự động loại bỏ 1 lần nhanh nhất và 1 lần chậm nhất do GC pause đột biến) để lấy giá trị trung bình 5 lần chạy ổn định ở giữa.
3. **Tính tái lập:** Dữ liệu sinh bằng `java.util.Random` với seed cố định (`42` hoặc `123456`). Dữ liệu được sinh ngoài vùng đo thời gian, mỗi thuật toán nhận bản sao độc lập (`.clone()`).

---

## 4. 7 Kiểu dữ liệu thử nghiệm

1. **Random**: Phân bố ngẫu nhiên đều các số nguyên.
2. **Sorted**: Đã sắp xếp tăng dần hoàn toàn.
3. **Reversed**: Đã sắp xếp giảm dần (ngược chiều).
4. **Duplicates**: Chứa nhiều phần tử trùng lặp (chỉ 100 giá trị khác nhau).
5. **Partially Sorted (1%)**: Mảng tăng dần bị xáo trộn ngẫu nhiên 1% vị trí.
6. **Partially Sorted (5%)**: Mảng tăng dần bị xáo trộn ngẫu nhiên 5% vị trí.
7. **Partially Sorted (10%)**: Mảng tăng dần bị xáo trộn ngẫu nhiên 10% vị trí.

---

## 5. Cấu trúc Thư mục

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

## 6. Hướng dẫn chạy

### Bước 1: Biên dịch toàn bộ mã nguồn
```bash
mkdir bin
javac -d bin src/InsertionSort.java src/MergeSort.java src/OptimizedMergeSort.java src/SortTest.java
javac -d bin -cp bin benchmark/BenchmarkRunner.java
```

### Bước 2: Chạy kiểm tra tính đúng đắn (22 test case)
```bash
java -cp bin SortTest
```

### Bước 3: Chạy benchmark đo thời gian (7 bộ dữ liệu)
```bash
java -cp bin BenchmarkRunner
```
Kết quả đo sẽ tự động được lưu vào thư mục `results/`.

### Bước 4: Tạo biểu đồ và báo cáo PDF
```bash
python report/plot_charts.py
python report/generate_report.py
```

---

## 7. Kết quả thực nghiệm chính

### 7.1. Khảo sát CUTOFF tối ưu ($N = 100.000$, ngẫu nhiên)
* Thực nghiệm đo đạc từ $CUTOFF = 1$ đến $64$.
* Vùng CUTOFF hiệu quả nhất rơi vào khoảng **8 – 16**. Điểm tối ưu đạt tại **`CUTOFF = 8`** (18.41 ms), được chọn làm mốc chuẩn mực đồng nhất cho các bài so sánh diện rộng.

### 7.2. Hiệu năng theo kiểu dữ liệu ($N = 1.000.000$, CUTOFF = 8)

| Kiểu dữ liệu | MergeSort (ms) | Optimized (ms) | Cải thiện (%) |
|---|:---:|:---:|:---:|
| **Gần sắp xếp (5%)** | 422.42 | 355.87 | **+15.8%** |
| **Gần sắp xếp (1%)** | 365.07 | 314.65 | **+13.8%** |
| **Gần sắp xếp (10%)** | 499.11 | 432.68 | **+13.3%** |
| **Đã sắp xếp (Sorted)** | 353.83 | 308.57 | **+12.8%** |
| **Trùng lặp (Duplicates)** | 342.37 | 304.99 | **+10.9%** |
| **Ngẫu nhiên (Random)** | 517.35 | 488.79 | **+5.5%** |
| **Ngược chiều (Reversed)** | 349.89 | 360.06 | -2.9% |

### 7.3. Kết luận chính
1. **Hiệu quả rõ rệt trên mảng lớn:** Việc tích hợp CUTOFF = 8 giúp tiết kiệm từ 28 ms đến 66 ms trên mảng 1 triệu phần tử, giảm đáng kể chi phí cấp phát và đệ quy.
2. **Ưu thế vượt trội trên dữ liệu có thứ tự bộ phận:** Trên các tập dữ liệu Partially Sorted (1%, 5%, 10%), thuật toán cải tiến chạy nhanh hơn từ **13% đến 16%**, do Insertion Sort đạt hiệu năng tiệm cận $O(N)$ khi số nghịch thế ít.
3. **Tính ứng dụng thực tế:** Kỹ thuật CUTOFF là một cải tiến chi phí thấp nhưng mang lại giá trị thực tiễn cao, hoàn toàn phù hợp để tích hợp vào các thư viện sắp xếp chuẩn.

> Toàn bộ phân tích lý thuyết, bảng số liệu và 3 hình minh họa được trình bày trong file `report/BAO_CAO.pdf`.
