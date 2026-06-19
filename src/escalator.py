import json

SENSITIVE=['billing','refund','charge','legal','account modification']

def should_escalate(query,contexts,threshold=0.25):
    score=max([c['score'] for c in contexts],default=0)
    sensitive=any(k in query.lower() for k in SENSITIVE)
    return score < threshold or sensitive

def handoff(query,persona,contexts):
    return json.dumps({
        'persona':persona,
        'issue':query,
        'sources':[c['source'] for c in contexts],
        'confidence':max([c['score'] for c in contexts],default=0)
    },indent=2)
