class ValidationContext:
    def __init__(self, workflow_file, workflow):
        self.workflow_file = workflow_file
        self.workflow = workflow

    def _message(self, node, key, level, message):
        if node is None:
            print(f"?:?\t{level}\t{message}")
            return
        node_key_data = node.lc.data[key]
        node_key_line = node_key_data[0] + 1
        node_key_column = node_key_data[1]
        print(f"{node_key_line}:{node_key_column}\t{level}\t{message}")

    def info(self, node, key, message):
        """
        Reports an info message.

        :param node:
        :param key:
        :param message:
        :return:
        """
        self._message(node, key, "info", message)

    def warn(self, node, key, message):
        """
        Reports a warning.

        :param node:
        :param key:
        :param message:
        :return:
        """
        self._message(node, key, "warning", message)

    def error(self, node, key, message):
        """
        Reports an error.

        :param node:
        :param key:
        :param message:
        :return:
        """
        self._message(node, key, "error", message)


class ValidationRule:
    def validate(self, context: ValidationContext):
        raise NotImplementedError()
