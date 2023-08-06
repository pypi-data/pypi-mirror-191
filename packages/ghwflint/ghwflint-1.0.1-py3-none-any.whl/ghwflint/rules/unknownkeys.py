from ghwflint.matchers import GitHubWorkflowNodeMatcher
from ghwflint.rules.validator import ValidationRule, ValidationContext


class ValidationRuleUnknownKeys(ValidationRule):
    def _validate(self, context, node, available_matchers):
        """
        Validates a parsed YAML node against the given matchers.
        :param context:
        :param node: node whose entries to validate
        :param available_matchers: list of GitHubWorkflowStructureMatcher objects available for the current node
        """
        if isinstance(node, dict):
            keys = node.keys()
        elif isinstance(node, list):
            keys = range(len(node))
        else:
            return

        for key in keys:
            matchers = []
            for matcher in available_matchers:
                if matcher.matches(key):
                    matchers.append(matcher)
                    break
            if len(matchers) == 0:
                context.error(node, key, f"unexpected key '{key}'")
                continue
            value = node[key]
            matchers_children = []
            for matcher in matchers:
                matchers_children.extend(matcher.children)
            if len(matchers_children) > 0:
                if isinstance(value, dict) or isinstance(value, list):
                    self._validate(context, node[key], matchers_children)

    def validate(self, context: ValidationContext):
        """
        Validates a workflow file against the structure defined in GitHubStaticDefinitions.
        :param context:
        """
        root_matchers = GitHubWorkflowNodeMatcher.root_matchers()
        self._validate(context, context.workflow, root_matchers)
