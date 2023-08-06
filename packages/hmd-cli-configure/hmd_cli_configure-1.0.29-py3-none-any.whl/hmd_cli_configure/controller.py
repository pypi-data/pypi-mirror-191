import os
from pathlib import Path

import yaml
from cement import Controller, ex, minimal_logger, shell
from importlib.metadata import version
from hmd_cli_tools import get_version
from hmd_cli_tools.hmd_cli_tools import load_hmd_env, set_hmd_env
from hmd_cli_tools.prompt_tools import prompt_for_values
from dotenv import set_key


logger = minimal_logger("hmd-cli-configure")

VERSION_BANNER = """
hmd configure version: {}
"""


hmd_home_vars = {
    "HMD_HOME": {
        "prompt": "Select a folder to store NeuronSphere data and configuration:",
        "default": Path(os.path.expanduser("~")) / ".hmd",
    }
}
default_env_vars = {
    "HMD_AUTHOR_NAME": {"prompt": "Enter your name:"},
    "HMD_AUTHOR_EMAIL": {"prompt": "Enter your email:"},
    "HMD_DOCKER_DIR": {"hidden": True, "default": "./"},
    "HMD_DOCKER_INSTALL_LOCAL": {"hidden": True, "default": "true"},
}


class LocalController(Controller):
    class Meta:
        label = "configure"
        alias = "config"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Configures a local environment to use HMD CLI tools. Run 'hmd configure' to setup local environment."

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the configure command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(version("hmd_cli_configure")),
                },
            ),
        )

    def _default(self):
        hmd_home = os.environ.get("HMD_HOME")
        questions = default_env_vars
        if hmd_home is None:
            logger.warning("Could not find environment variable HMD_HOME.")
            questions = {**hmd_home_vars, **default_env_vars}

        results = prompt_for_values(questions)
        for key, value in results.items():
            if key == "HMD_HOME":
                if value is not None:
                    hmd_home = os.path.expandvars(os.path.expanduser(value))
                    os.environ["HMD_HOME"] = hmd_home
                    set_hmd_env("HMD_HOME", hmd_home)
                    load_hmd_env(override=False)
                    continue

            if value is not None:
                set_hmd_env(key, value)

        for h in self.app._meta.handlers:
            if h.Meta.label == self.Meta.label:
                continue
            setattr(h, "app", self.app)
            configure_cmd = getattr(h, "configure", None)
            if configure_cmd:
                # cfg_prompt = shell.Prompt(
                #     f"Configure hmd {h.Meta.label}:",
                #     options=["yes", "no"],
                #     default="yes",
                # )
                # cfg = cfg_prompt.prompt()

                # if cfg == "no":
                #     continue

                configure_cmd(h)

    @ex(
        help="Set environment variable in $HMD_HOME/.config/hmd.env",
        arguments=[
            (["key"], {"action": "store"}),
            (["value"], {"action": "store"}),
        ],
    )
    def set_env(self):
        key = self.app.pargs.key
        value = self.app.pargs.value

        set_hmd_env(key, value)
