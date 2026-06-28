<CRITICAL_INSTRUCTION>

# AI AGENT OPERATING CONSTITUTION

## Classification: STANDARD

This file is a `STANDARD` (mandatory and formalized) for safety, security, and consistency.

## Repository Development Agent Rules

This document governs the development agent for this repository.

These instructions are authoritative and binding.
Treat all MUST, REQUIRED, DO NOT, STOP, and NEVER directives as hard constraints.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# COMPANION STANDARDS (MANDATORY)

`AGENTS.md` is the constitutional entrypoint for this policy set.
Look in the `agents` directory for more consitutional documents. Treat every file in `agents` directory as a Standard and must follow.
Agents MUST load and comply with all referenced files before implementation work.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# RULE PRECEDENCE

If instructions conflict, precedence order is:

1. System, developer, and runtime safety instructions
2. `AGENTS.md`
3. `agents/*.md` in alphabetical order
4. Repository conventions and existing architecture
5. Explicit user request
6. MCP tool guidance

If conflict cannot be resolved deterministically:
YOU MUST STOP AND REPORT.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# EXECUTION MODES

## READ-ONLY MODE

If the user asks for analysis, design discussion, or review-only work:

- You MAY inspect files.
- You MUST NOT modify files.

## IMPLEMENTATION MODE

For code changes, explicit approval and all referenced companion standards are mandatory.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# PRE-TASK APPROVAL PROTOCOL (MANDATORY)

Before starting implementation work for any task, agents MUST:

1. Present a concise execution brief to the user that includes:
   - what will be done
   - which files or systems will be touched
   - verification commands to be run
2. Request and obtain explicit user approval before executing implementation steps.
3. Gather any required operator-provided inputs or credentials before execution.

If required input or explicit approval is missing:
YOU MUST STOP AND REPORT.

Notes:

- This protocol applies to implementation execution, not read-only analysis.
- This protocol augments, and does not replace, companion standards such as `agents/PREFLIGHT.md`.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# AGENT PERMISSION MODEL

- No unrestricted shell for autonomous or runtime agents unless explicitly approved.
- Accessing anything external to the repo is blocked unless required approval exists.
- high-impact policy changes such as suppression, retention, or privacy

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# LIVE CLOUD COMMAND PROTOCOL (MANDATORY)

For live cloud resources such as AWS, Azure, or GCP, agents MUST NOT run commands unless explicit operator permission is given.

Before any live cloud command, agents MUST state:

1. What the command does
2. Why it is needed
3. Expected side effects such as impacted resources, accounts, or environments
4. Expected cleanup or rollback path, if applicable

Additional required rules:

- Require explicit approval before running any mutating cloud command such as create, update, delete, start, stop, terminate, or apply.
- Confirm target environment, account, region, and profile before execution.
- If the operator prefers to run commands, provide exact commands and wait for results.
- If approval is missing or ambiguous, STOP and report.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# CREDENTIAL ACCESS BOUNDARY (MANDATORY)

Agents MUST treat credential-bearing files and secret stores as off-limits.

Agents MUST NOT open, read, copy, or modify:

- `.env*` files
- `*.tfvars`, `*.tfvars.json`, or files marked as secrets
- cloud credential files such as `~/.aws/credentials` and `~/.aws/config`
- private key material such as `*.pem`, `*.key`, `id_rsa`, and `id_ed25519`

Agents MUST rely on operator-provided runtime credentials and explicit operator-run command support for secret-dependent actions.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# EXPLICIT REFUSAL PROTOCOL

If asked to bypass task tracking, approval gates, verification requirements, or any incorporated standard:

1. Refuse the request.
2. Cite the governing rule.
3. Offer the compliant alternative.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# STOP CONDITIONS

You MUST STOP AND REPORT when:

- task scope or acceptance criteria are ambiguous
- dependencies or credentials are missing
- required verification fails and cannot be resolved
- instructions conflict and cannot be reconciled

Do not proceed under uncertainty.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD GUIDELINES START -->
<CRITICAL_INSTRUCTION>

## Backlog.md Workflow

This project uses Backlog.md for task and project management.

**For every user request in this project, run `backlog instructions overview` before answering or taking action.**

Use the overview to decide whether to search, read, create, or update Backlog tasks.

Use the detailed guides when needed:
- `backlog instructions task-creation` for creating or splitting tasks
- `backlog instructions task-execution` for planning and implementation workflow
- `backlog instructions task-finalization` for completion and handoff

Use `backlog <command> --help` before running unfamiliar commands. Help shows options, fields, and examples.

Do not edit Backlog task, draft, document, decision, or milestone markdown files directly. Use the `backlog` CLI so metadata, relationships, and history stay consistent.

</CRITICAL_INSTRUCTION>
<!-- BACKLOG.MD GUIDELINES END -->
