from .utils import with_tmp_conf, write
import secenv


@with_tmp_conf
def test_format_dotenv(config):
    config_as_py = {"contexts": {"dev": {"vars": {"VAR": "value"}}}}
    write(config, config_as_py)

    secenv.load_config()
    ctx = secenv.gen_context("dev", [])
    output = secenv.context.format_output(ctx, "dotenv")
    assert output == "VAR='value'"


@with_tmp_conf
def test_format_shell(config):
    config_as_py = {"contexts": {"dev": {"vars": {"VAR": "value"}}}}
    write(config, config_as_py)

    secenv.load_config()
    ctx = secenv.gen_context("dev", [])
    output = secenv.context.format_output(ctx, "shell")
    assert output == "export VAR='value'"


@with_tmp_conf
def test_format_github_actions(config):
    config_as_py = {"contexts": {"dev": {"vars": {"VAR": "value"}}}}
    write(config, config_as_py)

    secenv.load_config()
    ctx = secenv.gen_context("dev", [])
    output = secenv.context.format_output(ctx, "github_actions")
    assert output == "echo 'VAR=value' >> $GITHUB_ENV\necho '::add-mask::value'"
