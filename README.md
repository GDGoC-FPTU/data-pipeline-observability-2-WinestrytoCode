[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=24112947&assignment_repo_type=AssignmentRepo)
# Day 10 Lab: Data Pipeline & Data Observability

**Student Email:** vang1910tn@gmail.com
**Name:** Nguyễn Thị Vang
**Student ID:** AI20K-2A202600723

---

## Mo ta

Bài Lab này xây dựng một ETL Pipeline tự động bằng Python để xử lý, làm sạch và chuẩn hóa dữ liệu sản phẩm từ file JSON sang CSV. Sau đó, chúng tôi tiến hành chạy một thực nghiệm mô phỏng Agent RAG (Stress Test) để so sánh hành vi và độ chính xác của AI Agent khi nhận dữ liệu sạch (`Clean Data`) đã qua kiểm định chất lượng so với khi nhận dữ liệu bẩn (`Garbage Data`).

Các bước thực hiện bao gồm:
1. **Extract:** Đọc dữ liệu từ file `raw_data.json`.
2. **Validate:** Lọc bỏ các bản ghi không hợp lệ (giá trị price <= 0 hoặc category trống).
3. **Transform:** Áp dụng giảm giá 10% cho cột `price`, chuẩn hóa danh mục `category` thành định dạng Title Case, và thêm cột dấu thời gian `processed_at`.
4. **Load:** Lưu dữ liệu sạch ra file `processed_data.csv`.
5. **Stress Test:** So sánh phản hồi của Agent với dữ liệu sạch và dữ liệu rác được tạo tự động từ script `generate_garbage.py`.

---

## Cach chay (How to Run)

### Prerequisites
Cài đặt các thư viện cần thiết bằng cách kích hoạt môi trường ảo và chạy lệnh:
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas pytest
```

### Chay ETL Pipeline
Để chạy tiến trình trích xuất, kiểm định, chuyển đổi và lưu trữ dữ liệu sạch:
```bash
python solution.py
```

### Chay Agent Simulation (Stress Test)
1. **Tạo dữ liệu rác (Garbage Data):**
   ```bash
   python generate_garbage.py
   ```
2. **Chạy kiểm thử giả lập phản hồi của Agent:**
   ```bash
   python agent_simulation.py
   ```

### Chay unit tests
Để đảm bảo tất cả các yêu cầu kiểm định và chức năng đều đạt chuẩn chấm điểm tự động:
```bash
pytest tests/test_autograder.py
```

---

## Cau truc thu muc

```
├── solution.py              # ETL Pipeline script
├── processed_data.csv       # Output cua pipeline
├── experiment_report.md     # Bao cao thi nghiem
├── generate_garbage.py      # Script tao du lieu rac
├── agent_simulation.py      # Script chay mo phong Agent
└── README.md                # File nay
```

---

## Ket qua

- **ETL Pipeline:** 
  - Đã trích xuất thành công **5** bản ghi từ `raw_data.json`.
  - Kiểm định phát hiện **2** bản ghi lỗi (1 bản ghi có giá âm, 1 bản ghi trống danh mục).
  - Đã chuyển đổi thành công và ghi nhận **3** bản ghi sạch vào file `processed_data.csv`.

- **Thực nghiệm Stress Test với AI Agent:**
  - **Với Clean Data:** Agent đưa ra câu trả lời chính xác 10/10, khuyên dùng sản phẩm điện tử tốt nhất là Laptop trị giá $1200.
  - **Với Garbage Data:** Agent đưa ra phản hồi sai lệch 1/10 do bị đánh lừa bởi bản ghi dị biệt (Nuclear Reactor có giá $999999).
