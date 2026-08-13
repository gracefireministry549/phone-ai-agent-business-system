from __future__ import annotations
import time
from typing import Any
from .schemas import AgentOutput, MeetingSummary
from . import llm

MAX_TRANSCRIPT_CHARS = 20_000

def process_transcript(transcript: str) -> AgentOutput:
    text = (transcript or "").strip()
    if not text:
        raise ValueError("transcript is empty")
    start = time.perf_counter()
    raw: dict[str, Any] = llm.chat_json(text[:MAX_TRANSCRIPT_CHARS])
    summary = MeetingSummary(**raw)
    return AgentOutput(
        summary=summary,
        word_count=len(text.split()),
        processing_seconds=time.perf_counter() - start,
        llm_provider=llm.provider_name(),
        llm_model=llm.model_name(),
    )

def to_markdown(output: AgentOutput) -> str:
    s = output.summary
    lines = [f"# {s.title or 'Meeting Summary'}", "", f"_Processed in {output.processing_seconds:.2f}s via {output.llm_provider}/{output.llm_model} · {output.word_count} words_", ""]
    lines.append(f"**Participants:** {', '.join(s.participants) if s.participants else '_none detected_'}")
    lines += ["", "## Summary", s.summary]
    if s.decisions:
        lines += ["", "## Decisions"]
        for d in s.decisions:
            who = f" — _{d.made_by}_" if d.made_by else ""
            lines.append(f"- {d.statement}{who}")
    if s.action_items:
        lines += ["", "## Action items"]
        for a in s.action_items:
            owner = a.owner or "Unassigned"
            due = f" by {a.due}" if a.due else ""
            lines.append(f"- **[{a.priority.upper()}]** {a.task} — _{owner}{due}_")
    if s.risks:
        lines += ["", "## Risks", *[f"- {r}" for r in s.risks]]
    return "\n".join(lines) + "\n"
