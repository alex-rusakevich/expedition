import platform


def validate_manifest(manifest: dict):
    assert manifest["requirements"]["system"] in (
        "any",
        platform.system(),
    ), f'incompatible platform: \'{manifest["requirements"]["system"]}\''

    assert manifest["requirements"]["machine"] in (
        "any",
        platform.machine(),
    ), f'incompatible machine: \'{manifest["requirements"]["machine"]}\''

    compiler = manifest["requirements"]["compiler"]

    if compiler["name"] == "any" and compiler["version"] != "any":
        raise Exception(
            "if compiler name is set to be 'any', then it's version also must be 'any'"
        )
