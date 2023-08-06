import subprocess


class ExecuteException(Exception):
    pass


class Shell:
    @staticmethod
    def convert_is_digit(value):
        if value.isdigit() and not ',' in value and not '.' in value:
            return int(value)
        elif value.isdigit() and ',' in value or '.' in value:
            return float(value)

    def execute_with_output(self, command):
        output = subprocess.check_output(command, shell=True)
        output_as_string = output.decode("utf-8")
        normal_output = output_as_string.rstrip('\n')
        if '\n' in normal_output:
            values = normal_output.split('\n')
            normalized_list = []
            for value in values:
                if value.isdigit():
                    normalized_list.append(self.convert_is_digit(value))
                else:
                    normalized_list.append(value.strip())
            return normalized_list
        elif normal_output.isdigit():
            return self.convert_is_digit(normal_output)
        else:
            return normal_output

    def execute(self, command, output=True):
        try:
            if output:
                return self.execute_with_output(command)
            else:
                return subprocess.call(command, shell=True)
        except subprocess.CalledProcessError as e:
            raise ExecuteException(f"Return code: {e.returncode}. Not execute command: {e.cmd}")
