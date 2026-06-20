# 拾刻 OCR 文本到行动卡训练/测试集 v1

> 用途：训练和评测“OCR 识别出的文字 -> 结构化行动卡”的能力，尤其覆盖混淆文本、附加准备事项、低置信度、负例、同一截图多行动事项和用户界面噪声。

## 1. 数据集目标

拾刻不是普通 OCR，也不是把识别文字复制成标题。模型需要把 OCR 文本拆成：

```text
主事件 / 时间 / 地点 / 任务 / 准备事项 / 建议动作 / 缺失字段 / 用户确认提示
```

重点训练能力：

- 不把整句 OCR 塞进标题。
- 不丢失“记得带书、带学生证、提前到、先签到、打印材料”等附加事项。
- 不把状态栏、笔记标题、截图工具栏、网速、字数、分类等 UI 噪声当作任务内容。
- 不在信息不足时臆造时间、地点、作业或样例字段。
- 不在普通用户输出里出现 `后端 /v2/analyze-image`、`schema_valid`、`manual_review`、`provider` 等工程词。

## 2. 文件

- JSONL：`shike_action_card_training_cases_v1.jsonl`，每行一个 case，适合模型评测脚本。
- Pretty JSON：`shike_action_card_training_cases_v1.pretty.json`，适合人工审阅。

## 3. 数据分布

| 类别 | 数量 | 说明 |
|---|---:|---|
| `ambiguous` | 3 | 信息不足、低置信度 |
| `assignment` | 7 | 作业/论文/材料提交截止 |
| `course` | 12 | 课程通知、上课、教室变更、携带物品 |
| `event` | 8 | 活动海报、报名截止、线下/线上活动 |
| `exam` | 3 | 考试/补考/模拟考试 |
| `interview` | 2 | 面试/笔试 |
| `meeting` | 5 | 会议/组会/评审/汇报 |
| `multi` | 3 | 同一 OCR 多行动卡 |
| `negative` | 5 | 无行动价值或弱行动碎片 |
| `ocr` | 4 | OCR 噪声、状态栏、截图工具栏 |
| `prep` | 5 | 准备事项/携带物品/材料 |
| `travel` | 3 | 高铁/航班/集合 |
| **总计** | **60** |  |

## 4. 推荐输出结构

为了让“记得带书”等信息不丢失，建议在 v2 行动卡里支持：

```json
{
  "scene_type": "course_notice",
  "confidence": 0.92,
  "title": "英语口语课",
  "time": {
    "start_text": "明天早上九点",
    "deadline_text": null,
    "normalized_start": "2026-06-10T09:00:00+08:00",
    "normalized_deadline": null
  },
  "location": {
    "raw": "E520",
    "map_query": "E520",
    "confidence": 0.8
  },
  "task": {
    "summary": "上英语口语课，记得带书",
    "priority": "medium",
    "topic": "course"
  },
  "preparation_items": [
    "带书"
  ],
  "checklist_items": [
    {
      "text": "带书",
      "source": "ocr",
      "confidence": 0.91
    }
  ],
  "suggested_actions": [
    {
      "type": "calendar",
      "label": "加入课程日历",
      "requires_permission": true
    },
    {
      "type": "reminder",
      "label": "课前提醒：带书",
      "requires_permission": true
    },
    {
      "type": "map",
      "label": "打开教室位置",
      "requires_permission": false
    }
  ],
  "missing_fields": [],
  "user_warnings": [
    "时间来自“明天”，请用户确认日期。"
  ],
  "explanation": "文本包含课程、时间、地点和准备事项，适合生成课程行动卡。"
}
```

## 5. 代表样例

### course_001 · easy

OCR 输入：

```text
明天早上九点上英语口语 教室E520，记得带书
```

期望行动卡摘要：

1. **英语口语课**
   - 场景：`course_notice`
   - 时间：明天早上九点；截止：None
   - 地点：E520
   - 准备事项：带书
   - 缺失字段：无
   - 建议动作：加入课程日历, 课前提醒：带书, 打开教室位置
   - 不应输出：高数A班, B203, 第5章, 今晚18:30, null

### course_002 · medium

OCR 输入：

```text
晚上九点上 高数 B地点在303
```

期望行动卡摘要：

