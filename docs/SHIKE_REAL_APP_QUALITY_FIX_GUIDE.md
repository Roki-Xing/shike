# 拾刻真实应用质量修复指导：识别准确性、权限、截图助手、系统协同与 UI 去工程化

> 适用方式：放入仓库 `docs/SHIKE_REAL_APP_QUALITY_FIX_GUIDE.md`，然后用 Codex `/goal` 按阶段持续执行。  
> 目标：把云真机上看到的“能跑 Demo”升级为“像真实 App、识别可信、交互自然、系统协同完整、评审可复测”的复赛作品。  
> 安全红线：不要把 AppKEY、私钥、服务器 token、真实 OCR、手机号、学号、真实相册内容写入代码、文档、日志、录屏或 APK。

---

## 0. 当前真实问题结论

这轮云真机表现暴露的问题不是单点 bug，而是 5 个产品级短板：

1. **识别链路仍有样例污染**：真实截图只出现“今天晚上需要上高数 A”时，结果仍可能被填成“高数 A 班教室变更 / B203 / 18:30 / 22:00 / 第 5 章作业”。这说明真实 OCR/模型结果和 Mock/样例 fallback 没有隔离干净。
2. **截图助手还没形成用户感知闭环**：仓库已有 MediaStore + 通知式截图助手能力，但需要权限引导、首启说明、云真机可验证录屏和更自然的“检测到截图，是否交给拾刻？”通知。
3. **权限策略像工程功能，不像产品体验**：通知、截图助手、相册、相机、日历、地图等权限/系统能力应在首启 Onboarding 里按用途解释，不能散落到各个按钮后才突然弹系统框。
4. **系统协同不够强**：当前有 Calendar Intent、AlarmManager、本地通知、地图 deeplink、截图删除请求，但用户感受到的仍像按钮集合；需要动作执行结果、失败兜底、回到今日行动台的闭环更清晰。
5. **UI 仍有工程痕迹**：后端、Mock、调试、模型编排、3B 诊断、自检、演示路线等内容不能出现在普通用户主路径。普通用户只应看到“导入、确认、安排、追踪”。

复赛评审材料提醒，复赛看的是作品开发、大模型理解与应用能力、API 调用能力、开发能力和创新思维；提交物也必须包含可运行作品、演示视频/海报、PPT 与代码打包。因此下一步应优先修复“真实运行体验”，而不是继续堆验收脚本。

---

## 1. P0：识别准确性与样例污染修复

### 1.1 当前高风险点

后端 `MockModelAdapter._course_output` 仍保留固定输出：

```text
高数A班教室变更
今晚18:30
今晚22:00
B203
第5章作业
```

这对离线演示有用，但对真实云真机测试是危险的。只要真实链路因凭据、网络、模型输出、schema 校验失败而回退 Mock，用户就会看到“看似准确但其实是假数据”的行动卡。

必须建立三类模式：

| 模式 | 允许使用 Mock 固定样例吗 | UI 是否显示给普通用户 |
|---|---|---|
| `demo_mode` | 允许 | 只在 DebugDemoScreen |
| `cloud_device_test` | 不允许，除非录制 fallback 场景 | 不显示 Mock 字样 |
| `release_user` | 不允许固定样例污染真实输入 | 不显示工程词 |

### 1.2 正确识别策略

真实输入必须严格遵守：

```text
只从 OCR 文本、OCR block、图片证据、用户编辑字段中抽取。
没有证据的时间、地点、任务不得自动补样例。
缺字段就进 missing_fields 和待确认。
```

例如：

```text
输入：今天晚上需要上高数A
```

正确输出：

```json
{
  "scene_type": "course_notice",
  "title": "上高数 A",
  "time": {
    "start_text": "今天晚上",
    "deadline_text": null,
    "normalized_start": null,
    "normalized_deadline": null
  },
  "location": null,
  "task": {
    "summary": "今天晚上需要上高数 A，具体时间和地点待确认",
    "priority": "medium",
    "topic": "course"
  },
  "suggested_actions": [
    {"type": "reminder", "label": "稍后确认上课时间", "requires_permission": true}
  ],
  "missing_fields": ["exact_start_time", "location"],
  "explanation": "文本只包含课程主题和相对时间，缺少具体时间和地点。"
}
```

