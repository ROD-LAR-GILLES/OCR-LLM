SYSTEM_PROMPT = "You are an expert HTML formatter..."
def refine(markdown: str) -> str:
    resp = client.chat.completions.create(
        model=settings.llm_model,
        messages=[{"role":"system","content":SYSTEM_PROMPT},
                  {"role":"user","content":markdown}],
        temperature=0.2)
    return resp.choices[0].message.content