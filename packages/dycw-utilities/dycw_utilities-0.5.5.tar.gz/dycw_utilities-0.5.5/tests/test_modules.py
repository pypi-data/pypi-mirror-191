from collections.abc import Callable
from functools import partial
from operator import le, lt
from types import ModuleType
from typing import Any, Optional, Union

from pytest import mark, param

from tests.modules import package_with, package_without, standalone
from utilities.modules import yield_module_contents, yield_modules


class TestYieldModules:
    @mark.parametrize(
        ("module", "recursive", "expected"),
        [
            param(standalone, False, 1),
            param(standalone, True, 1),
            param(package_without, False, 2),
            param(package_without, True, 2),
            param(package_with, False, 2),
            param(package_with, True, 5),
        ],
    )
    def test_main(
        self,
        module: ModuleType,
        recursive: bool,
        expected: int,
    ) -> None:
        assert len(list(yield_modules(module, recursive=recursive))) == expected


class TestYieldModuleContents:
    @mark.parametrize(
        ("type_", "predicate", "expected"),
        [
            param(None, None, 14),
            param(int, None, 3),
            param(float, None, 3),
            param((int, float), None, 6),
            param(int, partial(le, 0), 2),
            param(int, partial(lt, 0), 1),
            param(float, partial(le, 0), 2),
            param(float, partial(lt, 0), 1),
        ],
    )
    def test_main(
        self,
        type_: Optional[Union[type, tuple[type, ...]]],
        predicate: Callable[[Any], bool],
        expected: int,
    ) -> None:
        it = yield_module_contents(standalone, type=type_, predicate=predicate)
        assert len(list(it)) == expected
