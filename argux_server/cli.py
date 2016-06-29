"""CLI questions (for argux-server_genconfig script)."""

__INPUT_FUNC = input


def yesno_question(question, default=None):
    """Prints a yes/no question

    It can be answered with 'y','Y','n','N'

    If default is specified, an empty input is replaced with the default.
    """

    answer = option_question(
        question,
        options=['y', 'n'],
        default=default)

    if answer == 'y':
        return True

    return False


def option_question(question, options, default=None, print_options=True):
    """Prints a question with predefined options

    If default is specified, an empty input is replaced with the default value.
    """

    _options = list(options)

    # Format the question
    if print_options:
        question = question + ' ' + str(options)

    if default is not None:
        question = question + ' (Default: ' + default + ') '
        # Default must be one of the existing answers.
        if default in options:
            _options.append('')
        else:
            raise ValueError(
                'Default must be one of ' +
                str(options))

    answer = __INPUT_FUNC(question)
    while answer not in _options:
        answer = __INPUT_FUNC(
            'Answer with one of these options: ' +
            str(options))

    if answer == '':
        answer = default

    return answer
