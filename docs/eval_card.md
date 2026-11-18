# Eval card — LogiX-VN refund agent, v1

## Thiết lập và bằng chứng

- Code: nhánh `starter/d09` của fork, bắt đầu từ commit gốc `9e1549a`. Agent gốc là `src/lab8/shapes/swarm_reference.py` của Day 8, không chỉnh sửa.
- Eval set: `v1`, SHA `eacb642055c0`, 14 claim công khai × seeds 11/22/33/44/55 = 70 trial. Nhãn nằm trong `labels_v1.json`, tách khỏi item. Metric spec v1.0; Python 3.12.4; MockLLM.
- Report do `lab9.eval` sinh: baseline `E-swarm-20261118-eacb`, bản sửa `E-fixed-20261118-eacb`, hồi quy `E-seeded_regression-20261118-eacb`. Mỗi report có đủ 70 cặp `(item_id, seed)`.

## Kết quả

| Metric | Baseline swarm | Fixed | Seeded regression | Ngưỡng / vai trò |
|---|---:|---:|---:|---|
| approval_bypass | 0 | 0 | 0 | max 0, blocking |
| secret_leak | 0 | 0 | 0 | max 0, blocking |
| refund_amount_correct | 0,9857 | 1,0000 | 0,8571 | min 0,95 + không giảm có ý nghĩa, blocking |
| pass_rate | 0,9857 | 1,0000 | 0,7143 | min 0,85 + không giảm có ý nghĩa, blocking |
| reply_amount_matches_ledger | 1,0000 | 1,0000 | 0,7857 | min 0,95 + không giảm có ý nghĩa, blocking; bắt FM-08 |
| db_fact_kept | 0,9857 | 1,0000 | 0,9286 | min 0,95, theo dõi |
| status_correct | 0,9857 | 1,0000 | 0,8571 | min 0,85, theo dõi |
| proposal_amount_correct | 0,9857 | 1,0000 | 0,7857 | min 0,85, theo dõi |
| pass_5 | 0,9286 | 1,0000 | 0,7143 | min 0,80, theo dõi |
| cost_per_success | 49,5670 | 48,7157 | 81,2020 | tăng tối đa 10%, theo dõi |

Paired bootstrap theo **item** (trung bình qua 5 seed/item), 1.000 resample, percentile CI 95%, RNG 2027:

| So sánh PR − baseline | Δ pass_rate | CI 95% | Gate |
|---|---:|---:|---|
| fixed − swarm | +0,014 | [+0,000; +0,043] | exit 0 |
| seeded_regression − swarm | −0,271 | [−0,500; −0,057] | exit 1: `pass_rate`, `refund_amount_correct`, `reply_amount_matches_ledger` |

Kiểm tra `lab9.mutation --detect`: phát hiện 100% trial fail của seeded regression bằng grader giải thích được, báo nhầm 0% trên fixed. Case phân tích bước sai đầu tiên: [trace_case.md](trace_case.md), FM-03 `C-002@11`, regression test `test_ticket_delay_cannot_override_order_delay`.

## Judge và giới hạn

Tone judge: κ 0,757; precision 0,857; recall 0,800, đạt floors. Helpful judge: κ 0,375; recall 0,300, loại khỏi gate. Chi tiết trong [judge_audit.md](judge_audit.md). Các metric liên quan tiền và approval dùng code.

Gate owner: chủ fork cá nhân kiểm tra report và sửa code/grader trước khi merge; không có waiver tự động. Pilot chỉ bao gồm 14 public claims. MockLLM không đại diện model thật; 14 item cho CI rộng nên khó phát hiện hồi quy nhỏ hoặc hiếm. Judge dùng CSV replay công khai, chưa có held-out do người gắn nhãn mới. `swarm` của Day 8 không phát event `reply`, nên metric FM-08 không quan sát được số tiền trong phản hồi của baseline; muốn so sánh reply ở production phải thu event này nhất quán.

Tăng `eval_set_version` khi thêm hoặc sửa claim/nhãn. Tăng `metric_spec_version` khi thay định nghĩa grader hoặc ngưỡng, chạy lại baseline và ghi lý do trong PRD.
