# -*- coding: utf-8 -*-
import importlib
import sys
from typing import Dict, List

from rich.markdown import Markdown
from rich.panel import Panel

from kiara_plugin.jupyter.defaults import OFFICIAL_KIARA_PLUGINS

try:
    from importlib.metadata import distribution, packages_distributions  # type: ignore
except Exception:
    from importlib_metadata import distribution, packages_distributions  # type:ignore


def ensure_kiara_plugins(*plugins, update: bool = False):
    """Ensure that the specified packages are installed.

    Arguments:
      package_names: The names of the packages to install.
      update: If True, update the packages if they are already installed

    Returns:
        'None' if nothing was done, else a string containing information about what was installed
    """

    installed_packages: Dict[str, str] = {}
    all_packages = packages_distributions()

    for name, pkgs in all_packages.items():
        for pkg in pkgs:
            dist = distribution(pkg)
            if (
                pkg in installed_packages.keys()
                and installed_packages[pkg] != dist.version
            ):
                raise Exception(
                    f"Multiple versions of package '{pkg}' available: {installed_packages[pkg]} and {dist.version}."
                )
            installed_packages[pkg] = dist.version

    if not plugins:
        plugins = tuple(OFFICIAL_KIARA_PLUGINS)

    if not update:
        plugin_packages: List[str] = []
        pkgs = [p.replace("_", "-") for p in installed_packages.keys()]
        for package_name in plugins:
            if package_name.startswith("git:"):
                package_name = package_name.replace("git:", "")
                git = True
            else:
                git = False
            package_name = package_name.replace("_", "-")
            if not package_name.startswith("kiara-plugin."):
                package_name = f"kiara-plugin.{package_name}"

            if git or package_name.replace("_", "-") not in pkgs:
                if git:
                    package_name = package_name.replace("-", "_")
                    plugin_packages.append(
                        f"git+https://x:x@github.com/DHARPA-project/{package_name}@develop"
                    )
                else:
                    plugin_packages.append(package_name)
    else:
        plugin_packages = list(plugins)

    in_jupyter = "google.colab" in sys.modules or "jupyter_client" in sys.modules
    if not in_jupyter:
        raise Exception("No juptyer environment detected.")

    if not plugin_packages:
        # nothing to do
        return None

    cmd = ["-q", "--isolated", "install"]
    if update:
        cmd.append("--upgrade")
    cmd.extend(plugin_packages)

    from IPython import get_ipython
    from rich.console import Console

    console = Console()
    with console.status("Installing kiara plugins..."):
        ipython = get_ipython()
        cmd_str = f"sc -l stdout = {sys.executable} -m pip {' '.join(cmd)}"
        ipython.magic(cmd_str)

    importlib.invalidate_caches()

    msg = "Installed packages:\n\n"
    for p in plugin_packages:
        msg += f" - {p}\n"
    msg = f"{msg}\n\nDepending on the state of your current environment, you might see error messages below, in which case you'll have to restart the jupyter kernel manually."
    return Panel(Markdown(msg), title="kiara plugin(s) installed", title_align="left")
