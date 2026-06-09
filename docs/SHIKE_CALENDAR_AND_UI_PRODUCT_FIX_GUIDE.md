# 拾刻：日历准确性与真实产品界面专项优化指导

> 建议放入仓库：`docs/SHIKE_CALENDAR_AND_UI_PRODUCT_FIX_GUIDE.md`
>
> 目标：修复云真机实测中暴露的两个高优先级问题：
>
> 1. 导入日历不准确：AI 识别出的相对时间、日期、地点与系统日历预填不一致。
> 2. 页面重复与工程化：普通用户界面出现重复模块、工程文案、调试入口和不该暴露的技术细节。

---

## 0. 当前问题结论

从云真机视频看，拾刻已经具备“截图/导入 -> AI 解析 -> 确认 -> 打开系统日历”的链路，但仍存在明显产品缺陷：

- 日历页预填时间不可信，可能使用了样例时间、fallback epoch 或错误解析后的时间。
- 首页、导入页、确认页之间重复展示同一张行动卡，用户不知道下一步应该在哪里操作。
- “后端 /v2/analyze-image”“后端模型编排”“解析当前草稿”“活动样例解析”等工程词还出现在普通用户路径里。
- “确认后安排”模块过大且常驻首页，遮挡底部导航，像调试面板而不是真实产品。
- AI 输出还没有完全变成结构化行动卡，部分结果只是把 OCR 文本拼成标题。

复赛评审重点看产品功能、产品界面、产品交互、可运行作品和大模型调用能力。因此下一轮不是继续堆功能，而是把“识别结果 -> 日历/提醒/地图”的闭环做准确、简洁、可信。

---

## 1. 日历不准确：根因与修复方向

### 1.1 根因一：Android 仍可能使用样例 epoch

当前 Android `ShikeItem` 只有一个 `startEpochMillis`，如果从模型结果映射时没有正确解析 `normalized_start`，就容易回退到 `sampleCourse().startEpochMillis` 或 `sampleEvent().startEpochMillis`。

错误表现：

```text
用户输入：明天早上九点上英语口语教室 E520
AI 页面：明天早上九点 / E520
日历页面：日期或时间变成样例日期、当前时间附近，或不符合“明天 09:00”
```

必须改成：

```text
模型返回 normalized_start
  -> Android 解析成 startEpochMillis
  -> Calendar Intent 使用该 epoch
  -> 若没有 normalized_start，但 start_text 是“明天早上九点”
       Android 按 current_date + user_timezone 二次归一化
  -> 若仍无法确定，禁止日历按钮，只允许提醒/待确认
```

### 1.2 根因二：`deadline_text = null` 被展示成 `null`

普通用户界面不能出现：

```text
明天早上九点 / null
```

应改成：

```text
明天早上九点
暂无截止时间
```

或在时间字段里分开展示：

```text
开始时间：明天 09:00
截止时间：无
```

### 1.3 根因三：日历动作没有 action plan 中间层

现在日历按钮看起来像直接把当前 `ShikeItem` 扔给系统日历。应该先生成 `CalendarDraft`：

```kotlin
data class CalendarDraft(
    val title: String,
    val startAtMillis: Long?,
    val endAtMillis: Long?,
    val location: String?,
    val description: String,
    val disabledReason: String?,
)
```

日历按钮只在 `disabledReason == null` 时可点。

---

## 2. 日历准确性目标规格

### 2.1 课程通知示例

输入：

```text
明天早上九点上英语口语教室 E520
```

期望行动卡：

```text
标题：英语口语课
场景：课程通知
开始时间：明天 09:00
截止时间：无
地点：E520
任务：上英语口语课
建议动作：加入日历、课前提醒、查看地图
风险提示：日期来自“明天”，请确认是否正确
```

日历预填：

```text
标题：英语口语课
开始：当前日期次日 09:00
结束：次日 10:00，默认 60 分钟
地点：E520
备注：由拾刻从课程通知解析。用户确认后打开系统日历新增页，由用户保存。
```

### 2.2 禁用规则

