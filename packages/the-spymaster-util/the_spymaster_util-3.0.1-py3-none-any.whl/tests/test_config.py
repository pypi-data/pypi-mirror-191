import os
from typing import Optional

from the_spymaster_util.config import LazyConfig


class ExampleConfig(LazyConfig):
    @property
    def x(self) -> Optional[int]:
        x = self.get("X")
        return int(x) if x else None

    @property
    def y(self) -> Optional[str]:
        return self.get("Y")


def test_get_config_from_env_vars_is_lazy():
    config = ExampleConfig()
    assert config.x is None
    assert config.y is None
    os.environ["X"] = "1"
    os.environ["Y"] = "y"
    assert config.x == 1
    assert config.y == "y"
    os.environ.pop("X")
    os.environ.pop("Y")
    assert config.x is None
    assert config.y is None


def test_config_update():
    config = ExampleConfig()
    assert config.x is None
    assert config.y is None
    config.update(X=1, Y="y")
    assert config.x == 1
    assert config.y == "y"
    config.update(X=2)
    config.set("Y", "z")
    assert config.x == 2
    assert config.y == "z"
