from flask import Flask, render_template,make_response
from flask import request

app = Flask(__name__, template_folder='templates')
@app.route('/')
def student():
    return render_template('save.html')
@app.route('/result',methods = ['POST', 'GET'])
def result():
    data={'tags[]': '74751', 'token': 'c812c1ff-2a5a0fe-efad139-d754416-71e1e60-2ce', 'rule_email': 'sv.kothai@gmail.com', 'fields[Raffle.Instagram Handle]': 'priya', 'fields[Raffle.Phone Number]': '+44 78 3063 3285', 'fields[Raffle.First Name]': 'Lakshmanan', 'fields[Raffle.Last Name]': 'S', 'fields[Raffle.Shipping Address]': 'Queens Road', 'fields[Raffle.Postal Code]': 'NE61 2TD', 'fields[Raffle.City]': 'WEST EDINGTON','fields[Raffle.Country]': 'GB', 'fields[Raffle.Signup Newsletter]': '1', 'fields[SignupSource.ip]': '192.0.0.1', 'fields[SignupSource.useragent]': 'Mozilla', 'email_field': '1', 'language': 'sv','g-recaptcha-response': '03AGdBq26csmo47MS8grr0txAzzqpIXHAw3euzZzQ4HDYOInPXZK5S9dOqeWvdmVLKLQXQV4A85v4fydOvXByN1_SQCQmo4EInwriPF1uwhNXBxC6deErcUy50pw_vGnllfYoqO3EbyjLZGaXGg1WB9vQgDYC_Ir_KyiUnCCnQE4QZyktAtk_oZwD4oJDeUbRxs40XSwVyqUl24OwTO1HXQCugT3VKudLNbOLHgyy0ZVd5JedsAKHBb0J-wTN7c3puW0sOKA8jsZ2CdUx_dPhH6NlbfrAn2orypPJvskYCQVZpBSoIZ6Gjgy0BWu7wcs43Z0Dl6HdDG3EN5cmZ-rLNgofkpxL6BoqBKJd37MS93Ny_nmIgnJMs-7r8pcZFmr32YsdRKWXzQjARKK8obWWWmkA4d62AEyLZdj7qmG_Q4cg_oN5Bepy8hntmWGXYXe-vVGIENdlLhEfYIwiq6TQlfjL8r248F2R_ZxJ_AEkUcyAz1_0ExEBajqP3_yatRcRHoErUTj2j8Qd-fX1qWmOvftFx6D761FgCNg'}
    return render_template("result1.html",result = data)


if  __name__ == '__main__':
    app.run(debug = True)