错误输出：

```text
B203 / 18:30 / 22:00 / 第5章作业
```

### 1.3 后端修复要求

新增或强化：

```text
validation/validate_no_sample_contamination.py
validation/validate_real_ocr_routing.py
validation/validate_provider_not_mock_in_cloud_mode.py
```

检查点：

- `今天晚上需要上高数A` 不得输出 `B203`、`18:30`、`22:00`、`第5章`。
- `/v2/analyze-image` 若进入 fallback，必须在 `risks` 中标记 `text_fallback` 或 `manual_review`，不能伪装为真实模型成功。
- `SHIKE_RUNTIME_MODE=cloud_device_test` 或 `release_user` 时，真实图片/文本输入不得走固定 demo 样例。
- `MockModelAdapter` 只允许在 `demo_mode` 或后端不可用 fallback 录屏中出现。
- 后端审计日志记录 `provider`、`route`、`status`、`input_id_hash`、`ocr_block_count`、`repair_risks`，不记录完整 OCR 和图片。

### 1.4 Prompt 修复要求

`analyze_image_system_prompt.txt` 与文本解析 prompt 必须包含：

```text
你只能依据 OCR_TEXT、OCR_BLOCKS、图片中可见内容和用户提供的 scene_hint 输出字段。
不得使用示例字段填充结果。
如果时间、地点、任务没有在证据中出现，必须设为 null 或待确认，并写入 missing_fields。
不得把 B203、18:30、22:00、第5章等样例字段带入真实输入，除非 OCR 明确出现。
每个关键字段必须能在 evidence 中找到来源。
```

---

## 2. P0：截图助手与通知入口

### 2.1 能不能实现“截图后弹窗/提醒是否进入拾刻”？

可以做，但正确产品形态应是：

```text
截图助手模式开启
-> 观察 MediaStore 最近截图
-> 识别疑似新截图
-> 发系统通知：检测到截图，是否交给拾刻？
-> 用户点通知
-> 打开拾刻导入页
```

不要把主方案做成全局悬浮窗。悬浮窗/辅助功能权限会让用户和评委警惕，且普通 App 不应默认监听所有屏幕。

### 2.2 当前仓库已有基础

当前 `AndroidManifest.xml` 已声明：

```xml
android.permission.DETECT_SCREEN_CAPTURE
android.permission.READ_MEDIA_IMAGES
android.permission.POST_NOTIFICATIONS
```

`MainActivity` 已有：

```kotlin
ScreenshotObserver
showScreenshotDetectedNotification
ACTION_IMPORT_SCREENSHOT
pendingScreenshotCandidate
```

说明截图助手已经不是空想。下一步是把它从“工程能力”做成“用户可理解能力”。

### 2.3 首启权限引导

首次打开 App 应出现一页 Onboarding，而不是直接把用户丢进功能页。

文案建议：

```text
拾刻需要这些权限来帮你少漏事：

1. 通知权限
用于截图后提醒你“是否交给拾刻”，以及到点提醒。

2. 图片权限
仅用于你开启截图助手后识别新截图；默认不上传原图。

3. 相机权限
用于拍活动海报或公告。

4. 日历与地图
用户确认后才打开系统日历或地图，不会自动替你执行。
```

交互：

```text
[开启截图助手] [稍后再说]
```

如果用户点开启，再依次申请：

```text
POST_NOTIFICATIONS
READ_MEDIA_IMAGES
CAMERA 只在拍照时申请
```

### 2.4 验收

新增：

```bash
python3 shike/validation/validate_permission_onboarding.py
python3 shike/validation/validate_screenshot_assist.py
```

必须检查：

- 首启有权限解释页。
- 通知权限不是静默假设已开。
- 截图助手开关默认关闭或明确提示。
- 关闭截图助手后不再观察 MediaStore。
- 新截图通知文案是用户语言，不是工程语言。

---

## 3. P0：日历、提醒、地图协同升级

### 3.1 当前问题

当前系统协同能力已经存在，但用户感知还不强：

- 日历：使用系统新增页 Intent，用户需要在系统日历中保存。
- 提醒：使用 AlarmManager / 通知权限。
- 地图：使用 geo deeplink。
- 失败：保留行动卡。