| 情况 | 日历 | 提醒 | 地图 |
|---|---|---|---|
| 未确认字段 | 禁用 | 禁用 | 禁用 |
| 缺少具体时间 | 禁用 | 可创建“稍后确认提醒” | 视地点而定 |
| 缺少地点 | 可用 | 可用 | 禁用 |
| 只有截止时间 | 可创建截止日历/提醒 | 可用 | 视地点而定 |
| 时间是相对词但可归一化 | 可用，但展示“请确认日期” | 可用 | 视地点而定 |
| 模型置信度低 | 默认不执行，需用户确认 | 默认待确认 | 默认待确认 |

### 2.3 日历文案边界

只能说：

```text
已打开系统日历新增页，请在日历中保存。
```

不能说：

```text
已写入日历
已同步到日历
日历已保存
```

除非后续真的接入 Calendar Provider 并拿到写入权限和成功结果。

---

## 3. 页面重复与不该展示内容

### 3.1 普通用户不应看到的词

普通模式必须隐藏：

```text
后端
/v1/analyze
/v2/analyze-image
MockModelAdapter
Mock
validate_
交付物自检
3分钟演示路线
后端模型编排
解析当前草稿
活动样例解析
课程样例
3B 多模态诊断
provider
schema_valid
```

这些内容可以保留在 DebugDemoScreen，但只能通过设置页连续点击版本号进入。

### 3.2 用户可见文案替换表

| 当前文案 | 用户侧文案 |
|---|---|
| 后端 /v2/analyze-image | 云端 AI 解析 |
| 后端模型编排 | AI 正在生成行动卡 |
| OCR 文本草稿 | 识别到的文字 |
| 解析当前草稿 | 生成行动卡 |
| 活动样例解析 | Debug 样例解析，仅调试页显示 |
| 模型状态 | 解析状态 |
| validate / 自检 | 交付检查，仅调试页显示 |
| null | 不显示，或“暂无” |

### 3.3 首页目标

首页只展示：

1. 今日主行动卡。
2. 待确认摘要。
3. 即将截止摘要。
4. 快捷导入入口。
5. 底部导航。

首页不应该常驻：

- AI 解析确认完整表单。
- 行动编排完整面板。
- 后端状态。
- 大块“确认后安排”绿色面板。
- 调试按钮和样例按钮。

---

## 4. 目标用户流程

### 4.1 首页导入截图

```text
首页点“选择截图”
  -> 立即显示“正在把截图变成行动卡”进度卡
  -> 读取图片
  -> OCR 识别
  -> 结构化解析
  -> 生成行动卡
  -> 展示结构化确认页
```

用户不应该手动切换到导入页再找“解析当前草稿”。

### 4.2 确认页

确认页只做一件事：让用户确认 AI 字段。

建议结构：

```text
AI 解析结果
课程：英语口语
时间：明天 09:00
地点：E520
任务：上课
置信度：94%

风险：
- “明天”已按当前日期换算，请确认
- 地点 E520 可能需要校区/楼栋确认

[确认并安排] [先存入待确认]
```

### 4.3 行动编排页

```text
确认后安排
[✓] 加入日历：明天 09:00-10:00，英语口语课，E520
[✓] 提醒：课前 30 分钟
[✓] 地图：E520

[执行选中动作]
```

执行后展示结果：

```text
日历：已打开系统新增页，请保存
提醒：已调度本地提醒
地图：已打开地图 / 地点已复制
```

---

## 5. 建议新增验证脚本

### 5.1 `validate_calendar_prefill_accuracy.py`

检查：

- 输入“明天早上九点上英语口语教室 E520”后，Android 解析结果不出现 `null`。
- `CalendarDraft.startAtMillis` 对应次日 09:00。
- `CalendarContract.EXTRA_EVENT_BEGIN_TIME` 使用 `CalendarDraft.startAtMillis`，不是 `sampleCourse().startEpochMillis`。
- 日历说明文案只说“打开系统新增页”，不说“已写入”。
- 缺时间时日历按钮禁用。

### 5.2 `validate_no_user_facing_debug_copy.py`

检查普通 UI 源码中不出现：

```text
后端 /v2/analyze-image
MockModelAdapter
validate_
交付物自检
3分钟演示路线
后端模型编排
活动样例解析
课程样例
```

允许这些词只出现在 `DebugDemoScreen`、文档、测试中。

### 5.3 `validate_action_card_structure_ui.py`

检查：

