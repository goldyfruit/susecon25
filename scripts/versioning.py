def read_version(version_file):
    """
    Reads the version information from a specified version file.

    The function parses the file to extract `VERSION_MAJOR`, `VERSION_MINOR`,
    and `VERSION_BUILD` values. It assumes that these values are defined as
    key-value pairs (e.g., `VERSION_MAJOR = 1`) and stops reading once it
    encounters a line starting with `# END_VERSION_BLOCK`.

    Args:
        version_file (str): The path to the version file.

    Returns:
        tuple: A tuple containing three integers representing the major,
               minor, and build version numbers (VERSION_MAJOR, VERSION_MINOR,
               VERSION_BUILD).

    Raises:
        ValueError: If any of the version numbers are not properly formatted
                    as integers.
        FileNotFoundError: If the specified version file does not exist.
    """
    VERSION_MAJOR = 0
    VERSION_MINOR = 0
    VERSION_BUILD = 0

    with open(version_file, "r") as file:
        content = file.read()
    for l in content.split("\n"):
        l = l.strip()
        if l.startswith("# END_VERSION_BLOCK"):
            break
        if l.startswith("VERSION_MAJOR"):
            VERSION_MAJOR = int(l.split("=")[-1])
        elif l.startswith("VERSION_MINOR"):
            VERSION_MINOR = int(l.split("=")[-1])
        elif l.startswith("VERSION_BUILD"):
            VERSION_BUILD = int(l.split("=")[-1])
    return VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD


def update_version(part, version_file):
    """
    Updates the version number in the specified version file by incrementing the given version part.

    Parameters:
        part (str): The version part to increment. Must be one of:
                    - "major" to increment the major version and reset minor and build to 0.
                    - "minor" to increment the minor version and reset build to 0.
                    - "build" to increment the build version.
        version_file (str): Path to the file containing the version information.

    The version file should contain a version block formatted as:
        # START_VERSION_BLOCK
        VERSION_MAJOR = X
        VERSION_MINOR = Y
        VERSION_BUILD = Z
        # END_VERSION_BLOCK

    The function reads the current version, updates the specified part, and writes the new version
    back to the file while preserving any content outside the version block.

    Raises:
        ValueError: If `part` is not one of "major", "minor", or "build".
    """
    VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD = read_version(version_file)

    if part == "major":
        VERSION_MAJOR += 1
        VERSION_MINOR = 0
        VERSION_BUILD = 0
    elif part == "minor":
        VERSION_MINOR += 1
        VERSION_BUILD = 0
    elif part == "build":
        VERSION_BUILD += 1

    with open(version_file, "r") as file:
        contents = file.read().split("# END_VERSION_BLOCK")[-1]

    with open(version_file, "w") as file:
        file.write(
            f"""# START_VERSION_BLOCK
VERSION_MAJOR = {VERSION_MAJOR}
VERSION_MINOR = {VERSION_MINOR}
VERSION_BUILD = {VERSION_BUILD}
# END_VERSION_BLOCK"""
            + contents
        )
