# Copyright (c) 2023, Tejal KUmbhar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import os
from frappe.query_builder.utils import DocType
from frappe.utils import encode, get_files_path




class VisitorInformation(Document):
	

	def before_save(self):
		self.send_email(self.email)

	@frappe.whitelist()    
	def send_email(self, email):
	# Your email sending logic goes here
		message = "Thank you for Visiting at \n\n" + str(self.company_name) + "\n\n<br><br>"
		attachments = []
		# Add product information to the email message
		for product in self.get("product"):
			message += f"Product Name: {product.product}\n<br>"
			message += f"Description: {product.description}\n<br>"
			message += f"Product Attachment: <a href='{product.product_attach}'>{product.product_name} Attachment</a>\n\n<br><br>"
		# frappe.throw(str(product.product_attach))	
			# Attachments
		
		# for product in self.get("product"):
			# attachment = {
			# 	"fname": product.product,
			#   	# "content":(product.product_attach)
			# 	"content": frappe.get_doc("File",{"file_url":'https://mobilecrm.erpdata.in/files/1699339835316.pdf'}).get_content() #marksheet -0064   product.product_attach 1699339835316.pdf
			# }
			base_path = frappe.get_site_path("public")
	
			file_path = "/home/erpadmin/bench-mobcrm/sites/mobilecrm.erpdata.in/public"+str(product.product_attach)
			gogo="/home/erpadmin/bench-mobcrm/sites/mobilecrm.erpdata.in/public/files/1699339835316.pdf"
		# base_path = frappe.utils.get_site_base_url()#frappe.get_site_path("public")
		# frappe.throw(str(file_path)+"===="+gogo)

			if os.path.exists(file_path):
				# frappe.throw(str(file_path))

				with open(file_path, "rb") as file:
					attachment_content = file.read()
					attachment_name = str(product.product_attach)
					attachments.append({"fname": attachment_name, "fcontent": attachment_content})
					print("File content read successfully.")
			else:
				print("File not found.")

			# if os.path.exists(file_path):
			# 	with open(file_path, "rb") as file:
			# 		attachment = file.read()
			# 		print("File content read successfully.")
			# else:
			# 	print("File not found.")

			# attachments.append(attachment)

			# Send the email using frappe.sendmail() /home/erpadmin/bench-mobcrm/sites/mobilecrm.erpdata.in/public/files/1699339835316.pdf
   

	# def get_file(file_name):
	# 	file_doc = frappe.get_doc("File", {"file_url": file_name})
	# 	parts = file_doc.get_extension()
	# 	extension = parts[1]
	# 	extension = extension.lstrip(".")


	# 	return file_doc, extension
		# frappe.throw(str(attachment)) Product_attach
  
  
			# production_doc =frappe.get_doc("Product",product.product_name)
		# if product.product_attach:
		# 	attachment_name = product.product_attach
		# 	# attachment_content = frappe.get_doc("File", production_doc.product_image).get_content()
		# 	# attachment_content = frappe.get_value('File', production_doc.product_image, 'file_url')get_file
		# 	# file_url = file_url.replace(/#/g, "%23")
		# 	# p = frappe.get_file_url(product.attachment_field) #url = doc.get_url()             attachment_content = frappe.get_value('File', {'name': product.attachment_field}, 'file_url')

		# 	# q = frappe.get_url(product.attachment_field)
		# 	# frappe.throw(str(production_doc.product_image))
		# 	attachment_content= self.get_file(product.product_attach)
		# 	# frappe.throw(str(attachment_content))
		# 	# frappe.throw(str(attachment_content))
		# 	attachments.append({"fname": attachment_name, "fcontent": attachment_content})

  
		frappe.sendmail(
			recipients=[email],
			subject=str(self.company_name),
			message=message,
			attachments=attachments
		)
		frappe.msgprint("Email sent")


	def delete_prodcut_name_field_from_product(self):
		prodct =frappe.get_all("Designations", filters = {"name":self.product_name} )
		if prodct:
			p=frappe.get_doc("Designations",prodct[0].name)
			p.delete()
   
   
   
	def get_file(self,fname):
		"""Returns [`file_name`, `content`] for given file name `fname`"""
		file_path = self.get_file_path(fname)

		# read the file
		with open(encode(file_path), mode="rb") as f:
			content = f.read()
			try:
				# for plain text files
				content = content.decode()
			except UnicodeDecodeError:
				# for .png, .jpg, etc
				pass

		return [file_path.rsplit("/", 1)[-1], content]


	def get_file_path(self,file_name):
		"""Returns file path from given file name"""
		if "../" in file_name:
			return

		File = DocType("File")

		f = (
			frappe.qb.from_(File)
			.where((File.name == file_name) | (File.file_name == file_name))
			.select(File.file_url)
			.run()
		)

		if f:
			file_name = f[0][0]

		file_path = file_name

		if "/" not in file_path:
			file_path = "/files/" + file_path

		if file_path.startswith("/private/files/"):
			file_path = get_files_path(*file_path.split("/private/files/", 1)[1].split("/"), is_private=1)

		elif file_path.startswith("/files/"):
			file_path = get_files_path(*file_path.split("/files/", 1)[1].split("/"))

		else:
			frappe.throw(("There is some problem with the file url: {0}").format(file_path))

		return file_path
   
   
