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
    #we get Unique record of H and T from cane weight page 
	@frappe.whitelist()
	def get_data(self):
		har_list=[]
		trans_list=[]
		vendor_list=[]
		doc = frappe.db.get_list("Cane Weight",
                                                filters={"docstatus":1,"date": ["between", [self.from_date, self.to_date]],"season" : self.season ,"branch" : self.branch,"h_and_t_billing_status":False},
                                                fields=["harvester_code","transporter_code","harvester_name","transporter_name","contract_id","harvester_contract"])
		for d in doc:
				if(d.transporter_code not in trans_list):
					trans_list.append(d.transporter_code)
					vendor_list.append({"vender_name":d.transporter_name,
							"vender_id":d.transporter_code,
							"contract_id":d.contract_id,
							"type":"Transporter"})
		for d in doc:
			if(d.harvester_code not in har_list):
				har_list.append(str(d.harvester_code))
				vendor_list.append({"vender_name":d.harvester_name,
						"vender_id":d.harvester_code,
						"contract_id":d.harvester_contract,
						"type":"Harvester"}) 
		
	
		for index in range(len(vendor_list)):
			self.append(
					"h_and_t_table",
					{
						"vender_name":vendor_list[index]["vender_name"],
						"vender_id":vendor_list[index]["vender_id"],
						"type":vendor_list[index]["type"],
						"contract_id":vendor_list[index]["contract_id"],
					}
				)   
   
	#To select all venders after clicking select all
	@frappe.whitelist()
	def selectall(self):
		children = self.get("h_and_t_table")
		if not children:
			return
		all_selected = all([child.check for child in children])
		value = 0 if all_selected else 1
		for child in children:
			child.check = value	
   
	#To get data into H and T Invisible table
	#all record of H and T get collected from from_date to to_date
	@frappe.whitelist()
	def get_all_data_calcalation(self):
		for vender in self.get("h_and_t_table"):
			if(vender.check):
				doc = frappe.db.get_list("Cane Weight",
                                                filters={"docstatus": 1,"date": ["between", [self.from_date, self.to_date]],"season" : self.season ,"branch" : self.branch ,"h_and_t_billing_status":False},
                                              fields=["harvester_contract","harvester_code","transporter_code","harvester_name","transporter_name","contract_id","distance","actual_weight","vehicle_type","cart_number"],)
				for d in doc:
					if(str(vender.vender_id)==str(d.harvester_code) and str(vender.type)==str("Harvester")):
						self.append(
						"child_h_and_t_invisible",
						{
							"vender_name":d.harvester_name,
							"vender_id":d.harvester_code,
							"type":"Harvester",
							"contract_id":d.harvester_contract,
							"distance":d.distance,
							"distance_amt":round(float(self.get_rate(d.distance,str(d.vehicle_type),"Harvester")),2) if (self.get_rate(d.distance,str(d.vehicle_type),"Harvester")) else frappe.throw(f"Please create the rate chart for vehicle type '{d.vehicle_type}' in Harvester Rate Chart"),
							"weight":round((d.actual_weight),3),
							"total":round((float(d.actual_weight)*float(self.get_rate(d.distance,str(d.vehicle_type),"Harvester"))),2) if (self.get_rate(d.distance,str(d.vehicle_type),"Harvester")) else frappe.throw(f"Please create the rate chart for vehicle type  '{d.vehicle_type}' in Harvester Rate Chart"),
							"vehicle_type":d.vehicle_type,
							"cartno":d.cart_number,
							"other_id":d.contract_id
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
							"distance_amt":round((float(self.get_rate(d.distance,str(d.vehicle_type),"Transporter"))),2) if (self.get_rate(d.distance,str(d.vehicle_type),"Transporter")) else frappe.throw(f"Please create the rate chart for vehicle type  '{d.vehicle_type}' in Transporter Rate Chart"),
							"weight":round((d.actual_weight),3),
							'total':round(d.actual_weight*float(self.get_rate(d.distance,str(d.vehicle_type),"Transporter")),2) if (self.get_rate(d.distance,str(d.vehicle_type),"Transporter")) else frappe.throw(f"Please create the rate chart for vehicle type  '{d.vehicle_type}' in Transporter Rate Chart"),
							"vehicle_type":d.vehicle_type,
							"cartno":d.cart_number,
							"other_id":d.harvester_contract
						}
					)
				
		#To get data into dictionary for the calculation	
		#Dictionary is used for further calculation in calculation table
		data_calculation_dict={}
		str_create=""
		for index in self.get("child_h_and_t_invisible"):
			str_create=index.vender_id+""+index.type+""+index.contract_id+""+index.other_id
			if str_create not in data_calculation_dict:
				data_calculation_dict[str_create]={
					        "vender_name":str(index.vender_name),
							"vender_id":index.vender_id,
							"type":index.type,
							"contract_id":index.contract_id,
							"total":round(float(index.total),2),
							"vehicle_type":index.vehicle_type,
							"deduction":0,
							"payable_amt":0, 
							"total_weight":round(float(index.weight),3),
							"sales_invoice_deduction":0,
							"other_deductions":0,
							"lone_deduction":0,
							"loan_interest_deduction":0,
							"all_deduction_information":" ",
							"tds_deduction":0,
							"sd_deduction":0,
							"cartno":index.cartno,
							"hire_charge":0,
							"remaining_hire":0,
							"hire_acc":"",
							"cart_no_list":"",
							"transporter":"",
							"penalty_charge":0,
							"other_collection":0,
							"other_deduction":0,
							"partner_id":index.other_id,
							"temp_str":""

				}			
			else:
				data_calculation_dict[str_create]["total"]+=round(float(index.total),2)
				data_calculation_dict[str_create]["total_weight"]+=round(float(index.weight),2)
    
    
		#To get deduction amount and payable amount below code is returned
		tds_per_with_pan=0
		tds_per_without_pan=0
		tds_account=0
		vehicle_no=0
		vehicle1=""
		vehicle2=""
		security_aacount=0
		security_per=0
		vehicleA=""
		vehicleB=""
		if self.include_tds:
			tds=frappe.get_all("Branch",filters={'name':self.branch},
												fields=["tds_percentage_value_with","tds_percentage_value_without","tds_account","max_vehicle_limit","vehicle","vehicle1"])
			for t in tds:
				tds_per_with_pan=t.tds_percentage_value_with if(t.tds_percentage_value_with or t.tds_percentage_value_with==0) else frappe.throw("Please set the TDS Percantage Amount in Branch")
				tds_per_without_pan=t.tds_percentage_value_without if(t.tds_percentage_value_without or t.tds_percentage_value_without==0) else frappe.throw("Please set the TDS Percantage Amount in Branch")
				tds_account=t.tds_account if(t.tds_account) else frappe.throw("Please set the TDS Percantage Account in Branch")
				vehicle_no=t.max_vehicle_limit if(t.max_vehicle_limit or t.max_vehicle_limit==0) else frappe.throw("Please set the max no of vehicle on which TDS will apply in Branch")
				vehicle1=t.vehicle if(t.vehicle) else frappe.throw("Please set the vehicle type in Branch for that TDS will not apply")
				vehicle2=t.vehicle1 if(t.vehicle1) else frappe.throw("Please set the vehicle type in Branch for that TDS will not apply ")
    
		if self.include_security_deposite:
			sd=frappe.get_all("Branch",filters={'name':self.branch},
												fields=["vehiclea","vehicleb","security_deposit_account","security_deposite_amt"])
			for t in sd:
				vehicleA=t.vehiclea if(t.vehiclea) else frappe.throw("Please set the vehicle type in Branch for that SD will not apply")
				vehicleB=t.vehicleb if(t.vehicleb) else frappe.throw("Please set the vehicle type in Branch for that SD will not apply")
				security_aacount=t.security_deposit_account if(t.security_deposit_account) else frappe.throw("Please set the Account for Security Deposit Percantage in Branch")
				security_per=t.security_deposite_amt if(t.security_deposite_amt) else frappe.throw("Please set the SD Percentage in Branch")
		contract_dict={}
		for d in data_calculation_dict:
			sales_invoice_deduction_amt=0
			other_deductions_amt=0
			other_deductions=""
			loan_installment_amt=0
			loan_interest_amt=0
			hire_charge_amt=0
			penalty_charge=0
			total_deduction=0
			payable_amt=0
			total_amt=0
			total_of_h_t=0
			tds_deduction_amt_trs=0
			total_amt_tds_cal_trs=0
			total_amt_tds_cal_har=0
			total_amt_sd_cal_har=0
			total_amt_sd_cal_trs=0
			sd_dedution_amt_trs=0
			tds_ded_list_tras=[]
			sd_ded_list_tr=[]
			sales_invoices = []
			other_deduction_dict =[]
			loan_installment=[]
			loan_installment_intrest=[]
			all_deduction = []
			hire_cherge_list=[]
			chart_no_list=[]
			penalty_deuction_li=[]
			penalty_charge=0
			hire_ded_amt=0	
			if(str(data_calculation_dict[d]["contract_id"]) not in contract_dict):
				contract_dict[str(data_calculation_dict[d]["contract_id"])]=[d]
			else:
				contract_dict[str(data_calculation_dict[d]["contract_id"])].append(d)
			if(data_calculation_dict[d]["type"]=="Transporter"):
				#To calculate TDS deduction amount for Transporter
				if self.include_tds:
					count=0
					weight_count=0
					contract = frappe.get_value("H and T Contract",data_calculation_dict[d]["contract_id"],["vehicle_type","total_vehicle"],as_dict=1)
					if(contract.vehicle_type!=str(vehicle1) and contract.vehicle_type!=str(vehicle2)):
						count=int(contract.total_vehicle)
					cane_weight = frappe.get_all("Cane Weight",
                                                filters={"docstatus": 1,"season" : self.season ,"branch" : self.branch,"h_and_t_billing_status":False,"transporter_code":data_calculation_dict[d]["vender_id"]},
                                                fields=["vehicle_type"])
					for c in cane_weight:
						if(c.vehicle_type!=str(vehicle1) and c.vehicle_type!=str(vehicle2)):
							weight_count+=1
					if(count>vehicle_no and weight_count>vehicle_no):
						if(data_calculation_dict[d]["vehicle_type"]!=str(vehicle1) and  data_calculation_dict[d]["vehicle_type"]!=str(vehicle2)):
							pancard=0
							total_amt_tds_cal_trs=data_calculation_dict[d]["total"]
							farmer=frappe.get_doc("Farmer List",data_calculation_dict[d]["vender_id"],["pan_number"],as_dict=1)
							if(farmer.pan_number):
								pancard=1
							if(pancard):	
								tds_deduction_amt_trs=total_amt_tds_cal_trs*tds_per_with_pan/100
							else:
								tds_deduction_amt_trs=total_amt_tds_cal_trs*tds_per_without_pan/100
							tds_ded_list_tras=[{"Farmer Code": data_calculation_dict[d]["vender_id"],"TDS Deduction Amount":round(float(tds_deduction_amt_trs),2),"Account": tds_account,"Contract Id":data_calculation_dict[d]["contract_id"],"Deduction Name":"TDS"}]
							
				#To calculate hire charge deduction amount for Transporter
				if self.include_hire_charges:
					if(data_calculation_dict[d]["cartno"]):
						vehicle_1=""
						vehicle_2=""
						cart_no=0
						vehicle_charge1=0
						vehicle_charge2=0
						days=0
						hire_account=""
						hire_charge=frappe.get_all("Branch",filters={'name':self.branch},
													fields=["vehiclec","vehicled","hire_charge1","hire_charge_2","hire_charge_account"])
						for i in hire_charge:
							vehicle_1=str(i.vehiclec) if(i.vehiclec) else frappe.throw("Please set the Vehicle type on which hire charge will apply")
							vehicle_charge1=i.hire_charge1 if(i.hire_charge1 or i.hire_charge1==0 ) else frappe.throw(f"Please set the hire charge for vehicle {vehicle_1} ")
							vehicle_2=str(i.vehicled) if(i.vehicled) else frappe.throw("Please set the Vehicle type on which hire charge will apply")
							vehicle_charge2=i.hire_charge_2 if(i.hire_charge_2 or int(i.hire_charge_2)==0 )else frappe.throw(f"Please set the hire charge for vehicle {vehicle_2} ")
							hire_account=str(i.hire_charge_account) if(i.hire_charge_account) else frappe.throw("Please set the Hire charge Account")
						cart_no=int(data_calculation_dict[d]["cartno"])
						vehicle = frappe.db.get_list("Vehicle Registration",
												filters={"season" : self.season ,"vehicle_type":data_calculation_dict[d]["vehicle_type"],"h_and_t_contract":data_calculation_dict[d]["contract_id"]},
												fields=["name"],)
						for i in vehicle:
							chart_table = frappe.get_all("Vehicle Registration item",filters={"parent":i.name},fields=["cart_no","updated_issue","issue_date"])
							for rows in chart_table:
								if str(rows.cart_no)==str(cart_no):
									if(rows.updated_issue):
										chart_no_list.append(str(i.name))
										chart_no_list.append(str(cart_no))
										date1 = datetime.strptime(str(rows.updated_issue), '%Y-%m-%d')
										date2 = datetime.strptime(str(self.to_date), '%Y-%m-%d')
										delta = date2 - date1
										days = delta.days
									else:
										issue_date=rows.issue_date if(rows.issue_date) else frappe.throw(f"Please set the Vehicle Issue date in Vehicle Registration for Contract {data_calculation_dict[d]['contract_id']}")
										chart_no_list.append(str(i.name))
										chart_no_list.append(str(cart_no))
										date1 = datetime.strptime(str(issue_date), '%Y-%m-%d')
										date2 = datetime.strptime(str(self.to_date), '%Y-%m-%d')
										delta = date2 - date1
										days = delta.days
						
						count=0
						if  data_calculation_dict[d]["vehicle_type"]==vehicle_1:
							hire_ded_amt=vehicle_charge1*days
							count=1
						if  data_calculation_dict[d]["vehicle_type"]==vehicle_2:
							hire_ded_amt=vehicle_charge2*days
							count=1
						if count==1:
							data_calculation_dict[d]["cart_no_list"]=str(chart_no_list)
							data_calculation_dict[d]["hire_acc"]=str(hire_account)
							hire_charge_amt=hire_ded_amt
							hire_cherge_list=[{"Farmer Code": data_calculation_dict[d]["vender_id"],"Hire Charge Amount": round(float(hire_ded_amt),2),"Account": hire_account,"Contract Id":data_calculation_dict[d]["contract_id"],"Deduction Name":"Hire Charge"}] 
							
				#To calculate SD deduction amount for Transporter
				if self.include_security_deposite:
					if data_calculation_dict[d]["vehicle_type"]!=str(vehicleA) and  data_calculation_dict[d]["vehicle_type"]!=str(vehicleB):
						total_amt_sd_cal_trs=data_calculation_dict[d]["total"]
						sd_dedution_amt_trs=total_amt_sd_cal_trs*security_per/100
						sd_ded_list_tr=[{"Farmer Code": data_calculation_dict[d]["vender_id"],"SD Deduction Amount": round(float(sd_dedution_amt_trs),2),"Account": security_aacount,"Contract Id":data_calculation_dict[d]["contract_id"],"Deduction Name":"Security Deposit"}]
						
   			#To get the dedution amount for Harvester
			if(data_calculation_dict[d]["type"]=="Harvester"):
				temp_str=""
				for index in data_calculation_dict:
					if(data_calculation_dict[index]!=data_calculation_dict[d] and data_calculation_dict[d]["contract_id"]==data_calculation_dict[index]["contract_id"] and  data_calculation_dict[d]["partner_id"]==data_calculation_dict[index]["contract_id"] ):
						temp_str=index
						break
				if temp_str:
					data_calculation_dict[d]["temp_str"]=str(temp_str)
					data_calculation_dict[d]["transporter"]=data_calculation_dict[temp_str]["vender_id"]
					data_calculation_dict[temp_str]["transporter"]=data_calculation_dict[d]["vender_id"]
				#To calculate TDS deduction amount for Harvester
				if self.include_tds:
					if data_calculation_dict[d]["vehicle_type"]!=str(vehicle1) and  data_calculation_dict[d]["vehicle_type"]!=str(vehicle2):
						pancard=0
						total_amt_tds_cal_har=data_calculation_dict[d]["total"]
						farmer=frappe.get_all("Farmer List",
																	filters={"branch" : self.branch,"name":data_calculation_dict[d]["vender_id"]},
																			fields=["pan_number"])
						for i in farmer:
							if(i.pan_number):
								pancard=1
						if(pancard):	
							tds_deduction_amt_trs=total_amt_tds_cal_har*tds_per_with_pan/100
						else:
							tds_deduction_amt_trs=total_amt_tds_cal_har*tds_per_without_pan/100
						tds_ded_list_tras=[{"Farmer Code": data_calculation_dict[d]["vender_id"],"TDS Deduction Amount":round(float(tds_deduction_amt_trs),2),"Account": tds_account,"Contract Id":data_calculation_dict[d]["contract_id"],"Deduction Name":"TDS"}]
				#To calculate SD deduction amount for Harvester
				if self.include_security_deposite:
						if data_calculation_dict[d]["vehicle_type"]!=str(vehicleA) and  data_calculation_dict[d]["vehicle_type"]!=str(vehicleB):
							total_amt_sd_cal_har=data_calculation_dict[d]["total"]
							sd_dedution_amt_trs=total_amt_sd_cal_har*security_per/100
							sd_ded_list_tr=[{"Farmer Code": data_calculation_dict[d]["vender_id"],"SD Deduction Amount":round(float(sd_dedution_amt_trs),2),"Account": security_aacount,"Contract Id":data_calculation_dict[d]["contract_id"],"Deduction Name":"Security Deposit"}]
			other_deductions = frappe.get_all("Deduction Form",
																	filters={"h_and_t_contract_id":data_calculation_dict[d]["contract_id"],"docstatus":1, "season" : self.season , "deduction_status" : 0,"branch" : self.branch,"deduction_name":["!=", "Penalty"] },
																	fields=["farmer_code", "account", "name", "deduction_amount","paid_amount" ,"h_and_t_contract_id", "farmer_application_loan_id","interest_calculate_on_amount", "rate_of_interest" , "from_date_interest_calculation","interest_account" ,"update_from_date_interest_calculation"],)
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
											for o_i in other_deductions if o_i.farmer_application_loan_id and o_i.from_date_interest_calculation and (round((float(o_i.deduction_amount) - float(o_i.paid_amount)),2)) != 0]
				installment_ded=[]
				if int(len(contract_dict[str(data_calculation_dict[d]["contract_id"])]))>1:
					for i in range(len(contract_dict[str(data_calculation_dict[d]["contract_id"])])):
						if(str(d)!=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])):
							index=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])
							formatted_input = re.sub(r'\]\[', '],[', str(data_calculation_dict[index]["all_deduction_information"]))
							formatted_input = '[' + formatted_input + ']'
							parsed_list = ast.literal_eval(formatted_input)
							if(len(parsed_list)>=8):
								installment_ded=parsed_list[2]
								if(installment_ded):
									for j in loan_installment_intrest:
										for k in installment_ded:
											if(j["Farmer Loan ID"] == k["Farmer Loan ID"] ):
												j["Installment Interest Amount"]=j["Installment Interest Amount"]-k["Installment Interest Amount"]
										loan_installment_intrest = [m for m in loan_installment_intrest if m["Installment Interest Amount"] != 0]
				loan_interest_amt = sum(float(m["Installment Interest Amount"]) for m in loan_installment_intrest)
				
			if self.includes_sales_invoice_deduction: 
				deduction_doc = frappe.get_all("Sales Invoice",
																filters={"h_and_t_contract":data_calculation_dict[d]["contract_id"],"status": ["in", ["Unpaid", "Overdue", "Partly Paid"]],},
																		fields=["outstanding_amount", "customer", "name", "debit_to","h_and_t_contract"],)
				
				sales_invoices=[{"Sales invoice ID": d_d.name,"Outstanding Amount": d_d.outstanding_amount,"Account": d_d.debit_to,"Contract Id":d_d.h_and_t_contract}for d_d in deduction_doc]  # in this list all sales invoice will recored with there accound and outstanding_amount info
				sales_invoice_ded=[]
				if int(len(contract_dict[str(data_calculation_dict[d]["contract_id"])]))>1:
					for i in range(len(contract_dict[str(data_calculation_dict[d]["contract_id"])])):
						if(str(d)!=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])):
							index=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])
							formatted_input = re.sub(r'\]\[', '],[', str(data_calculation_dict[index]["all_deduction_information"]))
							formatted_input = '[' + formatted_input + ']'
							parsed_list = ast.literal_eval(formatted_input)
							if(len(parsed_list)>=8):
								sales_invoice_ded=parsed_list[0]
								if(sales_invoice_ded):
									for j in sales_invoices:
										for k in sales_invoice_ded:
											if(j["Sales invoice ID"] == k["Sales invoice ID"] ):
												j["Outstanding Amount"]=j["Outstanding Amount"]-k["Outstanding Amount"]
									sales_invoices = [m for m in sales_invoices if m["Outstanding Amount"] != 0]
				sales_invoice_deduction_amt= sum(float(d["Outstanding Amount"]) for d in sales_invoices)  # calculating sum of all sales invoice	
				
			if self.other_deduction:
				other_deduction_dict=[{"Farmer Code": o_d.farmer_code,"Deduction Amount": round((float(o_d.deduction_amount) - float(o_d.paid_amount)),2),"Account": o_d.account,"DFN": o_d.name,"Contract Id":o_d.h_and_t_contract_id}for o_d in other_deductions if not o_d.farmer_application_loan_id ]
				other_ded=[]
				if int(len(contract_dict[str(data_calculation_dict[d]["contract_id"])]))>1:
					for i in range(len(contract_dict[str(data_calculation_dict[d]["contract_id"])])):
						if(str(d)!=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])):
							index=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])
							formatted_input = re.sub(r'\]\[', '],[', str(data_calculation_dict[index]["all_deduction_information"]))
							formatted_input = '[' + formatted_input + ']'
							parsed_list = ast.literal_eval(formatted_input)
							if(len(parsed_list)>=8):
								other_ded=parsed_list[3]
								if(other_ded):
									for j in other_deduction_dict:
										for k in other_ded:
											if(j["DFN"] == k["DFN"] ):
												j["Deduction Amount"]=j["Deduction Amount"]-k["Deduction Amount"]
									other_deduction_dict = [m for m in other_deduction_dict if m["Deduction Amount"] != 0]
				other_deductions_amt=sum(float(g["Deduction Amount"]) for g in other_deduction_dict)
				
			if self.includes_loan_installment:
				loan_installment = [{"Farmer Loan ID": o_l.farmer_application_loan_id, "Farmer ID": o_l.farmer_code , "season": self.season, "Account": o_l.account, "Installment Amount": round((float(o_l.deduction_amount) - float(o_l.paid_amount)),2),"Contract Id":o_l.h_and_t_contract_id }for o_l in other_deductions if o_l.farmer_application_loan_id and (round((float(o_l.deduction_amount) - float(o_l.paid_amount)),2)) != 0 ]
				loan_inst_ded=[]
				if int(len(contract_dict[str(data_calculation_dict[d]["contract_id"])]))>1:
					for i in range(len(contract_dict[str(data_calculation_dict[d]["contract_id"])])):
						if(str(d)!=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])):
							index=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])
							formatted_input = re.sub(r'\]\[', '],[', str(data_calculation_dict[index]["all_deduction_information"]))
							formatted_input = '[' + formatted_input + ']'
							parsed_list = ast.literal_eval(formatted_input)
							if(len(parsed_list)>=8):
								loan_inst_ded=parsed_list[1]
								if(loan_inst_ded):
									for j in loan_installment:
										for k in loan_inst_ded:
											if(j["Farmer Loan ID"] == k["Farmer Loan ID"] ):
												j["Installment Amount"]=j["Installment Amount"]-k["Installment Amount"]
									loan_installment = [m for m in loan_installment if m["Installment Amount"] != 0]	
				loan_installment_amt = sum(float(j["Installment Amount"]) for j in loan_installment)
			
			if self.include_penalty_charges:
					panalty = frappe.get_all("Deduction Form",
																	filters={"farmer_code":data_calculation_dict[d]["vender_id"],"h_and_t_contract_id":data_calculation_dict[d]["contract_id"],"deduction_name":"Penalty","docstatus":1, "season" : self.season , "deduction_status" : 0,"branch" : self.branch },
																	fields=["farmer_code", "account", "name", "deduction_amount","paid_amount" ,"h_and_t_contract_id","farmer_application_loan_id"],)
					penalty_deuction_li=[{"Farmer Code": o_d.farmer_code,"Penalty Amount": round((float(o_d.deduction_amount) - float(o_d.paid_amount)),2),"Account": o_d.account,"DFN": o_d.name,"Contract Id":o_d.h_and_t_contract_id}for o_d in panalty if not o_d.farmer_application_loan_id ]
					other_ded=[]
					if int(len(contract_dict[str(data_calculation_dict[d]["contract_id"])]))>1:
						for i in range(len(contract_dict[str(data_calculation_dict[d]["contract_id"])])):
							if(str(d)!=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i]) and data_calculation_dict[d]["vender_id"]==data_calculation_dict[str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])]["vender_id"]):
								index=str(contract_dict[str(data_calculation_dict[d]["contract_id"])][i])
								formatted_input = re.sub(r'\]\[', '],[', str(data_calculation_dict[index]["all_deduction_information"]))
								formatted_input = '[' + formatted_input + ']'
								parsed_list = ast.literal_eval(formatted_input)
								if(len(parsed_list)>=8):
									other_ded=parsed_list[7]
									if(other_ded):
										for j in penalty_deuction_li:
											for k in other_ded:
												if(j["DFN"] == k["DFN"] ):
													j["Penalty Amount"]=j["Penalty Amount"]-k["Penalty Amount"]
										penalty_deuction_li = [m for m in penalty_deuction_li if m["Penalty Amount"] != 0]
					penalty_charge=sum(float(g["Penalty Amount"]) for g in penalty_deuction_li)
			total_deduction = (sales_invoice_deduction_amt+ loan_installment_amt+ loan_interest_amt+other_deductions_amt+round(float(tds_deduction_amt_trs),2)+round(float(sd_dedution_amt_trs),2)+round(float(hire_ded_amt),2)+round(float(penalty_charge),2))
			total_amt=data_calculation_dict[d]["total"]
			payable_amt=total_amt-total_deduction
			if(payable_amt>=0):
				data_calculation_dict[d]["deduction"]=round(float(total_deduction),2)
			else:
				doc_acc = frappe.get_all("Child Account Priority For H and T",
													filters={"parent": self.branch},
													fields={"priority_account", "idx"},order_by="idx ASC")  # frappe.msgprint(str(doc_acc))  #$$$$$
				all_deduction =(loan_installment_intrest + loan_installment + sales_invoices+other_deduction_dict+tds_ded_list_tras+sd_ded_list_tr+hire_cherge_list+penalty_deuction_li)  # frappe.msgprint(str(all_deduction))
				all_deduction = sorted(all_deduction,key=lambda x: next((item["idx"] for item in doc_acc if item["priority_account"] == x["Account"]),len(doc_acc) + 1,),)
				total_of_h_t=total_amt
				while float(total_of_h_t) <= float(total_deduction):
					last_poped_entry = all_deduction.pop(-1)
					total_sum = float(sum([
											float(entry.get("Installment Interest Amount", 0))
											+ float(entry.get("Installment Amount", 0))
										+ float(entry.get("Outstanding Amount", 0))
											+ float(entry.get("Deduction Amount", 0))
											+ float(entry.get("TDS Deduction Amount", 0))
											+ float(entry.get("SD Deduction Amount", 0))
											+ float(entry.get("Hire Charge Amount", 0))
											+ float(entry.get("Penalty Amount", 0))
											for entry in all_deduction 
										]))

					total_deduction = round(float(total_sum), 2)
					total_payable = float(total_of_h_t)-float(total_deduction)

				contains_key = next((key for key in ["Outstanding Amount","Installment Amount","Installment Interest Amount","Deduction Amount","Hire Charge Amount","Penalty Amount"] if key in last_poped_entry),None,)
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

				if (str(contains_key))== "Hire Charge Amount":
					paid_amount =round(float(total_payable),2)
					total_deduction =round(( float(total_deduction)+ float(total_payable)),2)
					total_payable=0
					last_poped_entry['Hire Charge Amount'] = paid_amount
					all_deduction.append(last_poped_entry)
     
				if (str(contains_key))== "Penalty Amount":
					paid_amount =round(float(total_payable),2)
					total_deduction =round(( float(total_deduction)+ float(total_payable)),2)
					total_payable=0
					last_poped_entry['Penalty Amount'] = paid_amount
					all_deduction.append(last_poped_entry)
     
				if (str(contains_key)) == "Deduction Amount":
					new_other_deduction_amount = round(float(total_payable), 2)
					total_deduction = round((float(total_deduction) + float(total_payable)), 2)
					total_payable = 0
					last_poped_entry["Deduction Amount"] = new_other_deduction_amount
					all_deduction.append(last_poped_entry)
					
				
				data_calculation_dict[d]["deduction"]=round(float(total_deduction),2)
				
				loan_installment_amt = sum(float(record['Installment Amount']) for record in all_deduction if 'Installment Amount' in record)
				loan_interest_amt = sum(float(record['Installment Interest Amount']) for record in all_deduction if 'Installment Interest Amount' in record)
				sales_invoice_deduction_amt = sum(float(record['Outstanding Amount']) for record in all_deduction if 'Outstanding Amount' in record)
				other_deductions_amt = sum(float(record['Deduction Amount']) for record in all_deduction if 'Deduction Amount' in record)
				hire_ded_amt=sum(float(record['Hire Charge Amount']) for record in all_deduction if 'Hire Charge Amount' in record)
				penalty_charge=sum(float(record['Penalty Amount']) for record in all_deduction if 'Penalty Amount' in record)

				loan_installment = [record for record in all_deduction if 'Installment Amount' in record]
				loan_installment_intrest = [record for record in all_deduction if 'Installment Interest Amount' in record]
				sales_invoices = [record for record in all_deduction if 'Outstanding Amount' in record]
				other_deduction_dict = [record for record in all_deduction if 'Deduction Amount' in record]
				hire_cherge_list=[record for record in all_deduction if 'Hire Charge Amount' in record]
				penalty_deuction_li=[record for record in all_deduction if 'Penalty Amount' in record]

			data_calculation_dict[d]["sales_invoice_deduction"]=float(sales_invoice_deduction_amt)
			data_calculation_dict[d]["other_deductions"]=float(other_deductions_amt)
			data_calculation_dict[d]["lone_deduction"]=float(loan_installment_amt)
			data_calculation_dict[d]["loan_interest_deduction"]=float(loan_interest_amt)
			data_calculation_dict[d]["penalty_charge"]=round(float(penalty_charge),2)
			data_calculation_dict[d]["hire_charge"]=round(float(hire_ded_amt),2)
			for j in tds_ded_list_tras:
				data_calculation_dict[d]["tds_deduction"]=float(j["TDS Deduction Amount"])
			for j in sd_ded_list_tr:
				data_calculation_dict[d]["sd_deduction"]=float(j["SD Deduction Amount"])
			if hire_charge_amt:
				data_calculation_dict[d]["remaining_hire"]=hire_charge_amt-hire_ded_amt
			data_calculation_dict[d]["all_deduction_information"]=str(sales_invoices)+str(loan_installment)+str(loan_installment_intrest)+str(other_deduction_dict)+str(tds_ded_list_tras)+str(sd_ded_list_tr)+str(hire_cherge_list)+str(penalty_deuction_li)
	
			if(data_calculation_dict[d]["vehicle_type"]=="BULLOCK CART" and data_calculation_dict[d]["type"]=="Harvester" and data_calculation_dict[d]["transporter"]==data_calculation_dict[d]["vender_id"]):
				if data_calculation_dict[d]["temp_str"]:
					temp_str=data_calculation_dict[d]["temp_str"]
					data_calculation_dict[d]["other_collection"]=data_calculation_dict[temp_str]["total"]
					data_calculation_dict[d]["other_deduction"]=data_calculation_dict[temp_str]["deduction"]
					data_calculation_dict[temp_str]["other_collection"]=data_calculation_dict[d]["total"]
					data_calculation_dict[temp_str]["other_deduction"]=data_calculation_dict[d]["deduction"]
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
							"vehicle_type":data_calculation_dict[d]["vehicle_type"],
							"deduction":round(float(data_calculation_dict[d]["deduction"]),2),
							"payable_amt":round((float(data_calculation_dict[d]["total"])-float(data_calculation_dict[d]["deduction"])),2),
							"sales_invoice_deduction":round(float(data_calculation_dict[d]["sales_invoice_deduction"]),2),
							"other_deductions":round(float(data_calculation_dict[d]["other_deductions"]),2),
							"lone_deduction":round(float(data_calculation_dict[d]["lone_deduction"]),2),
							"loan_interest_deduction":round(float(data_calculation_dict[d]["loan_interest_deduction"]),2),
							"all_deduction_information":data_calculation_dict[d]["all_deduction_information"],
							"tds_deduction":round(float(data_calculation_dict[d]["tds_deduction"]),2),
							"sd_deduction":round(float(data_calculation_dict[d]["sd_deduction"]),2),
							"cartno":data_calculation_dict[d]["cartno"],
							"hire_charge":round(float(data_calculation_dict[d]["hire_charge"]),2),
							"remaining_hire_charge":data_calculation_dict[d]["remaining_hire"],
							"hire_account":str(data_calculation_dict[d]["hire_acc"]),
							"cart_no_list":str(	data_calculation_dict[d]["cart_no_list"]),
							"transporter":str(data_calculation_dict[d]["transporter"]),
							"penalty_charge":round(float(data_calculation_dict[d]["penalty_charge"]),2),
							"other_collection":round(float(data_calculation_dict[d]["other_collection"]),2),
							"other_deduction":round(float(data_calculation_dict[d]["other_deduction"]),2),
							"partner_id":data_calculation_dict[d]["partner_id"]
						}
			)
		self.total_values()

	#To get Net Deduction and collection for Transporter and Harvester
	def total_values(self):
		total_weight = 0
		total_collection_amount = 0
		total_deduction = 0
		total_payable_amount = 0
		total_weight_har=0
		total_collection_amount_har=0
		total_deduction_har=0
		total_payable_amount_har=0
		total_weight_bul = 0
		total_collection_amount_bul = 0
		total_deduction_bul = 0
		total_payable_amount_bul = 0
		totals=self.get("calculation_table")
		for d in totals:
			if(d.type=="Transporter"):
				total_weight = total_weight+round(float(d.total_weight),2)
				total_collection_amount = total_collection_amount+round(float(d.total),2)
				total_deduction = total_deduction+round(float(d.deduction),2)
				total_payable_amount = total_payable_amount+round(float(d.payable_amt),2)
			if(d.type=="Harvester"):
				total_weight_har= total_weight_har+round(float(d.total_weight),2)
				total_collection_amount_har= total_collection_amount_har+round(float(d.total),2)
				total_deduction_har = total_deduction_har+round(float(d.deduction),2)
				total_payable_amount_har= total_payable_amount_har+round(float(d.payable_amt),2)
			if(d.vehicle_type=="BULLOCK CART"):
				total_weight_bul= total_weight_bul+round(float(d.total_weight),2)
				total_collection_amount_bul= total_collection_amount_bul+round(float(d.total),2)
				total_deduction_bul = total_deduction_bul+round(float(d.deduction),2)
				total_payable_amount_bul= total_payable_amount_bul+round(float(d.payable_amt),2)
				
		self.new_total_weight = total_weight
		self.net_total_collection_amountrs = total_collection_amount
		self.net_total_deductionrs = total_deduction
		self.net_total_payable_amountrs = total_payable_amount
  
		self.net_total_weight_har=total_weight_har
		self.net_total_coll_har=total_collection_amount_har
		self.net_total_ded_har=total_deduction_har
		self.net_total_pay_har=total_payable_amount_har
  

		self.net_total_wight_bul=total_weight_bul
		self.net_total_collection_bul=total_collection_amount_bul
		self.net_total_ded_bul=total_deduction_bul
		self.net_total_pay_bul=total_payable_amount_bul
  

	#To get the km rate 
	def get_rate(self,distance,vehicle_type,vender_type):
		dict1={}
		count=True
		if(vender_type=="Transporter"):
			doc=frappe.db.get_list("Transporter Rate Chart",
													filters={"season" : self.season ,"branch" : self.branch, "vehicle_type":vehicle_type},
												fields=["name","per_km_rate"])
			for i in doc:
				rate_per_km=i.get("per_km_rate")
				chart_table = frappe.get_all("Child Rate Chart",filters={"parent":i.name},fields=["distance","rate"])
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
			rate_per_km=0
			doc=frappe.db.get_list("Harvester Rate Chart",
													filters={"season" : self.season ,"branch" : self.branch, "vehicle_type":vehicle_type},
												fields=["name","per_km_rate"])
			for i in doc:
				rate_per_km=i.get("per_km_rate")
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
		self.delete_hire_ded()
		self.delete_issue_date()
  
	def cancel_journal_entry(self):
		if(self.journal_entry_id):
			doc = frappe.get_doc("Journal Entry",(str(self.journal_entry_id)))
			if doc.docstatus == 1:
				doc.cancel()
		
	def bill_status_change_of_cane_weight_on_trash(self):
		for s in self.get("calculation_table"):
			if(s.type=="Transporter"):
				doc = frappe.db.get_list("Cane Weight",
														filters={"date": ["between", [self.from_date, self.to_date]],"season" : self.season ,"branch" : self.branch,"h_and_t_billing_status":True,"contract_id":s.contract_id},
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
			list_data_pen=[]
			formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
			formatted_input = '[' + formatted_input + ']'
			parsed_list = ast.literal_eval(formatted_input)
			list_data_od=eval(str(parsed_list))
			list_data_od=list_data_od[3]
			list_data_pen=eval(str(parsed_list))
			list_data_pen=list_data_pen[7]
			if(list_data_od):
				for data_od in list_data_od:
					doc=frappe.get_doc("Deduction Form",str(data_od['DFN']))
					frappe.db.set_value("Deduction Form",str(data_od['DFN']),"paid_amount",(float(doc.paid_amount)-(float(data_od['Deduction Amount']))))
					frappe.db.set_value("Deduction Form",str(data_od['DFN']),"deduction_status",0)
			if(list_data_pen):
				for data_od in list_data_pen:
					doc=frappe.get_doc("Deduction Form",str(data_od['DFN']))
					frappe.db.set_value("Deduction Form",str(data_od['DFN']),"paid_amount",(float(doc.paid_amount)-(float(data_od['Penalty Amount']))))
					frappe.db.set_value("Deduction Form",str(data_od['DFN']),"deduction_status",0)


	def je_of_sales_invoice_and_farmer_loan(self):
		counter =0
		bench_doc=frappe.get_doc("Branch",self.branch)
		if bench_doc:
			if not (bench_doc.company):
				frappe.throw( f" Please set Company for Branch '{str(self.branch) } '")	
			if not (bench_doc.cane_transport_charges_):
				frappe.throw( f" Please set Cane Transport charges Account for Branch '{str(self.branch) } '")
			if not (bench_doc.cane_harvest_charges):
				frappe.throw( f" Please set Cane Harvesting Charges Account for Branch '{str(self.branch) } '")
			if not (bench_doc.debit_in_account_harvesting_billing):
				frappe.throw( f" Please set Debit In Account for Harvesting Billing for Branch '{str(self.branch) } '")
			if not (bench_doc.debit_in_account_bc_billing):
				frappe.throw( f" Please set Debit In Account for BC Billing for Branch '{str(self.branch) } '")
			if not (bench_doc.debit_in_account_h_and_t_):
				frappe.throw( f" Please Set Debit In Account for Transporter Billing for Branch '{str(self.branch) } '")
			company = bench_doc.company
			cane_charge=bench_doc.cane_transport_charges_
			caneharcharge = bench_doc.cane_harvest_charges
			acc_to_set_debit_har=bench_doc.debit_in_account_harvesting_billing
			acc_to_set_debit_side = bench_doc.debit_in_account_h_and_t_
			debit_in_account_bc_billing=bench_doc.debit_in_account_bc_billing
		je = frappe.new_doc("Journal Entry")
		je.voucher_type = "Journal Entry"
		je.company = company
		je.posting_date = self.today
		for s in self.get("calculation_table"):
			list_data_se = []
			list_data_lo = []
			list_data_li = []
			list_data_od = []
			list_data_sd=[]
			list_data_tds=[]
			list_data_hr=[]
			list_data_pen=[]
			parsed_list=""
			if s.deduction:
				counter = counter + 1
				formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
				formatted_input = '[' + formatted_input + ']'
				parsed_list = ast.literal_eval(formatted_input)
				list_data_se=parsed_list[0]
				list_data_lo=parsed_list[1]
				list_data_li=parsed_list[2]
				list_data_od=parsed_list[3]
				list_data_tds=parsed_list[4]
				list_data_sd=parsed_list[5]
				list_data_hr=parsed_list[6]
				list_data_pen=parsed_list[7]
				if(s.type=="Transporter" and s.vehicle_type=="BULLOCK CART" and s.transporter==s.vender_id and s.partner_id==s.contract_id):
					total_ded=round(float(s.deduction),2)+round(float(s.other_deduction),2)
					total_colle=round(float(s.total),2)+round(float(s.other_collection),2)
					je.append(
						"accounts",
						{
							"account":str(cane_charge) ,
							"debit_in_account_currency":total_colle,				
					},)
					je.append(
							"accounts",
							{
								"account": debit_in_account_bc_billing,
								"party_type": "Supplier",
								"party": s.vender_id,
								"credit_in_account_currency":total_colle,
								"contract_id":s.contract_id
								
					},)
					je.append(
							"accounts",
							{
								"account": debit_in_account_bc_billing,
								"party_type": "Supplier",
								"party": s.vender_id,
								"debit_in_account_currency":total_ded,
								"contract_id":s.contract_id
								
					},)
					for k in self.get("calculation_table"):
						if(k.vehicle_type=="BULLOCK CART" and k.vender_id==s.vender_id and k.contract_id==s.contract_id):
							counter = counter + 1
							formatted_input = re.sub(r'\]\[', '],[', k.all_deduction_information)
							formatted_input = '[' + formatted_input + ']'
							parsed_list = ast.literal_eval(formatted_input)
							list_data_se=parsed_list[0]
							list_data_lo=parsed_list[1]
							list_data_li=parsed_list[2]
							list_data_od=parsed_list[3]
							list_data_tds=parsed_list[4]
							list_data_sd=parsed_list[5]
							list_data_hr=parsed_list[6]
							list_data_pen=parsed_list[7]
							if list_data_se:
								for data_se in list_data_se:
									if int(data_se["Outstanding Amount"]) != 0:
										if(s.type=="Harvester"):
											cont_doc=frappe.get_doc("H and T Contract",s.contract_id)
											je.append(
												"accounts",
												{
													"account":data_se["Account"],
													"party_type": "Customer",
													"party":cont_doc.transporter_code ,
													"credit_in_account_currency": data_se["Outstanding Amount"],
													"reference_type": "Sales Invoice",
													"reference_name": data_se["Sales invoice ID"],
													"contract_id":s.contract_id
												},)
										else:
											je.append(
												"accounts",
												{
													"account":data_se["Account"],
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

							if list_data_tds:
								for data_od in list_data_tds:
									if int(data_od["TDS Deduction Amount"]) != 0:
										je.append(
											"accounts",
											{
												"account": data_od["Account"],
												"party_type": "Supplier",
												"party": s.vender_id,
												"credit_in_account_currency": data_od["TDS Deduction Amount"],
												"contract_id":s.contract_id
											},) 
							if list_data_sd:
								for data_od in list_data_sd:
									if int(data_od["SD Deduction Amount"]) != 0:
										je.append(
											"accounts",
											{
												"account": data_od["Account"],
												"party_type": "Supplier",
												"party": s.vender_id,
												"credit_in_account_currency": data_od["SD Deduction Amount"],
												"contract_id":s.contract_id
											},) 
							if list_data_hr:
								for data_od in list_data_hr:
									if int(data_od["Hire Charge Amount"]) != 0:
										je.append(
											"accounts",
											{
												"account": data_od["Account"],
												"party_type": "Supplier",
												"party": s.vender_id,
												"credit_in_account_currency": data_od["Hire Charge Amount"],
												"contract_id":s.contract_id
											},) 
							if list_data_pen:
								for data_od in list_data_pen:
									if int(data_od["Penalty Amount"]) != 0:
										je.append(
											"accounts",
											{
												"account": data_od["Account"],
												"party_type": "Supplier",
												"party": s.vender_id,
												"credit_in_account_currency": data_od["Penalty Amount"],
												"contract_id":s.contract_id
											},) 
				else:
					if(s.vehicle_type!="BULLOCK CART"):
						if(s.type=="Transporter"):	
							je.append(
							"accounts",
							{
								"account":str(cane_charge) ,
								"debit_in_account_currency": s.total,				
							},)
							je.append(
								"accounts",
								{
									"account":acc_to_set_debit_side,
									"party_type": "Supplier",
									"party": s.vender_id,
									"credit_in_account_currency": s.total,
									"contract_id":s.contract_id
									
								},)
							je.append(
								"accounts",
								{
									"account":acc_to_set_debit_side,
									"party_type": "Supplier",
									"party": s.vender_id,
									"debit_in_account_currency": s.deduction,
									"contract_id":s.contract_id
									
								},)
							
						else:
							je.append(
							"accounts",
							{
								"account":str(caneharcharge) ,
								"debit_in_account_currency": s.total,				
							},)
							je.append(
								"accounts",
								{
									"account":acc_to_set_debit_har,
									"party_type": "Supplier",
									"party": s.vender_id,
									"credit_in_account_currency": s.total,
									"contract_id":s.contract_id
									
								},)
							je.append(
								"accounts",
								{
									"account":acc_to_set_debit_har,
									"party_type": "Supplier",
									"party": s.vender_id,
									"debit_in_account_currency": s.deduction,
									"contract_id":s.contract_id
									
								},)
				if(s.vehicle_type!="BULLOCK CART"):
					if list_data_se:
						for data_se in list_data_se:
							if int(data_se["Outstanding Amount"]) != 0:
								if(s.type=="Harvester"):
									cont_doc=frappe.get_doc("H and T Contract",s.contract_id)
									je.append(
										"accounts",
										{
											"account":data_se["Account"],
											"party_type": "Customer",
											"party": cont_doc.transporter_code,
											"credit_in_account_currency": data_se["Outstanding Amount"],
											"reference_type": "Sales Invoice",
											"reference_name": data_se["Sales invoice ID"],
											"contract_id":s.contract_id
										},)
								else:
									je.append(
										"accounts",
										{
											"account":data_se["Account"],
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

					if list_data_tds:
						for data_od in list_data_tds:
							if int(data_od["TDS Deduction Amount"]) != 0:
								je.append(
									"accounts",
									{
										"account": data_od["Account"],
										"party_type": "Supplier",
										"party": s.vender_id,
										"credit_in_account_currency": data_od["TDS Deduction Amount"],
										"contract_id":s.contract_id
									},) 
					if list_data_sd:
						for data_od in list_data_sd:
							if int(data_od["SD Deduction Amount"]) != 0:
								je.append(
									"accounts",
									{
										"account": data_od["Account"],
										"party_type": "Supplier",
										"party": s.vender_id,
										"credit_in_account_currency": data_od["SD Deduction Amount"],
										"contract_id":s.contract_id
									},) 
					if list_data_hr:
						for data_od in list_data_hr:
							if int(data_od["Hire Charge Amount"]) != 0:
								je.append(
									"accounts",
									{
										"account": data_od["Account"],
										"party_type": "Supplier",
										"party": s.vender_id,
										"credit_in_account_currency": data_od["Hire Charge Amount"],
										"contract_id":s.contract_id
									},) 
					if list_data_pen:
						for data_od in list_data_pen:
							if int(data_od["Penalty Amount"]) != 0:
								je.append(
									"accounts",
									{
										"account": data_od["Account"],
										"party_type": "Supplier",
										"party": s.vender_id,
										"credit_in_account_currency": data_od["Penalty Amount"],
										"contract_id":s.contract_id
									},) 
				
			else:
				counter = counter + 1
				if(s.type=="Transporter" and s.vehicle_type=="BULLOCK CART" and s.transporter==s.vender_id and s.partner_id==s.contract_id):
					total_colle=round(float(s.total),2)+round(float(s.other_collection),2)
					je.append(
						"accounts",
						{
							"account":str(cane_charge) ,
							"debit_in_account_currency":total_colle,				
					},)
					je.append(
							"accounts",
							{
								"account": debit_in_account_bc_billing,
								"party_type": "Supplier",
								"party": s.vender_id,
								"credit_in_account_currency":total_colle,
								"contract_id":s.contract_id
								
					},)
				else:
					if(s.vehicle_type!="BULLOCK CART"):
						if(s.type=="Transporter"):
							je.append(
							"accounts",
							{
								"account":str(cane_charge) ,
								"debit_in_account_currency": s.total,				
							},)
							je.append(
								"accounts",
								{
									"account": acc_to_set_debit_side,
									"party_type": "Supplier",
									"party": s.vender_id,
									"credit_in_account_currency": s.total,
									"contract_id":s.contract_id
								
								},)
						else:
							je.append(
							"accounts",
							{
								"account":str(caneharcharge) ,
								"debit_in_account_currency": s.total,				
							},)
							je.append(
								"accounts",
								{
									"account": acc_to_set_debit_har,
									"party_type": "Supplier",
									"party": s.vender_id,
									"credit_in_account_currency": s.total,
									"contract_id":s.contract_id
								
								},)
					
		if counter > 0:
			je.insert()
			je.save()
			self.journal_entry_id =str(je.name)
			je.submit()

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
			list_data_pen=[]
			formatted_input = re.sub(r'\]\[', '],[', s.all_deduction_information)
			formatted_input = '[' + formatted_input + ']'
			parsed_list = ast.literal_eval(formatted_input)
			list_data_od=eval(str(parsed_list))
			list_data_od =list_data_od[3]
			list_data_pen=eval(str(parsed_list))
			list_data_pen=list_data_pen[7]
			if(list_data_od):
				for data_od in list_data_od:
					doc=frappe.get_doc("Deduction Form",str(data_od['DFN']))
					frappe.db.set_value("Deduction Form",str(data_od['DFN']),"paid_amount",(float(doc.paid_amount)+(float(data_od['Deduction Amount']))))
					if (float(doc.paid_amount)+(float(data_od['Deduction Amount']))) == doc.deduction_amount:
						frappe.db.set_value("Deduction Form",str(data_od['DFN']),"deduction_status",1)
			if(list_data_pen):
				for data_od in list_data_pen:
					doc=frappe.get_doc("Deduction Form",str(data_od['DFN']))
					frappe.db.set_value("Deduction Form",str(data_od['DFN']),"paid_amount",(float(doc.paid_amount)+(float(data_od['Penalty Amount']))))
					if (float(doc.paid_amount)+(float(data_od['Penalty Amount']))) == doc.deduction_amount:
						frappe.db.set_value("Deduction Form",str(data_od['DFN']),"deduction_status",1)
        
	def add_deduction_doc(self):
		for s in self.get("calculation_table"):
			if float(s.remaining_hire_charge)>0 and s.type=="Transporter":
				doc = frappe.new_doc('Deduction Form')
				doc.farmer_code =s.vender_id
				doc.deduction_amount=float(s.remaining_hire_charge)
				doc.season=self.season
				doc.branch=self.branch
				doc.date=self.today
				doc.vender_type="H and T"
				doc.account=s.hire_account
				doc.h_and_t_contract_id=s.contract_id 
				doc.deduction_status=0
				doc.insert()
				s.deduction_doc=str(doc.name)
				doc.submit()
	
	def delete_hire_ded(self):
		for s in self.get("calculation_table"):
			if float(s.remaining_hire_charge)>0 and s.type=="Transporter":	
				doc = frappe.get_doc("Deduction Form",(str(s.deduction_doc)))
				if doc.docstatus == 1:
					doc.cancel()
     
	def set_issue_date(self):
		for s in self.get("calculation_table"):
			if(s.type=="Transporter" and s.cartno>0 and s.cart_no_list):
				li=eval(str(s.cart_no_list))
				if(li):
					par_name=li[0]
					cart_no=li[1]
					parent_doc = frappe.get_doc("Vehicle Registration",str(par_name))
					for row in parent_doc.get("vehicle_details_tab"):
						if(str(int(row.cart_no))==str(int(cart_no))):
							row.updated_issue=self.to_date
					parent_doc.save()
    
	
	def delete_issue_date(self):
		for s in self.get("calculation_table"):
			if(s.type=="Transporter" and s.cartno>0 and s.cart_no_list):
				li=eval(str(s.cart_no_list))
				if(li):
					par_name=li[0]
					cart_no=li[1]
					parent_doc = frappe.get_doc("Vehicle Registration",str(par_name))
					for row in parent_doc.get("vehicle_details_tab"):
						if(str(int(row.cart_no))==str(int(cart_no))):
							row.updated_issue=None
					parent_doc.save()
    
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
		self.delete_row_record()
		self.add_deduction_doc()
		self.set_issue_date()
  
	def delete_row_record(self):
		doc = frappe.get_all("Child H and T Data",filters ={"parent": self.name , "check" : 0},)
		for d in doc:
			frappe.delete_doc("Child H and T Data", d.name)
	
      
	def change_status_on_cane_weight(self):
		for s in self.get("calculation_table"):
			if(s.type=="Transporter"):
				doc = frappe.db.get_list("Cane Weight",
														filters={"date": ["between", [self.from_date, self.to_date]],"season" : self.season ,"branch" : self.branch,"h_and_t_billing_status":False,"contract_id":s.contract_id},
														fields=["name","h_and_t_billing_status"],)
				for d in doc:
					frappe.db.set_value("Cane Weight",d.name,"h_and_t_billing_status",True)
	