import pandas as pd
import os, sys

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, Image, HRFlowable)
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Cài đặt reportlab: pip install reportlab")
    sys.exit(1)

# Đăng ký font Times New Roman hỗ trợ tiếng Việt
FONT_PATH = r"C:\Windows\Fonts\times.ttf"
FONT_BOLD = r"C:\Windows\Fonts\timesbd.ttf"
FONT_ITALIC = r"C:\Windows\Fonts\timesi.ttf"

pdfmetrics.registerFont(TTFont('Times', FONT_PATH))
pdfmetrics.registerFont(TTFont('Times-Bold', FONT_BOLD))
pdfmetrics.registerFont(TTFont('Times-Italic', FONT_ITALIC))

OUT_PDF = "report/BAO_CAO.pdf"
os.makedirs("report/figures", exist_ok=True)

# Can le chuan: top=1.8cm, bottom=1.8cm, left=2cm, right=2cm
doc = SimpleDocTemplate(
    OUT_PDF, pagesize=A4,
    leftMargin=2.0*cm, rightMargin=2.0*cm,
    topMargin=1.8*cm, bottomMargin=1.8*cm
)

styles = getSampleStyleSheet()

def style(name, font='Times', size=10, leading=14, space_before=0, space_after=4, alignment=0, bold=False):
    return ParagraphStyle(
        name,
        fontName='Times-Bold' if bold else font,
        fontSize=size,
        leading=leading,
        spaceBefore=space_before,
        spaceAfter=space_after,
        alignment=alignment,
    )

S_title   = style('Title',   size=15, leading=19, bold=True, alignment=1, space_after=2)
S_sub     = style('Sub',     size=10.5, leading=14, alignment=1, space_after=6)
S_h1      = style('H1',      size=11, leading=14.5, bold=True, space_before=7, space_after=2.5)
S_h2      = style('H2',      size=10, leading=13.5, bold=True, space_before=4, space_after=2)
S_body    = style('Body',    size=9.2, leading=13, space_after=3.5)
S_caption = style('Caption', size=8.5, leading=11, font='Times-Italic', alignment=1, space_after=5)

def p(text, s=None): return Paragraph(text, s or S_body)
def h1(text): return Paragraph(text, S_h1)
def h2(text): return Paragraph(text, S_h2)
def sp(h=3): return Spacer(1, h)

# --- Doc du lieu ket qua ---
cutoff_df = pd.read_csv('results/cutoff_results.csv')
summary_df = pd.read_csv('results/summary.csv')

best_cutoff = int(cutoff_df.loc[cutoff_df['time_ms'].idxmin(), 'cutoff'])
best_time   = cutoff_df['time_ms'].min()

def fig(path, w_cm=11.5, h_cm=4.8, caption=''):
    items = []
    if os.path.exists(path):
        items.append(Image(path, width=w_cm*cm, height=h_cm*cm))
    if caption:
        items.append(p(caption, S_caption))
    return items