问题是 UI 没有把“已打开日历页 / 已调度提醒 / 地图已打开 / 失败已保留”表达成清楚的结果流。

### 3.2 日历

保守方案继续使用：

```text
Intent.ACTION_INSERT + CalendarContract.Events.CONTENT_URI
```

文案必须是：

```text
已打开系统日历新增页，请在日历中保存。
```

不能写：

```text
已写入日历
```

除非你后续申请 Calendar Provider 权限并真正写入。

### 3.3 提醒

提醒要分成两类：

| 类型 | 触发 |
|---|---|
| 截图助手通知 | 截图后询问是否导入 |
| 行动提醒 | 用户确认行动卡后，按时间调度 |

必须在执行结果里显示：

```text
本地提醒已调度
模式：精确定时 / 普通定时降级
触发时间：...
```

### 3.4 地图

地图打开前要检查地点是否可靠：

```text
location.raw != null
location.confidence >= 0.6
```

否则按钮禁用，文案：

```text
缺少可靠地点，先补充地点后再打开地图。
```

地图不可用时：

```text
已复制地点，行动卡保留在收件箱。
```

### 3.5 验收

强化：

```bash
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_calendar_map_reminder_ux.py
```

检查：

- 未确认前日历/提醒/地图不可执行。
- 缺时间时日历禁用。
- 缺地点时地图禁用。
- 日历文案不声称已写入。
- 提醒调度模式可见。
- 地图失败复制地点。

---

## 4. P0：普通用户界面去工程化

### 4.1 不应该出现在普通用户页面的内容

以下内容必须移入 DebugDemoScreen，并且 Debug 入口需要隐藏：

```text
后端地址
MockModelAdapter
/v1/analyze
/v2/analyze-image
3B 多模态诊断
交付物自检中心
validate_*
3分钟演示路线
模型编排：本地 mock 待命
云侧 provider 配置
```

普通用户只应该看到：

```text
首页：今天要处理什么
导入：选截图 / 拍照 / 分享 / 手动输入
确认：AI 识别到什么、哪里不确定、我能怎么改
安排：日历 / 提醒 / 地图
收件箱：处理到哪一步
设置：隐私、截图助手、清除数据、关于
```

### 4.2 首页目标

首页一屏内只保留：

```text
顶部：拾刻 + 今日行动台 + 设置入口
主卡片：最需要处理的 1 张行动卡
快捷导入：选择截图 / 拍照 / 手动输入
摘要：待确认 / 即将截止 / 地点待处理
底部导航：首页 / 导入 / 收件箱 / 设置
```

不要让首页滚成很长。

### 4.3 底部导航

保留 4 项：

```text
首页
导入
收件箱
设置
```

Debug 入口：

```text
设置 -> 关于拾刻 -> 连点版本号 5 次
```

当前仓库已有开发者模式 5 连击逻辑，下一步是确保用户路径里完全看不到“调试”两个字。

### 4.4 视觉标准

方向：

```text
克制、清爽、可信、留白、有层次
```

不要：

```text
大段工程说明
重复卡片
假状态栏
假电量
大量按钮堆叠
```

状态栏应交给系统，不在 App 内自绘假 10:28 / 100%。

### 4.5 验收

新增或强化：

```bash
python3 shike/validation/validate_user_facing_copy.py
python3 shike/validation/validate_home_one_screen.py
python3 shike/validation/validate_no_fake_status_bar.py
python3 shike/validation/validate_frontend_polish.py
```

---

## 5. P1：导入后清理原截图

### 5.1 产品价值

这是拾刻最有惊喜感的闭环：

```text
截图 -> 识别 -> 行动卡 -> 安排 -> 原截图不再睡在相册
```

### 5.2 交互

用户确认行动卡后展示：

```text
这张截图已经生成行动卡，是否把原图移入系统回收站？
[移入回收站] [保留原图]
```

不允许静默删除。

### 5.3 技术

优先使用：

```kotlin
MediaStore.createTrashRequest(...)
```

如果来源 URI 不是 MediaStore 或不支持删除：

```text
该来源不支持直接清理，可手动在相册中删除。
```

### 5.4 验收

