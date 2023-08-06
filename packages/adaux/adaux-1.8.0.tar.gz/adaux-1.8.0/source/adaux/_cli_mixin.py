# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import io
import shutil
import subprocess
import typing as tp
from pathlib import Path

from ._components import AllComponents
from ._components._02_base import BaseComponent
from ._gitlab import GitlabSetter
from ._tick import TickSetter
from ._util import LazyVersionStr


class CliMixin(BaseComponent):  # pylint: disable=too-many-ancestors
    def __init__(self, target: Path, silent: bool = False) -> None:
        super().__init__()
        self.verbose = not silent
        self.target = Path(target or "devops").resolve()

        if str(Path.cwd()) in str(self.target):
            self.target = self.target.relative_to(Path.cwd())

        valid_suffix = [".yml", ".yaml", ".cfg"]
        candidates = [
            (self.target.parent / "auxilium").with_suffix(sfx) for sfx in valid_suffix
        ]
        self.auxcon_file = candidates[0]

        # fuzzy finder via git root
        if not any(cand.exists() for cand in candidates) and target is None:
            resp = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                check=False,
            )
            if resp.returncode == 0:
                git_root = Path(resp.stdout.decode().strip())
                self.target = git_root / "devops"
                candidates = [
                    (git_root / "auxilium").with_suffix(sfx) for sfx in valid_suffix
                ]

        for cand in candidates:
            if cand.exists():
                self.auxcon_file = cand
                self.load_auxcon()
                break
        self._print(f"adaux {LazyVersionStr()} at your service", fg="blue")

    @property
    def target_custom(self) -> Path:
        return self.target / "custom"

    def demo(self: "CliMixin") -> None:
        self.clear_to_demo()
        out = io.StringIO()
        self.save_auxcon_to_stream(out)
        self._print(out.getvalue())

    def show(self: "CliMixin", full: bool = False) -> None:
        out = io.StringIO()
        self.save_auxcon_to_stream(out, stage1=not full)
        self._print(out.getvalue())

    def init(
        self: "CliMixin",
        project_name: str,
        project_slug: str,
        python_version: str,
        author: str,
        force: bool = False,
    ) -> None:

        self.clear_to_template(
            project_name=project_name,
            project_slug=project_slug,
            python_version=python_version,
            author=author,
        )

        self.target.mkdir(parents=True, exist_ok=True)
        self.save_auxcon_and_print(force)

    def save_auxcon_and_print(self, force: bool = False, stage1: bool = True) -> None:
        dest = self.auxcon_file
        over, fg_col = "", "green"
        if dest.exists():
            if not force:
                raise RuntimeError(f"{dest} exists, use -f or --force to overwrite.")
            over, fg_col = "over", "yellow"

        with self.extra(stage1=stage1):
            self.save_auxcon()

        # pylint: disable=protected-access
        self._print(f"{over}written template to {dest}", fg=fg_col)

    def sync(self: "CliMixin") -> None:
        proj = self.auxcon.project
        clean = self.type_wo_disabled(discard_before="SentinelMixin")()
        # full holds all possible defaults (in case something got disabled)
        full = AllComponents().type_wo_disabled(discard_before="SentinelMixin")()  # type: ignore

        for ns in [clean, full]:
            ns.clear_to_template(
                project_name=proj.name,
                project_slug=proj.slug,
                python_version=proj.minimal_version,
                author=proj.author,
            )
        self.update_to_template(clean.auxcon, full.auxcon)
        with self.extra(stage1=True):
            self.save_auxcon()

    def bake(self: "CliMixin") -> None:
        if not self.auxcon_file.exists():
            raise RuntimeError(f"{self.auxcon_file} does not exists! use 'aux init'")
        super().bake()

    def gitlab(self: "CliMixin", token: str) -> None:
        gls = GitlabSetter(self, token)
        with self.extra():
            gls.bake()

    def pipeline(
        self: "CliMixin", token: str, show_success: bool
    ) -> tp.Tuple[bool, bool]:
        gls = GitlabSetter(self, token)
        with self.extra():
            return gls.pipeline(show_success)

    def tick(
        self: "CliMixin",
        release_message: str,
        major: bool = False,
        minor: bool = False,
        commit: bool = False,
    ) -> None:
        if major and minor:
            raise RuntimeError("cannot set major and minor tick at the same time!")
        if len(release_message) < 16:
            raise RuntimeError("message cannot be shorter than 16 char")
        ticker = TickSetter(self, release_message, major, minor)
        with self.extra():
            ticker.bake()
            if commit:
                ticker.commit()

    def release(
        self: "CliMixin", token: str, rerelease: bool = False
    ) -> tp.Tuple[bool, bool]:
        gls = GitlabSetter(self, token)
        with self.extra():
            return gls.release(rerelease)

    def convert(self: "CliMixin", src: Path, dest: Path, force: bool = False) -> None:
        self.auxcon_file = src
        self.load_auxcon()
        self.auxcon_file = dest
        self.save_auxcon_and_print(force)

    def ci(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("ci")
        cmd = ["python", str(self.target / "CI" / "python_ci.py"), *args]
        subprocess.run(cmd, check=False)

    def cov(self: "CliMixin", open_html: bool = False) -> None:
        self._raise_if_disabled("coverage")
        cov_cache = self.target / "cache" / "coverage"
        datafile = cov_cache / "data_file"
        cov_file = self.target.parent / ".coverage"
        if datafile.exists():
            if cov_file.exists():
                datafile.unlink()
            else:
                datafile.rename(cov_file)
        cmd = [
            "pytest",
            "--cov",
            f"--cov={self.auxcon.project.name}",
            f"--cov-report=html:{cov_cache}",
        ]
        subprocess.run(cmd, check=True)
        cov_file.rename(datafile)

        if open_html:
            cmd = ["open", str(cov_cache / "index.html")]
            subprocess.run(cmd, check=True)

    def dcp(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("docker")
        cmd = [
            "docker",
            "compose",
            "-f",
            str(self.target / "docker" / "compose.yml"),
            *args,
        ]
        subprocess.run(cmd, check=False)

    def docs(self: "CliMixin", open_html: bool = False) -> None:
        self._raise_if_disabled("docs")

        docs_cache = self.target / "cache" / "docs"

        with self.extra():
            aux = self.auxcon
            cmd = ["sphinx-apidoc", "-o", aux.docs.root, aux.project.module_dir]
            subprocess.run(cmd, check=True)
            cmd = ["sphinx-build", "-M", "html", aux.docs.root, docs_cache]
            if aux.docs.get("strict", True):
                cmd.append("-W")
            subprocess.run(cmd, check=True)
            cmd = [
                "python",
                self.target / "docs" / "postprocess_html.py",
                (docs_cache / "html" / aux.project.second_name).with_suffix(".html"),
            ]
            subprocess.run(cmd, check=True)

        if open_html:
            cmd = ["open", docs_cache / "html" / "index.html"]
            subprocess.run(cmd, check=True)

    def mp(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("mypy")
        cmd = ["git", "add", "-u"]
        subprocess.run(cmd, check=True)
        cmd = [
            "pre-commit",
            "run",
            f"--config={self.target/'pre-commit'/'config.yaml'}",
            "mypy",
            *args,
        ]
        self._run_with_line_limit(cmd)

    def pipi(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("pip")
        optional = ""
        if args:
            optional = f'[{",".join(args)}]'
        cmd = [
            "pip",
            "install",
            "-e",
            f"{self.target.parent}{optional}",
            "--config-settings",
            "editable_mode=strict",
        ]
        subprocess.run(cmd, check=False)

    def pl(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("pylint")
        cmd = ["git", "add", "-u"]
        subprocess.run(cmd, check=True)
        cmd = [
            "pre-commit",
            "run",
            f"--config={self.target/'pre-commit'/'config.yaml'}",
            "pylint",
            *args,
        ]
        self._run_with_line_limit(cmd)

    def pra(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("pre-commit")
        cmd = ["git", "add", "-u"]
        subprocess.run(cmd, check=True)
        if not args:
            args = ("--all",)
        cmd = [
            "pre-commit",
            "run",
            f"--config={self.target/'pre-commit'/'config.yaml'}",
            *args,
        ]
        subprocess.run(cmd, check=False)

    def sdist(self: "CliMixin", zipped: bool = False) -> None:
        self._raise_if_disabled("package")
        cmd = ["python", "setup.py", "sdist"]
        subprocess.run(cmd, check=True)

        if not zipped:
            files = list((self.target.parent / "dist").glob("*.tar.gz"))
            for file in files:
                path = file.with_name(file.name.replace(".tar.gz", ""))
                if path.exists():
                    shutil.rmtree(path, ignore_errors=True)
            cmd = ["tar", "-zxf", *map(str, files), "-C", "dist"]
            subprocess.run(cmd, check=True)
            for file in files:
                file.unlink()

    def _raise_if_disabled(self, component: str) -> None:
        if not self.is_enabled(component):
            raise RuntimeError(
                f"{component} disabled for this project, check your auxilium file."
            )

    @staticmethod
    def _run_with_line_limit(cmd: tp.List[str], limit: int = 50) -> None:
        proc = subprocess.run(cmd, check=False, stdout=subprocess.PIPE)
        i = 0
        for i, line in enumerate(proc.stdout.decode("utf-8").split("\n")):
            if i < limit:
                print(line)
        if i >= limit:
            print(f"{i-limit} more lines not shown, only the first {limit}...")


class CliRenderer(CliMixin, AllComponents):  # pylint: disable=too-many-ancestors
    pass
