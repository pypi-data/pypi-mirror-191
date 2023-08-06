import subprocess


class Shell:
    @classmethod
    def convert_is_digit(cls, value):
        if value.isdigit() and not ',' in value and not '.' in value:
            return int(value)
        elif value.isdigit() and ',' in value or '.' in value:
            return float(value)

    @classmethod
    def execute(cls, command):
        try:
            output = subprocess.check_output(command, shell=True)
            output_as_string = output.decode("utf-8")
            normal_output = output_as_string.rstrip('\n')
            if '\n' in normal_output:
                values = normal_output.split('\n')
                normalized_list = []
                for value in values:
                    if value.isdigit():
                        normalized_list.append(cls.convert_is_digit(value))
                    else:
                        normalized_list.append(value.strip())
                return normalized_list
            elif normal_output.isdigit():
                return cls.convert_is_digit(normal_output)
            else:
                return normal_output
        except subprocess.CalledProcessError:
            raise ValueError("Could not execute command")
