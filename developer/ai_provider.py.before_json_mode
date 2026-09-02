# ==========================================================
# NITRON AI PROVIDER SYSTEM v4.0
# Local Ollama + OpenAI
# ==========================================================

import json
import os
import urllib.request
import urllib.error


# ==========================================================
# BASE PROVIDER
# ==========================================================

class AIProvider:

    name = "unknown"

    def available(self):
        return False

    def generate(self, prompt):
        raise NotImplementedError(
            "Provider must implement generate()."
        )


# ==========================================================
# OPENAI PROVIDER
# ==========================================================

class OpenAIProvider(AIProvider):

    name = "openai"

    def __init__(self, model=None):

        self.api_key = os.environ.get(
            "OPENAI_API_KEY"
        )

        self.model = (
            model
            or os.environ.get(
                "NITRON_AI_MODEL",
                "gpt-5-mini"
            )
        )

        self.url = (
            "https://api.openai.com/v1/responses"
        )

    def available(self):

        return bool(
            self.api_key
        )

    def generate(self, prompt):

        if not self.available():

            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        payload = {
            "model": self.model,
            "input": prompt
        }

        data = json.dumps(
            payload
        ).encode("utf-8")

        request = urllib.request.Request(
            self.url,
            data=data,
            headers={
                "Content-Type":
                    "application/json",

                "Authorization":
                    f"Bearer {self.api_key}"
            },
            method="POST"
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=120
            ) as response:

                raw = response.read()

            result = json.loads(
                raw.decode("utf-8")
            )

            return self._extract_text(
                result
            )

        except urllib.error.HTTPError as error:

            body = error.read().decode(
                "utf-8",
                errors="replace"
            )

            raise RuntimeError(
                f"OpenAI API error "
                f"{error.code}: {body}"
            )

        except urllib.error.URLError as error:

            raise RuntimeError(
                "Could not connect to OpenAI: "
                f"{error}"
            )

    def _extract_text(self, result):

        text = result.get(
            "output_text"
        )

        if isinstance(
            text,
            str
        ) and text.strip():

            return text.strip()

        parts = []

        for item in result.get(
            "output",
            []
        ):

            if not isinstance(
                item,
                dict
            ):
                continue

            for block in item.get(
                "content",
                []
            ):

                if not isinstance(
                    block,
                    dict
                ):
                    continue

                if block.get(
                    "type"
                ) == "output_text":

                    value = block.get(
                        "text",
                        ""
                    )

                    if value:
                        parts.append(
                            value
                        )

        final_text = "\n".join(
            parts
        ).strip()

        if not final_text:

            raise RuntimeError(
                "OpenAI returned no text."
            )

        return final_text


# ==========================================================
# LOCAL OLLAMA PROVIDER
# ==========================================================

class LocalProvider(AIProvider):

    name = "local"

    def __init__(
        self,
        url=None,
        model=None
    ):

        self.url = (
            url
            or os.environ.get(
                "NITRON_LOCAL_AI_URL",
                "http://127.0.0.1:11434"
            )
        ).rstrip("/")

        self.model = (
            model
            or os.environ.get(
                "NITRON_LOCAL_AI_MODEL",
                "qwen2.5-coder:1.5b"
            )
        )

    # ======================================================
    # SERVER CHECK
    # ======================================================

    def available(self):

        try:

            request = urllib.request.Request(
                self.url
            )

            with urllib.request.urlopen(
                request,
                timeout=3
            ) as response:

                return response.status == 200

        except Exception:

            return False

    # ======================================================
    # MODEL LIST
    # ======================================================

    def models(self):

        try:

            request = urllib.request.Request(
                self.url + "/api/tags"
            )

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                data = json.loads(
                    response.read().decode(
                        "utf-8"
                    )
                )

            models = []

            for item in data.get(
                "models",
                []
            ):

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                name = item.get(
                    "name"
                )

                if name:
                    models.append(
                        name
                    )

            return models

        except Exception:

            return []

    # ======================================================
    # MODEL CHECK
    # ======================================================

    def model_available(self):

        return self.model in self.models()

    # ======================================================
    # GENERATE
    # ======================================================

    def generate(self, prompt):

        if not self.available():

            raise RuntimeError(
                "Local AI server is not running."
            )

        if not self.model_available():

            available_models = self.models()

            if available_models:

                raise RuntimeError(
                    "Local AI model "
                    f"'{self.model}' is not installed.\n"
                    "Available models:\n"
                    + "\n".join(
                        f"  - {model}"
                        for model in available_models
                    )
                )

            raise RuntimeError(
                "No Ollama models are installed."
            )

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        data = json.dumps(
            payload
        ).encode("utf-8")

        request = urllib.request.Request(
            self.url + "/api/generate",
            data=data,
            headers={
                "Content-Type":
                    "application/json"
            },
            method="POST"
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=600
            ) as response:

                raw = response.read()

            result = json.loads(
                raw.decode("utf-8")
            )

            text = result.get(
                "response"
            )

            if not isinstance(
                text,
                str
            ) or not text.strip():

                raise RuntimeError(
                    "Local AI returned no text."
                )

            return text.strip()

        except urllib.error.HTTPError as error:

            body = error.read().decode(
                "utf-8",
                errors="replace"
            )

            raise RuntimeError(
                f"Local AI error "
                f"{error.code}: {body}"
            )

        except urllib.error.URLError as error:

            raise RuntimeError(
                "Local AI connection failed: "
                f"{error}"
            )


