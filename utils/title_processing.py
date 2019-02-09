import getpass


class TitleProcessing:
    def __init__(self, process_name, window_title):
        self.process_name = process_name
        self.window_title = window_title

    def get_sublime_path(self):
        s = self.window_title
        end_ind = s.find(" - Sublime Text")
        if end_ind == -1:
            return s
        s = s[:end_ind]  # Removes Sublime Text
        if s.endswith(')'):
            i = len(s) - 2
            while (i > 0 and not (s[i] == '(' and s[i - 1] == ' ')):
                i -= 1
            if i != 0:
                s = s[:i]  # Removes open project
        s = s.rstrip()  # Removes trailing white spaces
        if s.endswith('•'):  # Didn't save the file
            s = s[:-1]
        s = s.rstrip()  # Removes trailing white spaces
        if s.startswith('~'):
            s = "/home/" + getpass.getuser() + s[1:]
        return s

    def get_browser_title(self):
        end_text = ""
        if self.window_title.endswith(" - Chromium"):
            end_text = " - Chromium"
        elif self.window_title.endswith(" - Google Chrome"):
            end_text = " - Google Chrome"
        elif self.window_title.endswith(" - Mozilla Firefox"):
            end_text = " - Mozilla Firefox"
        else:
            return self.window_title
        s = self.window_title
        end_ind = s.find(end_text)
        if end_ind == -1:
            return s
        s = s[:end_ind]  # Remove end_text
        s = s.rstrip()  # Removes trailing white spaces
        return s

    def get_path(self):
        if self.process_name in ["sublime_text", "subl"]:
            return self.get_sublime_path()
        elif self.process_name == "BROWSER":
            return self.get_browser_title()
        else:
            return self.window_title
