import os
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()


class AISummarizer:
    """Summarize long email text using a hosted Hugging Face model."""

    def __init__(
        self,
        api_url: str = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn",
        token: str | None = None,
        chunk_words: int = 700,
        output_word_limit: int = 120,
    ):
        self.api_url = api_url
        self.token = token or os.getenv("HUGGING_FACE_TOKEN")
        self.chunk_words = chunk_words
        self.output_word_limit = output_word_limit

    def summarize(self, email_body: str) -> str:
        if not email_body or not email_body.strip():
            return "No content to summarize."

        if not self.token:
            return self._trim_words(email_body, self.output_word_limit)

        headers = {"Authorization": f"Bearer {self.token}"}
        chunks = self._chunk_text(email_body)
        summaries: List[str] = []

        for chunk in chunks:
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json={
                        "inputs": chunk,
                        "parameters": {
                            "max_length": 120,
                            "min_length": 20,
                            "do_sample": False,
                        },
                    },
                    timeout=30,
                )
                response.raise_for_status()
                result = response.json()
                if isinstance(result, list) and result and "summary_text" in result[0]:
                    summaries.append(result[0]["summary_text"])
                else:
                    summaries.append(chunk)
            except Exception:
                summaries.append(chunk)

        final = " ".join(summaries)
        return self._trim_words(final, self.output_word_limit)

    def _chunk_text(self, text: str) -> List[str]:
        words = text.split()
        return [
            " ".join(words[i : i + self.chunk_words])
            for i in range(0, len(words), self.chunk_words)
        ]

    @staticmethod
    def _trim_words(text: str, max_words: int) -> str:
        words = text.split()
        if len(words) <= max_words:
            return text.strip()
        return " ".join(words[:max_words]).strip() + "..."
