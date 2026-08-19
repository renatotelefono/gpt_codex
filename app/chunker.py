import re


def split_text(text: str, max_chars: int = 5000):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, current = [], ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
        while len(paragraph) > max_chars:
            split_at = paragraph.rfind(" ", 0, max_chars)
            split_at = max_chars if split_at == -1 else split_at
            chunks.append(paragraph[:split_at].strip())
            paragraph = paragraph[split_at:].strip()
        current = paragraph

    if current:
        chunks.append(current)
    return chunks
