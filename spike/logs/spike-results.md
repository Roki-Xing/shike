# Spike 结果

| 检查项 | 状态 | 说明 |
|---|---|---|
| OCR/图片导入模拟 | 通过 | 载入 3 个样例请求 |
| 结构化字段抽取 | 通过 | 课程通知与活动海报均返回 scene_type/time/location/task |
| 日历或提醒写入 | 通过 | action plan 生成 calendar/reminder 动作，权限拒绝时降级 |
| 地图 deeplink | 通过 | map 动作生成，权限拒绝时降级为 copy_location |
| SQLite 状态存储 | 通过 | 收件箱写入 3 条记录 |
