"""Custom Terminal-Bench agents for A/B-ing the orchestrate+trinity workflow
protocol against a plain agentic loop, on the SAME model.

Design: subclass the stock `Terminus` agent and change ONLY the prompt. The
episode loop, structured-output schema, model, temperature, token accounting and
command execution are all inherited unchanged, so the only variable between the
baseline and the treatment is the workflow scaffolding injected into the prompt.
This is the repository's workflow outcome benchmark: use Terminal-Bench tasks
instead of repo-local hidden tests or fixture suites.

Substrate note: this runs as Tier B (single-context role-play of the tri-role /
decompose protocol) on one model — not real multi-worker routing across models.

Run:
  # baseline (plain terminus) — same model, for the A arm
  tb run --agent terminus --model openai/gpt-5.5 -k temperature=1 ...
  # treatment (workflow) — the B arm
  tb run --agent-import-path docs/evals/tbench/workflow_agent.py:WorkflowTerminus \
         --model openai/gpt-5.5 -k temperature=1 ...
"""

from pathlib import Path

from terminal_bench.agents.terminus_1 import Terminus

# Injected before the stock terminus instructions. Encodes per-task routing
# (orchestrate vs trinity) plus the verify-before-complete gate that is the whole
# point of trinity — the model must act as Verifier and confirm the task's success
# criteria by inspecting real output before it may set is_task_complete=true.
WORKFLOW_PREAMBLE = """\
You will solve this task using a disciplined multi-role workflow, not a single
naive pass. Internally play these roles across your episodes; keep the roles
distinct in your reasoning.

ROUTING (decide first, in your first state_analysis):
- If the task splits into independent or sequential sub-parts (multiple files,
  multiple services, build-then-test), use the ORCHESTRATE protocol.
- If it is one coherent problem, use the TRINITY protocol.

TRINITY protocol (single coherent task):
1. THINKER: state the explicit acceptance criteria for "done" (what file/state/
   output must exist and what it must contain) before touching anything. Put this
   in your explanation.
2. WORKER: execute the smallest concrete step toward those criteria.
3. VERIFIER: after each change, actively CHECK the result against the acceptance
   criteria by inspecting real output (cat the file, run the script, echo $?,
   re-run the failing command). Do NOT trust that a command worked because it
   returned no error.
4. Set is_task_complete=true ONLY after the Verifier role has confirmed EVERY
   acceptance criterion against observed output. If a check fails, diagnose the
   specific defect and revise — do not loop blindly.

ORCHESTRATE protocol (multi-part task):
1. DECOMPOSE the task into an ordered list of sub-parts; state it in your
   explanation.
2. Solve each sub-part in turn, carrying forward only what the next part needs.
3. After all parts, SYNTHESIZE and run an end-to-end verification of the whole
   task's success criteria against observed output before completing.

In every response, your state_analysis must name which role you are currently
acting as. Never declare the task complete on an unverified assumption.

----- TASK BEGINS -----
"""


class WorkflowTerminus(Terminus):
    """Terminus with the orchestrate+trinity workflow protocol injected into the
    initial prompt. Everything else is identical to the baseline agent."""

    @staticmethod
    def name() -> str:
        # Distinct name so runs/logs don't collide with stock terminus.
        return "workflow-terminus"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The stock template has an "Instruction:\n{instruction}" slot. We prepend
        # the workflow preamble to the instruction text by wrapping the template
        # so {instruction} is expanded to include the protocol. Simplest robust
        # approach: keep the template, but inject via the instruction at format
        # time is not possible here (perform_task formats it), so we patch the
        # template string to carry the preamble ahead of the instruction slot.
        self._prompt_template = self._prompt_template.replace(
            "Instruction:\n{instruction}",
            "Instruction:\n" + WORKFLOW_PREAMBLE + "{instruction}",
        )
