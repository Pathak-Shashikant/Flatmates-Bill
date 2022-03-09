from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request
from flatmate_bills.flat import Bill, Flatmate
from flatmate_bills.pdf_gen import PdfReport, FileShare

API_KEY = "AYIqc3qnQRhSOHEEvJbV0z"

app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class BillFormPage(MethodView):
    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html', form=bill_form)

    def post(self):
        billform = BillForm(request.form)
        bill = Bill(amount=float(billform.amount.data), period=billform.bill_period.data)
        flatmate1 = Flatmate(name=billform.name_first_flatmate.data,
                             days_in_house=int(billform.day_stayed_first_flatmate.data))
        flatmate2 = Flatmate(name=billform.name_second_flatmate.data,
                             days_in_house=int(billform.day_stayed_second_flatmate.data))
        pdf_report = PdfReport(filename=f"Bill_due_for_{bill.period}")
        pdf_report.generate(flatmate1, flatmate2, bill)
        file_share = FileShare(filepath=f"flatmate_bills/files/{pdf_report.filename}.pdf", api_key=API_KEY)

        return render_template('bill_form_page.html', name1=flatmate1.name, amount1=flatmate1.pays(bill, flatmate2),
                               name2=flatmate2.name, amount2=flatmate2.pays(bill, flatmate1), form=billform, result=True
                               , pdf=file_share.share())


class ResultPage(MethodView):
    def post(self):
        billform = BillForm(request.form)
        bill = Bill(amount=float(billform.amount.data), period=billform.bill_period.data)
        flatmate1 = Flatmate(name=billform.name_first_flatmate.data,
                             days_in_house=int(billform.day_stayed_first_flatmate.data))
        flatmate2 = Flatmate(name=billform.name_second_flatmate.data,
                             days_in_house=int(billform.day_stayed_second_flatmate.data))
        return render_template('result.html', name1=flatmate1.name, amount1=flatmate1.pays(bill, flatmate2),
                               name2=flatmate2.name, amount2=flatmate2.pays(bill, flatmate1))


class BillForm(Form):
    amount = StringField(label='Bill Amount: ', validators=[DataRequired()], default=100)
    bill_period = StringField(label='Bill Period: ', validators=[DataRequired()], default='January 2022')
    name_first_flatmate = StringField(label='Name: ', validators=[DataRequired()], default='First Flatmate')
    day_stayed_first_flatmate = StringField(label='Days of Stay: ', validators=[DataRequired()], default=25)
    name_second_flatmate = StringField(label='Name: ', validators=[DataRequired()], default='Second Flatmate')
    day_stayed_second_flatmate = StringField(label='Days of Stay: ', validators=[DataRequired()], default=25)
    calculate = SubmitField(label='Calculate')


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill', view_func=BillFormPage.as_view('bill_form_page'))
# app.add_url_rule('/result', view_func=ResultPage.as_view('result_page'))

app.run(debug=True)
