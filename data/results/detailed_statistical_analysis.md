# Báo Cáo Phân Tích Thống Kê Chi Tiết Thực Nghiệm MergeSort Cutoff

## 1. Tổng Quan Điều Kiện Thực Nghiệm
- Tổng số cấu hình đo lường: 300
- Tổng số lượt chạy đo đạc thời gian thực tế: 3000

## 2. Xác Định Ngưỡng Cutoff Tối Ưu Theo Quy Mô Mảng (Dữ Liệu Ngẫu Nhiên)

| Kích thước mảng (N) | MergeSort chuẩn (ms) | Cutoff Tối ưu | Thời gian tối ưu (ms) | Cutoff = 7 (ms) | Cutoff = 10 (ms) | Mức cải thiện (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1,000 | 0.1425 | 12 | 0.0955 | 0.1002 | 0.0964 | +32.97% |
| 10,000 | 1.8026 | 20 | 1.2723 | 1.3489 | 1.3130 | +29.42% |
| 100,000 | 23.2767 | 4 | 20.2456 | 22.9241 | 22.4130 | +13.02% |
| 500,000 | 228.6152 | 6 | 203.8703 | 215.6855 | 205.6245 | +10.82% |
| 1,000,000 | 525.6362 | 4 | 511.1456 | 600.4282 | 528.8466 | +2.76% |


## 3. Đánh Giá Ảnh Hưởng Của Phân Bố Dữ Liệu (N = 500.000)

| Phân bố dữ liệu | MergeSort chuẩn (ms) | Cutoff = 7 (ms) | Cutoff = 10 (ms) | Cutoff Tối ưu | Thời gian tối ưu (ms) | Tỷ lệ cải thiện (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Ngẫu nhiên (Random) | 228.6152 | 215.6855 | 205.6245 | 6 | 203.8703 | +10.82% |
| Đã sắp xếp (Sorted) | 140.7348 | 146.7049 | 131.3725 | 64 | 100.0152 | +28.93% |
| Nghịch đảo (Reversed) | 146.4273 | 139.9982 | 146.9426 | 4 | 139.4070 | +4.79% |
| Trùng lặp (Duplicates) | 143.2311 | 131.6191 | 129.8196 | 12 | 129.0968 | +9.87% |
