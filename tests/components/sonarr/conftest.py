"""Fixtures for Sonarr integration tests."""
from collections.abc import Generator
import json
from unittest.mock import MagicMock, patch

import pytest
from sonarr import Application as SonarrApp

from homeassistant.components.sonarr.const import DOMAIN
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry, load_fixture


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        title="Sonarr",
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.189"},
        unique_id=None,
    )


@pytest.fixture
def mock_setup_entry() -> Generator[None, None, None]:
    """Mock setting up a config entry."""
    with patch("homeassistant.components.sonarr.async_setup_entry", return_value=True):
        yield


@pytest.fixture
def mock_sonarr_config_flow(
    request: pytest.FixtureRequest,
) -> Generator[None, MagicMock, None]:
    """Return a mocked Sonarr client."""
    fixture: str = "sonarr/app.json"
    if hasattr(request, "param") and request.param:
        fixture = request.param

    device = SonarrApp(json.loads(load_fixture(fixture)))
    with patch(
        "homeassistant.components.sonarr.config_flow.Sonarr", autospec=True
    ) as sonarr_mock:
        client = sonarr_mock.return_value
        client.update.return_value = device
        yield client


@pytest.fixture
def mock_roku(request: pytest.FixtureRequest) -> Generator[None, MagicMock, None]:
    """Return a mocked Sonarr client."""
    fixture: str = "sonarr/app.json"
    if hasattr(request, "param") and request.param:
        fixture = request.param

    device = SonarrApp(json.loads(load_fixture(fixture)))
    with patch(
        "homeassistant.components.sonarr.Sonarr", autospec=True
    ) as sonarr_mock:
        client = sonarr_mock.return_value
        client.update.return_value = device
        yield client


@pytest.fixture
async def init_integration(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry, mock_sonarr: MagicMock
) -> MockConfigEntry:
    """Set up the Sonarr integration for testing."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    return mock_config_entry
