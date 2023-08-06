# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import collections
import typing as tp

from .._proto_namespace import _ProtoNamespace
from ._02_base import BaseComponent


class MetaMixin(BaseComponent):
    def set_defaults(self) -> None:
        super().set_defaults()
        self.auxcon.setdefault("meta", _ProtoNamespace())
        self.auxcon.meta.setdefault("disabled", [])

    def cleanup(self, **kwgs: tp.Any) -> None:
        super().cleanup(meta=self.__keys(), **kwgs)

    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("disabled",)

    def clear_to_demo(self, **kwgs: tp.Any) -> None:
        super().clear_to_demo(**kwgs)
        self.auxcon.meta.disabled = ["some_module"]

    def is_enabled(self, component_name: str) -> bool:
        for x in self.__class__.__mro__:
            if self._comp_name_type_match(component_name, x):
                return component_name not in self.auxcon.meta.disabled
        return False

    def type_wo_disabled(
        self,
        disabled_list: tp.Optional[tp.List[str]] = None,
        *,
        discard_before: str = "",
        check_absence: bool = True,
    ) -> "BaseComponent":
        if disabled_list is None:
            disabled_list = self.auxcon.meta.disabled
        res: tp.List[type] = []
        for part in self.__class__.__mro__:
            if part.__name__ == discard_before:
                res.clear()
            if part.__name__ in ["AllComponents", "DynComponent"]:
                continue
            if not any(self._comp_name_type_match(x, part) for x in disabled_list):
                res.append(part)
        res_type = BaseComponent.compose(*reversed(res))

        # check if disabled did not get added by enabled
        if check_absence:
            compare_to = self.type_wo_disabled(
                discard_before="SentinelMixin", check_absence=False
            )
            parents: tp.MutableMapping[
                type, tp.Sequence[type]
            ] = collections.defaultdict(list)
            for part in compare_to.__mro__[1:]:  # remove bottom dyn
                parents[part] = part.__mro__[1:]  # remove self == part
                if any(self._comp_name_type_match(x, part) for x in disabled_list):
                    used_by = [
                        key.__name__ for key, val in parents.items() if part in val
                    ]
                    raise RuntimeError(
                        f"{part.__name__} cannot be disabled, as it is used by {', '.join(used_by)}"
                    )

        return res_type

    @classmethod
    def _comp_name_type_match(
        cls, component_name: str, component_type: tp.Type[tp.Any]
    ) -> bool:
        return cls._canon_comp_name(component_name) == cls._canon_type_name(
            component_type
        )

    @classmethod
    def _canon_type_name(cls, component_type: tp.Type[tp.Any]) -> str:
        return component_type.__name__.lower().replace("mixin", "")

    @classmethod
    def _canon_comp_name(cls, component_name: str) -> str:
        return component_name.replace("-", "")
