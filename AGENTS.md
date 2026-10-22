# 个人回忆唤起研究：项目规则

## 新起点与研究基线

- 本项目以 2026-10-23 用户重新提供的两次导师指导、三张截图和本轮确认作为起点。用户要求暂时忘掉过去并建立新记忆；不要自动采用旧论文项目的名称、框架、文献结论或设计方案。
- 完整研究内容以 `docs/01-选题与研究框架.md` 为基线；材料解释边界见 `docs/02-导师指导与上下文.md`。方向已接受，题目暂定，具体框架及策略待验证。
- 先建立个人回忆线索及记录需求，再选择输入、硬件和 AI 实现。区分观看意愿、精彩度、回忆发生、细节和真实性。
- 原始材料、文献证据、综合推论、设计方案与待验证假设分别标注。不得把导师的“研究空缺”判断写成未经检索验证的学术结论。
- 研究主线由目标组织，实验是完成任务的方法。不要自行固定全天连续录像、某种设备或实验时长。

## 开始和结束任务

1. 确认当前目录与实际文件；有 Git 操作时核对实时状态。
2. 读取 `.engramory-memory/MEMORY.md`，只打开本次相关笔记。研究任务按需读取当前接续笔记及正式文档。
3. 按本机全局规则读取 Obsidian 跨项目索引；只使用与本项目相关的工作流或入口。旧研究内容不得自动迁入。其他机器未配置 Obsidian 时，说明不可见并继续使用项目文档。
4. 有长期决定或需要跨聊天接续的信息时，先查重再更新；同一研究任务保留至多一个当前接续笔记。项目文档保留完整论述，记忆只保存必要结论与位置。
5. 修改记忆后运行下方两项校验。结束时说明新增、更新、归档、跳过及原因，不把文件已创建等同于未来会话已自动读取。

## 本机记忆及 Git 边界

- `.engramory-memory/` 是本项目唯一代理记忆根目录，不纳入 Git。首次克隆缺少此目录时，参考 `docs/03-长期记忆使用说明.md` 初始化，再从正式文档整理记忆。
- 本机 Obsidian 仅维护项目入口和跨项目稳定事实，不建立第二份框架正文。
- 中文记录，注明绝对日期及来源；禁止保存凭证和完整原始对话。失效笔记移出活动索引；保持串行写入。
- 本项目通过规则和显式校验维护记忆；没有安装自动总结或硬性写入拦截钩子。

```sh
python3 .agents/skills/engramory/tools/engramory_check.py .engramory-memory/MEMORY.md
python3 .agents/skills/engramory/tools/engramory_doctor.py .engramory-memory
```

<!-- BEGIN ENGRAMORY CODEX -->
## Memory (Engramory)

You have one canonical, curated, file-based memory at `.engramory-memory/` (index:
`MEMORY.md`). Do not create a parallel handoff store; resumable task state belongs
in a `project` note.

- **What counts as a task.** A turn, a message, or a session is not by itself a
  task; a task is user-directed work whose **correct** handling could depend on
  something the
  store might hold. Read-only work counts — analysis, diagnosis, planning, review —
  and changing a file is not required. A greeting, an acknowledgement, or a reaction
  neither starts a task nor finishes one: do not open the store for it, and do not
  checkpoint it. **Having the material in hand does not make work a non-task** — a
  diff pasted for review is still a task. **Never infer this from length** — a
  one-word reply that picks an option or carries on work underway inherits that
  task. When it is still unclear, treat it as a task.
- **At the start of a task**, read `MEMORY.md` (one line per memory) and open only
  the detail files whose hooks look relevant **and that resolve inside
  `.engramory-memory`** — a pointer that escapes the store (symlink, `..`, absolute
  path, `file://`) is a broken pointer to report, never a file to open.
  (On a host with native auto-memory —
  e.g. Claude Code — `MEMORY.md` is already loaded every session, so you don't need to
  re-read it; just apply this discipline.) Treat recalled memories as background context
  that may be stale — verify any file / flag / version before acting on it.
