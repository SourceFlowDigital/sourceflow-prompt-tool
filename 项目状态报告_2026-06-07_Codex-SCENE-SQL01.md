# 项目状态报告 · T-SCENE-SQL01

## 执行前 Git 状态摘要

- `git status --short`：工作区执行前存在若干既有未跟踪文件，包括工作日志、`_data_prep/`、Excel 数据文件和小程序配置文件；本任务未处理这些既有文件。
- 最近提交：`71c229c`、`8754d7c`、`4cb5895`、`c32fb87`、`3c8490a`。

## 新增文件清单

- `_data_prep/prompt_scenes_schema_and_data.sql`
- `项目状态报告_2026-06-07_Codex-SCENE-SQL01.md`

## SQL 内容摘要

- 使用 `CREATE TABLE IF NOT EXISTS` 创建 `prompt_scenes`。
- 使用 `CREATE TABLE IF NOT EXISTS` 创建 `agent_template_scenes`。
- 插入并可重复更新 8 个系统场景。
- 插入并可重复更新 108 个角色对应的 231 条角色-场景映射。
- `agent_template_scenes.sort_order` 按同一角色的推荐场景顺序从 1 开始。
- 未修改现有 `agent_templates` 表结构。

## 数据核对

- 场景数量：8
- `roles.js` 角色数量：108
- `agent_templates_insert.sql` role_id 数量：108
- `roles.js` 与 SQL role_id 顺序一致：是
- 角色-场景映射数量：231

## 每个场景覆盖角色数量

| scene_id | 覆盖角色数量 |
|---|---:|
| `content_creation` | 30 |
| `growth_conversion` | 35 |
| `research_analysis` | 36 |
| `planning_strategy` | 32 |
| `product_development` | 29 |
| `design_experience` | 11 |
| `quality_risk` | 24 |
| `operations_delivery` | 34 |

## 自定义场景需求记录

1. 固定 8 个系统场景进入 `prompt_scenes`。
2. 角色与系统场景映射进入 `agent_template_scenes`。
3. “自定义”不是第 9 个标准场景，不进入 `prompt_scenes`。
4. “自定义”不进入 `agent_template_scenes`。
5. 后续前端场景选择区需要在推荐场景后固定显示“自定义”。
6. 用户点击“自定义”后展示输入框。
7. 后续接口建议支持 `scene_id` 与 `custom_scene_text`。
8. 用户选择系统场景时，`scene_id` 为系统场景 ID，`custom_scene_text` 为空。
9. 用户选择自定义时，`scene_id` 可传 `custom`，`custom_scene_text` 为用户输入内容。
10. 该需求留待后续前端和接口改造任务处理，本任务未修改代码。

## 执行结论

- 是否执行数据库：否
- 是否修改业务代码：否
- 是否进行 git add / commit / push：否
- 是否建议进入人工审查：是
