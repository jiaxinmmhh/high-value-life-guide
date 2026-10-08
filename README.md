# 高性价比人生决策 Skill

将eternity4719《高性价比人生指南》转成能按问题调用的决策工具：先比较成本、收益与证据，再挑一两项实际行动。

## 已包含什么
- 主Skill：决策流程、四种资源账、证据规则、章节与主题导航。
- 33节方法文件：可执行规则、例子、适用边界，以及全部603条的标题／证据／PDF页码。
- 五篇附录方法、术语表、操作模板和一页决策速查。
- 本地检索工具：按关键词、编号、章节、书中证据等级查询。
- 来源版本与核验说明，[完整性和检索检查报告](VALIDATION.md)。

本包整理方法和定位，未逐条复写603条的完整收益数据。需精确数字或具体操作时，回读原PDF和当前权威资料。PDF没有打包，方便保持Skill轻量；后续机器上回读需要自行提供同一版本PDF。

## GitHub 获取

仓库：[jiaxinmmhh/high-value-life-guide](https://github.com/jiaxinmmhh/high-value-life-guide)，私有。安装包见[v1.0.0版本](https://github.com/jiaxinmmhh/high-value-life-guide/releases/tag/v1.0.0)，访问需要仓库权限。

已登录GitHub CLI时，可以取得整个Skill：

```bash
gh repo clone jiaxinmmhh/high-value-life-guide
```

## 在Codex中使用
将整个 `high-value-life-guide` 文件夹放到Codex能发现的技能目录，如个人的 `~/.codex/skills/`，或项目内的 `.agents/skills/`。文件夹第一层应直接包含 `SKILL.md`、`chapters/` 等。重新打开聊天后调用。

当前交付为可安装包，尚未写入你的全局技能目录。它与作者仓库原有的 `life-decision-guide` 是不同的转换产物。

可以直接说：

> 用 high-value-life-guide 帮我判断：每天单程通勤一小时，要不要搬家？把钱和时间分开算。

> 用 high-value-life-guide 处理我的拖延，给我一个今天能开始的动作和退出条件。

> 查第23节，帮我把正在学的内容改成自测、间隔和实际应用计划。

> 朋友让我担保，按书里的方法帮我列清楚需要核对的责任。

> 找第32节的留学身份条目，先指出书中主张，再核验当前官方规则。

若还没安装，也可以直接把此文件夹的 `SKILL.md` 指给当前AI读取使用。

## 本地查询
在Skill文件夹内运行：

```bash
python3 scripts/search.py "担保"
python3 scripts/search.py "替朋友担保签不签" --limit 5
python3 scripts/search.py --id 4.2
python3 scripts/search.py --chapter 23 --limit 30
python3 scripts/search.py "运动" --evidence A --json
```

检索只依赖Python标准库，不联网、不读其他目录、不修改文件。命中标题不代表已验证该建议。

可选的PDF回读工具需要pypdf：

```bash
python3 scripts/read_pdf_pages.py --pdf "/绝对路径/原书.pdf" --start 134 --end 137
```

也可以在PDF阅读器直接跳转同一物理页。脚本不会自动安装依赖或自动去查网上资料。

## 来源和授权
书中版本：2026-09-25 08:51，北京时间，提交6576d14；转换日期：2026-10-08。原PDF的摘要值在 `references/manifest.json`。

PDF841页声明以Unlicense发布。本包转换内容也采用Unlicense。应用示例均标为重构或组合示例；未经核验的医学、法律、财务和政策主张保留为来源线索。
