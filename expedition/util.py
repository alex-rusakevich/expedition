def ask_for(label, default=None, options=[]):
    default_msg = f" (default is '{default}')" if default else ""
    cs_options = ""

    if len(options) >= 2:
        cs_options = (
            ", ".join([f"'{i}'" for i in options][:-1]) + f" and '{options[-1]}'"
        )
    else:
        cs_options = ", ".join([f"'{i}'" for i in options])

    options_msg = f" (options are {cs_options})" if options else ""
    input_msg = label + options_msg + default_msg + f": "
    input_msg = input_msg.replace(") (default", "; default")

    inp = input(input_msg).strip() or default

    if options and inp not in options:
        raise AssertionError(
            f"Unknown option: '{inp}', the available options are {cs_options}"
        )

    return inp
