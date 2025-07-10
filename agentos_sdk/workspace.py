import os


def check_workspace_dir(preset_dir: str = "artifacts"):
    """
    Ensure the ARTIFACTS_DIR environment variable is set and return its value.

    If ARTIFACTS_DIR is not set, it defaults to "artifacts".
    Returns the path as a string.
    """
    artifacts_dir = os.getenv("ARTIFACTS_DIR")
    if not artifacts_dir:
        artifacts_dir = preset_dir
        os.environ["ARTIFACTS_DIR"] = artifacts_dir
    return artifacts_dir
