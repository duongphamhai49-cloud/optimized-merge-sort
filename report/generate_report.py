import pandas as pd
import os, sys

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, Image, PageBreak)
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Cai dat reportlab: pip install reportlab")
    sys.exit(1)

# Dang ky font Times New Roman ho tro tieng Viet
FONT_PATH = r"C:\Windows\Fonts\times.ttf"
FONT_BOLD = r"C:\Windows\Fonts\timesbd.ttf"
FONT_ITALIC = r"C:\Windows\Fonts\timesi.ttf"

pdfmetrics.registerFont(TTFont('Times', FONT_PATH))
pdfmetrics.registerFont(TTFont('Times-Bold', FONT_BOLD))
pdfmetrics.registerFont(TTFont('Times-Italic', FONT_ITALIC))

OUT_PDF = "report/BAO_CAO.pdf"
os.makedirs("report/figures", exist_ok=True)

doc = SimpleDocTemplate(
    OUT_PDF, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

styles = getSampleStyleSheet()
W = A4[0] - 4.5*cm

def style(name='Normal', font='Times', size=11, leading=16, space_before=0, space_after=6, alignment=0, bold=False):
    return ParagraphStyle(
        name,
        fontName='Times-Bold' if bold else font,
        fontSize=size,
        leading=leading,
        spaceBefore=space_before,
        spaceAfter=space_after,
        alignment=alignment,
    )

S_title   = style('Title',   size=16, leading=20, bold=True, alignment=1, space_after=4)
S_sub     = style('Sub',     size=12, leading=16, alignment=1, space_after=2)
S_h1      = style('H1',      size=13, leading=18, bold=True, space_before=14, space_after=6)
S_h2      = style('H2',      size=12, leading=16, bold=True, space_before=10, space_after=4)
S_body    = style('Body',    size=11, leading=16, space_after=6)
S_caption = style('Caption', size=10, leading=14, font='Times-Italic', alignment=1, space_after=10)

def p(text, s=None):
    return Paragraph(text, s or S_body)

def h1(text): return Paragraph(text, S_h1)
def h2(text): return Paragraph(text, S_h2)
def sp(h=8): return Spacer(1, h)

# --- Doc du lieu ket qua ---
cutoff_df = pd.read_csv('results/cutoff_results.csv')
summary_df = pd.read_csv('results/summary.csv')
best_cutoff = int(cutoff_df.loc[cutoff_df['time_ms'].idxmin(), 'cutoff'])
best_time   = cutoff_df['time_ms'].min()

def fig(path, w_cm=14, caption=''):
    items = []
    if os.path.exists(path):
        items.append(Image(path, width=w_cm*cm, height=w_cm*cm*0.62))
    if caption:
        items.append(p(caption, S_caption))
    return items

def tbl(data, col_widths=None):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Times'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN',    (0,0), (-1,-1), 'CENTER'),
        ('GRID',     (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.Color(0.85, 0.85, 0.85)),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.Color(0.95,0.95,0.95)]),
        ('TOPPADDING',  (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

# ============================================================
# XAY DUNG NOI DUNG PDF
# ============================================================
story = []

# --- Trang bia ---
story += [
    sp(60),
    p('TRƯỜNG ĐẠI HỌC CÔNG NGHỆ — ĐHQG HÀ NỘI', S_sub),
    p('Khoa Công nghệ Thông tin', S_sub),
    sp(40),
    p('BÁO CÁO THỰC NGHIỆM', S_title),
    p('MÔN: CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT', S_sub),
    sp(30),
    p('<b>Đề tài:</b> Merge Sort tối ưu với ngưỡng chuyển sang Insertion Sort (Cutoff)', S_body),
    sp(50),
    p('Sinh viên:  <b>Phạm Hải Dương</b>', S_body),
    p('Mã sinh viên:  <b>25021700</b>', S_body),
    p('Ngành:  Khoa học Máy tính', S_body),
    sp(80),
    p('Hà Nội, 2026', style('footer', size=11, alignment=1)),
    PageBreak(),
]

# --- 1. Gioi thieu ---
story += [
    h1('1. Giới thiệu'),
    p('Merge Sort là thuật toán sắp xếp chia để trị kinh điển với độ phức tạp thời gian '
      'O(n log n) trong mọi trường hợp. Tuy nhiên, khi mảng con đã được chia nhỏ xuống kích thước nhỏ, '
      'chi phí phân nhánh đệ quy và cấp phát mảng phụ lại tạo ra overhead đáng kể. '
      'Ngược lại, Insertion Sort dù có độ phức tạp O(n²) trong trường hợp xấu nhất nhưng lại '
      'chạy cực nhanh trên các mảng nhỏ và mảng gần như đã có thứ tự.'),
    p('Đề tài thực hiện khảo sát kỹ thuật tối ưu Cutoff: khi kích thước mảng con '
      '<i>≤ cutoff</i>, chuyển sang dùng Insertion Sort thay vì tiếp tục đệ quy. '
      'Thực nghiệm được thực hiện trên <b>7 kiểu phân bố dữ liệu</b> khác nhau để đánh giá toàn diện.'),
]

# --- 2. Thuat toan ---
story += [
    h1('2. Mô tả thuật toán và bộ dữ liệu'),
    h2('2.1. Cài đặt thuật toán'),
    p('Cả ba thuật toán (MergeSort, InsertionSort, OptimizedMergeSort) được cài đặt tuân thủ '
      'chính xác giáo trình <i>Algorithms 4th Edition</i> (Robert Sedgewick &amp; Kevin Wayne). '
      'Mảng phụ aux[] được cấp phát một lần duy nhất. Với OptimizedMergeSort, điều kiện ngắt là '
      '<i>hi ≤ lo + cutoff − 1</i>.'),
    h2('2.2. Bảy kiểu phân bố dữ liệu thử nghiệm'),
    p('1. <b>Ngẫu nhiên (Random):</b> Các giá trị sinh ngẫu nhiên đồng đều.<br/>'
      '2. <b>Đã sắp xếp (Sorted):</b> Mảng tăng dần hoàn toàn (0, 1, 2, ..., n-1).<br/>'
      '3. <b>Ngược chiều (Reversed):</b> Mảng giảm dần hoàn toàn (n-1, ..., 0).<br/>'
      '4. <b>Trùng lặp (Duplicates):</b> Mảng chứa nhiều phần tử trùng lặp (chỉ có 100 giá trị khác nhau).<br/>'
      '5. <b>Gần sắp xếp 1% (Partially Sorted 1%):</b> Mảng tăng dần bị xáo trộn ngẫu nhiên 1% vị trí.<br/>'
      '6. <b>Gần sắp xếp 5% (Partially Sorted 5%):</b> Mảng tăng dần bị xáo trộn ngẫu nhiên 5% vị trí.<br/>'
      '7. <b>Gần sắp xếp 10% (Partially Sorted 10%):</b> Mảng tăng dần bị xáo trộn ngẫu nhiên 10% vị trí.'),
]

# --- 3. Moi truong thuc nghiem ---
story += [
    h1('3. Môi trường thực nghiệm'),
    tbl([
        ['Thành phần', 'Chi tiết'],
        ['Hệ điều hành', 'Windows 11'],
        ['JDK', 'OpenJDK 21.0.11 LTS'],
        ['Phương pháp đo', 'System.nanoTime()'],
        ['Số bộ dữ liệu', '7 kiểu phân bố'],
        ['Kích thước kiểm thử (n)', '1.000; 10.000; 100.000; 500.000; 1.000.000'],
        ['Số lần lặp mỗi trường hợp', '5 lần (lấy trung bình cộng)'],
        ['JVM warm-up', '3 lần chạy thử trước khi bấm giờ'],
    ], col_widths=[7*cm, 9*cm]),
]

# --- 4. Ket qua ---
story += [
    h1('4. Kết quả thực nghiệm'),
    h2('4.1. Ảnh hưởng của giá trị Cutoff (n = 100.000, dữ liệu ngẫu nhiên)'),
]

cutoff_data = [['Cutoff', 'Thời gian TB (ms)']]
for _, row in cutoff_df.iterrows():
    c = int(row['cutoff'])
    marker = ' ← tối ưu' if c == best_cutoff else ''
    cutoff_data.append([str(c), f"{row['time_ms']:.3f}{marker}"])
story.append(tbl(cutoff_data, col_widths=[5*cm, 8*cm]))
story.append(sp(6))
story += fig('report/figures/fig1_cutoff_vs_time.png', 13,
             f'Hình 1. Thời gian chạy theo giá trị cutoff (n=100.000, ngẫu nhiên). Cutoff tối ưu là {best_cutoff} ({best_time:.2f} ms).')

story.append(h2('4.2. So sánh theo kích thước mảng (Dữ liệu ngẫu nhiên)'))
rand_df = summary_df[summary_df['type'] == 'random'].sort_values('size')
size_data = [['Kích thước (n)', 'MergeSort (ms)', 'Optimized (ms)', 'Giảm (%)']]
for _, row in rand_df.iterrows():
    size_data.append([
        f"{int(row['size']):,}",
        f"{row['merge_ms']:.2f}",
        f"{row['optimized_ms']:.2f}",
        f"{row['speedup_pct']:.1f}%"
    ])
story.append(tbl(size_data, col_widths=[4*cm, 4*cm, 4*cm, 4*cm]))
story.append(sp(6))
story += fig('report/figures/fig2_size_vs_time.png', 13,
             'Hình 2. Thời gian sắp xếp theo kích thước mảng trên dữ liệu ngẫu nhiên.')

story.append(h2('4.3. Hiệu năng trên 7 kiểu dữ liệu (n = 1.000.000)'))
large_df = summary_df[summary_df['size'] == 1000000]
type_names = {
    'random': 'Ngẫu nhiên',
    'sorted': 'Đã sắp xếp',
    'reversed': 'Ngược chiều',
    'duplicates': 'Nhiều trùng lặp',
    'partially_sorted_1pct': 'Gần sắp xếp (1%)',
    'partially_sorted_5pct': 'Gần sắp xếp (5%)',
    'partially_sorted_10pct': 'Gần sắp xếp (10%)'
}
dist_data = [['Kiểu phân bố dữ liệu', 'MergeSort (ms)', 'Optimized (ms)', 'Giảm (%)']]
for _, row in large_df.iterrows():
    dist_data.append([
        type_names.get(row['type'], row['type']),
        f"{row['merge_ms']:.2f}",
        f"{row['optimized_ms']:.2f}",
        f"{row['speedup_pct']:.1f}%"
    ])
story.append(tbl(dist_data, col_widths=[5*cm, 4*cm, 4*cm, 3*cm]))
story.append(sp(6))
story += fig('report/figures/fig4_distribution.png', 13.5,
             'Hình 4. So sánh hiệu năng giữa MergeSort và OptimizedMergeSort trên 7 kiểu dữ liệu (n = 1.000.000).')

# --- 5. Nhan xet ---
story += [
    h1('5. Nhận xét và kết luận'),
    p(f'1. <b>Vùng Cutoff tối ưu:</b> Giá trị cutoff tốt nhất đo được rơi vào khoảng <b>6–16</b> '
      f'(trong lần chạy này đạt cực tiểu tại cutoff = {best_cutoff} với {best_time:.2f} ms). '
      'Khi cutoff quá nhỏ (1–4), việc chuyển đổi chưa triệt tiêu được overhead đệ quy. '
      'Khi cutoff quá lớn (> 32), chi phí O(k²) của Insertion Sort trên mảng con bắt đầu lấn át.'),
    p('2. <b>Đặc tính trên dữ liệu Partially Sorted (1%, 5%, 10%):</b> '
      'Insertion Sort có ưu thế vượt trội khi số lượng nghịch thế (inversions) nhỏ. '
      'Ở các mảng con gần như đã có thứ tự (1% và 5% xáo trộn), việc chuyển sang Insertion Sort '
      'giúp OptimizedMergeSort giảm từ 11% đến 18% thời gian so với MergeSort chuẩn.'),
    p('3. <b>Kết luận:</b> Cải tiến Cutoff sang Insertion Sort là phương pháp đơn giản nhưng '
      'đem lại hiệu quả thực tế rõ rệt trên hầu hết các kiểu dữ liệu, đặc biệt trên dữ liệu có kích thước lớn '
      'và dữ liệu đã có sẵn thứ tự bộ phận.'),
]

doc.build(story)
print(f"Da tao thanh cong: {OUT_PDF}")
