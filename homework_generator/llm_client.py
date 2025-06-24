"""LLM client abstraction layer."""

import hashlib
import json
from typing import Optional
from pathlib import Path

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
    import litellm
    import diskcache

    DEPENDENCIES_AVAILABLE = True
except ImportError:
    # For testing without dependencies installed
    DEPENDENCIES_AVAILABLE = False

    def retry(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    stop_after_attempt = wait_exponential = lambda *args, **kwargs: None


class LLMClient:
    """Abstraction layer for LLM interactions."""

    def __init__(
        self, model: str, cache_enabled: bool = True, api_key: Optional[str] = None, base_url: Optional[str] = None
    ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.cache_enabled = cache_enabled

        if cache_enabled and DEPENDENCIES_AVAILABLE:
            cache_dir = Path("llm_cache")
            cache_dir.mkdir(exist_ok=True)
            self.cache = diskcache.Cache(str(cache_dir))
        else:
            self.cache = None

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        if not DEPENDENCIES_AVAILABLE:
            # Return mock response for testing
            return self._mock_response(prompt, **kwargs)

        # Check cache first
        cache_key = self._get_cache_key(prompt, **kwargs)
        if self.cache and cache_key in self.cache:
            return self.cache[cache_key]

        # Set up litellm parameters
        messages = [{"role": "user", "content": prompt}]

        # Configure API key if provided
        if self.api_key:
            if self.model.startswith("gpt"):
                import os

                os.environ["OPENAI_API_KEY"] = self.api_key

        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.1),
                max_tokens=kwargs.get("max_tokens", 4000),
                **kwargs,
            )

            content = response.choices[0].message.content

            # Cache the response
            if self.cache:
                self.cache[cache_key] = content

            return content

        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {e}")

    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Generate cache key for the request."""
        # Create deterministic key from model, prompt, and parameters
        key_data = {
            "model": self.model,
            "prompt": prompt,
            "params": sorted(kwargs.items()),
        }
        content = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def _mock_response(self, prompt: str, **kwargs) -> str:
        """Generate mock response for testing."""
        return json.dumps(
            {
                "assignments": [
                    {
                        "title": "Mock Assignment 1: Basic Problems",
                        "grade_level": "5th Grade",
                        "subject": "Mathematics",
                        "difficulty": "Medium",
                        "estimated_time": "15 minutes",
                        "instructions": "Complete these practice problems.",
                        "questions": [
                            "What is 2 + 3?",
                            "Calculate 10 - 4",
                            "Solve 6 × 2",
                        ],
                        "materials_needed": ["pencil", "paper"],
                        "learning_objectives": ["Practice basic arithmetic"],
                    }
                ]
            }
        )

    def clear_cache(self) -> None:
        """Clear the LLM response cache."""
        if self.cache:
            self.cache.clear()
