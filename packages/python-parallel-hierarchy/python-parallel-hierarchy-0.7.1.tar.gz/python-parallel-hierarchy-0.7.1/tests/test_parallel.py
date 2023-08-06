#
#     Copyright 2021-2023 Joël Larose
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#

from __future__ import annotations

import pytest

from parallel_hierarchy import ParallelFactory
from sampleclasses import *

class TestParallelFactory:
    def test_factory_classdef(self):
        factory_1 = ParallelFactory(A, View, suffix="_1")

        assert factory_1

    def test_factory_root(self):
        factory_2 = ParallelFactory(A, View, suffix="_2")

        new_cls = factory_2.get(A)
        assert new_cls.__name__ == "A_2"
        assert new_cls.source_class == A

    def test_factory_with_ancestor(self):
        factory_3 = ParallelFactory(A, View, suffix="_3")

        new_cls = factory_3(B)
        assert new_cls.__name__ == "B_3"
        assert new_cls.source_class == B
        assert len(new_cls.__bases__) == 1
        assert new_cls.__bases__[0].__name__ == "A_3"

    def test_factory_multiple_inheritance(self):
        factory_4 = ParallelFactory(A, View, suffix="_4")

        new_cls = factory_4(E)
        assert new_cls.__name__ == "E_4"
        assert new_cls.source_class == E

        base_names = {b.__name__ for b in new_cls.__bases__}
        assert len(base_names) == 2
        assert {"B_4",  "D_4"} == base_names

        # At the moment, I don't care about the actual order, just the content
        mro_names = {b.__name__ for b in new_cls.mro()}
        assert len(mro_names) == 7
        assert {"A_4", "B_4", "C_4", "D_4", "E_4", "object", "View"} == mro_names

    def test_no_generic_params(self):
        with pytest.raises(TypeError) as err:
            bad_factory = ParallelFactory("A", "View", suffix="_Bad")

        assert err
        assert locals().get("bad_factory") is None
        err_msgs = err.value.args[0]
        assert isinstance(err_msgs, list)
        assert err_msgs == ["SourceBase must be a type", "ParaBase must be a type"]

    def test_no_affix(self):
        with pytest.raises(AttributeError) as err:
            no_affix_factory = ParallelFactory(A, View)

        assert err
        assert locals().get("no_affix_factory") is None
        err_msg = err.value.args[0]
        assert err_msg == "At least one of 'prefix' or 'suffix' must be specified with a " \
                          "non-empty string."

    def test_cover_affix_none(self):
        factory_5 = ParallelFactory(A, View, prefix="F5_", suffix=None)

        factory_6 = ParallelFactory(A, View, prefix=None, suffix="_6")

        assert factory_5.parallel_suffix == ""
        assert factory_6.parallel_prefix == ""

    def test_register_error(self):
        factory_7 = ParallelFactory(A, View, suffix="_7")

        class B_7:
            """Intentionally "forgot" to provide base class."""

        with pytest.raises(TypeError) as err:
            factory_7.register(B_7)

        assert err.type is TypeError

    def test_get_none(self):
        factory_8 = ParallelFactory(A, View, suffix="_8")

        with pytest.raises(ValueError) as err:
            factory_8(None)

        assert err.type is ValueError

    def test_get_wrong_type(self):
        factory_9 = ParallelFactory(A, View, suffix="_9")

        with pytest.raises(TypeError) as err:
            factory_9(str)

        assert err.type is TypeError

    def test_bad_custom_build_call(self):
        factory_10 = ParallelFactory(A, View, suffix="_10")

        class F:
            """Intentionally "forgot" to provide base class."""

        with pytest.raises(TypeError) as err:
            factory_10.build_parallel_class(F, "F_10")

        assert err.type is TypeError

    def test_has(self):
        factory_11 = ParallelFactory(A, View, suffix="_11")

        assert not factory_11.has("A_11")
        assert not factory_11.has("A")
        assert not factory_11.has(A)

        ViewA = factory_11(A)  # Local alias for class A_11
        assert factory_11.has("A_11")
        assert factory_11.has("A")
        assert factory_11.has(A)
        assert factory_11.has(ViewA)

        assert not factory_11.has("B_11")
        ViewE = factory_11(E)  # Local alias for class E_11
        assert factory_11.has("B_11")
        assert factory_11.has("B")
        assert factory_11.has("C")
        assert factory_11.has("D")
        assert factory_11.has(ViewE)

        assert not factory_11.has(str)
        assert not factory_11.has(99)

    def test_register_good(self):
        factory_12 = ParallelFactory(A, View, suffix="_12")

        class B_12(factory_12(A)):
            """Intentionally "forgot" to provide base class."""

        assert not factory_12.has(B)
        factory_12.register(B_12)
        assert factory_12.has(B)
        assert factory_12(B) is B_12

    def test_build_with_mixin(self):
        factory_13 = ParallelFactory(A, View, suffix="_13")

        class Mixin_13:
            pass

        class D_13(Mixin_13, factory_13(C)):
            pass

        assert not factory_13.has(D)
        assert factory_13.has(C)
        assert not factory_13.has(B)
        gen_D_13 = factory_13(D)
        assert gen_D_13 is not D_13
        factory_13.register(D_13)
        my_D_13 = factory_13(D)
        assert my_D_13 is D_13
        assert Mixin_13 in my_D_13.__bases__
        assert Mixin not in my_D_13.__bases__

        gen_E_13 = factory_13(E)
        assert issubclass(gen_E_13, Mixin_13)
