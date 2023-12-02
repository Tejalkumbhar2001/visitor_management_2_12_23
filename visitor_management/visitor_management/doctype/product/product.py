# Copyright (c) 2023, Tejal KUmbhar and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Product(Document):

    def validate(self):
        pass
        # # Implement a custom logic to filter users based on their associated company
        # allocated_to = []
        # for user in self.assigned_to:
        #     if user.company == self.company:
        #         assigned_to.append(user.user)
        # self.custom_assigned_to = assigned_to
		
