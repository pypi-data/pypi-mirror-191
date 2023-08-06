from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner
from rules.when_follows_name import WhenFollowsNameRule

rule = WhenFollowsNameRule()
collection = RulesCollection()
collection.register(rule)
test_playbooks_dir = f'tests/playbooks/{rule.id}'

def test_file_positive() -> None:
    """Positive test for when_follows_name."""
    success = f'{test_playbooks_dir}/success.yml'
    good_runner = Runner(success, rules=collection)
    assert [] == good_runner.run()

def test_file_negative() -> None:
    """Negative test for when_follows_name."""
    success = f'{test_playbooks_dir}/fail.yml'
    bad_runner = Runner(success, rules=collection)
    errors = bad_runner.run()
    assert 3 == len(errors)