# ==========================================================
# PROVIDER MANAGER
# ==========================================================

class AIProviderManager:

    def __init__(self):

        self.openai = OpenAIProvider()

        self.local = LocalProvider()

    # ======================================================
    # STATUS
    # ======================================================

    def status(self):

        return {
            "local": self.local.available(),
            "openai": self.openai.available()
        }

    # ======================================================
    # PROVIDER INFORMATION
    # ======================================================

    def info(self):

        return {
            "local": {
                "available":
                    self.local.available(),
                "model":
                    self.local.model,
                "models":
                    self.local.models()
            },

            "openai": {
                "available":
                    self.openai.available(),
                "model":
                    self.openai.model
            }
        }

    # ======================================================
    # SELECT PROVIDER
    # ======================================================

    def get_provider(
        self,
        preferred=None
    ):

        preferred = (
            preferred
            or os.environ.get(
                "NITRON_AI_PROVIDER",
                "auto"
            )
        ).lower().strip()

        # --------------------------------------------------
        # EXPLICIT LOCAL
        # --------------------------------------------------

        if preferred == "local":

            if not self.local.available():

                raise RuntimeError(
                    "Local AI server is not running."
                )

            if not self.local.model_available():

                raise RuntimeError(
                    "Local model is not installed: "
                    f"{self.local.model}"
                )

            return self.local

        # --------------------------------------------------
        # EXPLICIT OPENAI
        # --------------------------------------------------

        if preferred == "openai":

            if not self.openai.available():

                raise RuntimeError(
                    "OpenAI API key is not configured."
                )

            return self.openai

        # --------------------------------------------------
        # AUTOMATIC
        # --------------------------------------------------
        #
        # Local AI is preferred.
        #
        # This allows Nitron to continue working
        # without OpenAI API credits.
        # --------------------------------------------------

        if self.local.available():

            if self.local.model_available():

                return self.local

        if self.openai.available():

            return self.openai

        raise RuntimeError(
            "No AI provider is available.\n"
            "Start Ollama or configure OPENAI_API_KEY."
        )

    # ======================================================
    # GENERATE
    # ======================================================

    def generate(
        self,
        prompt,
        preferred=None
    ):

        provider = self.get_provider(
            preferred
        )

        return provider.generate(
            prompt
        )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    manager = AIProviderManager()

    print()
    print("=" * 60)
    print("NITRON AI PROVIDER SYSTEM v4.0")
    print("=" * 60)

    print()
    print("Provider status:")

    for name, available in manager.status().items():

        print(
            f"  {name}: "
            f"{'AVAILABLE' if available else 'OFFLINE'}"
        )

    print()
    print("Local models:")

    models = manager.local.models()

    if models:

        for model in models:

            print(
                "  -",
                model
            )

    else:

        print(
            "  No models detected."
        )

    print()

    try:

        provider = manager.get_provider()

        print(
            "Selected provider:",
            provider.name
        )

        print(
            "Model:",
            getattr(
                provider,
                "model",
                "unknown"
            )
        )

    except Exception as error:

        print(
            "No provider available:"
        )

        print(
            error
        )

    print()
    print("=" * 60)
