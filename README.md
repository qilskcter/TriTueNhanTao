# <center>Trí Tuệ Nhân Tạo</center>

## Giới thiệu

Repository này lưu trữ mã nguồn, bài tập về nhà và bài tập trên lớp liên quan đến môn học **Trí Tuệ Nhân Tạo (252ARIN330585_06)**.

Mục tiêu cốt lõi của repository là hiện thực hóa các giải thuật tìm kiếm, tối ưu hóa, lập luận logic và các mô hình học máy cơ bản từ lý thuyết vào mã nguồn thực tế.

### Thông tin cá nhân

* **Họ và tên:** Nguyễn Đình Khanh ([@qilskcter](https://github.com/qilskcter))
* **Mã số sinh viên:** 24110244
* **Ngôn ngữ lập trình:** Python 3.14.3
* **Môi trường phát triển:** Jupyter Notebook, VS Code, v.v.

---

# Project cá nhân

## Bài toán máy hút bụi

### Tính năng

* Sử dụng các giải thuật đã học như:

  * BFS
  * DFS
  * IDS
  * UCS
  * Greedy
  * A*
  * IDA*
  * Hill Climbing
* Có giao diện trực quan (Visualizer).
* Hiển thị log và từng bước thực hiện.
* Hỗ trợ theo dõi quá trình tìm kiếm theo thời gian thực.

### Liên kết Project

[Project cá nhân](./Project_ca_nhan/)

---

# Các thuật toán

# 1. Tìm kiếm mù (Uninformed Search)

## BFS (Breadth-First Search)

Phát triển tất cả các nút ở độ sâu $d$ trước khi chuyển xuống độ sâu $d+1$. Sử dụng cấu trúc dữ liệu **Queue (FIFO)**.

### Các cách tiếp cận

* **Cách 1:** BFS truyền thống với Goal-test khi lấy nút ra khỏi hàng đợi.
* **Cách 2 (Early Goal Check):** Tối ưu bằng cách kiểm tra Goal-test ngay khi sinh nút con.

---

## DFS (Depth-First Search)

Ưu tiên phát triển nút ở độ sâu lớn nhất hiện tại. Sử dụng **Stack (LIFO)** hoặc đệ quy.

### Các cách tiếp cận

* **Cách 1:** DFS cơ bản (Graph Search) với Closed Set.
* **Cách 2 (Early Goal Check):** Kiểm tra Goal-test ngay khi sinh nút con.

---

## IDS (Iterative Deepening Search)

Kết hợp tính tối ưu của BFS và hiệu quả bộ nhớ của DFS bằng cách lặp DFS với giới hạn độ sâu tăng dần.

### Các cách tiếp cận

* **Cách 1:** Tăng tuyến tính giới hạn độ sâu sau mỗi vòng lặp.
* **Cách 2 (Early Goal Check):** Kiểm tra Goal-test ngay khi sinh nút con.

---

## UCS (Uniform Cost Search)

Mở rộng các nút dựa trên chi phí đường đi nhỏ nhất từ nút gốc:

$$
f(n) = g(n)
$$

Trong đó:

* $g(n)$ là chi phí thực tế từ nút gốc đến nút hiện tại.

Thuật toán sử dụng **Priority Queue** và đảm bảo tìm được đường đi tối ưu trên đồ thị có trọng số không âm.

---

# 2. Tìm kiếm có thông tin (Informed Search)

## Greedy Best-First Search

Lựa chọn phát triển nút có giá trị heuristic nhỏ nhất:

$$
f(n) = h(n)
$$

Trong đó:

* $h(n)$ là chi phí ước lượng từ nút hiện tại đến đích.

Thuật toán có tốc độ nhanh nhưng không đảm bảo tìm được đường đi tối ưu.

---

## A* Search

Thuật toán tìm kiếm tối ưu toàn cục dựa trên hàm đánh giá:

$$
f(n) = g(n) + h(n)
$$

Trong đó:

* $g(n)$ là chi phí thực tế từ nút gốc đến nút hiện tại.
* $h(n)$ là chi phí ước lượng từ nút hiện tại đến đích.

A* đảm bảo tính tối ưu và hoàn chỉnh nếu heuristic admissible.

---

## IDA* (Iterative Deepening A*)

Kết hợp giữa Iterative Deepening DFS và heuristic của A*.

### Hàm đánh giá

$$
f(n) = g(n) + h(n)
$$

Trong đó:

* $g(n)$ là chi phí thực tế từ trạng thái ban đầu đến nút hiện tại.
* $h(n)$ là chi phí ước lượng từ nút hiện tại đến đích.

IDA* thực hiện tìm kiếm theo từng ngưỡng $f(n)$ tăng dần thay vì lưu toàn bộ frontier như A*, giúp tiết kiệm bộ nhớ đáng kể.

Thuật toán vẫn đảm bảo tính tối ưu nếu heuristic admissible, tuy nhiên có thể phải duyệt lại nhiều nút.

---

# 3. Tìm kiếm cục bộ (Local Search)

## Simple Hill Climbing

Thuật toán leo đồi cơ bản hoạt động bằng cách chọn trạng thái kế tiếp đầu tiên có heuristic tốt hơn trạng thái hiện tại.

### Hàm heuristic

$$
f(n) = h(n)
$$

Trong đó:

* $h(n)$ biểu diễn mức độ "xấu" của trạng thái hiện tại.

Nếu không tồn tại trạng thái tốt hơn, thuật toán sẽ dừng lại.

### Đặc điểm

* Đơn giản
* Tốc độ nhanh
* Dễ mắc kẹt tại:

  * Local Optimum
  * Plateau
  * Ridge

---

## Steepest Ascent Hill Climbing

Biến thể cải tiến của Hill Climbing.

Tại mỗi bước, thuật toán sẽ đánh giá toàn bộ các trạng thái lân cận và chọn trạng thái có heuristic tốt nhất.

### Hàm heuristic

$$
f(n) = h(n)
$$

### Đặc điểm

* Chất lượng kết quả tốt hơn Simple Hill Climbing.
* Chi phí tính toán cao hơn do phải duyệt toàn bộ neighbor.
* Không đảm bảo tìm được nghiệm tối ưu toàn cục.

---

## Stochastic Hill Climbing

Thuật toán lựa chọn ngẫu nhiên một trạng thái tốt hơn trong số các neighbor khả thi thay vì luôn chọn trạng thái tốt nhất.

### Hàm heuristic

$$
f(n) = h(n)
$$

### Đặc điểm

* Tăng khả năng thoát khỏi local optimum.
* Tạo sự đa dạng trong quá trình tìm kiếm.
* Kết quả có thể khác nhau giữa các lần chạy.

---

## Random-Restart Hill Climbing

Biến thể của Hill Climbing cho phép khởi động lại từ nhiều trạng thái ngẫu nhiên khác nhau khi thuật toán bị mắc kẹt.

### Hàm heuristic

$$
f(n) = h(n)
$$

### Đặc điểm

* Tăng xác suất tìm được nghiệm tốt.
* Hiệu quả trên không gian trạng thái lớn.
* Giảm ảnh hưởng của local optimum.

---

# Tổng kết

Repository này đóng vai trò như một bộ sưu tập thực hành các giải thuật AI cơ bản, giúp:

* Hiểu rõ nguyên lý hoạt động của từng thuật toán.
* So sánh ưu nhược điểm giữa các phương pháp tìm kiếm.
* Trực quan hóa quá trình tìm kiếm thông qua visualizer.
* Ứng dụng lý thuyết AI vào các bài toán thực tế.
