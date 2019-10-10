# Flask imports
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, Response, jsonify
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, SelectMultipleField, BooleanField
from wtforms.validators import InputRequired, Email
from wtforms.widgets import TextArea, ListWidget, CheckboxInput
from wtforms import ValidationError

# E-mail functionality imports
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

app = Flask(__name__)

# Defining the Form Class for Sending SMS Form

class SendSMSForm(Form):
    firstname = StringField('First Name', [validators.Regexp('^[a-zA-Z\s]*$', message="**First Name can only contain letters or space"),validators.Length(min=1, max=25, message="**First Name must be between 1 & 25 characters")])
    lastname = StringField('Last Name',[validators.Regexp('^[a-zA-Z\s]*$', message="**Last Name can only contain letters or space"),validators.Length(min=1, max=25, message="**Last Name must be between 1 & 25 characters")])
    phonenumber = StringField('Phone Number', [validators.Regexp('^(\+0?1\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', message="**Please Enter a valid US number")])
    mobile_carrier = SelectField('Cell Phone Carrier', choices = 
        [
            ('@txt.att.net', 'AT&T'),
            ('@tmomail.net', 'T-Mobile'),
            ('@vzwpix.com', 'Verizon'),
            ('@pm.sprint.com', 'Sprint'), 
            ('@mypixmessages.com', 'XFinity Mobile'), 
            ('@vmpix.com', 'Virgin Mobile'), 
            ('@mmst5.tracfone.com', 'Tracfone'), 
            ('@mymetropcs.com', 'Metro PCS'), 
            ('@myboostmobile.com', 'Boost Mobile'),
            ('@tmomail.net', 'Mint Mobile'), 
            ('@mms.cricketwireless.net', 'Cricket'), 
            ('@text.republicwireless.com', 'Republic Wireless'), 
            ('@msg.fi.google.com', 'Google Fi (Project Fi)'),
            ('@mms.uscc.net', 'U.S. Cellular'), 
            ('@message.ting.com', 'Ting'), 
            ('@mailmymobile.net', 'Consumer Cellular'), 
            ('@cspire1.com', 'C-Spire'), 
            ('@vtext.com', 'Page Plus')
        ], default=("N/A","N/A"))
    message_content = TextAreaField('Message Content')

    
# Send SMS Function
@app.route('/', methods=['GET', 'POST'])
def send_sms():

    # Retrieving information entered by the user from the Send SMS form when user hits 'Send Message' Button
    form = SendSMSForm(request.form)

    if request.method == 'POST' :

        firstname = form.firstname.data # Retrieving First Name Information entered by User
        lastname = form.lastname.data   # Retrieving Last Name Information entered by User
        phonenumber = form.phonenumber.data # Retrieving Phone Number Information entered by User
        mobile_carrier = form.mobile_carrier.data   # Retrieving First Name Information entered by User
        message_content = form.message_content.data # Retrieving First Name Information entered by User

        # Composing the Message to be sent 
        messageToNumber_body = 'Subject:Message from MindPROS SMSApp\n\n'+ 'Hi'+ ' ' + firstname + ' ' + lastname + ',\n\n' + message_content
        
        # Constructing the 'To' email address by combining the mobile number and appropriate carrier email address tag
        to_number = str(phonenumber)+ str(mobile_carrier)

        # 'From' email address credentials - Can Replace with a different email address
        auth = ('bhargav@mind-pros.com', 'bhargav1234')

        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login(auth[0], auth[1])

        # Send text message through SMS gateway of destination number
        server.sendmail( auth[0], to_number, messageToNumber_body)

        flash('Message Sent!', 'success')
             
        return redirect(url_for('send_sms'))


    return render_template('send_sms.html', form=form)


if __name__ == '__main__':
    app.secret_key='secret123'  # Need a secret key to allow our app to interact with mail servers 
    app.run(debug=True)
