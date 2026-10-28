import os
import json
import re
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from prompt_templates import build_prompt

T = TypeVar("T", bound=BaseModel)


def clean_json_string(raw: str) -> str:
    """Strips markdown code fences and cleans json response."""
    cleaned = raw.strip()
    # Remove ```json ... ``` or ``` ... ```
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    return cleaned.strip()


class LLMExtractor:
    def __init__(self, provider: str = "gemini", model_name: str = None):
        """
        provider: 'gemini' or 'openai'
        model_name: specific model to use (default: gemini-3.8-flash for gemini, gpt-4o-mini for openai)
        """
        self.provider = provider.lower()
        if self.provider == "gemini":
            if not HAS_GENAI:
                raise ImportError("google-genai package is not installed. Run `pip install google-genai`.")
            self.model_name = model_name or "gemini-3.8-flash"
            api_key = os.getenv("GEMINI_API_KEY")
            self.client = genai.Client(api_key=api_key) if api_key else genai.Client()
        elif self.provider == "openai":
            if not HAS_OPENAI:
                raise ImportError("openai package is not installed. Run `pip install openai`.")
            self.model_name = model_name or "gpt-4o-mini"
            api_key = os.getenv("OPENAI_API_KEY")
            self.client = openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'gemini' or 'openai'.")

    def extract(self, doc_type: str, raw_text: str, schema_class: Type[T]) -> T:
        """
        Executes prompt pipeline and returns a validated Pydantic model instance.
        """
        schema_dict = schema_class.model_json_schema()
        prompt = build_prompt(doc_type=doc_type, raw_text=raw_text, schema_json=schema_dict)

        raw_output = ""
        if self.provider == "gemini":
            # Native Gemini structured output
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_json_schema=schema_dict,
                    temperature=0.1
                )
            )
            raw_output = response.text or ""

        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            raw_output = response.choices[0].message.content or ""

        # Validate with Pydantic
        clean_text = clean_json_string(raw_output)
        try:
            parsed_dict = json.loads(clean_text)
            validated_obj = schema_class.model_validate(parsed_dict)
            return validated_obj
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON from model response: {e}\nRaw output: {raw_output}")
        except ValidationError as e:
            raise ValueError(f"Pydantic schema validation failed: {e}\nParsed dict: {clean_text}")
