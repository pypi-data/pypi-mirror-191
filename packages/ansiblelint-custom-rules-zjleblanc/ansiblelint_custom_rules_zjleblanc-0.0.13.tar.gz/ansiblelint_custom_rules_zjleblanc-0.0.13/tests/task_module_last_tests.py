from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner
from rules.task_module_last import TaskModuleLastRule

rule = TaskModuleLastRule()
collection = RulesCollection()
collection.register(rule)
test_playbooks_dir = f'tests/playbooks/{rule.id}'

def test_file_positive() -> None:
    """Positive test for task_module_last."""
    success = f'{test_playbooks_dir}/success.yml'
    good_runner = Runner(success, rules=collection)
    results = good_runner.run()
    assert [] == results

def test_file_negative() -> None:
    """Negative test for task_module_last."""
    fail = f'{test_playbooks_dir}/fail.yml'
    bad_runner = Runner(fail, rules=collection)
    results = bad_runner.run()
    for r in results:
        print(r)
    assert 2 == len(results)