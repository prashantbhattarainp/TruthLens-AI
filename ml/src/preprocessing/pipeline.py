"""Composable preprocessing orchestration; it never reads or writes raw datasets."""

from __future__ import annotations

import hashlib
from typing import Iterable

from preprocessing.components import SpacyTokenProcessor, TextTransform, build_text_transforms
from preprocessing.config import PreprocessingConfig
from preprocessing.models import InputDocument, ProcessedDocument, ProcessingFailure, ProcessingResult
from preprocessing.spacy_runtime import SpacyRuntime, load_spacy_runtime


class PreprocessingPipeline:
    """Apply configured text operations, then spaCy tokenization and token filters."""

    def __init__(self, config: PreprocessingConfig) -> None:
        self.config = config
        self.runtime: SpacyRuntime = load_spacy_runtime(config)
        self._text_transforms: tuple[TextTransform, ...] = build_text_transforms(config)
        self._token_processor = SpacyTokenProcessor(config, self.runtime.has_lemmatizer)

    @property
    def enabled_operations(self) -> tuple[str, ...]:
        token_operations = ["tokenization"] if self.config.tokenization.enabled else []
        if self.config.stopword_removal.enabled:
            token_operations.append("stopword_removal")
        if self.config.lemmatization.enabled:
            token_operations.append("lemmatization")
        return tuple([transform.name for transform in self._text_transforms] + token_operations)

    def process_document(self, source: InputDocument) -> ProcessedDocument:
        """Process one document and raise any failure to the caller for retention."""
        prepared = self._prepare(source)
        if not self.config.tokenization.enabled:
            return ProcessedDocument(
                document_id=source.document_id,
                source_text_sha256=_text_sha256(source.text),
                processed_text=prepared,
                tokens=(),
            )
        doc = self.runtime.nlp(prepared)
        tokens = self._token_processor.process(doc)
        return ProcessedDocument(
            document_id=source.document_id,
            source_text_sha256=_text_sha256(source.text),
            processed_text=" ".join(tokens),
            tokens=tokens,
        )

    def process_documents(self, sources: Iterable[InputDocument]) -> ProcessingResult:
        """Batch spaCy work while retaining document-level failure evidence and order."""
        source_list = list(sources)
        prepared: list[tuple[InputDocument, str]] = []
        failures: list[ProcessingFailure] = []
        for source in source_list:
            try:
                prepared.append((source, self._prepare(source)))
            except Exception as error:  # retained in an audit artifact below
                failures.append(_failure(source, error))

        documents: list[ProcessedDocument] = []
        if self.config.tokenization.enabled:
            texts = (text for _, text in prepared)
            for (source, _), doc in zip(
                prepared,
                self.runtime.nlp.pipe(texts, batch_size=self.config.spacy.batch_size),
                strict=True,
            ):
                try:
                    tokens = self._token_processor.process(doc)
                    documents.append(
                        ProcessedDocument(
                            document_id=source.document_id,
                            source_text_sha256=_text_sha256(source.text),
                            processed_text=" ".join(tokens),
                            tokens=tokens,
                        )
                    )
                except Exception as error:  # retained in an audit artifact below
                    failures.append(_failure(source, error))
        else:
            documents.extend(
                ProcessedDocument(
                    document_id=source.document_id,
                    source_text_sha256=_text_sha256(source.text),
                    processed_text=text,
                    tokens=(),
                )
                for source, text in prepared
            )

        return ProcessingResult(
            documents=tuple(documents),
            failures=tuple(failures),
            attempted_count=len(source_list),
        )

    def _prepare(self, source: InputDocument) -> str:
        if not source.document_id.strip():
            raise ValueError("document_id must be nonempty.")
        if not isinstance(source.text, str):
            raise TypeError("text must be a string.")
        text = source.text
        for transform in self._text_transforms:
            text = transform.apply(text)
        return text


def _text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _failure(source: InputDocument, error: Exception) -> ProcessingFailure:
    return ProcessingFailure(
        document_id=source.document_id,
        error_type=type(error).__name__,
        message=str(error),
    )