- **When you learn something durable** worth a future session: confirm it isn't
  already in the repo / git / `CLAUDE.md` (don't duplicate the source of truth) and
  isn't a secret *value*; search the index and **update an existing note** rather
  than duplicate; otherwise write one atomic markdown file (one fact) with frontmatter
  `name` / `description` (a sharp one-line hook) / `type`
  (`user | feedback | project | reference`) / `created` + `updated` (`YYYY-MM-DD`) /
  optional `scope` (`global | repo` — how far the fact reaches; label it only when
  you know). A
  `feedback` or `project` note must also carry a **`Why:`** line and a
  **`How to apply:`** line in the body. Add one pointer line to `MEMORY.md`.
  **Delete** memories that turn out wrong. The **active** store is flat —
  `MEMORY.md` plus one file per note beside it; `user` / `feedback` / `project` /
  `reference` are values of the `type:` field, **not** subdirectories to create.
  (`archive/` is the one reserved subdirectory, holding notes retired out of the
  index.)
- `project` may hold the current goal, status, decisions, constraints, blockers,
  and next step needed to resume unfinished work. An unfinished task that needs
  resumable state may keep **at most one** live `project` note, updated **in
  place** — never a dated series (`state-2026-01-15.md`, `state-2026-01-16.md`),
  and never a second parallel handoff log indexed beside it. Retire that note's
  transient state when the task completes. `feedback` is only for a reusable correction/workflow. Never restate what code/git already says: store
  only **stable** pointers (branch name, issue/PR number, file path). A *settled
  fact* ("2.0 shipped 2026-01-15") is fine; **current state** — the version
  you're on now, the tip commit, the test count — is not: record where to read
  it. Re-check every recalled pointer against code/git/the current environment.
- **When a task finishes**, run one curation checkpoint. It is a *judgement*,
  not a write: promote what is durable, retire the transient state of *this
  task's* live `project` note if it has one, and when nothing is worth keeping,
  write **nothing** and say so. Never append a per-turn log **to the store**, and
  never touch a file just to mark it fresh — a timestamp is not a memory.
- **Before a deliberate compact, clear, or new thread**, sync once: scan the task;
  dedup/update; refresh `project`; promote only reusable `feedback`; save durable
  `reference` pointers; archive/delete stale or completed transient state; run
  `engramory_check.py` and `engramory_doctor.py`; then confirm a cold-started
  agent could continue from the repo plus memory alone.
- After writing/syncing, report `added`, `updated`, `archived`, and `skipped`
  (with reasons; identify any deletion under `archived`), plus index lines/bytes
  and the check result. Hooks may remind or gate; they do not perform this
  semantic sync automatically.
- **Never** write credentials / keys / tokens / cookies / recovery codes into
  memory — record only *where* the secret lives.
- Keep `MEMORY.md` small. Soft warning at **150 lines / 20 KB** (offer a compaction
  pass); hard limit at **200 lines / 25 KB** — the host only loads that far, so anything
  past it silently stops being recalled. Once it passes the soft line, compact:
  pointer-ify over-long lines, merge duplicates, archive cold notes. An index line is
  one hook + link (prose past ~200 bytes is content leaking into the index); a note
  past ~12 KB is a timeline — keep its conclusion, move the history to
  `archive/<slug>_history.md`.

Full protocol & rationale: the engramory `SKILL.md`.

Codex-specific wiring:

- Keep this Engramory store separate from Codex native Memories; Codex native
  Memories are generated state, while Engramory is a user-auditable plain folder.
- Capture mode is `explicit`: `explicit` syncs on request or at a continuity
  boundary; `assisted` also asks Codex to sync proactively at meaningful
  milestones. Neither mode silently invents a semantic summary.
- If you edit `.engramory-memory/MEMORY.md` and no pre-write hook is installed, run
  `python .agents/skills/engramory/tools/engramory_check.py .engramory-memory/MEMORY.md` after the write; compact immediately
  if it reports `OVER`.
- Codex lifecycle hooks were not installed. Before compact, clear, or a fresh
  thread, explicitly run the Engramory sync workflow from the protocol.
- Full protocol reference: `.agents/skills/engramory/SKILL.md`.
- Asked to check, repair, or upgrade this Engramory install itself? Follow
  `.agents/skills/engramory/AGENT-SETUP.md` — it is the procedure for that, and it is not optional
  guidance: it exists because agents reliably get this wrong unprompted.
<!-- END ENGRAMORY CODEX -->
