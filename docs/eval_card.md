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

## Bổ sung v2 — Advanced / Expert

- Eval set v2: 28 item (14 v1 + 14 adversarial), 5 seed/item, SHA `ca1fa5324602`. `fm_map.yaml` map 8 cơ chế của pack sang FM-02–FM-09; `evalset --v2 --build` và `--check` trả 0 vấn đề. FM-09 có trace đối chứng `C-110@11`: investigator từ chối `outside_principal_scope`.
- Baseline `E-swarm-20261118-ca1f`: `pass_rate=0,9786`, `pass_hat_5=0,8929`, `approval_bypass=0`, `secret_leak=0`. `pass_hat_5` blocking có sàn 0,80; slice `money_movement` và `adversarial` cũng blocking.
- A/A giữa seed `[11,22,33,44,55]` và `[66,77,88,99,110]` trên cùng MockLLM cho Δ = 0 ở mọi metric, kể cả `pass_hat_5`. Sàn 0,80 thấp hơn baseline 0,8929 và nằm ngoài dải A/A quan sát được. Với LLM thật, dải nhiễu có thể rộng hơn 0; phải đo lại trước khi dùng sàn này.
- Scorecard `lab9.mutation`: chặn 3/3 regression (`seeded_regression`, `slice_regression`, `flaky_regression`), 0 báo nhầm trên `fixed` và `honest_refactor`.
- `slice_regression` có `pass_rate=0,9357` (Δ −0,043, CI [−0,121; +0,029]) và `pass_hat_5=0,8929`, nên metric toàn bộ vẫn qua. Slice `money_movement/pass_rate=0,85`, Δ −0,150, CI [−0,300; +0,000], bị chặn; slice `adversarial` không chặn case này.
- `flaky_regression` bị chặn bởi `pass_hat_5` và các metric khác trong scorecard. Bốn trap công khai (`evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, `loosened_spec`) đều bị gate chặn; baseline so với chính nó vẫn qua.
- Hai probe bổ sung chạy trên cả 140 trial v2: `misreport` giữ `pass_rate=1,0` nhưng `reply_amount_matches_ledger=0,7857` và bị chặn đúng metric; `quiet_override` không ghi event override nhưng gate vẫn chặn bằng `refund_amount_correct` và slice `denial`.

Giới hạn: 5 seed/item không đủ phát hiện ổn định lỗi hiếm khoảng 1/3 seed trong mọi slice; một bug chỉ xuất hiện trên vài item có thể để CI chạm 0. Traps ẩn của giảng viên và các kiểu sửa report ngoài bộ công khai chưa được kiểm chứng. Tiền/approval và integrity được chấm bằng code, nhưng không thay thế audit độc lập trên dữ liệu thật.
