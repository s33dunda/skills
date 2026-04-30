# Prior Art: Harness Efficiency and Agent Scaffolding

References relevant to the harness-efficiency-study ExecPlan. Organized by what each source contributes to our study design or hypothesis.

Retrieved: 2026-04-28

---

## Primary: OpenAI Harness Engineering Case Study

**Citation:** Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world," OpenAI, February 11, 2026.
**URL:** https://openai.com/index/harness-engineering/
**Full-text mirror:** `skills/cultivate/references/harness-openai-blog.md`

**Key quantitative findings:**
- 3 engineers × 5 months → ~1M lines of code, ~1,500 PRs merged at 3.5 PRs/engineer/day.
- Throughput *increased* as the team grew (3→7 engineers), suggesting the harness, not the headcount, was the scaling variable.
- Before encoding "golden principles" into the repo, the team spent 20% of engineering time (every Friday) manually cleaning up AI-generated drift. Encoding the rules as mechanical checks eliminated that cost.

**Relevance to our study:**
These are the highest-quality published numbers on harness-enabled agent productivity. They are observational (one team, one product, no control group), which is exactly the gap our study closes. They establish a plausible upper bound on effect size and identify the specific mechanisms (map-not-manual AGENTS.md, enforced invariants, agent-legible observability) that a cultivate harness instantiates.

**What this source does NOT provide:**
A controlled comparison. The same team without a harness is never measured. We cannot isolate how much of the 3.5 PR/day throughput is model capability vs. harness vs. team skill.

---

## SWE-bench: Repository-Level Variance

**Citation:** Carlos E. Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", ICLR 2024. https://arxiv.org/abs/2310.06770
**Citation:** SWE-bench Pro, "Can AI Agents Solve Long-Horizon Software Engineering Tasks?", 2025. https://arxiv.org/pdf/2509.16941
**Citation:** Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," NeurIPS 2024. https://arxiv.org/abs/2405.15793

**Key finding:**
Across SWE-bench repos, agent success rates show ~5x variance: some repos see <10% resolution across all models, others exceed 50% on capable models. Task resolution rate degrades as the number of files modified and lines changed increases. Language matters (Python/Go > JS/TS).

**Relevance to our study:**
- Validates our between-subjects design: by running control and treatment on the *same* repos and tasks, we hold inherent repo difficulty constant. A pure cross-repo comparison (harnessed repos vs. different unharnessed repos) would confound harness quality with repo difficulty — exactly the flaw SWE-bench results make visible.
- The "lines modified / files touched" degradation finding is a concrete covariate we should log per run. If treatment tasks require fewer files touched to solve the same issue (because the harness helps the agent navigate faster), that's a secondary efficiency signal.
- SWE-bench does not control for repo scaffolding or documentation quality as a variable. Our study fills that specific gap.

**Understanding Code Agent Behaviour:**
"Understanding Code Agent Behaviour: An Empirical Study of Success and Failure Trajectories," arxiv.org/abs/2511.00197. Analyzes failure modes on SWE-bench tasks. Key finding: agents fail more often on under-specified tasks and when the codebase lacks navigable structure. Supports our hypothesis that a harness reduces the "where do I start?" failure class.

---

## AGENTS.md: Command-First vs. Prose-Only

**Citation:** Blake Crosley, "AGENTS.md Patterns: What Actually Changes Agent Behavior," February 28, 2026.
**URL:** https://blakecrosley.com/blog/agents-md-patterns

**Key finding:**
Prose-only documentation with no verifiable commands produces zero observable behavioral change in agents. The patterns that measurably change behavior are: exact shell commands with exit-code checking, explicit Definition of Done, task-organized sections (When Writing / When Reviewing), and a Never list. 60,000+ projects use AGENTS.md across 8+ agent tools.

**Relevance to our study:**
Our treatment condition must include command-first AGENTS.md content — not just prose summaries of the codebase. This is already the cultivate default (every AGENTS.md template leads with Useful Commands and Definition of Done). But it means our harness quality check (Milestone B) should verify that treatment repos have executable commands in their AGENTS.md, not just structured prose.

**Design implication added to plan:** Add an AGENTS.md quality check to Milestone B validation criteria.

---

## Codex Modernization: Before/After Evidence

**Citation:** Derrick Choi, "Modernizing your Codebase with Codex," OpenAI Cookbook, November 19, 2025.
**URL:** https://cookbook.openai.com/examples/codex/code_modernization

**Relevance:** Describes structured context provision (step-by-step plans, explicit validation commands) enabling Codex to modernize legacy codebases. Qualitative case study, no control group, but converges on the same mechanisms: plan-first, command-verifiable, narrow scope.

---

## Aaron Friel: ExecPlans for Multi-Hour Problem Solving

**Citation:** Aaron Friel, "Using PLANS.md for multi-hour problem solving," OpenAI Cookbook, October 7, 2025.
**URL:** https://cookbook.openai.com/articles/codex_exec_plans

**Relevance:** Establishes that agents working from explicit execution plans (with milestones, decision logs, and progress notes) complete complex tasks more reliably than agents working from freeform prompts. Directly motivates the ExecPlan component of the cultivate harness. Qualitative; no A/B data.

---

## Summary: What the Prior Art Tells Us

| Finding | Source | Implication for our design |
| --- | --- | --- |
| 3.5 PRs/engineer/day at scale (observational) | Lopopolo 2026 | Sets plausible upper bound on effect size; our study adds the missing control |
| 5x repo-level variance in agent success | SWE-bench 2024 | Use same repos in both conditions — between-subjects design already handles this |
| Success degrades with files modified / lines changed | SWE-bench 2024 | Log `files_touched` and `lines_changed` as covariates per run |
| Prose-only docs → zero behavioral change | Crosley 2026 | Treatment must include command-first AGENTS.md; check this in Milestone B |
| Agent failures cluster on under-specified / hard-to-navigate tasks | Code Agent Behaviour 2024 | Navigation task type is high-signal; keep 2 synthetic nav tasks per repo |
| Explicit plans → more reliable complex-task completion | Friel 2025 | ExecPlan harness component is load-bearing, not decorative |

**The core gap this study closes:** No existing work isolates repo scaffolding (harness presence/absence) as a controlled variable while holding repo, task, and model constant. SWE-bench shows correlation; we are measuring causation within pairs.
