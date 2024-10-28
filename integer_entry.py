import customtkinter


class IntegerEntry(customtkinter.CTkEntry):
    def __init__(self, master: customtkinter.CTkFrame, variable_name: str, default_value: str, max_length: int,
                 max_value: int = 9999999, min_value: int = 1):
        super().__init__(master)
        self.variable_name = variable_name
        self.max_length = max_length
        self.max_value = max_value
        self.min_value = min_value

        validation_command = (self.register(self.validate_entry), "%d", "%S", "%V", "%P")
        self.configure(validate="all", validatecommand=validation_command)

        self.insert(index=0, string=default_value)

    def validate_entry(self, action_code: str, attempted_text: str, callback_reason: str,
                       text_after_change: str) -> bool:
        if callback_reason == "focusout" or callback_reason == "focusin":
            if text_after_change == "":
                self.insert(index=0, string=self.min_value)
        if self.max_length:
            if len(text_after_change) > self.max_length:
                return False
        if action_code == "1":
            try:
                int(attempted_text)
            except ValueError:
                return False
        self.master.setvar(name=self.variable_name, value=text_after_change)
        return True