1. **高数课**
   - 场景：`course_notice`
   - 时间：晚上九点；截止：None
   - 地点：B地点303
   - 准备事项：无
   - 缺失字段：date, exact_location
   - 建议动作：提醒我确认上课信息, 确认地点后打开路线
   - 不应输出：B203, 18:30, 22:00, 第5章

### assignment_003 · hard

OCR 输入：

```text
大物实验报告不是今晚，是明天晚上10点交，纸质版带到实验室
```

期望行动卡摘要：

1. **大物实验报告提交**
   - 场景：`assignment_deadline`
   - 时间：None；截止：明天晚上10点
   - 地点：实验室
   - 准备事项：带纸质版实验报告
   - 缺失字段：exact_location
   - 建议动作：截止前提醒：带纸质版实验报告, 确认实验室后打开路线
   - 不应输出：今晚22:00

### event_005 · medium

OCR 输入：

```text
创新创业路演 6月15日14:00 腾讯会议 会议号 884 221 090 参赛队提前10分钟入会
```

期望行动卡摘要：

1. **创新创业路演**
   - 场景：`event_poster`
   - 时间：6月15日14:00；截止：None
   - 地点：腾讯会议 884 221 090
   - 准备事项：提前10分钟入会
   - 缺失字段：无
   - 建议动作：加入路演日历, 提前10分钟提醒入会

### multi_001 · hard

OCR 输入：

```text
明天9点英语口语E520记得带书；同一张图下面还写着：英语作文周五晚10点前交
```

期望行动卡摘要：

1. **英语口语课**
   - 场景：`course_notice`
   - 时间：明天9点；截止：None
   - 地点：E520
   - 准备事项：带书
   - 缺失字段：无
   - 建议动作：加入课程日历, 课前提醒：带书, 打开教室位置

2. **英语作文提交**
   - 场景：`assignment_deadline`
   - 时间：None；截止：周五晚10点前
   - 地点：无
   - 准备事项：无
   - 缺失字段：无
   - 建议动作：截止前提醒提交英语作文

### negative_001 · negative

OCR 输入：

```text
哈哈哈哈这个表情包太好笑了，今晚冲！
```

期望行动卡摘要：

1. **无需行动碎片**
   - 场景：`unknown`
   - 时间：无；截止：无
   - 地点：无
   - 准备事项：无
   - 缺失字段：scene_type, time, location, task
   - 建议动作：不生成行动，稍后确认
   - 不应输出：calendar, map, 今晚日程

### ocr_noise_001 · hard

OCR 输入：

```text
18:16  0.30KB/s  明天早上九点上英语口语教室E520  记得带书  标题  未分类
```

期望行动卡摘要：

1. **英语口语课**
   - 场景：`course_notice`
   - 时间：明天早上九点；截止：None
   - 地点：E520
   - 准备事项：带书
   - 缺失字段：无
   - 建议动作：加入课程日历, 课前提醒：带书, 打开教室位置
   - 不应输出：18:16, 0.30KB/s, 标题, 未分类

## 6. 评测建议

建议新增验证脚本：

```bash
python3 shike/validation/validate_flexible_action_item_extraction.py
python3 shike/validation/validate_preparation_item_calendar_reminder.py
python3 shike/validation/validate_no_backend_copy_in_user_ui.py
python3 shike/validation/validate_no_sample_contamination.py
```

最低通过标准：

- 60 个 case 中至少 52 个主字段正确。
- 所有 `do_not_output` 禁止词不得出现。
- 所有带 `preparation_items` 的样例，准备事项召回率不低于 90%。
- 所有负例不得自动创建日历或地图。
- 所有 `null` 不得在用户 UI 中原样显示。

## 7. Codex Goal

```text
/goal 将 shike_action_card_training_cases_v1.jsonl 接入拾刻模型评测。新增 validate_flexible_action_item_extraction.py，读取每条 case 的 ocr_text，调用当前 /v2/analyze-image 或文本 fallback，比较 scene_type、title、time、location、preparation_items、suggested_actions、missing_fields 和 do_not_output。重点保证“记得带书、带学生证、提前到、打印材料”等准备事项不丢，且普通用户输出不出现后端路径、schema_valid、manual_review、provider、Mock 等工程词。完成条件：新增评测脚本通过，生成 docs/flexible-action-card-eval-report.md。
```
