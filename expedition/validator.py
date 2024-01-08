import platform


def validate_manifest(manifest: dict):
    assert manifest["requirements"]["system"] in (
        "any",
        platform.system(),
    ), f'incompatible platform: \'{manifest["requirements"]["system"]}\''

    assert manifest["requirements"]["architecture"] in (
        "any",
        platform.architecture()[0],
    ), f'incompatible architecture: \'{manifest["requirements"]["architecture"]}\''

    compiler = manifest["requirements"]["compiler"]

    if compiler["name"] == "any" and compiler["version"] != "any":
        raise Exception(
            "if compiler name is set to be 'any', then it's version also must be 'any'"
        )
