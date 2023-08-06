# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import contextlib
import subprocess
import typing as tp

from .._proto_namespace import _ProtoNamespace
from ._04_project import ProjectMixin


class GitlabMixin(ProjectMixin):
    def set_defaults(self) -> None:
        super().set_defaults()
        self.auxcon.setdefault("gitlab", _ProtoNamespace())

    def clear_to_template(self, **kwgs: str) -> None:
        super().clear_to_template(**kwgs)
        data = self.auxcon.gitlab
        data.vip_branches = [
            "develop;push_access_level=40;allow_force_push=True",
            "release",
        ]

    def clear_to_demo(self, **kwgs: str) -> None:
        super().clear_to_demo(**kwgs)
        data = self.auxcon.gitlab
        data.default_branch = "develop"
        data.release_branch = "release"
        data.remote_user = "administratum"
        data.remote_name = "auxilium"
        data.remote_url = "gitlab.x.y"

    def update_to_template(self, tpl: _ProtoNamespace, full: _ProtoNamespace) -> None:
        super().update_to_template(tpl, full)
        data = self.auxcon.gitlab
        if self.is_enabled("docs"):
            if "remote_url" in data and "remote_user" in data:
                return
            proc = subprocess.run(
                ["git", "remote", "-v"], capture_output=True, check=False
            )
            if proc.returncode != 0:
                return
            full_url = proc.stdout.decode("utf-8").split()[1]
            _, url = full_url.split("@", 1)
            defaults = {}
            defaults["remote_url"], rest = url.split(":", 1)
            defaults["remote_user"], rest = rest.split("/", 1)
            defaults["remote_name"] = rest.replace(".git", "")
            key = "remote_url"
            for key, val in defaults.items():
                if key not in data:
                    if key == "remote_name" and val == self.auxcon.project.name:
                        continue
                    data[key] = val
                    self._print(f"gitlab.{key}: added {data[key]}", fg="green")

    @contextlib.contextmanager
    def extra(self, stage1: bool = False) -> tp.Iterator[_ProtoNamespace]:
        with super().extra(stage1) as auxcone:
            data = auxcone.gitlab
            if stage1:
                if "vip_branches" in data:
                    data.vip_branches = self.list2nsl(data.vip_branches)
                    for x in data.vip_branches:
                        self._boolify(x, "allow_force_push")
                yield auxcone
                return
            data.vip_branches = self.list2ns(data.vip_branches)
            vip_branch_name = list(data.vip_branches)
            data.setdefault("default_branch", vip_branch_name[0])
            data.setdefault("release_branch", vip_branch_name[-1])

            if "remote_user" in data and "remote_url" in data:
                remote_name = data.get("remote_name", auxcone.project.second_name)
                auxcone.project.project_urls.Source = (
                    f"https://{data.remote_url}/{data.remote_user}/{remote_name}"
                )

            # https://docs.gitlab.com/ee/api/protected_branches.html
            default = {
                (False, False): dict(
                    allow_force_push=True, push_access_level=30, merge_access_level=30
                ),
                (True, False): dict(push_access_level=0, merge_access_level=30),
                (False, True): dict(push_access_level=0, merge_access_level=40),
            }
            for key, val in data.vip_branches.items():
                mark = (key == data.default_branch, key == data.release_branch)
                for skey, sval in default[mark].items():
                    val.setdefault(skey, sval)

            yield auxcone
