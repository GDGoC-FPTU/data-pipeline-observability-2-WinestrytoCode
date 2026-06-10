# Experiment Report: Data Quality Impact on AI Agent

**Student ID:** AI20K-2A202600723
**Name:** Nguyễn Thị Vang
**Date:** 2026-06-10

---

## 1. Ket qua thi nghiem

Chay `agent_simulation.py` voi 2 bo du lieu va ghi lai ket qua:

| Scenario | Agent Response | Accuracy (1-10) | Notes |
|----------|----------------|-----------------|-------|
| Clean Data (`processed_data.csv`) | Agent: Based on my data, the best choice is Laptop at $1200. | 10 | The agent correctly identifies the Laptop as the best electronic product from the cleaned, validated data. |
| Garbage Data (`garbage_data.csv`) | Agent: Based on my data, the best choice is Nuclear Reactor at $999999. | 1 | The agent picks the Nuclear Reactor because it has the highest price and matches the electronics category, ignoring the fact that it is a massive outlier and toxic data. |

---

## 2. Phan tich & nhan xet

### Tai sao Agent tra loi sai khi dung Garbage Data?

Khi sử dụng dữ liệu rác (`Garbage Data`), Agent đã đưa ra câu trả lời hoàn toàn sai lệch và không thực tế (chọn lò phản ứng hạt nhân trị giá $999,999 làm sản phẩm điện tử tốt nhất). Điều này xảy ra do các nguyên nhân chính sau:

1. **Các giá trị dị biệt cực đoan (Outliers):** Sản phẩm "Nuclear Reactor" với giá trị $999,999 là một ngoại lệ cực đoan được gán nhãn thuộc danh mục điện tử. Vì Agent chỉ áp dụng thuật toán tìm kiếm đơn giản (`idxmax()` trên cột `price`), nó sẽ chọn ngay bản ghi này mà không hề có cơ chế đánh giá xem sản phẩm đó có thực tế hoặc hợp lệ hay không.
2. **Sai lệch kiểu dữ liệu (Wrong Data Types):** Trong dữ liệu rác, một số bản ghi có giá trị giá là chuỗi chữ thay vì số (ví dụ: "ten dollars" thay vì số 10). Nếu Agent thực hiện các phép toán tính toán trung bình hoặc cộng dồn mà không kiểm tra kiểu dữ liệu trước, chương trình sẽ lập tức bị lỗi crash hoặc cho kết quả tính toán sai lệch.
3. **Trùng lặp mã định danh (Duplicate IDs):** Trùng lặp ID (ví dụ: Laptop và Banana cùng có ID là 1) gây mất tính toàn vẹn của dữ liệu dữ liệu quan hệ, làm cho việc truy vấn và định danh chính xác các sản phẩm trở nên không đáng tin cậy.
4. **Thiếu giá trị (Null values):** Các bản ghi có giá trị null hoặc rỗng dễ khiến các hàm xử lý chuỗi của pandas (như chuyển đổi chữ hoa/thường) bị lỗi `AttributeError` hoặc `TypeError` nếu không được xử lý an toàn từ trước.

Tóm lại, nếu không qua bước tiền xử lý và kiểm định (Data Validation & Cleaning) trong ETL pipeline, Agent sẽ mù quáng tin tưởng vào dữ liệu đầu vào và đưa ra kết quả vô nghĩa theo nguyên lý "Garbage In, Garbage Out".

---

## 3. Ket luan

**Quality Data > Quality Prompt?**

Tôi hoàn toàn đồng ý với nhận định này. Cho dù chúng ta có thiết kế một câu Prompt hoàn hảo hay tối ưu đến mức nào, Agent vẫn sẽ đưa ra câu trả lời sai lệch nếu nguồn dữ liệu cung cấp cho nó bị nhiễm độc (poisoned) hoặc chứa nhiều lỗi chất lượng. Prompt chỉ đóng vai trò định hướng cách lập luận và định dạng câu trả lời của Agent, trong khi chất lượng dữ liệu (Quality Data) mới là yếu tố quyết định tính đúng đắn, chính xác và độ tin cậy của thông tin đầu ra. Do đó, việc xây dựng một data pipeline có cơ chế quan sát và kiểm định chất lượng dữ liệu chặt chẽ là điều kiện tiên quyết và quan trọng nhất.
