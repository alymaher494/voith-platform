"""
Content processor using mT5-XLSum for summarization and FLAN-T5 for Q&A.
"""

import logging
from typing import Optional

try:
    from transformers import MT5ForConditionalGeneration, MT5Tokenizer, T5Tokenizer, T5ForConditionalGeneration
    import torch
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    MT5ForConditionalGeneration = None
    MT5Tokenizer = None
    T5Tokenizer = None
    T5ForConditionalGeneration = None
    torch = None

logger = logging.getLogger(__name__)


class ContentProcessor:
    """
    Content processor using mT5-XLSum for summarization and FLAN-T5 for question answering.
    """

    MODEL_SIZES = {
        "summarizer": "csebuetnlp/mT5_multilingual_XLSum",
        "qa": "google/flan-t5-base"
    }

    def __init__(self):
        """
        Initialize the content processor.
        """
        if not MT5_AVAILABLE:
            raise ImportError(
                "transformers and torch are required for content processing. "
                "Install with: pip install transformers torch")

        self.summary_model_name = self.MODEL_SIZES["summarizer"]
        self.qa_model_name = self.MODEL_SIZES["qa"]
        self._loaded = False

    def _load_model(self):
        if self._loaded:
            return

        self.tokenizer = MT5Tokenizer.from_pretrained(self.summary_model_name)
        self.summarizer = MT5ForConditionalGeneration.from_pretrained(self.summary_model_name)

        self.qa_tokenizer = T5Tokenizer.from_pretrained(self.qa_model_name)
        self.qa_model = T5ForConditionalGeneration.from_pretrained(self.qa_model_name)

        if torch.cuda.is_available():
            self.summarizer = self.summarizer.cuda()
            self.qa_model = self.qa_model.cuda()

        self._loaded = True

    def summarize(self, text: str, max_length: int = 150, summary_style: str = "structured"):
        allowed = {"bullet_points", "paragraph", "both", "structured"}
        if summary_style not in allowed:
            summary_style = "structured"

        self._load_model()

        # Handle long texts with chunking
        if len(text) > 2000:
            chunks = self._chunk_text(text, chunk_size=1300)
            partials = []

            for chunk in chunks:
                partial = self._generate_summary(chunk, max_length)
                partials.append(partial)

            # Merge partial summaries
            merged_text = " ".join(partials)
            final_summary = self._generate_summary(merged_text, max_length)
        else:
            final_summary = self._generate_summary(text, max_length)

        return self._format_summary(final_summary, summary_style)

    def _chunk_text(self, text: str, chunk_size: int = 1300) -> list:
        """Split text into chunks for long document summarization."""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        chunks = []
        current = ""
        for sentence in sentences:
            if len(current) + len(sentence) > chunk_size:
                if current:
                    chunks.append(current)
                current = sentence
            else:
                current += (" " + sentence) if current else sentence

        if current:
            chunks.append(current)

        return chunks

    def _generate_summary(self, text: str, max_length: int) -> str:
        """Generate summary for a text chunk."""
        inputs = self.tokenizer(
            f"summarize: {text}",
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        bad_words_ids = [
            [self.tokenizer.convert_tokens_to_ids(f"<extra_id_{i}>")]
            for i in range(100)
        ]

        outputs = self.summarizer.generate(
            **inputs,
            max_length=max_length,
            min_length=40,
            num_beams=4,
            do_sample=False,
            early_stopping=True,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2,
            bad_words_ids=bad_words_ids
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    def _format_summary(self, text: str, style: str) -> str:
        """Format the summary based on the specified style."""
        if style == "bullet_points":
            lines = text.split(". ")
            return "\n".join(f"- {l.strip()}" for l in lines if l.strip())

        if style == "paragraph":
            return text.replace("\n", " ").strip()

        if style == "both":
            lines = text.split(". ")
            bullets = "\n".join(f"- {l.strip()}" for l in lines if l.strip())
            paragraph = text.replace("\n", " ").strip()
            return f"Bullet Points:\n{bullets}\n\nParagraph Summary:\n{paragraph}"

        # structured (default)
        lines = text.split(". ")
        bullets = "\n".join(f"- {l.strip()}" for l in lines if l.strip())
        return f"""
Main Idea:
{text}

Key Points:
{bullets}

Conclusion:
This summarizes the most important elements of the content.
""".strip()

    def answer_question(self, question: str, context: str, max_length: int = 120):
        self._load_model()

        prompt = f"question: {question}\ncontext: {context}\nanswer:"

        inputs = self.qa_tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )

        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        output = self.qa_model.generate(
            **inputs,
            max_length=max_length,
            num_beams=4,
            do_sample=False
        )

        return self.qa_tokenizer.decode(output[0], skip_special_tokens=True).strip()
