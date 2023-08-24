#!/usr/bin/env python3

import argparse
import re
import subprocess


def get_ticket_id_from_branch_name(pattern: re.Pattern, branch: str) -> str:
    """
    Extracts the issue identifier from the branch name.

    Args
    ----
        pattern (re.Pattern): pattern to match the issue identifier
        branch (str): branch name

    Returns
    -------
        str or None: issue identifier if found, None otherwise

    """
    matches = re.findall(pattern, branch)
    if len(matches) > 0:
        return matches[0]


def modify_commit_message(content: str, issue_number: str,
                          pattern: re.Pattern) -> str:
    """
    Inserts the issue number into the commit message after the specified
    regex pattern.

    Args
    ----
        content (str): commit message contents
        issue_number (str): issue identifier to insert
        pattern (re.Pattern): pattern after which to insert the issue number

    Returns
    -------
        str: modified commit message

    """
    if match := re.search(pattern, content):
        return " ".join(
            [
                match.group().strip(),
                issue_number.strip(),
                content[match.end():].strip(),
            ]
        )
    return " ".join([issue_number.strip(), content])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    parser.add_argument(
        "-t",
        "--template",
        default="[{}]",
        help="Template to render ticket id into",
    )
    parser.add_argument(
        "-i",
        "--insert-after",
        default="^",
        help="Regex pattern describing the text after which to insert the issue key.",  # noqa: E501
    )
    parser.add_argument(
        "-p",
        "--pattern",
        default="[a-zA-Z0-9]{1,10}-[0-9]{1,5}",
        help="Regex pattern describing the issue key.",
    )
    parser.add_argument(
        "-d",
        "--default",
        help="Default prefix if no issue is found",
    )

    args = parser.parse_args()
    commit_msg_filepath = args.commit_msg_filepath
    template = args.template
    default = args.default
    insert_after = re.compile(args.insert_after)
    pattern = re.compile(args.insert_after)

    branch = ""
    try:
        branch = subprocess.check_output(
            ["git", "symbolic-ref", "--short", "HEAD"], universal_newlines=True
        ).strip()
    except Exception as e:
        print(e)

   if result := get_ticket_id_from_branch_name(pattern, branch):
        issue_number = result.upper()
    else:
        issue_number = ""
    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        content_subject = content.split("\n", maxsplit=1)[0].strip()
        f.seek(0, 0)
        if issue_number and issue_number not in content_subject:
            prefix = template.format(issue_number)
            new_msg = modify_commit_message(content, prefix, insert_after)
            f.write(new_msg)
        elif default:
            new_msg = modify_commit_message(content, default, insert_after)
            f.write(new_msg)
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
