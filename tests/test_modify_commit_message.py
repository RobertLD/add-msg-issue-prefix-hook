from add_msg_issue_prefix_hook.add_msg_issue_prefix import modify_commit_message
import re


def test_modify_commit_message():
    modified_message = modify_commit_message('tests commit message', 'my_prefix', re.compile('^'))
    assert modified_message == 'my_prefix tests commit message'

def test_modify_commit_message_strip():
    modified_message = modify_commit_message('tests commit message', ' my_prefix ', re.compile('^'))
    assert modified_message == 'my_prefix tests commit message'

def test_modify_commit_message_after():
    modified_message = modify_commit_message('tests commit message', 'my_prefix', re.compile('^tests'))
    assert modified_message == 'tests my_prefix commit message'
