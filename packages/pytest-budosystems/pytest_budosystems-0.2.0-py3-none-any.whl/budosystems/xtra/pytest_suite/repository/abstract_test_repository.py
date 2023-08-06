#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#
"""Minimal test suite for all implementations of `Repository`."""

from typing import Any
from abc import ABC, abstractmethod
from collections.abc import Generator
# from uuid import UUID

import pytest
from pytest import fixture

from budosystems.models.core import Entity
from budosystems.storage.repository import (
    Repository, SaveOption,
    EntitySaveFailed, EntityNotFound, EntityAlreadyExists,
    EntityReadFailed, EntityDeleteFailed,
    RepositoryNotAccessible,  # RepositoryError
)

from .conftest import (
    OneIntFieldEntity as _1IFE,
    # OneRefFieldEntity as _1RFE,
    OneComplexFieldEntity as _1CFE,
)

# pylint: disable=too-many-public-methods
class AbstractTestRepository(ABC):
    """Standard test suite for implementations of `Repository`."""

    @abstractmethod
    @fixture(scope="class")
    def repo_class(self) -> type[Repository]:
        """Returns the class for the implementation of `Repository` being tested."""

    @fixture(scope="class")
    def repo_args(self) -> dict[str, Any]:
        """Returns implementation specific arguments to instantiate the implementation of
        `Repository` being tested."""
        return {}

    @fixture(scope="class")
    def repo_inaccessible(self, repo_class: type[Repository]) -> Repository:
        """
        Returns an instance of the implementation of `Repository` with improper connection.
        """
        pytest.skip(f"No 'inaccessible' implementation of {str(repo_class)}")

    @fixture(scope="class")
    def repository(self,
                   repo_class: type[Repository],
                   repo_args: dict[str, Any],
                   init_data: list[Entity]
                   ) -> Generator[Repository, None, None]:
        """
        Returns an instance of the implementation of `Repository` being tested.
        """
        repo = repo_class(**repo_args)
        self.populate_init_data(repo, init_data)
        yield repo
        del repo

    def populate_init_data(self, repo: Repository, init_data: list[Entity]) -> None:
        """
        Initializes the data stored in a repository.

        :param repo: An instance of the repository.
        :param init_data: The initial data used for testing.
        """
        for ent in init_data:
            repo.save(ent, save_option=SaveOption.create_only)

    def test_save_new_create_only(self, repository: Repository,
                                  one_int_ent: type[_1IFE]) -> None:
        """Test: Save new Entity with 'create_only' save option."""

        ns = "int_100"
        new_val = 100
        ent = one_int_ent(name=ns, slug=ns, i_var=new_val)
        repository.save(entity=ent, save_option=SaveOption.create_only)
        by_slug = repository.match(one_int_ent, {"slug": ns})
        assert len(by_slug) == 1
        assert by_slug[0] == ent
        assert by_slug[0] is not ent

    def test_save_existing_create_only(self, repository: Repository,
                                       one_int_ent: type[_1IFE]) -> None:
        """Test: Save existing Entity with 'create_only' save option."""

        ns = "int_1"
        new_val = 101
        with pytest.raises(EntitySaveFailed) as e:
            ent = one_int_ent(name=ns, slug=ns, i_var=new_val)
            repository.save(entity=ent, save_option=SaveOption.create_only)
        assert e.type == EntitySaveFailed
        assert isinstance(e.value.reason, EntityAlreadyExists)
        by_name = repository.match(one_int_ent, {"name": ns})
        assert len(by_name) == 1
        assert by_name[0].i_var == 1

    def test_save_new_create_or_update(self, repository: Repository,
                                       one_int_ent: type[_1IFE]) -> None:
        """Test: Save new Entity with 'create_or_update' save option."""

        ns = "int_102"
        new_val = 102
        ent = one_int_ent(name=ns, slug=ns, i_var=new_val)
        repository.save(entity=ent, save_option=SaveOption.create_or_update)
        by_name = repository.match(one_int_ent, {"name": ns})
        by_value = repository.match(one_int_ent, {"i_var": new_val})
        assert len(by_name) == 1
        assert len(by_value) == 1
        assert by_name == by_value

    def test_save_existing_create_or_update(self, repository: Repository,
                                            one_int_ent: type[_1IFE]) -> None:
        """Test: Save existing Entity with 'create_or_update' save option."""

        ns = "int_3"
        new_val = 103
        ent = one_int_ent(name=ns, slug=ns, i_var=new_val)
        repository.save(entity=ent, save_option=SaveOption.create_or_update)
        by_name = repository.match(one_int_ent, {"name": ns})
        by_value = repository.match(one_int_ent, {"i_var": new_val})
        assert len(by_name) == 1
        assert len(by_value) == 1
        assert by_name == by_value
        assert not repository.match(one_int_ent, {"i_var": 3})

    def test_save_new_update_only(self, repository: Repository,
                                  one_int_ent: type[_1IFE]) -> None:
        """Test: Save new Entity with 'update_only' save option."""

        ns = "int_104"
        new_val = 104
        with pytest.raises(EntitySaveFailed) as e:
            ent = one_int_ent(name=ns, slug=ns, i_var=new_val)
            repository.save(entity=ent, save_option=SaveOption.update_only)
        assert e.type == EntitySaveFailed
        assert isinstance(e.value.reason, EntityNotFound)
        assert len(repository.match(one_int_ent, {"name": ns})) == 0

    def test_save_existing_update_only(self, repository: Repository,
                                       one_int_ent: type[_1IFE]) -> None:
        """Test: Save existing Entity with 'update_only' save option."""

        ns = "int_5"
        new_val = 105
        old_val = 3
        ent = one_int_ent(name=ns, slug=ns, i_var=new_val)
        repository.save(entity=ent, save_option=SaveOption.update_only)
        by_name = repository.match(one_int_ent, {"name": ns})
        by_value = repository.match(one_int_ent, {"i_var": new_val})
        assert len(by_name) == 1
        assert len(by_value) == 1
        assert by_name == by_value
        assert not repository.match(one_int_ent, {"i_var": old_val})

    def test_save_repo_not_accessible(self, repo_inaccessible: Repository,
                                      one_int_ent: type[_1IFE]) -> None:
        """Test: Save while repository is not accessible."""
        ns = "int_106"
        val = 106
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        with pytest.raises(EntitySaveFailed) as e:
            repo_inaccessible.save(entity=ent)
        assert e.type == EntitySaveFailed
        assert isinstance(e.value.reason, RepositoryNotAccessible)

    def test_load_repo_has_type_has_id(self, repository: Repository,
                                       one_int_ent: type[_1IFE]) -> None:
        """Test: Load from repository where type exists and id matches."""
        ns = "int_6"
        val = 6
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        db_ent = repository.load(entity_type=one_int_ent, entity_id=ent.entity_id)
        assert db_ent is not None
        assert db_ent == ent

    def test_load_repo_has_type_not_has_id(self, repository: Repository,
                                           one_int_ent: type[_1IFE]) -> None:
        """Test: Load from repository where type exists and id does not match."""
        ns = "int_107"
        val = 7
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        with pytest.raises(EntityReadFailed) as e:
            _db_ent = repository.load(entity_type=one_int_ent, entity_id=ent.entity_id)
        assert e.type == EntityReadFailed
        assert isinstance(e.value.reason, EntityNotFound)

    def test_load_repo_not_has_type_has_id(self, repository: Repository,
                                           one_int_ent: type[_1IFE],
                                           one_complex_ent: type[_1CFE]) -> None:
        """Test: Load from repository where type does not exist and id matches."""
        ns = "int_8"
        val = 8
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        with pytest.raises(EntityReadFailed) as e:
            _db_ent = repository.load(entity_type=one_complex_ent, entity_id=ent.entity_id)
        assert e.type == EntityReadFailed
        assert isinstance(e.value.reason, TypeError)

    def test_load_repo_not_has_type_not_has_id(self, repository: Repository,
                                               one_complex_ent: type[_1CFE]) -> None:
        """Test: Load from repository where type does not exist and id does not match."""
        ns = "c_109"
        val = 109j
        ent = one_complex_ent(name=ns, slug=ns, c_var=val)
        with pytest.raises(EntityReadFailed) as e:
            _db_ent = repository.load(entity_type=one_complex_ent, entity_id=ent.entity_id)
        assert e.type == EntityReadFailed
        assert isinstance(e.value.reason, TypeError)

    def test_load_repo_not_accessible(self, repo_inaccessible: Repository,
                                      one_int_ent: type[_1IFE]) -> None:
        """Test: Load while repository is not accessible."""
        ns = "int_10"
        val = 10
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        with pytest.raises(EntityReadFailed) as e:
            _db_ent = repo_inaccessible.load(entity_type=one_int_ent, entity_id=ent.entity_id)
        assert e.type == EntityReadFailed
        assert isinstance(e.value.reason, RepositoryNotAccessible)

    def test_delete_repo_has_type_has_id_must_exist_false(self, repository: Repository,
                                                          one_int_ent: type[_1IFE]) -> None:
        """Test: Delete from repository where type exists and id matches."""
        ns = "int_11"
        val = 11
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        repository.delete(entity_type=one_int_ent, entity_id=ent.entity_id, must_exist=False)
        by_name = repository.match(one_int_ent, {"name": ns})
        assert len(by_name) == 0

    def test_delete_repo_has_type_has_id_must_exist_true(self, repository: Repository,
                                                         one_int_ent: type[_1IFE]) -> None:
        """Test: Delete from repository where type exists and id matches."""
        ns = "int_12"
        val = 12
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        repository.delete(entity_type=one_int_ent, entity_id=ent.entity_id, must_exist=True)
        by_name = repository.match(one_int_ent, {"name": ns})
        assert len(by_name) == 0

    def test_delete_repo_has_type_not_has_id_must_exist_false(self, repository: Repository,
                                                              one_int_ent: type[_1IFE]) -> None:
        """Test: Delete from repository where type exists and id does not match."""
        ns = "int_113"
        val = 113
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        repository.delete(entity_type=one_int_ent, entity_id=ent.entity_id, must_exist=False)
        by_name = repository.match(one_int_ent, {"name": ns})
        assert len(by_name) == 0

    def test_delete_repo_has_type_not_has_id_must_exist_true(self, repository: Repository,
                                                             one_int_ent: type[_1IFE]) -> None:
        """Test: Delete from repository where type exists and id does not match."""
        ns = "int_114"
        val = 114
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        with pytest.raises(EntityDeleteFailed) as e:
            repository.delete(entity_type=one_int_ent, entity_id=ent.entity_id, must_exist=True)
        assert e.type == EntityDeleteFailed
        assert isinstance(e.value.reason, EntityNotFound)

    def test_delete_repo_not_has_type_has_id_must_exist_false(self, repository: Repository,
                                                              one_int_ent: type[_1IFE],
                                                              one_complex_ent: type[_1CFE]) -> None:
        """Test: Delete from repository where type does not exist and id matches."""
        ns = "int_15"
        val = 15
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        repository.delete(entity_type=one_complex_ent, entity_id=ent.entity_id, must_exist=False)
        by_name = repository.match(one_int_ent, {"name": ns})
        assert len(by_name) == 1, "Entity deleted when it should not have been deleted."

    def test_delete_repo_not_has_type_has_id_must_exist_true(self, repository: Repository,
                                                             one_int_ent: type[_1IFE],
                                                             one_complex_ent: type[_1CFE]) -> None:
        """Test: Delete from repository where type does not exist and id matches."""
        ns = "int_16"
        val = 16
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        with pytest.raises(EntityDeleteFailed) as e:
            repository.delete(entity_type=one_complex_ent, entity_id=ent.entity_id, must_exist=True)
        assert e.type == EntityDeleteFailed
        assert isinstance(e.value.reason, TypeError)

    def test_delete_repo_not_has_type_not_has_id_must_exist_false(
            self, repository: Repository,
            one_complex_ent: type[_1CFE]) -> None:
        """Test: Delete from repository where type does not exist and id does not match."""
        ns = "c_17"
        val = 17j
        ent = one_complex_ent(name=ns, slug=ns, c_var=val)
        repository.delete(entity_type=one_complex_ent, entity_id=ent.entity_id, must_exist=False)
        by_name = repository.match(one_complex_ent, {"name": ns})
        assert len(by_name) == 0

    def test_delete_repo_not_has_type_not_has_id_must_exist_true(
            self, repository: Repository,
            one_complex_ent: type[_1CFE]) -> None:
        """Test: Delete from repository where type does not exist and id does not match."""
        ns = "c_18"
        val = 18j
        ent = one_complex_ent(name=ns, slug=ns, c_var=val)
        with pytest.raises(EntityDeleteFailed) as e:
            repository.delete(entity_type=one_complex_ent, entity_id=ent.entity_id, must_exist=True)
        assert e.type == EntityDeleteFailed
        assert isinstance(e.value.reason, TypeError)

    def test_delete_repo_not_accessible(self, repo_inaccessible: Repository,
                                        one_int_ent: type[_1IFE]) -> None:
        """Test: Delete while repository is not accessible."""
        ns = "int_19"
        val = 19
        ent = one_int_ent(name=ns, slug=ns, i_var=val)
        with pytest.raises(EntityDeleteFailed) as e:
            repo_inaccessible.delete(entity_type=one_int_ent, entity_id=ent.entity_id)
        assert e.type == EntityDeleteFailed
        assert isinstance(e.value.reason, RepositoryNotAccessible)
