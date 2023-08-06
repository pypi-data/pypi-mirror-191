import ruamel.yaml

from ghwflint.rules.jobneeds import ValidationRuleJobNeeds
from ghwflint.rules.unknownkeys import ValidationRuleUnknownKeys
from ghwflint.rules.validator import ValidationContext


class RuamelPatchIgnoreAliases(ruamel.yaml.representer.RoundTripRepresenter):
    """
    Don't use YAML aliases and anchors, at all.
    """

    def ignore_aliases(self, data):
        return True


class Validator:
    yaml_parser = ruamel.yaml.YAML()
    yaml_parser.Representer = RuamelPatchIgnoreAliases
    validators = [
        ValidationRuleUnknownKeys(),
        ValidationRuleJobNeeds()
    ]

    def validate(self, workflow_file):
        """
        :param workflow_file: path to workflow file
        """
        with open(workflow_file) as f:
            workflow = self.yaml_parser.load(f)
        context = ValidationContext(workflow_file, workflow)
        for validator in self.validators:
            try:
                validator.validate(context)
            except Exception as e:
                context.warn(None, None, f"exception in {validator.__class__.__name__}: {e}")


if __name__ == "__main__":
    sample_validator = Validator()
    sample_validator.validate("../samples/workflow-unknownkeys.yml")
    sample_validator.validate("../samples/workflow-jobneeds.yml")
