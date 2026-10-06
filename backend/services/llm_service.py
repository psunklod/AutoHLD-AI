import re

import ollama


MODEL_NAME = "qwen2.5:1.5b-instruct-q4_0"


class LLMService:

    def __init__(
        self,
        model_name: str = MODEL_NAME
    ):
        self.model_name = model_name


    def _extract_structured_facts(
        self,
        question: str,
        context: str
    ) -> str | None:
        """
        Answer simple structured architecture questions
        directly from explicit HLD facts.

        This avoids asking a small LLM to enumerate facts
        that can be extracted deterministically.
        """

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
                r"Dependency\s*:\s*"
                r"(.+?)\s*(?:\n|$)",
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


    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        # ====================================================
        # STEP 1: Try deterministic structured extraction
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
        # STEP 2: Use Qwen for natural-language questions
        # ====================================================

        prompt = f"""
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