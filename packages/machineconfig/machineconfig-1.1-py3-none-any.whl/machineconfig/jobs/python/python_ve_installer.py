
import crocodile.toolbox as tb
import platform
import machineconfig
from rich.panel import Panel
from rich.console import Console
# from rich.text import Text
from rich.syntax import Syntax

system = platform.system()
lib_root = tb.P(machineconfig.__file__).parent


def main():
    console = Console()
    print("\n\n")
    console.rule("Existing Python versions", style="bold red")
    if system == "Windows":
        tb.P.get_env().Path.search("python.exe").reduce()[1:].print()
    else:
        tb.L(set(tb.P.get_env().Path.search("python3*").reduce().filter(lambda x: not x.is_symlink() and "-" not in x))).print()
    print("\n\n")
    console.rule(f"Existing virtual environments")
    ves = tb.P.home().joinpath("venvs").search("*", files=False).apply(lambda a_ve: (a_ve.name, a_ve.joinpath("pyvenv.cfg").read_text()))
    ves.apply(lambda a_ve: console.print(Panel(a_ve[1], title=a_ve[0], style="bold blue")))
    # ves.apply(lambda a_ve: tb.S(a_ve[1]).print(as_config=True, title=a_ve[0]))

    dotted_py_version = input("Enter python version (3.9): ") or "3.9"
    env_name = input("Enter virtual environment name (tst): ") or "tst"
    repos = input("Install essential repos? (y/[n]): ") or "n"

    env_path = tb.P.home().joinpath("venvs", env_name)
    if env_path.exists():
        env_path.delete(sure=True)

    scripts = lib_root.joinpath(f"setup_{system.lower()}/ve.{'ps1' if system == 'Windows' else 'sh'}").read_text()
    variable_prefix = "$" if system == "Windows" else ""
    scripts = tb.modify_text(txt_raw=scripts, txt_search="ve_name=", txt_alt=f"{variable_prefix}ve_name='{env_name}'", replace_line=True, strict=True)
    scripts = tb.modify_text(txt_raw=scripts, txt_search="py_version=", txt_alt=f"{variable_prefix}py_version='{dotted_py_version.replace('.', '') if system == 'Windows' else dotted_py_version}'", replace_line=True, strict=True)

    if repos == "y":
        text = lib_root.joinpath(f"setup_{system.lower()}/repos.{'ps1' if system == 'Windows' else 'sh'}").read_text()
        text = tb.modify_text(txt_raw=text, txt_search="ve_name=", txt_alt=f"{variable_prefix}ve_name='{env_name}'", replace_line=True)
        scripts += text

    print("\n")
    console.print(Panel(Syntax(scripts, lexer="ps1" if system == "Windows" else "sh"), title="Script to create virtual environment..."), style="bold red")

    return scripts


if __name__ == '__main__':
    pass
