import pytest
from click.testing import CliRunner

import coiled
from coiled.cli.upload import upload

from ...utils import ExperimentalFeatureWarning
from ..utils import conda_command, parse_conda_command


def test_upload(sample_user):
    name = "coiled-test-foo"
    fqn = f"{sample_user.account.name}/{name}"
    parse_conda_command(
        [conda_command(), "create", "-y", "-q", "--name", name, "--json", "toolz"]
    )

    assert fqn not in coiled.list_software_environments()

    runner = CliRunner()
    with pytest.warns(ExperimentalFeatureWarning):
        result = runner.invoke(upload, args=f"--name {name}")
    assert result.exit_code == 0

    assert fqn in coiled.list_software_environments()
