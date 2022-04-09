import json
import smtplib

config_filename = 'TestSimulation.json'


def load_simulation():
    test_simulation_json = open(config_filename)
    simulation = json.load(test_simulation_json)
    return simulation

# When gmail smtp is deprecated try local smtp (https://docs.python.org/3/library/email.examples.html)
def execute_email_warning(text):
    simulation = load_simulation()
    config = simulation['config']

    gmail_user = config['gmail']['email']
    gmail_password = config['gmail']['password']

    sent_from = gmail_user
    to = simulation['user_data']['email']
    subject = 'Test'
    body = 'consectetur adipiscing elit'

    email_text = "das ist ein test"

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)

        print(text)
