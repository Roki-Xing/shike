# ModelAdapter 与结构化输出契约

对应 issue：`SHIKE-050`

## 设计原则

`ModelAdapter` 屏蔽具体模型供应商，上层流程只依赖统一输入输出。模型负责理解和建议，规则层负责校验、状态机和系统 API 执行。

## 接口定义

```kotlin
interface ModelAdapter {
    suspend fun analyze(input: ShikeModelInput): ShikeModelOutput
}

data class ShikeModelInput(
    val inputId: String,
    val sourceType: SourceType,
    val imageUri: String?,
    val ocrText: String,
    val locale: String = "zh-CN",
    val sceneHint: SceneType? = null,
    val userTimezone: String = "Asia/Shanghai"
)

data class ShikeModelOutput(
    val sceneType: SceneType,
    val confidence: Double,
    val title: String,
    val time: TimeInfo?,
    val location: LocationInfo?,
    val task: TaskInfo,
    val suggestedActions: List<SuggestedAction>,
    val missingFields: List<String>,
    val explanation: String
)
```

## 适配方式

| 适配器 | 用途 | 上层是否需要改动 |
|---|---|---|
| `MockModelAdapter` | 初赛演示、离线 Spike、回归样例 | 不需要 |
| `OpenAICompatibleModelAdapter` | 初赛或复赛早期快速接入通用多模态/文本模型 | 不需要 |
| `BlueLMModelAdapter` | 复赛根据 vivo 官方能力替换 | 不需要 |

## 模型职责

- 判断 `scene_type`：`course_notice`、`event_poster`、`unknown`。
- 输出 `confidence`，低于 0.65 时规则层默认进入人工确认优先。
- 抽取 `time`、`location`、`task`。
- 建议 `calendar`、`reminder`、`map` 三类动作。
- 标出 `missing_fields`，例如 `registration_url`、`exact_date`、`building_name`。
- 用 `explanation` 解释为什么建议处理。

## 规则层职责

- 校验 JSON Schema。
- 将相对时间解析为明确日期。
- 检查地点是否足以地图跳转。
- 阻止无用户确认的日历/提醒写入。
- 根据权限状态选择真实执行或降级。
- 将执行结果写回本地状态机。

## 样例请求

```json
{
  "input_id": "sample-course-001",
  "source_type": "screenshot",
  "ocr_text": "高数A班今晚18:30改到B203，上课前请提前到新教室。作业第5章今晚22:00前提交。",
  "locale": "zh-CN",
  "scene_hint": "course_notice",
  "user_timezone": "Asia/Shanghai"
}
```

## 样例响应

```json
{
  "scene_type": "course_notice",
  "confidence": 0.94,
  "title": "高数A班教室变更",
  "time": {
    "start_text": "今晚18:30",
    "deadline_text": "今晚22:00",
    "normalized_start": "2026-04-24T18:30:00+08:00",
    "normalized_deadline": "2026-04-24T22:00:00+08:00"
  },
  "location": {
    "raw": "B203",
    "map_query": "B203",
    "confidence": 0.82
  },
  "task": {
    "summary": "查看新教室路线并提交第5章作业",
    "priority": "high",
    "topic": "course"
  },
  "suggested_actions": [
    {"type": "calendar", "label": "加入日历", "requires_permission": true},
    {"type": "reminder", "label": "课前30分钟提醒", "requires_permission": true},
    {"type": "map", "label": "打开教室路线", "requires_permission": false}
  ],
  "missing_fields": [],
  "explanation": "文本包含课程、时间、地点和截止事项，适合转成行动卡。"
}
```

