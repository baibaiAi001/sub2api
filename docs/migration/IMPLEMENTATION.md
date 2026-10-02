# 四项扩展移植记录

目标仓库：baibaiAi001/sub2api；基线 production bc83ff9c；开发分支 migration/four-extensions。

## 已迁移

- 图片生成工作台及设置，图生图、提示词优化、用户设置和权限检查；目录接口适配 fork 的 ListGroups，未引入旧自定义模型广场。
- 定制首页、品牌资源、国际化；价格链接使用 fork 已存在的原生 /model-plaza，GitHub 链接指向组织仓库。
- 教程前后端、封面管理、公开视频/播放计数及设置集成；224_tutorial_video_play_counts.sql 原样保留。
- 充值提醒组件；倍率读取正式支付接口，原生充值计算保持不变。只读核实生产 BALANCE_RECHARGE_MULTIPLIER=10.00。

未迁入旧 DeepSeek Harness、本地工具/Helper、旧 Pelican、旧模型广场实现、STATE 外部服务。fork 原生功能保留。

Wire 由工具重新生成；新增教程返回字段已更新 API 契约测试。新 fork 支持 gateway-only 运行角色，路由测试同步了新增数据库依赖。

## 已通过的验证

- 前端 vue-tsc 类型检查，7 个测试文件 / 23 个测试，以及生产构建。
- 四扩展前端及首页的定向 ESLint。
- 后端 image-generation 根包、handler、service 和 tutorials 测试。
- 后端 admin、service、server、server/middleware、server/routes、migrations、cmd/server 单元检查；首次 server 失败由教程字段期望和参数变化引起，修复后重跑 server 全部通过。
- 带嵌入前端的 Go 候选二进制编译。
- 旧教程 SQL 逐字节一致，git diff --check 和扩展范围检查通过。

## 隔离与上线边界

开发目录与生产 /home/sub2api/app 分离，生产 .env 和容器未切换。
备份 /home/sub2api/runtime/backups/20261002-pre-org-migration 包含数据库、应用数据、旧镜像、部署配置、源码 tar 和 Git bundle，SHA256 已校验。
全量数据库恢复演练单独记录在宿主 /home/sub2api/migration，恢复过程受 6 GiB 可用空间下限保护。
正式切换前必须完成恢复与兼容验证，重新停写备份，并关闭数据库遗留 openai_codex_ticket_enabled 等可能触发后台行为的设置。
代码完成不代表已达到生产发布条件；生产切换和推送待独立发布步骤执行。

## 本轮结果与发布阻断项

四模块移植提交：17889c3d8。前述验证已经通过，生产仍是 sub2api:20260930-v0.2.11-f3e555020。

2026-10-02 完整备份恢复演练未完成：无网络隔离 PostgreSQL 恢复数据后，在创建索引阶段因剩余空间不足 6 GiB 自动停止。释放本次缓存并重试 post-data 后，副本达到约 23 GB，再次触发相同空间保护。临时数据库目录已清理，完整压缩备份保留。

因此尚未验证：完整恢复耗时、候选程序在真实数据副本上的启动、30 条新迁移的实际执行、旧镜像读取迁移后数据库的兼容性，以及四项页面的端到端业务操作。不能把源码/测试通过等同于可正式发布，也不能保证全量恢复可在几分钟内完成。

下一步需为隔离环境提供足够空间（建议至少 50 GB 可用空间，含完整库、索引重建和临时文件余量），或迁至另一测试机。先完整恢复备份并验证，再运行迁移和新旧程序兼容演练。正式切换前重新停写备份；不能以本次开发前快照覆盖后续交易数据。

## 正式上线完成（2026-10-02 UTC）

清理授权的构建缓存后，重新完整恢复数据库成功（pg_restore 退出码 0）。在无外网副本上新镜像执行全部 30 条新迁移，记录由 296 增至 326；新旧镜像各通过 14 项 HTTP/API 检查。用户、账号、Key、余额、订单和教程计数相同；用量明细因原有 90 天保留清理减少，未发现账务变化。

正式停写备份：/home/sub2api/runtime/backups/20261002-org-cutover。数据库与应用数据 SHA256 校验通过。
当前镜像：sub2api:org-v2.9.7-custom.1-35621e321。
镜像 ID：sha256:7f2dd306dc0e0d35b81d183e6b9f7ea23e64be4c2b1ef8fe543b552dfb7fa9b5。

2026-10-02 19:40 UTC 切换后容器 healthy、公网 health=ok，生产 14 项接口检查通过，充值倍率仍为 10，遗留 ticket 开关关闭。上线检查窗口内无 ERROR/FATAL/panic，观察到正常业务 HTTP 200。未发起额外付费模型测试，未做完整浏览器交互验收。

快速回退脚本：备份目录 rollback-image.py。旧镜像已在迁移后副本验证可启动及读取相关接口；全量数据库恢复为最后手段，不能承诺未来启用新平台/新功能后仍可直接回退。
隔离演练容器与数据库副本已清理。完整代码历史、旧镜像归档及两份数据库备份保留。未推送远程 Git 或镜像仓库。
