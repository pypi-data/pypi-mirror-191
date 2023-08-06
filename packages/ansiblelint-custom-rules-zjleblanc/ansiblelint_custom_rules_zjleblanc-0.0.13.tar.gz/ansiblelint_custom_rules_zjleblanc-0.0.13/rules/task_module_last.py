"""Lint rule class to test if module specified last in task
"""
import typing
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from typing import Optional
    from ansiblelint.file_utils import Lintable

BLOCK_CONSTRUCT = 'block/always/rescue'

def handle_block_construct(key):
    if key in BLOCK_CONSTRUCT.split('/'):
        return False
    else:
        return f'One of {BLOCK_CONSTRUCT} should be specified last'

class TaskModuleLastRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if any tasks don't specify module last
    """
    id: str = 'task-module-last'
    shortdesc: str = 'module should always be specified last'
    description: str = """Tasks can have many keys set.
    For readability and clarity of indentation, specify the module last.
    """
    severity: str = 'MEDIUM'
    tags: typing.List[str] = [id, 'readability', 'formatting']
    needs_raw_task = True

    def matchtask(self, task: typing.Dict[str, typing.Any],
                  file: 'Optional[Lintable]' = None
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        last_key = None
        for key in reversed(task['__raw_task__'].keys()):
            if not key.startswith('__'):
                last_key = key
                break

        last_key_short_name = last_key.split('.')[-1]
        module = task['action']['__ansible_module__']
        module_short_name = module.split('.')[-1]

        if module == BLOCK_CONSTRUCT:
            return handle_block_construct(last_key_short_name)
        if last_key_short_name != module_short_name:
            return f'{module} should be specified last'
        return False
