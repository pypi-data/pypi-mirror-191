import pytest

from lnhub_rest._add_storage import validate_root_arg
from lnhub_rest._init_instance import (
    init_instance,
    validate_db_arg,
    validate_schema_arg,
    validate_storage_arg,
)


def test_validate_schema_arg():
    # test typos in schema string
    assert "bionty,swarm" == validate_schema_arg("bionty ,swarm")
    # test errors during validation
    with pytest.raises(ValueError):
        validate_schema_arg("xyz12")


def test_validate_storage_arg():
    # test typos in schema string
    validate_storage_arg("test/")
    # test errors during validation
    validate_storage_arg("gs://test")
    # test errors for hub-only instances
    validate_root_arg("gs://test")
    with pytest.raises(ValueError):
        validate_root_arg("23jf://test")


def test_validate_db_arg():
    postgresdsn = "postgresql://postgres:pwd@0.0.0.0:5432/pgtest"
    validate_db_arg(postgresdsn)
    mysqldsn = "mssql://postgres:pwd@0.0.0.0:5432/pgtest"
    with pytest.raises(ValueError):
        validate_db_arg(mysqldsn)


def test_db_unique_error():
    # postgres
    result = init_instance(
        owner="testuser2",
        name="retro",
        storage="s3://lndb-setup-ci",
        schema="retro,bionty",
        db="postgresql://batman:robin@35.222.187.204:5432/retro",
        _email="testuser2@lamin.ai",
        _password="goeoNJKE61ygbz1vhaCVynGERaRrlviPBVQsjkhz",
    )

    # lndb relies on the following three
    assert result != "instance-exists-already"
    assert result is not None
    assert isinstance(result, str)

    # sqlite
    # this fails because there is already an sqlite with the same name in that bucket
    # hence, the sqlite file would clash
    result = init_instance(
        owner="testuser2",
        name="lamindb-ci",
        storage="s3://lamindb-ci",
        _email="testuser2@lamin.ai",
        _password="goeoNJKE61ygbz1vhaCVynGERaRrlviPBVQsjkhz",
    )
    assert result != "instance-exists-already"
    assert result is not None
    assert isinstance(result, str)
