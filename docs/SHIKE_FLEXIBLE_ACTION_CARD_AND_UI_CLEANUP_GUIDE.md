# 拾刻灵活行动卡与界面收敛专项优化指导

> 目标：解决当前云真机版本中“识别基本可用但不够灵活、额外提醒被丢失、风险信息混乱、识别文字区出现代码/后端输出、页面重复与工程化”的问题。
>
> 建议路径：`docs/SHIKE_FLEXIBLE_ACTION_CARD_AND_UI_CLEANUP_GUIDE.md`

## 1. 当前问题判断

当前拾刻已经能从截图中识别课程、时间、地点等基础字段，但还没有把自然语言里的“附加事项”转成可执行、可确认、可追踪的结构化行动。

典型问题：

```text
输入：明天早上九点上英语口语教室 E520，记得带书
当前：标题/时间/地点能识别，但“记得带书”容易丢失
理想：课程、时间、地点、准备事项、提醒内容都进入行动卡
```

这说明当前信息结构还停留在：

```text
title + time + location + task + suggested_actions
```

但真实用户输入经常还有：

```text
记得带书
带学生证
提前十分钟到
带实验报告
课前交材料
不要迟到
到北门集合
先去签到
```

这些不是“备注废话”，而是行动卡的重要组成部分。

## 2. 核心原则

### 2.1 AI 输出不能只会“主事件”

模型要同时抽取：

```text
主事件：上英语口语课
时间：明天早上九点
地点：E520
准备事项：带书
建议动作：加入日历、课前提醒
提醒正文：英语口语课，记得带书
风险：相对时间需按当前日期确认
```

### 2.2 附加事项不能塞进标题

错误：

```text
标题：明天早上九点上英语口语教室E520记得带书
```

正确：

```text
标题：英语口语课
时间：明天 09:00
地点：E520
准备事项：带书
提醒内容：课前 30 分钟提醒：英语口语课，记得带书
```

### 2.3 普通用户界面不能出现工程语言

普通用户不应看到：

```text
后端 /v2/analyze-image
后端模型编排
OCR 文本草稿
MockModelAdapter
validate_*
schema_valid
manual_review
risk code
```

这些只允许出现在 DebugDemoScreen 或开发者模式。

普通用户应看到：

```text
AI 正在识别截图
识别到的文字
生成行动卡
请确认时间和地点
准备事项
需要你确认
```

## 3. 数据结构优化

### 3.1 新增 ActionCardUiModel

Android 端不要继续只依赖扁平 `ShikeItem` 展示完整信息。建议新增：

```kotlin
data class ActionCardUiModel(
    val title: String,
    val sceneLabel: String,
    val confidenceText: String,
    val startText: String?,
    val deadlineText: String?,
    val locationText: String?,
    val taskSummary: String,
    val preparationItems: List<String>,
    val suggestedActions: List<ActionUiModel>,
    val userWarnings: List<UserWarning>,
    val sourceTextPreview: String,
)
```

### 3.2 新增 preparation_items / checklist_items

后端 v2 契约建议增加：

```json
{
  "preparation_items": ["带书"],
  "checklist_items": [
    {
      "text": "带书",
      "source": "ocr",
      "confidence": 0.91
    }
  ]
}
```

如果短期不扩 schema，可先通过 `task.summary` 和 `explanation` 兜底，但 Android 端要做轻量解析，把“记得带书 / 带书 / 带学生证 / 提前到”等抽成准备事项。

### 3.3 CalendarDraft / ReminderDraft 也要承接准备事项

```kotlin
data class CalendarDraft(
    val title: String,
    val startAtMillis: Long?,
    val endAtMillis: Long?,
    val location: String?,
    val description: String,
    val disabledReason: String?,
)

data class ReminderDraft(
    val title: String,
    val triggerAtMillis: Long?,
    val detail: String,
    val disabledReason: String?,
)
```

日历 description 应包含：

```text
来源：拾刻识别
任务：上英语口语课
地点：E520
准备事项：带书
说明：已由用户确认后打开系统日历新增页
```

提醒 detail 应包含：

```text
英语口语课 · E520 · 记得带书
```

## 4. 模型 Prompt 优化

Prompt 必须明确要求：

```text
不要只抽取主事件。请把“记得带书、带材料、提前到、先签到、带证件、提交作业”等附加行动抽取为 preparation_items 或 checklist_items。
附加事项不能丢弃，不能塞进标题。
没有明确截止时间时 deadline_text 必须为 null，但前端不得显示 null。
风险提示必须面向用户，禁止输出内部错误码、接口名、schema_valid、manual_review、provider 等工程词。
```

示例输入：

```text
明天早上九点上英语口语教室E520，记得带书
```

