import os


class GitHubStaticDefinitions:
    """
    Based on all headers in https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
    Retrieved with `$$("h3 code").map(function(ele) {return ele.textContent}).join("\n")` on 2023-02-11
    """
    _EVENT_NAMES = os.path.join(os.path.dirname(__file__), "definitions/gh_event_names.txt")

    """
    Based on all headers in https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#about-yaml-syntax-for-workflows
    Retrieved with `$$("h2 code, h3 code").map(function(ele) {return ele.textContent}).join("\n")` on 2023-02-11
    """
    _WORKFLOW_YAML_PATHS = os.path.join(os.path.dirname(__file__), "definitions/gh_workflow_paths.txt")
    """
    Additional custom definitions not documented in the same manner or on the same page as the above.
    """
    _WORKFLOW_YAML_PATHS_CUSTOM = os.path.join(os.path.dirname(__file__), "definitions/gh_workflow_paths_custom.txt")

    @classmethod
    def _get_event_names(cls):
        with open(cls._EVENT_NAMES) as f:
            lines = f.read().splitlines()
            # remove empty lines
            lines = filter(lambda s: s != "", lines)
            # remove whitespace
            lines = map(lambda s: s.strip(), lines)
            return set(lines)

    @classmethod
    def _expand_workflow_yaml_path(cls, path):
        """
        Expands the workflow YAML paths to a list of all possible paths.
        For example, `on.<pull_request|pull_request_target>.<branches|branches-ignore>` is expanded to
        - `on.pull_request.branches`
        - `on.pull_request.branches-ignore`
        - `on.pull_request_target.branches`
        - `on.pull_request_target.branches-ignore`
        """
        path_segments = path.split(".")
        paths_expanded = [
            []
        ]
        for segment in path_segments:
            # single exact match
            if "<" not in segment and ">" not in segment:
                for path_expanded in paths_expanded:
                    path_expanded.append(segment)
                continue
            segment = segment[1:-1]
            # multiple exact matches
            if "|" in segment:
                segment_options = segment.split("|")
                paths_expanded_new = [
                ]
                for path_expanded in paths_expanded:
                    for segment_option in segment_options:
                        path_expanded_new = []
                        path_expanded_new.extend(path_expanded)
                        path_expanded_new.append(segment_option)
                        paths_expanded_new.append(path_expanded_new)
                paths_expanded = paths_expanded_new
                continue
            # special case of event_name remapped to all possible event names
            if segment == "event_name":
                paths_expanded_new = [
                ]
                for path_expanded in paths_expanded:
                    for event_name in cls._get_event_names():
                        path_expanded_new = []
                        path_expanded_new.extend(path_expanded)
                        path_expanded_new.append(event_name)
                        paths_expanded_new.append(path_expanded_new)
                paths_expanded = paths_expanded_new
                continue
            # wildcards
            for path_expanded in paths_expanded:
                path_expanded.append("*")
            continue
        # map segments back to string paths
        return map(lambda element: ".".join(element), paths_expanded)

    @classmethod
    def get_workflow_yaml_paths(cls):
        lines_expanded = []
        for file_path in [cls._WORKFLOW_YAML_PATHS, cls._WORKFLOW_YAML_PATHS_CUSTOM]:
            with open(file_path) as f:
                lines = f.read().splitlines()
                # remove empty lines
                lines = filter(lambda s: s != "", lines)
                # remove whitespace
                lines = map(lambda s: s.strip(), lines)
                # rewrite `[*]` to `.*`
                lines = map(lambda s: s.replace("[*]", ".*"), lines)
                # expand each line to all possible paths
                for line in lines:
                    lines_expanded.extend(cls._expand_workflow_yaml_path(line))
        return set(lines_expanded)


if __name__ == "__main__":
    print(GitHubStaticDefinitions.get_workflow_yaml_paths())
