# <center>Trí Tuệ Nhân Tạo</center>

## Giới thiệu
Repository này lưu trữ mã nguồn, bài tập về nhà và bài tập tại lớp liên quan đến môn học **Trí tuệ nhân tạo (252ARIN330585_06)**. 

Mục tiêu cốt lõi là hiện thực hóa các giải thuật tìm kiếm, tối ưu hóa, lập luận logic và các mô hình học máy cơ bản từ lý thuyết vào mã nguồn thực tế.

* **Họ và Tên:** Nguyễn Đình Khanh ([@qilskcter](https://github.com/qilskcter))
* **Mã số Sinh viên:** 24110244
* **Ngôn ngữ lập trình:** Python 3.14.3
* **Môi trường:** Jupyter Notebook, VS Code, v.v.

---

## Project cá nhân
**Bài toán máy hút bụi**
-  Sử dụng các giải thuật đã học (BFS, DFS, Greedy,...)
-  Có minh họa visualizer trực quan.
-  Có log và các bước thực hiện để thuận tiện trong việc theo dõi

[Project cá nhân](./Project_ca_nhan/)

---

## Các thuật toán

<b>1. Tìm kiếm mù (Uninformed Search)</b>

* <b>BFS (Breadth-First Search):</b> Phát triển tất cả các nút ở độ sâu $d$ trước khi chuyển xuống độ sâu $d+1$. Sử dụng cấu trúc dữ liệu Queue (FIFO).
Cách tiếp cận 1: Cài đặt BFS truyền thống với cơ chế Goal-test khi lấy nút ra khỏi hàng đợi.
Cách tiếp cận 2 (Early Goal Check): Tối ưu hóa bằng cách thực hiện Goal-test ngay khi tạo ra nút con (sinh cấu trúc).


* <b>DFS (Depth-First Search):</b> Ưu tiên phát triển nút ở độ sâu lớn nhất hiện tại. Sử dụng Stack (LIFO) hoặc đệ quy.
Cách tiếp cận 1: DFS cơ bản (Graph-search) quản lý tập trạng thái đã duyệt (Closed set).
Cách tiếp cận 2 (Early Goal Check): Tối ưu hóa bằng cách thực hiện Goal-test ngay khi tạo ra nút con (sinh cấu trúc).


* <b>IDS (Iterative Deepening Search):</b> Kết hợp tính tối ưu của BFS và hiệu quả bộ nhớ của DFS. Thuật toán lặp lại DFS với giới hạn độ sâu (Depth Limit) tăng dần từ 0.
Cách tiếp cận 1: Tăng tuyến tính độ sâu sau mỗi chu kỳ.
Cách tiếp cận 2 (Early Goal Check): Tối ưu hóa bằng cách thực hiện Goal-test ngay khi tạo ra nút con (sinh cấu trúc).


* <b>UCS (Uniform Cost Search):</b> Mở rộng các nút dựa trên chi phí đường đi thực tế thấp nhất từ nút gốc, ký hiệu là $g(n)$. Sử dụng Priority Queue. Đảm bảo tính tối ưu trên đồ thị có trọng số.

<b>2. Tìm kiếm có thông tin (Informed Search)</b>

* <b>Greedy:</b> Lựa chọn phát triển nút có giá trị heuristic thấp nhất: $f(n) = h(n)$. Thuật toán tối ưu hóa cục bộ, tốc độ nhanh nhưng không đảm bảo tìm được đường đi ngắn nhất.
* <b>A* :</b> Thuật toán tìm kiếm tối ưu toàn cục dựa trên hàm đánh giá tổng hợp:

$$f(n) = g(n) + h(n)$$



Trong đó $g(n)$ là chi phí thực tế từ nút gốc và $h(n)$ là chi phí ước lượng đến đích. Đảm bảo tính tối ưu và hoàn chỉnh nếu hàm $h(n)$ chấp nhận được (admissible).