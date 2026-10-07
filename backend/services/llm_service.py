import os
import re

import ollama
from google import genai


MODEL_NAME = "qwen2.5:1.5b-instruct-q4_0"
GEMINI_MODEL = "gemini-2.5-flash"


class LLMService:

    def __init__(
        self,
        model_name: str = MODEL_NAME
    ):
        self.model_name = model_name

        # Gemini is used only when GEMINI_API_KEY is configured.
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        self.gemini_client = None

        if self.gemini_api_key:
            self.gemini_client = genai.Client(
                api_key=self.gemini_api_key
            )


    def _extract_structured_facts(
        self,
        question: str,
        context: str
    ) -> str | None:

        question_lower = question.lower()

        # ====================================================
        # DEPENDENCIES
        # ====================================================

        if (
            "dependenc" in question_lower
            and (
                "what" in question_lower
                or "which" in question_lower
                or "list" in question_lower
            )
        ):

            dependencies = re.findall(
                r"Dependency\s*:\s*(.+?)\s*(?:\n|$)",
                context,
                re.IGNORECASE
            )

            cleaned = []

            for dependency in dependencies:
                dependency = dependency.strip()

                if dependency and dependency not in cleaned:
                    cleaned.append(dependency)

            if cleaned:

                lines = [
                    "The dependencies defined in the HLD are:"
                ]

                for index, dependency in enumerate(
                    cleaned,
                    start=1
                ):
                    lines.append(
                        f"{index}. {dependency}"
                    )

                return "\n".join(lines)


        # ====================================================
        # SOFTWARE COMPONENTS
        # ====================================================

        if (
            (
                "component" in question_lower
                or "software component" in question_lower
            )
            and (
                "what" in question_lower
                or "which" in question_lower
                or "list" in question_lower
            )
        ):

            components = re.findall(
                r"(?:Software\s+Component|SW\s+Component)"
                r"\s*:\s*([A-Za-z0-9_.-]+)",
                context,
                re.IGNORECASE
            )

            cleaned = []

            for component in components:
                component = component.strip()

                if component and component not in cleaned:
                    cleaned.append(component)

            if cleaned:

                lines = [
                    "The software components identified in the HLD are:"
                ]

                for index, component in enumerate(
                    cleaned,
                    start=1
                ):
                    lines.append(
                        f"{index}. {component}"
                    )

                return "\n".join(lines)


        # ====================================================
        # INTERFACES
        # ====================================================

        if (
            "interface" in question_lower
            and (
                "what" in question_lower
                or "which" in question_lower
                or "list" in question_lower
            )
        ):

            interfaces = re.findall(
                r"Interface\s*:\s*([A-Za-z0-9_.-]+)",
                context,
                re.IGNORECASE
            )

            cleaned = []

            for interface in interfaces:
                interface = interface.strip()

                if interface and interface not in cleaned:
                    cleaned.append(interface)

            if cleaned:

                lines = [
                    "The interfaces identified in the HLD are:"
                ]

                for index, interface in enumerate(
                    cleaned,
                    start=1
                ):
                    lines.append(
                        f"{index}. {interface}"
                    )

                return "\n".join(lines)


        # ====================================================
        # PORTS
        # ====================================================

        if (
            "port" in question_lower
            and (
                "what" in question_lower
                or "which" in question_lower
                or "list" in question_lower
            )
        ):

            ports = re.findall(
                r"Port\s*(?:Name)?\s*:\s*"
                r"([A-Za-z0-9_.-]+)",
                context,
                re.IGNORECASE
            )

            cleaned = []

            for port in ports:
                port = port.strip()

                if port and port not in cleaned:
                    cleaned.append(port)

            if cleaned:

                lines = [
                    "The ports identified in the HLD are:"
                ]

                for index, port in enumerate(
                    cleaned,
                    start=1
                ):
                    lines.append(
                        f"{index}. {port}"
                    )

                return "\n".join(lines)


        # ====================================================
        # SIGNALS
        # ====================================================

        if (
            "signal" in question_lower
            and (
                "what" in question_lower
                or "which" in question_lower
                or "list" in question_lower
            )
        ):

            signals = re.findall(
                r"Signal\s*(?:Name)?\s*:\s*"
                r"([A-Za-z0-9_.-]+)",
                context,
                re.IGNORECASE
            )

            cleaned = []

            for signal in signals:
                signal = signal.strip()

                if signal and signal not in cleaned:
                    cleaned.append(signal)

            if cleaned:

                lines = [
                    "The signals identified in the HLD are:"
                ]

                for index, signal in enumerate(
                    cleaned,
                    start=1
                ):
                    lines.append(
                        f"{index}. {signal}"
                    )

                return "\n".join(lines)


        return None


    def _build_prompt(
        self,
        question: str,
        context: str
    ) -> str:

        return f"""
You are AutoHLD AI, an assistant for analyzing AUTOSAR
High-Level Design (HLD) documents.

Answer the engineer's question using ONLY the provided HLD context.

IMPORTANT RULES:

1. Never invent information.
2. Use only information explicitly present in the context.
3. If the answer is explicitly present, answer directly.
4. If multiple relevant facts are present, include all of them.
5. Preserve technical names exactly as written.
6. Do not infer relationships that are not explicitly stated.
7. If the context does not contain enough information, say:
   "The provided HLD context does not contain enough information."
8. Keep the answer concise and engineering-focused.

HLD CONTEXT:
{context}

ENGINEER QUESTION:
{question}

ANSWER:
"""


    def _generate_with_ollama(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = self._build_prompt(
            question,
            context
        )

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]


    def _generate_with_gemini(
        self,
        question: str,
        context: str
    ) -> str:

        if not self.gemini_client:
            raise RuntimeError(
                "Gemini API key is not configured."
            )

        prompt = self._build_prompt(
            question,
            context
        )

        response = self.gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text


    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        # ====================================================
        # STEP 1: Deterministic structured extraction
        # ====================================================

        structured_answer = (
            self._extract_structured_facts(
                question,
                context
            )
        )

        if structured_answer is not None:
            return structured_answer


        # ====================================================
        # STEP 2: Prefer Ollama when available
        # ====================================================

        try:

            return self._generate_with_ollama(
                question,
                context
            )

        except Exception as ollama_error:

            # ====================================================
            # STEP 3: Cloud fallback using Gemini
            # ====================================================

            if self.gemini_client:

                try:

                    return self._generate_with_gemini(
                        question,
                        context
                    )

                except Exception as gemini_error:

                    raise RuntimeError(
                        "Both Ollama and Gemini failed. "
                        f"Ollama error: {ollama_error}. "
                        f"Gemini error: {gemini_error}."
                    )

            raise RuntimeError(
                "Ollama is not available. "
                "For local use, install and run Ollama with "
                f"the {self.model_name} model. "
                "For cloud deployment, configure GEMINI_API_KEY."
            )