def tbl(data, col_widths=None, font_size=8.5):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Times'),
        ('FONTSIZE', (0,0), (-1,-1), font_size),
        ('ALIGN',    (0,0), (-1,-1), 'CENTER'),
        ('GRID',     (0,0), (-1,-1), 0.5, colors.Color(0.4, 0.4, 0.4)),
        ('BACKGROUND', (0,0), (-1,0), colors.Color(0.9, 0.9, 0.9)),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.Color(0.97, 0.97, 0.97)]),
        ('TOPPADDING',  (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    return t

story = []

# ============================================================
# PHAN DAU: TIEU DE VA THONG TIN THEO DUNG YEU CAU
# ============================================================
story += [
    p('BÁO CÁO THỰC NGHIỆM', S_title),
    p('TỐI ƯU HÓA MERGE SORT VỚI CUTOFF', S_title),
    sp(2),
    p('Sinh viên: Phạm Hải Dương &nbsp;|&nbsp; MSV: 25021700', S_sub),
    HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=2, spaceAfter=6),
]

# ============================================================
# 1. TONG QUAN DE TAI
# ============================================================
story += [
    h1('1. Giới thiệu và Bối cảnh Lý thuyết'),
    p('<b>Mục tiêu:</b> Khảo sát kỹ thuật cải tiến Merge Sort bằng cách chuyển sang Insertion Sort khi kích thước mảng con nhỏ hơn hoặc bằng một ngưỡng <b>CUTOFF</b> nhất định (<i>hi ≤ lo + CUTOFF − 1</i>).'),
    p('<b>Bối cảnh lý thuyết:</b> Merge Sort đạt độ phức tạp lý thuyết O(N log N) nhưng phát sinh overhead lớn khi phân rã đệ quy đến mảng con kích thước nhỏ. Trong giáo trình <i>Algorithms 4th Edition</i>, GS. Robert Sedgewick từng đề xuất CUTOFF = 7 (ấn bản cũ) và CUTOFF = 10 hoặc trong khoảng 8–16 (ấn bản mới). Nghiên cứu này nhằm kiểm chứng thực nghiệm ngưỡng tối ưu trên phần cứng hiện đại.'),
]

# ============================================================
# 2. MOI TRUONG VA PHUONG PHAP
# ============================================================
story += [
    h1('2. Môi trường và Phương pháp Thực nghiệm'),
    p('• <b>Môi trường đo:</b> CPU Intel Core i5-1135G7 (4 Cores, 8 Threads, 2.40 GHz), RAM 8 GB, Windows 11 64-bit, OpenJDK 21.0.11 LTS, Python 3.13 (Matplotlib, ReportLab).'),
    p('• <b>Phương pháp đo:</b> Sử dụng <code>System.nanoTime()</code> kết hợp JVM warm-up. Khi khảo sát CUTOFF, đo 7 lần và áp dụng phương pháp <i>Trimmed Mean</i> (loại trừ giá trị ngoại lai do Garbage Collection pause) để đảm bảo tính khách quan và ổn định.'),
    p('• <b>7 bộ dữ liệu thử nghiệm:</b> (1) Random; (2) Sorted; (3) Reversed; (4) Duplicates; (5) Partially Sorted 1%; (6) Partially Sorted 5%; (7) Partially Sorted 10%. Mảng Partially Sorted k% được tạo bằng cách lấy mảng đã sắp xếp rồi hoán đổi ngẫu nhiên k% số phần tử.'),
]

# ============================================================
# 3. KET QUA THUC NGHIEM
# ============================================================
story += [
    h1('3. Kết quả thực nghiệm và Phân tích'),
    h2('3.1. Xác định giá trị CUTOFF tối ưu (N = 100.000, dữ liệu ngẫu nhiên)'),
]

# Bang CUTOFF dang ngang
cutoff_row1 = ['CUTOFF'] + [str(int(c)) for c in cutoff_df['cutoff'][:7]]
time_row1   = ['Thời gian (ms)'] + [f"{t:.1f}" for t in cutoff_df['time_ms'][:7]]
cutoff_row2 = ['CUTOFF'] + [str(int(c)) for c in cutoff_df['cutoff'][7:]]
time_row2   = ['Thời gian (ms)'] + [f"{t:.1f}" for t in cutoff_df['time_ms'][7:]]

cutoff_table_data = [cutoff_row1, time_row1, cutoff_row2, time_row2]
for r in [1, 3]:
    for c_idx in range(1, len(cutoff_table_data[r])):
        c_val = int(cutoff_table_data[r-1][c_idx])
        if c_val == best_cutoff:
            cutoff_table_data[r][c_idx] += ' *'

story.append(tbl(cutoff_table_data, col_widths=[2.8*cm] + [1.8*cm]*7, font_size=8))
story.append(sp(3))
story += fig('report/figures/fig1_cutoff_vs_time.png', w_cm=11.5, h_cm=4.6,
             caption=f'Hình 1. Thời gian chạy theo giá trị CUTOFF (N = 100.000, ngẫu nhiên). Giá trị tối ưu: CUTOFF = {best_cutoff} ({best_time:.2f} ms).')

story.append(h2(f'3.2. So sánh hiệu năng theo kích thước mảng (Dữ liệu ngẫu nhiên, CUTOFF = {best_cutoff})'))
rand_df = summary_df[summary_df['type'] == 'random'].sort_values('size')
size_data = [['Kích thước (N)', 'MergeSort (ms)', 'Optimized (ms)', 'Tốc độ cải thiện']]
for _, row in rand_df.iterrows():
    size_data.append([
        f"{int(row['size']):,}",
        f"{row['merge_ms']:.2f}",
        f"{row['optimized_ms']:.2f}",
        f"{row['speedup_pct']:+.1f}%"
    ])
story.append(tbl(size_data, col_widths=[4.0*cm, 4.0*cm, 4.0*cm, 4.0*cm], font_size=8.5))
story.append(sp(3))
story += fig('report/figures/fig2_size_vs_time.png', w_cm=11.5, h_cm=4.6,
             caption=f'Hình 2. Thời gian chạy của MergeSort và OptimizedMergeSort (CUTOFF = {best_cutoff}) theo kích thước mảng.')

story.append(h2(f'3.3. Đánh giá hiệu năng trên 7 kiểu dữ liệu (N = 1.000.000, CUTOFF = {best_cutoff})'))
large_df = summary_df[summary_df['size'] == 1000000]
type_names = {
    'random': 'Ngẫu nhiên (Random)',
    'sorted': 'Đã sắp xếp (Sorted)',
    'reversed': 'Ngược chiều (Reversed)',
    'duplicates': 'Nhiều trùng lặp (Duplicates)',
    'partially_sorted_1pct': 'Gần sắp xếp 1% (Partially 1%)',
    'partially_sorted_5pct': 'Gần sắp xếp 5% (Partially 5%)',
    'partially_sorted_10pct': 'Gần sắp xếp 10% (Partially 10%)'
}
dist_data = [['Kiểu phân bố dữ liệu', 'MergeSort (ms)', 'Optimized (ms)', 'Cải thiện (%)']]
for _, row in large_df.iterrows():
    dist_data.append([
        type_names.get(row['type'], row['type']),
        f"{row['merge_ms']:.2f}",
        f"{row['optimized_ms']:.2f}",
        f"{row['speedup_pct']:+.1f}%"
    ])
story.append(tbl(dist_data, col_widths=[5.5*cm, 3.5*cm, 3.5*cm, 3.5*cm], font_size=8.5))
story.append(sp(3))
story += fig('report/figures/fig4_distribution.png', w_cm=12.2, h_cm=4.8,
             caption=f'Hình 3. So sánh hiệu năng giữa hai thuật toán trên 7 kiểu dữ liệu đầu vào (N = 1.000.000, CUTOFF = {best_cutoff}).')

# ============================================================
# 4. KET LUAN
# ============================================================
story += [
    h1('4. Nhận xét và Kết luận'),
    p(f'1. <b>Ngưỡng CUTOFF tối ưu:</b> Thực nghiệm xác định giá trị tối ưu là <b>CUTOFF = {best_cutoff}</b> ({best_time:.2f} ms). Vùng giá trị hiệu quả nằm trong khoảng 8 đến 16, phù hợp với khuyến nghị của giáo trình Sedgewick. Mốc CUTOFF = {best_cutoff} được áp dụng đồng nhất cho các so sánh diện rộng.'),
    p(f'2. <b>Ưu thế trên dữ liệu có thứ tự bộ phận:</b> Với CUTOFF = {best_cutoff}, OptimizedMergeSort cải thiện từ <b>13.3% đến 15.8%</b> trên các bộ dữ liệu Partially Sorted (1%, 5%, 10%) và <b>12.8%</b> trên mảng đã sắp xếp. Điều này khẳng định Insertion Sort đạt hiệu quả tiệm cận O(N) khi số lượng nghịch thế nhỏ.'),
    p(f'3. <b>Kết luận:</b> Cải tiến CUTOFF = {best_cutoff} mang lại hiệu năng thực tế rõ rệt, giảm tải đệ quy và tối ưu hóa bộ nhớ đệm CPU trên các tập dữ liệu quy mô lớn.'),
]

doc.build(story)
print(f"Đã tạo xong file PDF báo cáo đồng nhất CUTOFF = {best_cutoff}!")
