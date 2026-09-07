import os
from config.constants import MODEL_VERSIONS
from config.settings import get_settings


class ModelRegistry:
    """Resolves model artifact availability. Falls back to deterministic
    engine logic (see core/engines/*/predictor.py) when artifacts are missing.
    """

    def __init__(self):
        self.settings = get_settings()

    def artifact_path(self, model_key: str) -> str:
        return os.path.join(self.settings.MODEL_ARTIFACT_PATH, model_key)

    def is_trained_model_available(self, model_key: str) -> bool:
        path = self.artifact_path(model_key)
        return os.path.isdir(path) and any(os.scandir(path)) if os.path.isdir(path) else False

    def version(self, model_key: str) -> str:
        return MODEL_VERSIONS.get(model_key, f"{model_key}_v0")


registry = ModelRegistry()
