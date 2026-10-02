# 组织仓库定制约束

本仓库以 ranxi2001/sub2api production 为功能上游。origin 为 baibaiAi001/sub2api。
仅保留图片生成工作台（image-generation）、首页（home-showcase）、教程（tutorials）、充值提醒（recharge-notice）四项站点定制。
production 保持基线；开发在 migration/four-extensions，验收后进入 custom/production。
未经用户明确授权不推送代码、不修改生产部署或数据库。迁移开发与线上 /home/sub2api/app 隔离。
扩展代码放 backend/internal/extensions 与 frontend/src/features；核心文件只保留必要组装，遵循 fork 的鉴权、调度和计费。
不手写 Wire 或 Ent 生成代码，按目标仓库命令生成。已执行迁移不可改内容、改名或删数据库记录。
不迁入旧模型广场实现、DeepSeek Helper、本地工具、旧 Pelican 图库及 STATE 外接服务。fork 原生功能仍保留。
保留历史业务数据和实际充值倍率；清理历史数据另行处理，不能在功能退出时直接删表。
任何候选程序不得连接生产数据库或缓存做验证。恢复演练必须隔离网络与持久目录。
合并前验证后端相关单元/契约/集成、前端类型和相关测试、构建、迁移 checksum；使用中文交付，明确未验证事项。
不得提交环境密钥、数据库备份、运行日志或二进制。
