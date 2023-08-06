import random
from . import errors

class Hasher():
    def __init__(self):
        pass

    def get_tcoi(self, text: str):
        text = text.strip()

        if text:
            is_found = [False, '']

            # Do we even have a hashfile?
            try:
                with open('.hashfile') as file:
                    file.close()

            except FileNotFoundError:
                with open('.hashfile', 'x') as file:
                    file.close()

            # Is the TCOI already there?
            with open('.hashfile') as file:
                lines = file.readlines()

                for line in lines:
                    line_list = line.split(': ')

                    found_text_list = line_list[:-1]

                    if len(found_text_list) == 1:
                        found_text = found_text_list[0]

                        if text == found_text:
                            is_found = [True, line.strip()]

                    elif len(found_text_list) > 1:
                        found_text = ": ".join(found_text_list)

                        if text == found_text:
                            is_found = [True, line.strip()]

                file.close()

            if is_found[0] == True:
                line = is_found[1]

                line_list = line.split(': ')

                found_text_list = line_list[:-1]
                found_tcoi = line_list[-1]

                if len(found_text_list) == 1:
                    found_text = found_text_list[0]

                    result = {
                        'text': found_text,
                        'tcoi': found_tcoi
                    }

                    return result

                elif len(found_text_list) > 1:
                    found_text = ": ".join(found_text_list)

                    result = {
                        'text': found_text,
                        'tcoi': found_tcoi
                    }

                    return result

            else:
                text_tcoi = 'Q-'
                letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890."

                for _ in range(28):
                    next_code = random.choice(letters)
                    text_tcoi += next_code

                result = f"{text}: {text_tcoi}"

                with open('.hashfile', 'a') as file:
                    file.write(f"{result}\n")

                result = {
                    'text': text,
                    'tcoi': text_tcoi
                }

                return result

        else:
            raise errors.EmptyText("CAN NOT GET TCOI!")

    def get_all_codes(self):
        with open('.hashfile') as file:
            lines = file.readlines()
            results = []

            for line in lines:
                line_list = line.split(': ')

                found_text_list = line_list[:-1]
                found_tcoi = line_list[-1]

                if len(found_text_list) == 1:
                    found_text = found_text_list[0]

                    result = {
                        'text': found_text,
                        'tcoi': found_tcoi
                    }

                    results.append(result)

                elif len(found_text_list) > 1:
                    found_text = ": ".join(found_text_list)

                    result = {
                        'text': found_text,
                        'tcoi': found_tcoi
                    }

                    results.append(result)

            file.close()

        return results

    def clear_hashfile(self):
        with open('.hashfile', 'w') as file:
            file.truncate(0)
            file.close()

    def get_tcois(self, texts: list):
        results = []
        
        for text in texts:
            result = self.get_tcoi(text)
            results.append(result)
        
        return results