- 存在 `ActionCardUiModel` 或等价结构。
- 确认页分开展示 title/time/location/task/actions/missing_fields/risks。
- `deadline_text == null` 时不会展示字符串 `null`。
- suggested_actions 被映射成可勾选动作，而不是只显示文本列表。

### 5.4 `validate_home_flow_simplification.py`

检查：

- 首页不包含完整确认表单。
- 首页不包含完整行动编排面板。
- 首页底部导航不遮挡内容。
- 首页上传截图后能触发 `AnalyzeProgressPanel` 或等价进度状态。

---

## 6. Codex Goal 建议

### Goal A：修复日历准确性

```text
/goal 修复拾刻导入日历不准确问题。检查 Android 模型结果映射、startEpochMillis、Calendar Intent 和相对时间归一化。要求：1) 从 /v2/analyze-image 或 /v1/analyze 返回的 normalized_start 生成 CalendarDraft.startAtMillis；2) 没有 normalized_start 但 start_text 是“明天早上九点”等可解析相对时间时，结合 current_date 和 Asia/Shanghai 归一化；3) 缺具体时间时禁用日历；4) deadline_text 为 null 不得在 UI 显示“null”；5) 日历文案只能说“打开系统新增页”，不能说“已写入/已同步”。完成条件：新增并通过 validate_calendar_prefill_accuracy.py、validate_action_execution.py、validate_real_world_ready.py。
```

### Goal B：清理普通用户页面

```text
/goal 清理拾刻普通用户页面中的重复模块和工程化内容。首页只保留今日主行动卡、待确认摘要、即将截止摘要、快捷导入和底部导航；导入页只保留导入与解析进度；确认页只保留结构化字段确认；行动编排页只保留日历/提醒/地图动作。普通用户路径不得出现后端/v2/analyze-image、MockModelAdapter、validate、自检、3分钟演示路线、后端模型编排、样例解析等词，这些只能在 DebugDemoScreen 中出现且需开发者模式解锁。完成条件：validate_no_user_facing_debug_copy.py、validate_home_flow_simplification.py、validate_frontend_polish.py、validate_demo_acceptance.py 通过。
```

### Goal C：结构化确认卡

```text
/goal 把 AI 输出从“识别文本拼标题”升级为结构化行动卡 UI。新增 ActionCardUiModel，分开展示课程/活动标题、开始时间、截止时间、地点、任务、置信度、风险、缺失字段和建议动作。禁止在 UI 显示 null；缺失字段用“待补充/暂无截止时间”。suggested_actions 映射为可勾选 ActionPlan。完成条件：validate_action_card_structure_ui.py、validate_calendar_prefill_accuracy.py、validate_user_facing_copy.py 通过。
```

### Goal D：一键导入闭环

```text
/goal 优化首页上传截图后的主流程。用户在首页选择截图或点击截图通知后，直接进入 AI 解析进度面板，不再要求手动切到导入页并点击解析当前草稿。进度步骤为读取图片、OCR识别、结构化解析、生成行动卡；成功后直接展示结构化确认卡，失败则进入待确认并允许手动编辑。完成条件：validate_analyze_progress_ui.py、validate_home_flow_simplification.py、validate_real_ocr_routing.py 通过。
```

---

## 7. 下一轮云真机验收清单

1. 输入“明天早上九点上英语口语教室 E520”，确认页不出现 `null`。
2. 点击日历后，系统日历预填为“明天 09:00”，不是样例日期或当前时间。
3. 缺时间时，日历按钮显示“补充时间后可用”。
4. 普通用户路径看不到“后端 /v2/analyze-image”“MockModelAdapter”“样例解析”。
5. 首页上传截图后直接显示解析进度，不需要切换页面。
6. 底部导航不遮挡内容。
7. 确认页结构化展示时间、地点、任务、风险和建议动作。
8. 执行后收件箱记录：日历打开、提醒调度、地图打开或失败降级。

---

## 8. 优先级排序

```text
P0 日历准确性：normalized_start -> CalendarDraft -> Calendar Intent
P0 清除普通用户路径里的工程词和 Debug 内容
P1 结构化行动卡 UI，禁止 null 文案
P1 首页截图导入直接进入解析进度
P1 行动编排从大按钮改成可勾选 ActionPlan
P2 截图删除/回收站闭环
P2 云真机重新录制日历准确性与 UI 精简证据
```
