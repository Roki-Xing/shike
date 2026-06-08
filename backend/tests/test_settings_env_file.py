import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from shike_backend.settings import DEFAULT_VIVO_MULTIMODAL_MODEL_CANDIDATES, Settings


class SettingsEnvFileTest(unittest.TestCase):
    def test_from_env_loads_private_env_file_without_process_exports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / "backend.env"
            env_path.write_text(
                "\n".join(
                    [
                        'export SHIKE_MODEL_PROVIDER="bluelm"',
                        "BLUELM_APP_ID=placeholder-app-id",
                        "BLUELM_APP_KEY=placeholder-app-key",
                        "BLUELM_MODEL=Volc-DeepSeek-V3.2",
                        "VIVO_MULTIMODAL_MODEL=placeholder-vision-model",
                        "VIVO_MULTIMODAL_MODELS=placeholder-vision-model, second-vision-model",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"SHIKE_BACKEND_ENV_FILE": str(env_path)}, clear=True):
                settings = Settings.from_env()

        self.assertEqual("bluelm", settings.model_provider)
        self.assertEqual("placeholder-app-id", settings.bluelm_app_id)
        self.assertEqual("placeholder-app-key", settings.bluelm_app_key)
        self.assertEqual("Volc-DeepSeek-V3.2", settings.bluelm_model)
        self.assertEqual("placeholder-vision-model", settings.vivo_multimodal_model)
        self.assertEqual(("placeholder-vision-model", "second-vision-model"), settings.vivo_multimodal_models)

    def test_from_env_keeps_process_environment_higher_priority_than_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / "backend.env"
            env_path.write_text(
                "\n".join(
                    [
                        "BLUELM_APP_ID=file-app-id",
                        "BLUELM_APP_KEY=file-app-key",
                        "BLUELM_MODEL=file-model",
                    ]
                ),
                encoding="utf-8",
            )
            environ = {
                "SHIKE_BACKEND_ENV_FILE": str(env_path),
                "BLUELM_APP_KEY": "process-app-key",
            }

            with patch.dict(os.environ, environ, clear=True):
                settings = Settings.from_env()

        self.assertEqual("file-app-id", settings.bluelm_app_id)
        self.assertEqual("process-app-key", settings.bluelm_app_key)
        self.assertEqual("file-model", settings.bluelm_model)

    def test_from_env_uses_default_multimodal_candidate_chain_when_list_is_absent(self) -> None:
        with patch.dict(os.environ, {"VIVO_MULTIMODAL_MODEL": "single-vision-model"}, clear=True):
            settings = Settings.from_env()

        self.assertEqual("single-vision-model", settings.vivo_multimodal_model)
        self.assertEqual(
            ("single-vision-model", *DEFAULT_VIVO_MULTIMODAL_MODEL_CANDIDATES),
            settings.vivo_multimodal_models,
        )

    def test_from_env_defaults_multimodal_to_vivo_vision_model_when_absent(self) -> None:
        with patch.dict(os.environ, {"BLUELM_MODEL": "Volc-DeepSeek-V3.2"}, clear=True):
            settings = Settings.from_env()

        self.assertEqual("vivo-BlueLM-V-2.0", settings.vivo_multimodal_model)
        self.assertIn("BlueLM-Vision-prd", settings.vivo_multimodal_models)

    def test_from_env_accepts_android16_guide_vivo_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / "backend.env"
            env_path.write_text(
                "\n".join(
                    [
                        "VIVO_APP_ID=guide-app-id",
                        "VIVO_APP_KEY=guide-app-key",
                        "VIVO_CHAT_BASE_URL=https://api-ai.vivo.com.cn/v1",
                        "VIVO_CHAT_MODEL=guide-chat-model",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"SHIKE_BACKEND_ENV_FILE": str(env_path)}, clear=True):
                settings = Settings.from_env()

        self.assertEqual("guide-app-id", settings.bluelm_app_id)
        self.assertEqual("guide-app-key", settings.bluelm_app_key)
        self.assertEqual("https://api-ai.vivo.com.cn", settings.bluelm_base_url)
        self.assertEqual("/v1/chat/completions", settings.bluelm_uri)
        self.assertEqual("guide-chat-model", settings.bluelm_model)
        self.assertEqual("guide-app-id", settings.vivo_ocr_app_id)
        self.assertEqual("guide-app-key", settings.vivo_ocr_app_key)
        self.assertEqual("guide-app-id", settings.vivo_multimodal_app_id)
        self.assertEqual("guide-app-key", settings.vivo_multimodal_app_key)

    def test_from_env_accepts_deepseek_provider_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / "backend.env"
            env_path.write_text(
                "\n".join(
                    [
                        "SHIKE_MODEL_PROVIDER=deepseek",
                        "DEEPSEEK_API_KEY=placeholder-deepseek-key",
                        "DEEPSEEK_BASE_URL=https://api.deepseek.com",
                        "DEEPSEEK_URI=/chat/completions",
                        "DEEPSEEK_MODEL=deepseek-v4-flash",
                        "DEEPSEEK_THINKING_ENABLED=false",
                        "DEEPSEEK_RESPONSE_FORMAT=true",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"SHIKE_BACKEND_ENV_FILE": str(env_path)}, clear=True):
                settings = Settings.from_env()

        self.assertEqual("deepseek", settings.model_provider)
        self.assertEqual("placeholder-deepseek-key", settings.deepseek_api_key)
        self.assertEqual("https://api.deepseek.com", settings.deepseek_base_url)
        self.assertEqual("/chat/completions", settings.deepseek_uri)
        self.assertEqual("deepseek-v4-flash", settings.deepseek_model)
        self.assertEqual(False, settings.deepseek_thinking_enabled)
        self.assertEqual(True, settings.deepseek_response_format_enabled)


if __name__ == "__main__":
    unittest.main()
