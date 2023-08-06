from ghwflint.definitions import GitHubStaticDefinitions


class GitHubWorkflowNodeMatcher:
    """
    Represents a section of a documented GitHub workflow YAML path pattern.

    For example the paths pattern `jobs.<job_id>.steps[*].id` and `jobs.<job_id>.steps[*].if` together would be represented by a tree of matchers like so:

    ```
    matcher(key="jobs", children={
           matcher(key="*", children={
                 matcher(key="steps", children={
                        matcher(key="*", children={
                                  matcher(pattern="id"),
                                  matcher(pattern="if")
                        })
                    })
            })
    })
    ```

    Each matcher should contain all children defined by GitHub's documentation.
    """

    def __init__(self, key):
        self.key = key
        self.children = []

    def matches(self, key):
        """
        Returns True if the given key matches the node key.
        """
        if self.key == "*":
            return True
        return self.key == key

    def __repr__(self):
        if len(self.children) == 0:
            return f"matcher(key='{self.key}')"
        # map children to repr, then join with ",\n", then indent each line
        children_reps = ",\n".join(map(repr, self.children))
        children = "\n".join(map(lambda line: f"  {line}", children_reps.splitlines()))
        return f"matcher(pattern='{self.key}', children=[\n{children}\n])"

    @classmethod
    def root_matchers(cls):
        """
        Builds a list of root-level GitHubWorkflowStructureMatcher objects based on static definitions.
        """
        root_matchers = []
        for path in GitHubStaticDefinitions.get_workflow_yaml_paths():
            segments = path.split(".")
            matchers = root_matchers
            for segment in segments:
                segment_matcher = None
                for child in matchers:
                    if child.key == segment:
                        segment_matcher = child
                        break
                if segment_matcher is None:
                    matcher = GitHubWorkflowNodeMatcher(key=segment)
                    matchers.append(matcher)
                    segment_matcher = matcher
                matchers = segment_matcher.children
        return root_matchers
