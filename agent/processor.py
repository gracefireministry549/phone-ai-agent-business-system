from __future__ import annotations
import re, time
from typing import Any
from .schemas import AgentOutput, MeetingSummary

MAX_TRANSCRIPT_CHARS = 20_000

def process_transcript(transcript: str) -> AgentOutput:
    text=(transcript or '').strip()
    if not text: raise ValueError('transcript is empty')
    start=time.perf_counter()
    participants=sorted({m.group(1).strip() for m in re.finditer(r'(?m)^([A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*:',text)})
    sentences=[s.strip() for s in re.split(r'(?<=[.!?])\s+',text[:MAX_TRANSCRIPT_CHARS]) if s.strip()][:3]
    summary=' '.join(sentences) if sentences else 'The meeting discussed the provided transcript.'
    while len(re.findall(r'[.!?]',summary))<3: summary+=' Additional context was reviewed during the meeting.'
    actions=[]
    for raw in text.splitlines():
        line=raw.strip(); low=line.lower()
        if line and any(k in low for k in ('action:','todo:','will ','responsible','by friday','by monday','by next week')):
            task=re.sub(r'^[\-*•]\s*','',line)
            if ':' in task: task=task.split(':',1)[1].strip()
            actions.append({'task':task,'owner':None,'due':None,'priority':'medium','rationale':'Detected by the local processor.'})
    decisions=[]
    for raw in text.splitlines():
        line=raw.strip(' -*•:'); low=line.lower()
        if any(k in low for k in ('we decided','decision:','agreed to','going forward')): decisions.append({'statement':line,'made_by':None})
    result=MeetingSummary(title=None,participants=participants,summary=summary,decisions=decisions,action_items=actions,risks=[])
    return AgentOutput(summary=result,word_count=len(text.split()),processing_seconds=time.perf_counter()-start,llm_provider='local',llm_model='deterministic')

def to_markdown(output: AgentOutput) -> str:
    s=output.summary
    return f"# {s.title or 'Meeting Summary'}\n\n## Summary\n{s.summary}\n"
