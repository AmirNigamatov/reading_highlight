import json
import os
from typing import List, Dict, Optional

DATA_FILE = 'data.json'

class Highlight:
    def __init__(self, text: str, source: str, tags: List[str]):
        self.text = text
        self.source = source
        self.tags = tags

    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'source': self.source,
            'tags': self.tags
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Highlight':
        return Highlight(data['text'], data['source'], data['tags'])

def load_highlights() -> List[Highlight]:
    """Загружает highlights из файла."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Highlight.from_dict(item) for item in data]

def save_highlights(highlights: List[Highlight]):
    """Сохраняет highlights в файл."""
    data = [h.to_dict() for h in highlights]
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_highlight(text: str, source: str, tags_str: str) -> Highlight:
    """Добавляет новый highlight."""
    tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
    highlight = Highlight(text, source, tags)
    highlights = load_highlights()
    highlights.append(highlight)
    save_highlights(highlights)
    return highlight

def view_highlights() -> List[Highlight]:
    """Возвращает все highlights."""
    return load_highlights()

def search_highlights(query: str) -> List[Highlight]:
    """Ищет highlights по тексту, источнику или тегам (простой поиск)."""
    highlights = load_highlights()
    results = []
    for h in highlights:
        if (query.lower() in h.text.lower() or 
            query.lower() in h.source.lower() or 
            any(query.lower() in tag.lower() for tag in h.tags)):
            results.append(h)
    return results