理想输出：

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
    "confidence": 0.78
  },
  "task": {
    "summary": "上英语口语课，记得带书",
    "priority": "medium",
    "topic": "course"
  },
  "preparation_items": ["带书"],
  "suggested_actions": [
    {"type": "calendar", "label": "加入课程日历", "requires_permission": true},
    {"type": "reminder", "label": "课前提醒：带书", "requires_permission": true}
  ],
  "missing_fields": [],
  "explanation": "文本包含课程、相对时间、教室地点和准备事项，适合生成课程行动卡。"
}
```

## 5. 风险与缺失字段 UI 收敛

当前风险区太像调试输出。建议改成“确认提示卡”。

### 5.1 用户态文案

```text
需要确认
- 时间：明天 09:00，已按当前日期推算
- 地点：E520，请确认是否为英语口语教室
- 准备：带书
```

### 5.2 只在有问题时展示风险

不要每次都展示大块风险区。规则：

```text
高置信 + 字段完整：不展示风险区，只展示“你可确认后安排”
中置信：展示“请确认以下字段”
低置信：展示“识别不稳定，建议手动确认”
```

### 5.3 风险字段映射

| 内部字段 | 用户看到 |
|---|---|
| relative_time | 时间来自“明天/今晚”，请确认日期 |
| location_low_confidence | 地点识别不够确定，请确认 |
| missing_location | 还缺地点，暂不能打开地图 |
| missing_exact_time | 还缺具体时间，暂不能加入日历 |
| provider_error | AI 暂时不可用，已保留待确认卡 |
| schema_valid | 不显示 |
| manual_review | 不显示，改成“待你确认” |

## 6. 识别文字区清理

“识别到的文字”只显示 OCR 原文或用户可编辑文本，不显示：

```text
后端 /v2/analyze-image：
schema_valid
provider=...
manual_review
risk code
模型解释长文本
```

建议拆成三块：

```text
识别到的文字
明天早上九点上英语口语教室E520，记得带书

AI 生成的行动卡
课程：英语口语课
时间：明天 09:00
地点：E520
准备：带书

为什么这样判断
文本中出现“上英语口语”“明天早上九点”“教室E520”“记得带书”。
```

## 7. 页面去重

### 7.1 首页

首页只保留：

```text
今日主行动卡
待确认摘要
即将截止摘要
快捷导入
```

不要在首页常驻：

```text
完整 AI 解析确认表单
完整行动编排面板
大块风险区
识别文字输入框
工程状态
```

### 7.2 导入页

导入页只做：

```text
选择截图
拍照导入
手动输入
AI 识别进度
```

导入成功后直接进入确认页。

### 7.3 确认页

确认页展示：

```text
结构化字段
准备事项
简洁确认提示
确认按钮
```

不要展示后端路径和代码输出。

### 7.4 行动编排页

行动编排页展示：

```text
加入日历
设置提醒
打开地图
原截图清理
```

其中准备事项要带入日历和提醒。

## 8. 需要新增的验证脚本

```bash
python3 shike/validation/validate_flexible_action_item_extraction.py
python3 shike/validation/validate_preparation_item_calendar_reminder.py
python3 shike/validation/validate_no_backend_copy_in_user_ui.py
python3 shike/validation/validate_risk_copy_user_friendly.py
python3 shike/validation/validate_structured_action_card_ui.py
```

### 8.1 validate_flexible_action_item_extraction.py

必须覆盖：

```text
明天早上九点上英语口语教室E520，记得带书
今晚七点组会腾讯会议，提前准备周报
明天下午三点实验课，带实验报告和学生证
周五十点面试，提前十分钟上线
```

检查：

```text
准备事项没有丢
标题不塞入所有原文
日历/提醒可用
没有 null
没有样例污染
```

### 8.2 validate_no_backend_copy_in_user_ui.py

普通用户 UI 源码不得出现或不得直接展示：

```text
后端 /v2/analyze-image
MockModelAdapter
schema_valid
manual_review
provider_error
validate_
```

这些只能在 DebugDemoScreen 或日志中出现。

## 9. Codex Goal

```text
/goal 修复拾刻当前“识别可用但不够灵活、附加事项丢失、风险文案混乱、普通页面出现后端/代码输出”的产品问题。重点：1) 对“明天早上九点上英语口语教室E520，记得带书”这类输入，必须抽取课程、时间、地点、准备事项“带书”，不得只把整句塞进标题；2) 新增 preparation_items/checklist_items 或 Android 端 ActionCardUiModel 兜底解析，让“带书、带材料、提前到、先签到、带证件”等附加事项进入行动卡、日历 description 和提醒 detail；3) 识别文字区只展示 OCR 原文，不得展示后端 /v2/analyze-image、schema_valid、manual_review、provider、risk code 等工程输出；4) 风险与缺失字段改成用户友好的“需要确认”提示，只在确有风险时展示，禁止大段杂乱风险表；5) 首页、导入页、确认页、行动编排页职责分离，避免重复展示确认表单、行动编排和识别文本。完成条件：validate_flexible_action_item_extraction.py、validate_preparation_item_calendar_reminder.py、validate_no_backend_copy_in_user_ui.py、validate_risk_copy_user_friendly.py、validate_structured_action_card_ui.py、validate_action_execution.py、validate_frontend_polish.py、validate_real_world_ready.py 通过。
```

## 10. 下一次云真机验收

请重点录这 5 个场景：

```text
1. 明天早上九点上英语口语教室E520，记得带书
   -> 展示：英语口语课 / 明天09:00 / E520 / 准备事项：带书

2. 点击加入日历
   -> 日历标题为“英语口语课”，描述包含“准备事项：带书”

3. 点击提醒
   -> 提醒内容包含“记得带书”

4. 确认页
   -> 不出现后端 /v2、schema_valid、manual_review、provider 等工程词

5. 风险提示
   -> 只展示“请确认时间/地点/准备事项”，不展示杂乱风险表
```
