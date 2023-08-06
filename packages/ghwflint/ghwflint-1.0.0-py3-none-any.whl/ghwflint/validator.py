import ruamel.yaml

from ghwflint.matchers import GitHubWorkflowNodeMatcher


class RuamelPatchIgnoreAliases(ruamel.yaml.representer.RoundTripRepresenter):
    """
    Don't use YAML aliases and anchors, at all.
    """

    def ignore_aliases(self, data):
        return True


class GitHubWorkflowValidator:
    yaml_parser = ruamel.yaml.YAML()
    yaml_parser.Representer = RuamelPatchIgnoreAliases
    root_matchers = GitHubWorkflowNodeMatcher.root_matchers()

    def _validate_node_dict(self, node, matchers):
        """
        Validates a parsed YAML node against the given matchers.
        :param node: node whose entries to validate
        :param matchers: list of GitHubWorkflowStructureMatcher objects available for the current node
        """
        if isinstance(node, dict):
            keys = node.keys()
        elif isinstance(node, list):
            keys = range(len(node))
        else:
            return

        for key in keys:
            matcher = None
            for child in matchers:
                if child.matches(key):
                    matcher = child
                    break
            if matcher is None:
                line_data = node.lc.data[key]
                line = line_data[0] + 1
                column = line_data[1]
                print(f"{line}:{column}\terror\tunexpected key '{key}'")
                continue
            value = node[key]
            if len(matcher.children) > 0:
                if isinstance(value, dict) or isinstance(value, list):
                    self._validate_node_dict(node[key], matcher.children)

    def validate(self, workflow_file):
        """
        Validates a workflow file against the structure defined in STRUCTURE.
        :param workflow_file: path to workflow file
        :return: True if the workflow file matches the structure, False otherwise
        """
        with open(workflow_file) as f:
            workflow = self.yaml_parser.load(f)
        self._validate_node_dict(workflow, self.root_matchers)


if __name__ == "__main__":
    validator = GitHubWorkflowValidator()
    validator.validate("../samples/workflow-invalid.yml")
