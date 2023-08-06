"""Lint rule class to test if when follows name
"""
import typing
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from typing import Optional
    from ansiblelint.file_utils import Lintable

class WhenFollowsNameRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if any tasks use when not following name
    """
    id: str = 'when-follows-name'
    shortdesc: str = 'when conditionals should follow directly after name'
    description: str = """when conditionals should follow directly after name
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
        
        prev_key = None
        for key in task['__raw_task__']:
            if key == 'when' and prev_key != 'name':
                return f'Use of when not following name'
            prev_key = key

        return False
