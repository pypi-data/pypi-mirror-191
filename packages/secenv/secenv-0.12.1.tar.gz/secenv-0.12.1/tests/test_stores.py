import os
from .utils import with_tmp_conf, skip_unimplemented_test, write

import pytest
import secenv


@skip_unimplemented_test
@with_tmp_conf
def test_store_aws_secret_exists(config):
    ...


@skip_unimplemented_test
@with_tmp_conf
def test_store_aws_secrets_with_same_prefix(config):
    ...


@skip_unimplemented_test
@with_tmp_conf
def test_store_aws_secret_not_exists(config):
    ...


@skip_unimplemented_test
@with_tmp_conf
def test_store_bitwarden_secret_exists(config):
    ...


@skip_unimplemented_test
@with_tmp_conf
def test_store_bitwarden_secret_not_exists(config):
    ...


@with_tmp_conf
def test_store_env_secret_exists(config):
    config_as_py = {"stores": {"local": {"type": "env"}}}
    write(config, config_as_py)

    os.environ["VAR"] = "value"

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["local"], {"secret": "VAR"})
    assert secret == "value"


@with_tmp_conf
def test_store_env_secret_not_exists(config):
    config_as_py = {"stores": {"local": {"type": "env"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(stores["local"], {"secret": "NEVER_GONNA_GIVE_YOU_UP"})


@skip_unimplemented_test
@with_tmp_conf
def test_store_pass_secret_exists(config):
    ...


@skip_unimplemented_test
@with_tmp_conf
def test_store_pass_secret_not_exists(config):
    ...


@skip_unimplemented_test
@with_tmp_conf
def test_store_vault_secret_exists(config):
    ...


@skip_unimplemented_test
@with_tmp_conf
def test_store_vault_secret_not_exists(config):
    ...
