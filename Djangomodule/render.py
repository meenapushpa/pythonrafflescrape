import jinja2
from bokeh.models.callbacks import CustomJS
import js2py

def render_jinja_html(template_loc,file_name,**context):
    store= jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_loc+'/')
    ).get_template(file_name).render(context)
    return store


if  __name__ == '__main__':
    data={'tags[]': '76713', 'token': 'c812c1ff-2a5a0fe-efad139-d754416-71e1e60-2ce', 'rule_email': 'wlslakshman@gmail.com', 'fields[Raffle.Instagram Handle]': 'Lakshmanan', 'fields[Raffle.Phone Number]': '+44 78 3063 3285', 'fields[Raffle.First Name]': 'Lakshmanan', 'fields[Raffle.Last Name]': 'S', 'fields[Raffle.Shipping Address]': "Queens Road", 'fields[Raffle.Postal Code]': "NE61 2TD", 'fields[Raffle.City]': "WEST EDINGTON", 'fields[Raffle.Signup Newsletter]': '1', 'fields[SignupSource.ip]': '192.0.0.1', 'fields[SignupSource.useragent]': 'Mozilla', 'email_field': '1', 'language': 'sv', 'g-recaptcha-response': '03AGdBq26csmo47MS8grr0txAzzqpIXHAw3euzZzQ4HDYOInPXZK5S9dOqeWvdmVLKLQXQV4A85v4fydOvXByN1_SQCQmo4EInwriPF1uwhNXBxC6deErcUy50pw_vGnllfYoqO3EbyjLZGaXGg1WB9vQgDYC_Ir_KyiUnCCnQE4QZyktAtk_oZwD4oJDeUbRxs40XSwVyqUl24OwTO1HXQCugT3VKudLNbOLHgyy0ZVd5JedsAKHBb0J-wTN7c3puW0sOKA8jsZ2CdUx_dPhH6NlbfrAn2orypPJvskYCQVZpBSoIZ6Gjgy0BWu7wcs43Z0Dl6HdDG3EN5cmZ-rLNgofkpxL6BoqBKJd37MS93Ny_nmIgnJMs-7r8pcZFmr32YsdRKWXzQjARKK8obWWWmkA4d62AEyLZdj7qmG_Q4cg_oN5Bepy8hntmWGXYXe-vVGIENdlLhEfYIwiq6TQlfjL8r248F2R_ZxJ_AEkUcyAz1_0ExEBajqP3_yatRcRHoErUTj2j8Qd-fX1qWmOvftFx6D761FgCNg'}
    render_jinja_html("templates","result1.html",result = data)
    #js = 'function submitRuleOptin(token) {rule-optin-form.submit(); }'
    #submitRuleOptin= js2py.eval_js(js)
    #callback = CustomJS(args=dict(data),code="""function submitRuleOptin("c812c1ff-2a5a0fe-efad139-d754416-71e1e60-2ce") { document.getElementById("rule-optin-form").submit(); }""")
    #print(callback)
