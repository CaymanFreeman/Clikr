import customtkinter

class IntegerEntry(customtkinter.CTkEntry):
    def __init__(self, master, variable_name, default_value, max_length, max_value=9999999, min_value=1):
        super().__init__(master)
        self.variable_name = variable_name
        self.max_length = max_length
        self.max_value = max_value
        self.min_value = min_value

        validation_command = (self.register(self.validate_entry), "%d", "%S", "%V", "%P")
        self.configure(validate="all", validatecommand=validation_command)

        self.insert(0, default_value)

    def validate_entry(self, action_code, attempted_text, callback_reason, text_after_change) -> bool:
        if callback_reason == "focusout" or callback_reason == "focusin":
            if text_after_change == "":
                self.insert(0, self.min_value)
        if self.max_length:
            if len(text_after_change) > self.max_length:
                return False
        if action_code == "1":
            try:
                int(attempted_text)
            except ValueError:
                return False
        self.master.setvar(self.variable_name, text_after_change)
        return True