"""Contract tests for You.com HTTP search samplers."""

from evals.samplers.applied_samplers.you_search_sampler import (
    YouEcoSearchSampler,
    YouLiteSearchSampler,
)
from evals.configs.samplers import NON_RESEARCH_SAMPLERS, SAMPLERS


def test_eco_search_uses_the_snippet_endpoint_and_formats_web_results():
    """Catches regressions to Eco Search's GET endpoint or snippet result shape."""
    sampler = YouEcoSearchSampler(sampler_name="you_eco_search", api_key="test-key")

    sampler._set_params()

    assert sampler.base_url == "https://ydc-index.io"
    assert sampler.endpoint == "/v1/eco_search"
    assert sampler.method == "GET"
    assert sampler.headers["X-API-Key"] == "test-key"
    assert sampler._get_payload("eco search query") == {
        "query": "eco search query",
        "offset": 0,
    }
    assert sampler.format_results(
        {
            "results": {
                "web": [
                    {
                        "title": "Eco result",
                        "url": "https://example.com/eco",
                        "description": "A lightweight result",
                        "snippets": ["first snippet", "second snippet"],
                    }
                ]
            }
        }
    ) == [
        "[Eco result](https://example.com/eco)\n"
        "snippet: first snippet second snippet\n"
        "description: A lightweight result"
    ]


def test_lite_search_posts_lite_mode_and_formats_highlights():
    """Catches regressions to Lite Search's v2 request contract and result context."""
    sampler = YouLiteSearchSampler(sampler_name="you_lite_search", api_key="test-key")

    sampler._set_params()

    assert sampler.base_url == "https://ydc-index.io"
    assert sampler.endpoint == "/v2/search"
    assert sampler.method == "POST"
    assert sampler.headers["X-API-Key"] == "test-key"
    assert sampler._get_payload("lite search query") == {
        "query": "lite search query",
        "mode": "lite",
        "count": 10,
    }
    assert sampler.format_results(
        {
            "results": [
                {
                    "title": "Lite result",
                    "url": "https://example.com/lite",
                    "highlights": ["first highlight", "second highlight"],
                }
            ]
        }
    ) == [
        "[Lite result](https://example.com/lite)\n"
        "highlights: first highlight second highlight"
    ]


def test_eco_and_lite_search_are_registered_for_default_evaluations():
    """Catches a sampler implementation that cannot be selected by the runner."""
    sampler_names = [sampler.sampler_name for sampler in SAMPLERS]

    assert "you_eco_search" in sampler_names
    assert "you_lite_search" in sampler_names
    assert "you_eco_search" in NON_RESEARCH_SAMPLERS
    assert "you_lite_search" in NON_RESEARCH_SAMPLERS
