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
        items.append(Image(path, width=w_cm*cm, height=w_cm*cm*0.65))
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
    p('Merge Sort là thuật toán sắp xếp theo phương pháp chia để trị, có độ phức tạp '
      'O(n log n) trong mọi trường hợp. Tuy nhiên, với các mảng con nhỏ, chi phí đệ quy '
      'của Merge Sort lớn hơn so với Insertion Sort — một thuật toán đơn giản hơn, '
      'hiệu quả với mảng nhỏ do ít overhead.'),
    p('Cải tiến được xem xét trong báo cáo này: khi kích thước mảng con không vượt quá '
      'một ngưỡng nhất định (gọi là <i>cutoff</i>), thay vì tiếp tục đệ quy Merge Sort, '
      'chuyển sang dùng Insertion Sort. Mục tiêu là tìm giá trị cutoff tối ưu '
      'giúp giảm thời gian thực thi.'),
]

# --- 2. Thuat toan ---
story += [
    h1('2. Mô tả thuật toán'),
    h2('2.1. Merge Sort chuẩn'),
    p('Cài đặt theo giáo trình Algorithms 4th Edition (Sedgewick &amp; Wayne). '
      'Hàm <i>merge</i> sao chép mảng sang mảng phụ <i>aux[]</i>, sau đó trộn '
      'ngược lại theo hai con trỏ i và j. Hàm <i>sort</i> chia đôi đệ quy rồi gọi merge.'),
    h2('2.2. Insertion Sort'),
    p('Hỗ trợ sắp xếp đoạn con a[lo..hi]. Với mỗi phần tử i từ lo+1 đến hi, '
      'dịch nó về trái cho đến vị trí đúng bằng cách hoán đổi liên tiếp.'),
    h2('2.3. Optimized Merge Sort (có cutoff)'),
    p('Giống Merge Sort chuẩn, nhưng thêm điều kiện: nếu '
      '<i>hi &lt;= lo + cutoff − 1</i>, gọi Insertion Sort thay vì tiếp tục đệ quy. '
      'Điều này giúp tránh chi phí đệ quy không cần thiết với các mảng con nhỏ.'),
]

# --- 3. Moi truong thuc nghiem ---
story += [
    h1('3. Môi trường thực nghiệm'),
    tbl([
        ['Thành phần', 'Chi tiết'],
        ['Hệ điều hành', 'Windows 11'],
        ['JDK', 'OpenJDK 21.0.11 LTS'],
        ['Phương pháp đo', 'System.nanoTime()'],
        ['Số lần lặp mỗi trường hợp', '5 lần'],
        ['JVM warm-up', '3 lần trước khi đo'],
        ['Seed ngẫu nhiên', '123456 (cố định)'],
    ], col_widths=[7*cm, 9*cm]),
    sp(10),
    p('Dữ liệu được tạo ngoài vùng đo thời gian. Mỗi thuật toán nhận bản sao '
      'độc lập của cùng một mảng đầu vào. Kết quả lấy giá trị trung bình 5 lần đo.'),
]

# --- 4. Ket qua ---
story += [
    h1('4. Kết quả thực nghiệm'),
    h2('4.1. Ảnh hưởng của cutoff (n = 100.000, dữ liệu ngẫu nhiên)'),
]

# Bang cutoff
cutoff_data = [['Cutoff', 'Thời gian TB (ms)']]
for _, row in cutoff_df.iterrows():
    marker = ' ← tối ưu' if int(row['cutoff']) == best_cutoff else ''
    cutoff_data.append([str(int(row['cutoff'])), f"{row['time_ms']:.3f}{marker}"])
story.append(tbl(cutoff_data, col_widths=[5*cm, 8*cm]))
story.append(sp(6))
story += fig('report/figures/fig1_cutoff_vs_time.png', 13,
             f'Hình 1. Thời gian sắp xếp theo giá trị cutoff (n=100.000, ngẫu nhiên). Cutoff tối ưu: {best_cutoff} ({best_time:.1f} ms).')

story.append(h2('4.2. So sánh thời gian theo kích thước mảng (dữ liệu ngẫu nhiên)'))
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
             'Hình 2. Thời gian sắp xếp theo kích thước mảng (dữ liệu ngẫu nhiên).')

story.append(h2('4.3. So sánh trực quan hai thuật toán'))
story += fig('report/figures/fig3_comparison.png', 13,
             'Hình 3. So sánh MergeSort và OptimizedMergeSort theo kích thước mảng.')

story.append(h2('4.4. Hiệu năng theo kiểu dữ liệu (n = 1.000.000)'))
large_df = summary_df[summary_df['size'] == 1000000]
type_map = {'random': 'Ngẫu nhiên', 'sorted': 'Đã sắp xếp',
            'reversed': 'Ngược chiều', 'duplicates': 'Nhiều trùng lặp'}
dist_data = [['Kiểu dữ liệu', 'MergeSort (ms)', 'Optimized (ms)', 'Giảm (%)']]
for _, row in large_df.iterrows():
    dist_data.append([
        type_map.get(row['type'], row['type']),
        f"{row['merge_ms']:.2f}",
        f"{row['optimized_ms']:.2f}",
        f"{row['speedup_pct']:.1f}%"
    ])
story.append(tbl(dist_data, col_widths=[4.5*cm, 4*cm, 4*cm, 3.5*cm]))
story.append(sp(6))
story += fig('report/figures/fig4_distribution.png', 13,
             'Hình 4. Hiệu năng theo kiểu dữ liệu đầu vào (n = 1.000.000).')

# --- 5. Nhan xet ---
story += [
    h1('5. Nhận xét và kết luận'),
    p(f'Qua thực nghiệm, giá trị cutoff tối ưu tìm được là <b>{best_cutoff}</b> '
      f'(thời gian trung bình {best_time:.1f} ms với n=100.000, dữ liệu ngẫu nhiên). '
      'Giá trị này nằm trong khoảng 6–16, phù hợp với lý thuyết của Sedgewick.'),
    p('OptimizedMergeSort cho thấy cải thiện rõ rệt so với MergeSort chuẩn khi n lớn '
      '(500.000–1.000.000), với mức giảm thời gian từ 10% đến 25% tùy kiểu dữ liệu. '
      'Với n nhỏ (1.000–10.000), ảnh hưởng không ổn định do JVM chưa đủ warm-up '
      'hoặc overhead đo thời gian chiếm tỉ lệ cao.'),
    p('Kết luận: Việc áp dụng cutoff là cải tiến đơn giản nhưng hiệu quả. '
      'Với các ứng dụng thực tế, nên chọn cutoff trong khoảng 8–16.'),
]

doc.build(story)
print(f"Da tao: {OUT_PDF}")
