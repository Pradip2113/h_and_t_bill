# Copyright (c) 2023, Abhishek and contributors
# For license information, please see license.txt

import ast
import re
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from datetime import datetime
class HandTBilling(Document):
    
    #To get data into H & T Table after clicking show list button
	@frappe.whitelist()
	def get_data(self):
		har_list=[]
		trans_list=[]
		vendor_list=[]
		doc = frappe.db.get_list("Cane Weight",
                                                filters={"docstatus": 1,"date": ["between", [self.from_date, self.to_date]],"season" : self.season ,"branch" : self.branch,"h_and_t_billing_status":False },
                                                fields=["harvester_code","transporter_code","harvester_name","transporter_name"])
		for d in doc:
			if(d.transporter_code not in trans_list):
				trans_list.append(d.transporter_code)
				vendor_list.append({"vender_name":d.transporter_name,
						"vender_id":d.transporter_code,
						"type":"Transporter"})
		for d in doc:
			if(d.harvester_code not in har_list):
				har_list.append(str(d.harvester_code))
				vendor_list.append({"vender_name":d.harvester_name,
						"vender_id":d.harvester_code,
						"type":"Harvester"}) 
		for index in range(len(vendor_list)):
			self.append(
					"h_and_t_table",
					{
						"vender_name":vendor_list[index]["vender_name"],
						"vender_id":vendor_list[index]["vender_id"],
						"type":vendor_list[index]["type"]
					}
				)   
   
	#To select all vender after clicking select all
	@frappe.whitelist()
	def selectall(self):
		children = self.get("h_and_t_table")
		if not children:
			return
		all_selected = all([child.check for child in children])
		value = 0 if all_selected else 1
		for child in children:
			child.check = value	
   
	#To get data into H and T Invisible
	@frappe.whitelist()
	def get_all_data_calcalation(self):
		for vender in self.get("h_and_t_table"):
			if(vender.check):
				doc = frappe.db.get_list("Cane Weight",
                                                filters={"date": ["between", [self.from_date, self.to_date]],"season" : self.season ,"branch" : self.branch },
                                              fields=["harvester_code","transporter_code","harvester_name","transporter_name","contract_id","distance","actual_weight","vehicle_type"],)
				for d in doc:
					if(str(vender.vender_id)==str(d.harvester_code) and str(vender.type)==str("Harvester")):
						self.append(
						"child_h_and_t_invisible",
						{
							"vender_name":d.harvester_name,
							"vender_id":d.harvester_code,
							"type":"Harvester",
							"contract_id":d.contract_id,
							"distance":d.distance,
							"distance_amt":round(float(self.get_rate(d.distance,str(d.vehicle_type),"Harvester")),2),
							"weight":round((d.actual_weight),3),
							"total":round((float(d.actual_weight)*float(self.get_rate(d.distance,str(d.vehicle_type),"Harvester"))),2),
							"vehicle_type":d.vehicle_type
						}
					)
					if(str(vender.vender_id)==str(d.transporter_code)and str(vender.type)==str("Transporter")):
						self.append(
						"child_h_and_t_invisible",
						{
							"vender_name":d.transporter_name,
							"vender_id":d.transporter_code,
							"type":"Transporter",
							"contract_id":d.contract_id,
							"distance":d.distance,
							"distance_amt":round((float(self.get_rate(d.distance,str(d.vehicle_type),"Transporter"))),2),
							"weight":round((d.actual_weight),3),
							'total':round(d.actual_weight*float(self.get_rate(d.distance,str(d.vehicle_type),"Transporter")),2),
							"vehicle_type":d.vehicle_type
						}
					)
				
		#To get data into dictionary for the calculation
		data_calculation_dict={}
		str_create=""
		for index in self.get("child_h_and_t_invisible"):
			str_create=index.vender_id+""+index.type+""+index.contract_id
			if str_create not in data_calculation_dict:
				data_calculation_dict[str_create]={
					        "vender_name":str(index.vender_name),
							"vender_id":index.vender_id,
							"type":index.type,
							"contract_id":index.contract_id,
							"total":round(float(index.total),2),
							"deduction":0,
							"payable_amt":0 , 
							"total_weight":round(float(index.weight),3),
							"total_transporter_deduction":0,
							"sales_invoice_deduction":0,
							"other_deductions":0,
							"lone_deduction":0,
							"loan_interest_deduction":0,
							"all_deduction_information":" "
				}
			else:
				data_calculation_dict[str_create]["total"]+=round(float(index.total),2)
				data_calculation_dict[str_create]["total_weight"]+=round(float(index.weight),2)
    
    
		#To get deduction amount and payable amount
		sales_invoices = []
		other_deduction_dict =[]
		loan_installment=[]
		loan_installment_intrest=[]
		all_deduction = []
		for d in data_calculation_dict:
			sales_invoice_deduction_amt=0
			other_deductions_amt=0
			other_deductions=""
			loan_installment_amt=0
			loan_interest_amt=0
			total_deduction=0
			payable_amt=0
			total_amt=0
			total_of_h_t=0
			har_total=0
			#To get the dedution amount
			if(data_calculation_dict[d]["type"]=="Transporter"):
				if self.includes_sales_invoice_deduction: 
					deduction_doc = frappe.get_all("Sales Invoice",
																	filters={"h_and_t_contract":data_calculation_dict[d]["contract_id"],"status": ["in", ["Unpaid", "Overdue", "Partly Paid"]],},
																			fields=["outstanding_amount", "customer", "name", "debit_to","h_and_t_contract"],)
					
					sales_invoices=[{"Sales invoice ID": d_d.name,"Outstanding Amount": d_d.outstanding_amount,"Account": d_d.debit_to,"Contract Id":d_d.h_and_t_contract}for d_d in deduction_doc]  # in this list all sales invoice will recored with there accound and outstanding_amount info
					sales_invoice_deduction_amt= sum(float(d["Outstanding Amount"]) for d in sales_invoices)  # calculating sum of all sales invoice			
				other_deductions = frappe.get_all("Deduction Form",
																		filters={"h_and_t_contract_id":data_calculation_dict[d]["contract_id"],"docstatus":1, "season" : self.season , "deduction_status" : 0},
																		fields=["farmer_code", "account", "name", "deduction_amount","paid_amount" ,"h_and_t_contract_id", "farmer_application_loan_id","interest_calculate_on_amount", "rate_of_interest" , "from_date_interest_calculation","interest_account" ,"update_from_date_interest_calculation",],)
				if self.other_deduction:
					other_deduction_dict=[{"Farmer Code": o_d.farmer_code,"Deduction Amount": round((float(o_d.deduction_amount) - float(o_d.paid_amount)),2),"Account": o_d.account,"DFN": o_d.name,"Contract Id":o_d.h_and_t_contract_id}for o_d in other_deductions if not o_d.farmer_application_loan_id ]
					other_deductions_amt=sum(float(g["Deduction Amount"]) for g in other_deduction_dict)

				if self.includes_loan_installment:
					loan_installment = [{"Farmer Loan ID": o_l.farmer_application_loan_id, "Farmer ID": o_l.farmer_code , "season": self.season, "Account": o_l.account, "Installment Amount": round((float(o_l.deduction_amount) - float(o_l.paid_amount)),2),"Contract Id":o_l.h_and_t_contract_id }for o_l in other_deductions if o_l.farmer_application_loan_id and (round((float(o_l.deduction_amount) - float(o_l.paid_amount)),2)) != 0 ]
					loan_installment_amt = sum(float(j["Installment Amount"]) for j in loan_installment)
				
				if self.includes_loan_interest:
					loan_installment_intrest = [{
													"Farmer Loan ID": o_i.farmer_application_loan_id,
													"Farmer ID": o_i.farmer_code,
													"season": self.season,
													"Account": o_i.interest_account,
													"Installment Interest Amount": round(round(float(float(o_i.interest_calculate_on_amount)-float(o_i.paid_amount)) * (float(o_i.rate_of_interest) / 100) * ((datetime.strptime(str(self.to_date), "%Y-%m-%d") - datetime.strptime((str(o_i.from_date_interest_calculation)), "%Y-%m-%d")).days / 365), 2) +  round(float(float(o_i.interest_calculate_on_amount)-float(o_i.paid_amount)) * (float(o_i.rate_of_interest) / 100) * ((datetime.strptime(str(self.to_date), "%Y-%m-%d") - datetime.strptime((str(o_i.update_from_date_interest_calculation)), "%Y-%m-%d")).days / 365), 2),2),
													"Contract Id":o_i.h_and_t_contract_id
												}
												
												if o_i.update_from_date_interest_calculation
												else 
												{
													"Farmer Loan ID": o_i.farmer_application_loan_id,
													"Farmer ID": o_i.farmer_code,
													"season": self.season,
													"Account": o_i.interest_account,
													"Installment Interest Amount": round(float(o_i.interest_calculate_on_amount)*(float(o_i.rate_of_interest) / 100)*((datetime.strptime(self.to_date, "%Y-%m-%d")- datetime.strptime((str(o_i.from_date_interest_calculation)),"%Y-%m-%d",)).days/ 365),2,),
													"Contract Id":o_i.h_and_t_contract_id
												}
												for o_i in other_deductions if o_i.farmer_application_loan_id and o_i.from_date_interest_calculation and (round((float(o_i.deduction_amount) - float(o_i.paid_amount)),2)) != 0 ]
					loan_interest_amt = sum(float(m["Installment Interest Amount"]) for m in loan_installment_intrest)
				total_deduction = (sales_invoice_deduction_amt+ loan_installment_amt+ loan_interest_amt+other_deductions_amt)
				total_amt=data_calculation_dict[d]["total"]
				payable_amt=total_amt-total_deduction
				if(payable_amt>=0):
					data_calculation_dict[d]["deduction"]=total_deduction
					data_calculation_dict[d]["total_transporter_deduction"]=total_deduction
				else:
					temp_str=""
					for index in data_calculation_dict:
						if(data_calculation_dict[index]!=data_calculation_dict[d] and data_calculation_dict[d]["contract_id"]==data_calculation_dict[index]["contract_id"]):
							temp_str=index
							break
					har_total=data_calculation_dict[temp_str]["total"]
					total_of_h_t=har_total+total_amt
					payable_amt=total_of_h_t-total_deduction
					if(payable_amt>=0):
						data_calculation_dict[d]["deduction"]=total_amt
						data_calculation_dict[temp_str]["deduction"]=har_total-payable_amt
						data_calculation_dict[d]["total_transporter_deduction"]=total_deduction
					else:
						doc_acc = frappe.get_all("Account Priority Child",
                                                            filters={"parent": self.branch},
                                                            fields={"priority_account", "idx"},order_by="idx ASC",)  # frappe.msgprint(str(doc_acc))  #$$$$$
						all_deduction = ( loan_installment_intrest   + loan_installment + sales_invoices+other_deduction_dict)  # frappe.msgprint(str(all_deduction))
						all_deduction = sorted(all_deduction,key=lambda x: next((item["idx"] for item in doc_acc if item["priority_account"] == x["Account"]),len(doc_acc) + 1,),)

						while float(total_of_h_t) < float(total_deduction):
							last_poped_entry = all_deduction.pop(-1)
							total_sum = float(sum([
													float(entry.get("Installment Interest Amount", 0))
													+ float(entry.get("Installment Amount", 0))
												+ float(entry.get("Outstanding Amount", 0))
													+ float(entry.get("Deduction Amount", 0))
													for entry in all_deduction 
												]))

							total_deduction = float(total_sum)
							total_payable = float(total_of_h_t)-float(total_deduction)

						contains_key = next((key for key in ["Outstanding Amount","Installment Amount","Installment Interest Amount","Deduction Amount"] if key in last_poped_entry),None,)
						if (str(contains_key)) == "Outstanding Amount":
							new_outstanding_amount = round(float(total_payable), 2)
							total_deduction = round((float(total_deduction) + float(total_payable)), 2)
							total_payable = 0
							last_poped_entry["Outstanding Amount"] = new_outstanding_amount
							all_deduction.append(last_poped_entry)
							
							
							
						if (str(contains_key))== "Installment Amount":
							# updating_temp_out_amount = last_poped_entry.get('Outstanding Amount')
							paid_amount =round(float(total_payable),2)
							total_deduction =round(( float(total_deduction)+ float(total_payable)),2)
							total_payable=0
							last_poped_entry['Installment Amount'] = paid_amount
							all_deduction.append(last_poped_entry)
							
							
							
						if (str(contains_key)) == "Deduction Amount":
							new_other_deduction_amount = round(float(total_payable), 2)
							total_deduction = round((float(total_deduction) + float(total_payable)), 2)
							total_payable = 0
							last_poped_entry["Deduction Amount"] = new_other_deduction_amount
							all_deduction.append(last_poped_entry)
							
       
						data_calculation_dict[d]["deduction"]=total_deduction-har_total
						data_calculation_dict[temp_str]["deduction"]=har_total-(total_of_h_t-total_deduction)
						data_calculation_dict[d]["total_transporter_deduction"]=total_deduction

						loan_installment_amt = sum(float(record['Installment Amount']) for record in all_deduction if 'Installment Amount' in record)
						loan_interest_amt = sum(float(record['Installment Interest Amount']) for record in all_deduction if 'Installment Interest Amount' in record)
						sales_invoice_deduction_amt = sum(float(record['Outstanding Amount']) for record in all_deduction if 'Outstanding Amount' in record)
						other_deductions_amt = sum(float(record['Deduction Amount']) for record in all_deduction if 'Deduction Amount' in record)
					
      
						loan_installment = [record for record in all_deduction if 'Installment Amount' in record]
						loan_installment_intrest = [record for record in all_deduction if 'Installment Interest Amount' in record]
						sales_invoices = [record for record in all_deduction if 'Outstanding Amount' in record]
						other_deduction_dict = [record for record in all_deduction if 'Deduction Amount' in record]

		
				data_calculation_dict[d]["sales_invoice_deduction"]=float(sales_invoice_deduction_amt)
				data_calculation_dict[d]["other_deductions"]=float(other_deductions_amt)
				data_calculation_dict[d]["lone_deduction"]=float(loan_installment_amt)
				data_calculation_dict[d]["loan_interest_deduction"]=float(loan_interest_amt)
				
				data_calculation_dict[d]["all_deduction_information"]=str(sales_invoices)+str(loan_installment)+str(loan_installment_intrest)+str(other_deduction_dict)
				
		#To append data to calculation table
		for d in data_calculation_dict:
			self.append(
						"calculation_table",	
						{
							"vender_name":data_calculation_dict[d]["vender_name"],
							"vender_id":data_calculation_dict[d]["vender_id"],
							"type":data_calculation_dict[d]["type"],
							"contract_id":data_calculation_dict[d]["contract_id"],
							"total_weight":data_calculation_dict[d]["total_weight"],
							"total":round(float(data_calculation_dict[d]["total"]),2),
							"deduction":round(float(data_calculation_dict[d]["deduction"]),2),
							"payable_amt":round((float(data_calculation_dict[d]["total"])-float(data_calculation_dict[d]["deduction"])),2),
							"total_transporter_deduction":round(float(data_calculation_dict[d]["total_transporter_deduction"]),2),
							"sales_invoice_deduction":data_calculation_dict[d]["sales_invoice_deduction"],
							"other_deductions":data_calculation_dict[d]["other_deductions"],
							"lone_deduction":data_calculation_dict[d]["lone_deduction"],
							"loan_interest_deduction":data_calculation_dict[d]["loan_interest_deduction"],
							"all_deduction_information":data_calculation_dict[d]["all_deduction_information"]
						}
			)
		self.total_values()
		# for s in self.get("calculation_table"):
		# 		list_data_lo =[]
		# 		formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
		# 		formatted_input = '[' + formatted_input + ']'
		# 		parsed_list = ast.literal_eval(formatted_input)
		# 		list_data_lo=eval(str(parsed_list[1]))
		# 		frappe.msgprint(str(list_data_lo))
		for s in self.get("calculation_table"):
					list_data_lo =[]
					formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
					formatted_input = '[' + formatted_input + ']'
					parsed_list = ast.literal_eval(formatted_input)
					list_data_lo =parsed_list
					if(list_data_lo):
						frappe.msgprint(str(list_data_lo[0]))
					else:
						pass
					
					
	#To get Net Deduction and collection
	def total_values(self):
		total_weight = 0
		total_collection_amount = 0
		total_deduction = 0
		total_payable_amount = 0
		totals=self.get("calculation_table")
		for d in totals:
			total_weight = total_weight+round(float(d.total_weight),2)
			total_collection_amount = total_collection_amount+round(float(d.total),2)
			total_deduction = total_deduction+round(float(d.total_transporter_deduction),2)
			total_payable_amount = total_payable_amount+round(float(d.payable_amt),2)
		self.new_total_weight = total_weight
		self.net_total_collection_amountrs = total_collection_amount
		self.net_total_deductionrs = total_deduction
		self.net_total_payable_amountrs = total_payable_amount
		
        
	#To get the km rate 
	def get_rate(self,distance,vehicle_type,vender_type):
		dict1={}
		count=True
		if(vender_type=="Transporter"):
			doc=frappe.db.get_list("Transporter Rate Chart",
													filters={"season" : self.season ,"branch" : self.branch, "vehicle_type":vehicle_type},
												fields=["name","per_km_rate"])
			rate_per_km=doc[0].get("per_km_rate")
			chart_table = frappe.get_all("Child Rate Chart",filters={"parent":doc[0].get("name")},fields=["distance","rate"])
			for rows in chart_table:
				if(str(rows["distance"])==str(int(distance))):
					count=False
					return rows.rate 
				else:
					dict1[int(rows.distance)]=float(rows.rate)
			if(count):	
				distance_rate=0
				extra_km=0
				extra_charge=0
				large_km=max(dict1)
				extra_km=distance-large_km
				extra_charge=extra_km*rate_per_km
				distance_rate=dict1[large_km]+extra_charge
				return distance_rate
		if(vender_type=="Harvester"):
			doc=frappe.db.get_list("Harvester Rate Chart",
													filters={"season" : self.season ,"branch" : self.branch, "vehicle_type":vehicle_type},
												fields=["name","per_km_rate"])
			rate_per_km=doc[0].get("per_km_rate")
			return rate_per_km

		

	#To update the status ater before cancel event on cane weight doctype
	def on_trash(self):
		self.bill_status_change_of_cane_weight_on_trash()

	def before_cancel(self):
		self.bill_status_change_of_cane_weight_on_trash()
		self.cancel_journal_entry()
		self.update_value_in_farmer_loan_cancel()
		self.set_date_in_farmer_loan_child_for_next_installment_on_cancel()
		self.update_value_in_deduction_form_on_cancel()

	def cancel_journal_entry(self):
		doc = frappe.get_doc("Journal Entry",(str(self.journal_entry_id)))
		if doc.docstatus == 1:
			doc.cancel()
	
	def bill_status_change_of_cane_weight_on_trash(self):
		doc = frappe.db.get_list("Cane Weight",
												filters={"date": ["between", [self.from_date, self.to_date]],"season" : self.season ,"branch" : self.branch,"h_and_t_billing_status":True},
												fields=["name","h_and_t_billing_status"],)
		for d in doc:
			frappe.db.set_value("Cane Weight",d.name,"h_and_t_billing_status",False)

	           
	def update_value_in_farmer_loan_cancel(self):
		if self.includes_loan_installment:
			for s in self.get("calculation_table"):	
				list_data_lo =[]
				formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
				formatted_input = '[' + formatted_input + ']'
				parsed_list = ast.literal_eval(formatted_input)
				list_data_lo=eval(str(parsed_list))
				if(list_data_lo):
					list_data_lo=list_data_lo[1]
					for data_lo in list_data_lo:
						child_doc_farmer_loan=frappe.get_all('Deduction Form', filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':data_lo['season'],"h_and_t_contract_id":data_lo["Contract Id"]}, fields=['name','paid_amount'])
						for d in child_doc_farmer_loan:
							frappe.db.set_value("Deduction Form",d.name,"paid_amount",round((float(d.paid_amount)-(float(data_lo['Installment Amount']))),2))
		
	def set_date_in_farmer_loan_child_for_next_installment_on_cancel(self):
		for s in self.get("calculation_table"):
			list_data_lo =[]
			formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
			formatted_input = '[' + formatted_input + ']'
			parsed_list = ast.literal_eval(formatted_input)
			list_data_lo=eval(str(parsed_list))
			if(list_data_lo):
				list_data_lo=list_data_lo[1]
				current_season = self.season
				next_seasons = str(int(current_season.split('-')[1]) ) + '-' + str(int(current_season.split('-')[1]) + 1) 
				for data_lo in list_data_lo:
					child_doc_farmer_loan=frappe.get_all('Deduction Form', 
														filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':next_seasons,"h_and_t_contract_id":data_lo["Contract Id"]}, 
														fields=['name',])
					for d in child_doc_farmer_loan:
						frappe.db.set_value("Deduction Form",d.name,"from_date_interest_calculation",None)
						
						
				for data_lo in list_data_lo:
					child_doc_farmer_loan=frappe.get_all('Deduction Form', 
														filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':self.season,"h_and_t_contract_id":data_lo["Contract Id"]}, 
														fields=['name',])
					for d in child_doc_farmer_loan:
						frappe.db.set_value("Deduction Form",d.name,"update_from_date_interest_calculation",None)
          
	def update_value_in_deduction_form_on_cancel(self):
		for s in self.get("calculation_table"):
			list_data_od =[]
			formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
			formatted_input = '[' + formatted_input + ']'
			parsed_list = ast.literal_eval(formatted_input)
			list_data_od=eval(str(parsed_list))
			if(list_data_od):
				list_data_od=parsed_list[3]
				for data_od in list_data_od:
					other_deduction_doc=frappe.get_all('Deduction Form', filters={'name': data_od['DFN'],"h_and_t_contract_id":data_od["Contract Id"]}, fields=['name',"paid_amount" , "deduction_amount"])
					for d in other_deduction_doc:
							frappe.db.set_value("Deduction Form",d.name,"paid_amount",(float(d.paid_amount)-(float(data_od['Deduction Amount']))))
							frappe.db.set_value("Deduction Form",d.name,"deduction_status",0)




	def je_of_sales_invoice_and_farmer_loan(self):
		counter =0
		branch_doc = frappe.get_all("Branch",
											filters={"name": self.branch},
											fields={"cane_rate", "name","company","debit_in_account_currency"},)
		if branch_doc:
			if not (branch_doc[0].company):
				frappe.throw( f" Please set Company for Branch '{str(self.branch) } '")
				
			if not (branch_doc[0].debit_in_account_currency):
				frappe.throw( f" Please set Debit Account for Branch '{str(self.branch) } '")
			company =  ((branch_doc[0].company))
			acc_to_set_debit_side = ((branch_doc[0].debit_in_account_currency))

		
		je = frappe.new_doc("Journal Entry")
		je.voucher_type = "Journal Entry"
		je.company = company
		je.posting_date = self.today

		for s in self.get("calculation_table"):
			if(s.type=="Transporter"):
				list_data_se = []
				list_data_lo = []
				list_data_li = []
				list_data_od = []
				parsed_list=""
				if s.total_transporter_deduction:
					counter = counter + 1
					formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
					formatted_input = '[' + formatted_input + ']'
					parsed_list = ast.literal_eval(formatted_input)
					list_data_se=parsed_list[0]
					list_data_lo=parsed_list[1]
					list_data_li=parsed_list[2]
					list_data_od=parsed_list[3]
					je.append(
						"accounts",
						{
							"account": acc_to_set_debit_side,
							"party_type": "Supplier",
							"party": s.vender_id,
							"debit_in_account_currency": round(s.total_transporter_deduction,2),
							"contract_id":s.contract_id
							
						},)
				
				if list_data_se:
					for data_se in list_data_se:
						je.append(
							"accounts",
							{
								"account": data_se["Account"],
								"party_type": "Customer",
								"party": s.vender_id,
								"credit_in_account_currency": data_se["Outstanding Amount"],
								"reference_type": "Sales Invoice",
								"reference_name": data_se["Sales invoice ID"],
								"contract_id":s.contract_id
							},)
						
				if list_data_lo:
					for data_lo in list_data_lo:
						je.append(
							"accounts",
							{
								"account": data_lo["Account"],
								"party_type": "Customer",
								"party": s.vender_id,
								"credit_in_account_currency": data_lo["Installment Amount"],
								"contract_id":s.contract_id
							},)
						
				if list_data_li:
					for data_li in list_data_li:
						if int(data_li["Installment Interest Amount"]) != 0:
							je.append(
								"accounts",
								{
									"account": data_li["Account"],
									"party_type": "Customer",
									"party": s.vender_id,
									"credit_in_account_currency": data_li["Installment Interest Amount"],
									"contract_id":s.contract_id
								},)
				
							
				if list_data_od:
					for data_od in list_data_od:
						if int(data_od["Deduction Amount"]) != 0:
							je.append(
								"accounts",
								{
									"account": data_od["Account"],
									"party_type": "Supplier",
									"party": s.vender_id,
									"credit_in_account_currency": data_od["Deduction Amount"],
									"contract_id":s.contract_id
								},)		            
		if counter > 0:
			je.insert()
			je.save()
			je.submit()
			journal_entry = frappe.db.get_all("Journal Entry", fields=["name"], order_by="creation DESC", limit=1)
			self.journal_entry_id = str(journal_entry[0].name)
			
  
	      
	def update_value_in_farmer_loan(self):
		if self.includes_loan_installment:
			for s in self.get("calculation_table"):
				list_data_lo =[]
				formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
				formatted_input = '[' + formatted_input + ']'
				parsed_list = ast.literal_eval(formatted_input)
				list_data_lo=eval(str(parsed_list))
				if(list_data_lo):
					list_data_lo=list_data_lo[1]
					for data_lo in list_data_lo:
						child_doc_farmer_loan=frappe.get_all('Deduction Form', filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':data_lo['season'],"h_and_t_contract_id":data_lo["Contract Id"]}, fields=['name','paid_amount'])
						for d in child_doc_farmer_loan:
							frappe.db.set_value("Deduction Form",d.name,"paid_amount",round((float(d.paid_amount)+(float(data_lo['Installment Amount']))),2))

	       
	def set_date_in_farmer_loan_child_for_next_installment(self):
		for s in self.get("calculation_table"):
			list_data_lo =[]
			formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
			formatted_input = '[' + formatted_input + ']'
			parsed_list = ast.literal_eval(formatted_input)
			parsed_list = ast.literal_eval(formatted_input)
			list_data_lo=eval(str(parsed_list))
			if(list_data_lo):
				list_data_lo=list_data_lo[1]
				current_season = self.season
				next_seasons = str(int(current_season.split('-')[1]) ) + '-' + str(int(current_season.split('-')[1]) + 1) 
				#Update date for Next season
				for data_lo in list_data_lo:
					child_doc_farmer_loan=frappe.get_all('Deduction Form', 
																		filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':next_seasons,"h_and_t_contract_id":data_lo["Contract Id"]}, 
																		fields=['name'])
					for d in child_doc_farmer_loan:
						frappe.db.set_value("Deduction Form",d.name,"from_date_interest_calculation",self.to_date)
				#Update date for current season
				for data_lo in list_data_lo:
					child_doc_farmer_loan=frappe.get_all('Deduction Form', 
																		filters={'farmer_application_loan_id': data_lo['Farmer Loan ID'],'season':self.season,"h_and_t_contract_id":data_lo["Contract Id"]}, 
																		fields=['name'])
					for d in child_doc_farmer_loan:
						frappe.db.set_value("Deduction Form",d.name,"update_from_date_interest_calculation",self.to_date)


	     
	def update_value_in_deduction_form(self):
		for s in self.get("calculation_table"):    
			list_data_od =[]
			formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
			formatted_input = '[' + formatted_input + ']'
			parsed_list = ast.literal_eval(formatted_input)
			list_data_od=eval(str(parsed_list))
			if(list_data_od):
				list_data_od=list_data_od[3]
				for data_od in list_data_od:
					other_deduction_doc=frappe.get_all('Deduction Form', filters={'name': data_od['DFN'],"h_and_t_contract_id":data_od["Contract Id"]}, fields=['name',"paid_amount" , "deduction_amount"])
					for d in other_deduction_doc:
							frappe.db.set_value("Deduction Form",d.name,"paid_amount",(float(d.paid_amount)+(float(data_od['Deduction Amount']))))
							if (float(d.paid_amount)+(float(data_od['Deduction Amount']))) == d.deduction_amount:
								frappe.db.set_value("Deduction Form",d.name,"deduction_status",1)

	#To update the status after before save event on cane weight doctype
	def before_save(self):
		self.change_status_on_cane_weight()
	#To update the status after before submit event on cane weight doctype
	def before_submit(self):
		self.change_status_on_cane_weight()
		self.je_of_sales_invoice_and_farmer_loan()
		self.update_value_in_farmer_loan()
		self.set_date_in_farmer_loan_child_for_next_installment()
		self.update_value_in_deduction_form()

	def change_status_on_cane_weight(self):
		doc = frappe.db.get_list("Cane Weight",
                                                filters={"date": ["between", [self.from_date, self.to_date]],"season" : self.season ,"branch" : self.branch,"h_and_t_billing_status":False },
                                                fields=["name","h_and_t_billing_status"],)
		for d in doc:
		  frappe.db.set_value("Cane Weight",d.name,"h_and_t_billing_status",True)
   