#!/usr/bin/env python3
"""Validate the backend /v2/analyze-image vivo multimodal contract."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a project file as UTF-8.

    Args:
        relative: Path under the Shike root.

    Returns:
        File content, or an empty string when missing.
    """

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def file_exists(relative: str) -> bool:
    """Return whether a project file exists."""

    return (ROOT / relative).is_file()


def main() -> int:
    """Run vivo multimodal contract checks.

    Returns:
        Process exit code.
    """

    main_py = read("backend/shike_backend/main.py")
    schemas_v2 = read("backend/shike_backend/schemas_v2.py")
    adapter = read("backend/shike_backend/adapters/vivo_cloud_multimodal_adapter.py")
    preprocess = read("backend/shike_backend/image_preprocess.py")
    prompt = read("backend/shike_backend/prompts/analyze_image_system_prompt.txt")
    template = read("backend/shike_backend/prompts/analyze_image_user_template.txt")
    settings = read("backend/shike_backend/settings.py")
    verifier = read("backend/verify_backend.py")
    live_smoke = read("backend/shike_backend/eval/live_smoke.py")
    text_fallback_test = read("backend/tests/test_analyze_image_text_fallback.py")
    settings_test = read("backend/tests/test_settings_env_file.py")
    vision_chat_test = read("backend/tests/test_vivo_cloud_multimodal_adapter.py")

    checks = [
        ("route_exists", '@app.post("/v2/analyze-image"' in main_py and "AnalyzeImageRequest" in main_py),
        ("schemas_v2_exists", file_exists("backend/shike_backend/schemas_v2.py")),
        (
            "image_payload_contract",
            all(token in schemas_v2 for token in ["class ImagePayload", "data_url", "mime", "sha256", "width", "height"]),
        ),
        (
            "ocr_blocks_contract",
            all(token in schemas_v2 for token in ["class OcrBlock", "x1", "y1", "x2", "y2", "confidence"]),
        ),
        (
            "source_types_cover_image_flows",
            all(
                token in schemas_v2
                for token in [
                    "screenshot_share",
                    "photo_picker",
                    "camera",
                    "manual",
                    "in_app_screen_capture",
                    "recent_screenshot_assist",
                ]
            ),
        ),
        (
            "response_contract_has_evidence_and_ignored_regions",
            "class ParsedActionCard" in schemas_v2 and "EvidenceSpan" in schemas_v2 and "ignored_regions" in schemas_v2,
        ),
        (
            "adapter_uses_openai_vision_content",
            "messages" in adapter
            and "image_url" in adapter
            and "data:image" in adapter
            and "https://" in adapter
            and "Authorization" in adapter
            and "Bearer" in adapter,
        ),
        (
            "adapter_classifies_provider_image_errors",
            "provider_model_does_not_support_image" in adapter
            and "provider_error:" in adapter
            and "_content_from_provider_response" in adapter,
        ),
        (
            "adapter_supports_signed_vision_chat_fallback",
            all(
                token in adapter
                for token in [
                    "_LEGACY_VISION_CHAT_URI",
                    "/vivogpt/completions",
                    "gen_sign_headers",
                    "requestId",
                    "contentType",
                    "legacy_http_status",
                    "systemPrompt",
                    "provider_error:401",
                ]
            ),
        ),
        (
            "adapter_reads_env_backed_settings",
            "vivo_multimodal_app_key" in settings
            and "VIVO_MULTIMODAL_APP_KEY" in settings
            and "VivoCloudMultimodalAdapter" in main_py,
        ),
        (
            "settings_defaults_to_vivo_vision_model",
            "DEFAULT_VIVO_MULTIMODAL_MODEL" in settings
            and "vivo-BlueLM-V-2.0" in settings
            and "BlueLM-Vision-prd" in settings
            and "test_from_env_defaults_multimodal_to_vivo_vision_model_when_absent" in settings_test,
        ),
        (
            "prompt_ignores_device_chrome",
            all(token in prompt for token in ["忽略", "状态栏", "电量", "系统时间", "底部导航", "用户确认前"]),
        ),
        (
            "prompt_has_location_and_action_gate_rules",
            all(
                token in prompt
                for token in [
                    "地点规则",
                    "不得把“首页/导入/收件箱/设置”等导航文案作为地点",
                    "输出动作规则",
                    "只有有明确 title + time 时才能建议 calendar",
                    "缺字段时仍可生成待确认卡，但动作必须带 disabled_reason",
                ]
            ),
        ),
        (
            "user_template_includes_image_context",
            all(token in template for token in ["current_date", "user_timezone", "OCR blocks", "schema_json", "只输出 JSON"]),
        ),
        (
            "preprocess_filters_status_and_nav",
            all(token in preprocess for token in ["build_ignored_regions", "filter_ocr_blocks", "looks_like_system_status_text", "10:28", "100%"]),
        ),
        (
            "preprocess_filters_shike_ui_copy",
            all(
                token in preprocess
                for token in [
                    "looks_like_shike_app_chrome_text",
                    "快捷导入",
                    "今日行动台空状态",
                    "待确认",
                    "收件箱状态",
                ]
            )
            and "test_filter_ocr_blocks_removes_shike_ui_copy_anywhere_on_screen" in read(
                "backend/tests/test_image_preprocess.py"
            ),
        ),
        (
            "route_enriches_image_with_server_ocr",
            all(
                token in main_py
                for token in [
                    "enrich_image_request_with_server_ocr",
                    "_image_base64_from_data_url",
                    "VivoOcrAdapter",
                    "OcrRequest",
                    "allow_ocr_fallback",
                    "server_ocr_unavailable",
                ]
            ),
        ),
        (
            "route_enriches_image_with_server_ocr_blocks",
            all(
                token in main_py
                for token in [
                    "recognize_detail",
                    "server_ocr_blocks",
                    "filter_ocr_blocks",
                    "ocr_blocks",
                    "server_ocr_blocks_filtered",
                ]
            )
            and all(token in verifier for token in ["服务端OCR块", "captured_request.ocr_blocks", "assert block.text"]),
        ),
        (
            "route_fails_to_manual_review_not_training_sample",
            "manual_review" in main_py and "sampleCourse" not in main_py and "高数A班" not in main_py,
        ),
        (
            "route_falls_back_to_text_model_when_image_model_unsupported",
            all(
                token in main_py
                for token in [
                    "fallback_analyze_image_with_text_model",
                    "_parsed_card_from_text_response",
                    "_disable_actions_until_user_confirmation",
                    "text_fallback_schema_valid",
                    "provider_model_does_not_support_image",
                    "legacy_http_status:401",
                    "用户确认前不可执行",
                ]
            )
            and all(
                token in verifier
                for token in [
                    "FailingMultimodalAdapter",
                    "CapturingTextAdapter",
                    "text_fallback_response",
                    "provider_model_does_not_support_image",
                ]
            ),
        ),
        (
            "text_fallback_unit_test_exists",
            "class AnalyzeImageTextFallbackTest" in text_fallback_test
            and "test_analyze_image_uses_text_model_when_provider_does_not_support_image" in text_fallback_test
            and "test_analyze_image_uses_text_model_when_vision_chat_is_unauthorized" in text_fallback_test
            and "provider_model_does_not_support_image" in text_fallback_test
            and "legacy_http_status:401" in text_fallback_test
            and "用户确认前不可执行" in text_fallback_test,
        ),
        (
            "route_respects_allow_cloud_image_false",
            all(
                token in main_py
                for token in [
                    "if not request.allow_cloud_image",
                    "cloud_image_disabled",
                    "ocr_hint_text_fallback",
                    "fallback_analyze_image_with_text_model",
                ]
            )
            and all(
                token in text_fallback_test
                for token in [
                    "ExplodingOcrAdapter",
                    "ExplodingMultimodalAdapter",
                    "test_analyze_image_uses_ocr_hint_only_when_cloud_image_disabled",
                    "allow_cloud_image",
                    "cloud_image_disabled",
                ]
            )
            and all(
                token in verifier
                for token in [
                    "ExplodingOcrAdapter",
                    "ExplodingMultimodalAdapter",
                    "image-cloud-disabled-001",
                    "cloud_image_disabled",
                    "text_adapter.captured_request.ocr_text == \"客户端OCR：今晚18:30 项目讨论 B203\"",
                ]
            ),
        ),
        (
            "live_smoke_supports_multimodal_models",
            "--multimodal" in live_smoke
            and "--multimodal-models" in live_smoke
            and "settings.vivo_multimodal_models" in live_smoke
            and "multimodal_status" in live_smoke
            and "multimodal_error" in live_smoke
            and "VivoCloudMultimodalAdapter" in live_smoke,
        ),
        (
            "route_tries_multimodal_candidates_before_text_fallback",
            all(
                token in settings
                for token in [
                    "DEFAULT_VIVO_MULTIMODAL_MODEL_CANDIDATES",
                    "vivo_multimodal_models",
                    "VIVO_MULTIMODAL_MODELS",
                    "_env_csv",
                    "_unique_nonempty",
                ]
            )
            and all(
                token in main_py
                for token in [
                    "_get_multimodal_adapters",
                    "_normalize_multimodal_adapters",
                    "for candidate in adapters",
                    "last_multimodal_error",
                    "adapter.analyze_image",
                ]
            )
            and all(
                token in text_fallback_test
                for token in [
                    "SuccessfulMultimodalAdapter",
                    "test_analyze_image_tries_next_multimodal_candidate_before_text_fallback",
                    "模型声称可直接执行",
                    "action[\"disabled_reason\"] == \"用户确认前不可执行\"",
                    "self.assertIsNone(text_adapter.request)",
                ]
            )
            and all(
                token in main_py
                for token in [
                    "def _require_user_confirmation_for_card",
                    "gated_card = _require_user_confirmation_for_card(card)",
                    "return gated_card.model_copy",
                ]
            )
            and "test_from_env_uses_default_multimodal_candidate_chain_when_list_is_absent" in settings_test
            and "DEFAULT_VIVO_MULTIMODAL_MODEL_CANDIDATES" in settings_test
            and all(
                token in verifier
                for token in [
                    "SuccessfulMultimodalAdapter",
                    "image-multimodal-candidates-001",
                    "text_adapter.captured_request is None",
                ]
            ),
        ),
        (
            "route_sanitizes_ignored_regions_metadata",
            all(
                token in main_py
                for token in [
                    "_ALLOWED_IGNORED_REGIONS",
                    "screenshot_toolbar_or_overlay",
                    "def _sanitized_ignored_regions",
                    "region in _ALLOWED_IGNORED_REGIONS",
                    "merged_regions = _sanitized_ignored_regions",
                ]
            )
            and all(
                token in text_fallback_test
                for token in [
                    "Top synthetic screenshot fixture text",
                    'self.assertEqual(["top_status_bar", "bottom_navigation_bar"], payload["ignored_regions"])',
                ]
            ),
        ),
        (
            "unit_test_covers_signed_vision_chat_fallback",
            "test_analyze_image_falls_back_from_openai_provider_401_to_signed_vivogpt_vision_chat"
            in vision_chat_test
            and "X-AI-GATEWAY-SIGNATURE" in vision_chat_test
            and "/vivogpt/completions" in vision_chat_test
            and "contentType" in vision_chat_test
            and "legacy_body" in vision_chat_test,
        ),
        (
            "live_smoke_supports_route_v2",
            "--route-v2" in live_smoke
            and "/v2/analyze-image" in live_smoke
            and "route_v2_status" in live_smoke
            and "route_v2_schema_valid" in live_smoke
            and "route_v2_actions_disabled" in live_smoke
            and "route_v2_ignored_regions_allowed" in live_smoke
            and "ALLOWED_IGNORED_REGIONS" in live_smoke
            and "_ignored_regions_allowed" in live_smoke
            and "TestClient(app)" in live_smoke,
        ),
        ("backend_smoke_covers_v2", "/v2/analyze-image" in verifier and "manual_review" in verifier),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"VIVO_MULTIMODAL_CONTRACT_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
