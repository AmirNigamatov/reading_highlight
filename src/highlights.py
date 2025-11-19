import json
import os
import uuid
from typing import List, Optional

MAX_TEXT_LEN = 1000
MAX_SOURCE_LEN = 200
MAX_TAGS = 10
MAX_TAG_LEN = 50


class ProblemDetail:
    def __init__(
        self,
        type: str,
        title: str,
        status: int,
        detail: str,
        instance: Optional[str] = None,
    ):
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail[:100] if len(detail) > 100 else detail
        self.instance = instance or str(uuid.uuid4())
        self.errors = {}

    def to_dict(self):
        return {
            "type": self.type,
            "title": self.title,
            "status": self.status,
            "detail": self.detail,
            "instance": self.instance,
            "errors": self.errors,
        }

    @staticmethod
    def raise_problem(
        type: str, title: str, status: int, detail: str, instance: Optional[str] = None
    ):
        problem = ProblemDetail(type, title, status, detail, instance)
        raise ValueError(json.dumps(problem.to_dict()))


class Highlight:
    def __init__(self, text: str, source: str, tags: List[str]):
        if (
            not isinstance(text, str)
            or not isinstance(source, str)
            or not isinstance(tags, list)
        ):
            ProblemDetail.raise_problem(
                "validation_error",
                "Invalid input types",
                400,
                "Text and source must be strings, tags must be a list",
            )
        if not text.strip():
            ProblemDetail.raise_problem(
                "validation_error", "Empty text", 400, "Text cannot be empty"
            )
        if not source.strip():
            ProblemDetail.raise_problem(
                "validation_error", "Empty source", 400, "Source cannot be empty"
            )
        if len(text) > MAX_TEXT_LEN:
            ProblemDetail.raise_problem(
                "validation_error",
                "Text too long",
                400,
                f"Text exceeds {MAX_TEXT_LEN} characters",
            )
        if len(source) > MAX_SOURCE_LEN:
            ProblemDetail.raise_problem(
                "validation_error",
                "Source too long",
                400,
                f"Source exceeds {MAX_SOURCE_LEN} characters",
            )
        if len(tags) > MAX_TAGS:
            ProblemDetail.raise_problem(
                "validation_error",
                "Too many tags",
                400,
                f"Cannot have more than {MAX_TAGS} tags",
            )
        for tag in tags:
            if not isinstance(tag, str) or len(tag) > MAX_TAG_LEN:
                ProblemDetail.raise_problem(
                    "validation_error",
                    "Invalid tag",
                    400,
                    f"Each tag must be a string, max {MAX_TAG_LEN} characters",
                )

        self.text = text.strip()
        self.source = source.strip()
        self.tags = [tag.strip() for tag in tags]

    def to_dict(self):
        return {"text": self.text, "source": self.source, "tags": self.tags}


DATA_FILE = "data.json"


def load_highlights() -> List[Highlight]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f, parse_float=str)
    return [Highlight(**item) for item in data]


def save_highlights(highlights: List[Highlight]):
    with open(DATA_FILE, "w") as f:
        json.dump([h.to_dict() for h in highlights], f, indent=2)


def add_highlight(text: str, source: str, tags: List[str]):
    highlights = load_highlights()
    highlights.append(Highlight(text, source, tags))
    save_highlights(highlights)
