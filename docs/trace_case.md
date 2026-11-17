# Trace case — C-002@11

| Trường | Bằng chứng |
|---|---|
| Trial | `seeded_regression C-002@11`, report `E-seeded_regression-20261118-f713` |
| Triệu chứng | Lab 8 grader: `status resolved != denied`; ledger ghi 20.000đ, nhãn là 0đ. |
| Bước sai đầu tiên | Event 3: `model_override {"delay_days": 5}` sau khi event 2 `investigator` đã đọc dữ kiện đơn từ DB. |
| Vì sao là bước đầu tiên | Event 1 chỉ tạo handoff; event 2 thu thập dữ liệu. Event 3 thay DB bằng số ngày trong ticket; quote ở event 4 và refund sau đó là hệ quả. |
| Failure mode | FM-03 `ticket_trust`. |
| Đối chứng | `fixed C-002@11`: sau `investigator` là event 3 `quote` 0đ, không có `model_override`; ledger 0đ, trạng thái `denied`, Lab 8 grader PASS. |
| Regression test | `tests/test_lab9_trace_regression.py::test_ticket_delay_cannot_override_order_delay`: xác nhận variant lỗi có override/ledger sai và `fixed` không override/ledger đúng. |
| Chưa chắc chắn | Trace mô phỏng MockLLM, không chứng minh hành vi của model thật hay tần suất lỗi ngoài 5 seed đã dùng. |

Chạy lại từ `src/`: `python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11` và cùng lệnh với `--shape fixed`.
