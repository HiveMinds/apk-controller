"""Functions to assist a script file for the DAVx5 app.."""
from pathlib import Path

from typeguard import typechecked

from src.appcommander.run_bash_code import run_bash_command


@typechecked
def install_self_signed_root_ca_on_android(
    app_version_dir: str,
) -> None:
    """Verifies the/a self-signed root ca file exists in the root dir of this
    repository.

    Then calls the bash function that installs it. Then returns the
    control back to the script flow for DAVx5 installation.
    """
    bash_script_path = f"{app_version_dir}bash_scripts/export_root_ca2.sh"
    ca_local_filepath: str = "ca.crt"
    # Verify the file exists.
    for filepath in [bash_script_path, ca_local_filepath]:
        if not Path(filepath).is_file():
            raise Exception(f"Error, filepath:{filepath} does not exist.")

    # TODO: execute commands individually with intermediate Python
    # verification, instead of in Bash script.

    command = (
        f"bash -c 'source {bash_script_path} && install_self_signe"
        + f'd_root_ca_on_android "{ca_local_filepath}"\''
    )

    print(f"command={command}")
    run_bash_command(
        await_compilation=True, bash_command=command, verbose=False
    )
