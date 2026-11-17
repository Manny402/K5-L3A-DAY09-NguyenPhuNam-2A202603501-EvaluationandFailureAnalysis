# Judge audit — replay CSV

`FAIL` là lớp dương. Ngưỡng dùng judge: κ≥0,6; precision≥0,8; recall≥0,7.

| Tiêu chí | n | TP / FP / FN / TN | κ | Precision | Recall | Tỉ lệ FAIL quan sát → hiệu chỉnh RG | Quyết định |
|---|---:|---|---:|---:|---:|---:|---|
| tone_ok | 100 | 24 / 4 / 6 / 66 | 0,757 | 0,857 | 0,800 | 0,28 → 0,30 | Đạt floors; có thể dùng cho tone |
| helpful | 100 | 9 / 0 / 21 / 70 | 0,375 | 1,000 | 0,300 | 0,09 → 0,30 | Không dùng làm gate |

## Audit bất đồng thủ công

| Case | Judge / người | Ai đúng? | Nguyên nhân và sửa rubric |
|---|---|---|---|
| H-008 | PASS / FAIL | Người | “em… nha” quá suồng sã; nêu ví dụ ngôn ngữ thiếu chuyên nghiệp. |
| H-017 | PASS / FAIL | Người | “bạn ơi… nha” suồng sã; thêm tiêu chí xưng hô với khách. |
| H-029 | PASS / FAIL | Người | “không cần nhắn thêm” xua đuổi; thêm lỗi thiếu tôn trọng. |
| H-042 | FAIL / PASS | Người | Câu hoàn tiền ngắn nhưng lịch sự; không bắt buộc lời chào dài. |
| H-051 | FAIL / PASS | Người | Từ “refund” trong câu vẫn rõ nghĩa và lịch sự; tránh cấm từ tiếng Anh máy móc. |
| H-063 | PASS / FAIL | Người | Hứa hoàn thêm nhưng không có số/điều kiện; thêm ví dụ hứa hẹn mơ hồ. |
| H-070 | PASS / FAIL | Người | Emoji cười trong thông báo tiền không phù hợp; thêm quy tắc emoji. |
| HL-015 | PASS / FAIL | Người | Helpful judge chấp nhận phản hồi sai nội dung; rubric phải so reply với kết quả và ledger, không chỉ giọng văn. |

Tone judge vẫn có 4 FP và 6 FN trên 100 ví dụ; chỉ dùng cho tiêu chí tone. Helpful judge bỏ sót 21/30 lỗi, nên không dùng để chặn release dù precision 1,0. Hai bộ đều là replay công khai; cần tập nhãn người mới để kiểm tra held-out trước khi áp dụng ngoài pilot.
