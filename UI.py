from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel


class UI(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.all_users_list_widget = QListWidget()
        self.layout.addWidget(QLabel("All Users:"))
        self.layout.addWidget(self.all_users_list_widget)

        self.active_users_list_widget = QListWidget()
        self.layout.addWidget(QLabel("Active Users:"))
        self.layout.addWidget(self.active_users_list_widget)

    # ------------------------------------------------------------------------------
    def update_active_users_list(self, active_users):
        self.active_users_list_widget.clear()
        for user in active_users:
            self.active_users_list_widget.addItem(user)

    # ------------------------------------------------------------------------------
    def update_all_users_list(self, all_users):
        self.all_users_list_widget.clear()
        for user in all_users:
            self.all_users_list_widget.addItem(user)

    # ------------------------------------------------------------------------------
    def remove_member_from_list(self, member_name):
        for index in range(self.all_users_list_widget.count()):
            item = self.all_users_list_widget.item(index)
            if item.text() == member_name:
                self.all_users_list_widget.takeItem(index)
                break

    # ------------------------------------------------------------------------------
    def update_member_name_in_list(self, old_name, new_name):
        for index in range(self.all_users_list_widget.count()):
            item = self.all_users_list_widget.item(index)
            if item.text() == old_name:
                item.setText(new_name)
                break

    # ------------------------------------------------------------------------------
    def update_member_status(self, member_name, has_access):
        for index in range(self.all_users_list_widget.count()):
            item = self.all_users_list_widget.item(index)
            if member_name in item.text():
                status_text = "Access: Granted" if has_access else "Access: Revoked"
                item.setText(f"{member_name} - {status_text}")
                break
