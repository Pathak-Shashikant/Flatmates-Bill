from flat import Bill, Flatmate
from pdf_gen import PdfReport, FileShare


API_KEY="AYIqc3qnQRhSOHEEvJbV0z"
# Take input from user such as
# names, bill period, bill amount and days of stay in house
print("********************Flat Mates Bill Split*********************")
bill_amount = float(input("Enter Bill Amount: "))
bill_period = input("Enter bill period (e.g December 2021): ")
flatmate1_name = input("What is the name of first Flatmate? ")
flatmate1_days_stay = int(input(f"How many days did {flatmate1_name} stayed? "))
flatmate2_name = input("What is the name of other Flatmate? ")
flatmate2_days_stay = int(input(f"How many days did {flatmate2_name} stayed? "))

# Initialising Classes
total_bill = Bill(amount=bill_amount, period=bill_period)
flatmate1 = Flatmate(name=flatmate1_name, days_in_house=flatmate1_days_stay)
flatmate2 = Flatmate(name=flatmate2_name, days_in_house=flatmate2_days_stay)

# calculate due amount of each flatmate
bill_due_flatmate1 = flatmate1.pays(total_bill, flatmate2)
bill_due_flatmate2 = total_bill.amount - bill_due_flatmate1

# Generate pdf
pdf_report = PdfReport(filename=f"Bill_due_for_{total_bill.period}")
pdf_report.generate(flatmate1, flatmate2, total_bill)

print(f"{flatmate1.name} to pay: ${bill_due_flatmate1:.2f}")
print(f"{flatmate2.name} to pay: ${bill_due_flatmate2:.2f}")

file_share = FileShare(filepath=f"files/{pdf_report.filename}.pdf", api_key=API_KEY)
print(file_share.share())
