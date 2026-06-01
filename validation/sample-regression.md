# 复赛样例回归验证

对应 issue：`SHIKE-080`

## 样例覆盖

`validation/regression-cases.json` 包含 110 条合成样例，覆盖课程通知、活动海报、会议通知、作业截止、面试通知、出行票务、低质量碎片和反例噪声。

覆盖边界：

- 清晰文本和清晰海报。
- 模糊时间、OCR 截断和低置信度。
- 地点缺失、缺少报名方式和地址简称。
- 多个截止时间、相对时间和相对截止。
- 会议、作业、面试、出行等青年日常行动场景。
- 无行动闲聊、广告噪声、纯说明文本等反例。

## 回归记录字段

| 字段 | 说明 |
|---|---|
| `id` | 样例唯一标识 |
| `scene` | `course_notice`、`event_poster`、`meeting_notice`、`assignment_deadline`、`interview_notice`、`travel_ticket`、`low_quality_fragment` 或 `negative_fragment` |
| `input` | OCR 文本或人工转写 |
| `expected_fields` | 应抽取字段 |
| `expected_missing_fields` | 允许或期望缺失字段 |
| `expected_actions` | 期望动作 |
| `edge` | 边界类型 |

## 复赛回归流程

1. 每次模型或规则层改动后，跑全量 110 条样例。
2. 对每条记录抽取字段、人工修正点、动作执行结果、收件箱状态。
3. 失败必须归因到模型、规则或系统权限三类之一。
4. 不允许只保留成功样例展示。
5. 先运行 `python3 validation/validate_model_eval_cases.py` 检查样例数量、唯一 ID、场景覆盖、低质量和反例覆盖。

## 通过标准

| 项 | 标准 |
|---|---|
| 字段抽取 | 清晰文本样例的关键字段全部命中 |
| 人工修正 | 低质量样例必须进入待确认或显示缺失字段 |
| 动作执行 | 每条样例至少产生一个可解释动作 |
| 状态流转 | 每条样例进入收件箱并拥有明确状态 |
| 隐私行为 | 云侧增强关闭时，复杂样例进入人工确认而非静默上传 |