```bash
python3 shike/validation/validate_screenshot_cleanup.py
```

检查：

- 删除动作必须在用户确认行动卡之后。
- 必须弹系统确认。
- 失败时 UI 明确说明。
- 清理结果写入收件箱执行结果。

---

## 6. P1：Codex 执行顺序

### Goal A：识别准确性与样例污染

```text
/goal 修复拾刻真实 OCR/图片识别准确性问题。重点检查是否仍有样例字段污染真实输入：输入“今天晚上需要上高数A”不得输出 B203、18:30、22:00、第5章作业。区分 demo_mode、cloud_device_test、release_user，真实云真机链路不得使用固定 Mock 样例，除非明确录制 fallback 场景。优先修改 MockModelAdapter、v2 analyze-image fallback、Prompt、Android 展示文案和验证脚本。完成条件：新增 validate_no_sample_contamination.py、validate_real_ocr_routing.py、validate_provider_not_mock_in_cloud_mode.py 并通过；verify_backend.py、validate_model_contract_strict.py、run_model_eval.py 通过。
```

### Goal B：截图助手与权限 Onboarding

```text
/goal 把截图助手从工程能力升级为用户可理解的首启权限体验。实现首启 Onboarding，说明通知权限、图片权限、相机权限、日历/地图协同用途；截图助手默认由用户显式开启。开启后通过 MediaStore 观察新截图，并用系统通知展示“检测到截图，是否交给拾刻？”。不要做默认全局悬浮窗；关闭截图助手后停止观察。完成条件：validate_permission_onboarding.py、validate_screenshot_assist.py、validate_secret_hygiene.py、validate_android_structure.py、validate_android_unit_tests.py 通过。
```

### Goal C：首页去工程化与艺术化

```text
/goal 把拾刻普通用户界面改成真实 App。首页一屏只展示今日主行动卡、快捷导入、待确认/即将截止摘要和底部导航；移除或隐藏假状态栏、假电量、后端地址、MockModelAdapter、validate、交付物自检、3分钟演示路线、3B诊断等工程内容。Debug 只能从设置页版本号 5 连击进入。完成条件：validate_user_facing_copy.py、validate_home_one_screen.py、validate_no_fake_status_bar.py、validate_frontend_polish.py、validate_demo_acceptance.py 通过。
```

### Goal D：系统协同闭环

```text
/goal 强化日历、提醒、地图三类系统协同。未确认前禁止执行；缺时间禁用日历，缺地点禁用地图；日历只声明“已打开系统新增页”，不声称已写入；提醒显示精确定时/普通定时降级模式；地图失败时复制地点并保留行动卡。执行结果写入收件箱。完成条件：validate_calendar_map_reminder_ux.py、validate_action_execution.py、validate_real_world_ready.py 通过。
```

### Goal E：原截图清理闭环

```text
/goal 实现导入成功后的原截图清理闭环。用户确认生成行动卡后，显示“是否把原截图移入系统回收站？”使用 MediaStore.createTrashRequest 或等价系统确认流程，不允许静默删除。来源不支持删除时给出解释。清理结果写入执行结果和收件箱。完成条件：validate_screenshot_cleanup.py、validate_action_execution.py、validate_real_world_ready.py 通过。
```

---

## 7. 复赛口播修正

旧口播容易给人感觉仍是原型。更新为：

```text
拾刻现在不是只做原型，我们已经在 vivo 云真机上跑通 Android APK。它的关键不是再做一个 OCR 或待办，而是把截图从“保存”推进到“行动”：截图后拾刻会提示是否导入，蓝心 OCR 和模型解析出时间、地点、任务，用户确认后才进入日历、提醒和地图；安排完成后还能把原截图移入系统回收站，减少相册沉积。模型不确定时不会乱执行，会标出缺失字段并进入待确认。
```

---

## 8. 最终判断标准

做到下面 6 点，才像真实应用：

1. 用户打开首页，不看到任何工程词。
2. 截图后有自然提醒：“是否交给拾刻？”
3. 识别结果不再被样例污染。
4. 缺字段时敢于说“不确定”。
5. 日历、提醒、地图执行结果明确且可回退。
6. 安排完成后可以处理原截图，真正解决“截图睡在相册里”。
