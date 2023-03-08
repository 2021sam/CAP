# # https://www.youtube.com/watch?v=BppyfPye8eo
# import csv, io, ast, time, datetime, django_filters
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse	#, HttpResponseRedirect
from cclog.models import Log
# from django.contrib.auth.decorators import permission_required
# from django.contrib.auth.models import User
from . import credentials


#	================================================================
#	==========================	EMAIL	========================
#	================================================================
def email( request ):
	body = get_logs_string()
	send_email( 'BEAR CC Log - Inline', body )
	return HttpResponse ('Sent')

def email_attach( request ):
	attachment = get_logs_attach()
	send_email_attach( 'BEAR CC Log - Attached', 'Log file is attached.', attachment )
	return HttpResponse ('Sent attachment.')



#	================================================================
#	==========================   GET LOGS   ========================
#	================================================================
def get_logs_string():
	s = ''
	records = Log.objects.all()
	for i in records.iterator():
		# t = f'{ i.log_id }, { i.user_id }, { i.cc_id}, {i.transaction_date}, {i.vendor}, {i.amount}, {i.ro1}, {i.ro2}, {i.ro3}, {i.ro4}, {i.ro5}, {i.invoice}, {i.returned}, {i.credit}, {i.voided}, {i.closed}, {i.start}, {i.stop}\n'
		t = f'{ i.log_id },{ i.user_id },{ i.cc_id},{i.transaction_date},{i.vendor},{i.amount},{i.ro1},{i.ro2},{i.ro3},{i.ro4},{i.ro5},{i.invoice},{i.returned},{i.credit},{i.voided},{i.closed},{i.start},{i.stop}\n'
		# print ( t )
		s += t

	return s


def get_logs_attach():
	from email.mime.text import MIMEText
	filename	= 'log.txt'		#	Include date in name.
	attachment	= MIMEText( get_logs_string() )
	attachment.add_header( 'Content-Disposition', 'attachment', filename=filename )
	return attachment



#	================================================================
#	==========================  SEND EMAIL  ========================
#	================================================================
def send_email( SUBJECT, BODY ):
	import smtplib
	import email.utils
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText

	# # This address must be verified.
	# SENDER = 'x@gmail.com'
	# SENDERNAME = 'Super x'
	#
	# # is still in the sandbox, this address must be verified.
	# RECIPIENT  = 'x@gmail.com'
	#
	# # Replace smtp_username with your Amazon SES SMTP user name.
	# USERNAME_SMTP = "DDESK3KDUIDOYTFG5"
	#
	# # Replace smtp_password with your Amazon SES SMTP password.
	# PASSWORD_SMTP = "BLBxhSDLDKLDJDLWK30Zy0NDnMZXrIAN80Qw6BYfZlHqt"
	#
	# # (Optional) the name of a configuration set to use for this message.
	# # If you comment out this line, you also need to remove or comment out
	# # the "X-SES-CONFIGURATION-SET:" header below.
	# # CONFIGURATION_SET = "ConfigSet"
	#
	# # If you're using Amazon SES in an AWS Region other than US West (Oregon),
	# # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
	# # endpoint in the appropriate region.
	# HOST = "email-smtp.us-west-1.amazonaws.com"
	# PORT = 587

	# The subject line of the email.
	# SUBJECT = 'Amazon SES Test (Python smtplib)'

	# The email body for recipients with non-HTML email clients.
	# BODY_TEXT = ("Amazon SES Test\r\n"
	# 			"This email was sent through the Amazon SES SMTP "
	# 			"Interface using the Python smtplib package."
	# 			)

	BODY_TEXT = ( BODY )
	# # The HTML body of the email.
	# BODY_HTML = """<html>
	# <head></head>
	# <body>
	# <h1>Amazon SES SMTP Email Test</h1>
	# <p>This email was sent with Amazon SES using the
	# 	<a href='https://www.python.org/'>Python</a>
	# 	<a href='https://docs.python.org/3/library/smtplib.html'>
	# 	smtplib</a> library.</p>
	# </body>
	# </html>
	# 			"""

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = SUBJECT
	msg['From'] = email.utils.formataddr((credentials.SENDERNAME, credentials.SENDER))
	msg['To'] = credentials.RECIPIENT
	# Comment or delete the next line if you are not using a configuration set
	# msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(BODY_TEXT, 'plain')
	# part2 = MIMEText(BODY_HTML, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	# msg.attach(part2)



	# Try to send the message.
	try:
		server = smtplib.SMTP(credentials.HOST, credentials.PORT)
		server.ehlo()
		server.starttls()
		#stmplib docs recommend calling ehlo() before & after starttls()
		server.ehlo()
		server.login(credentials.USERNAME_SMTP, credentials.PASSWORD_SMTP)
		server.sendmail(credentials.SENDER, credentials.RECIPIENT, msg.as_string())
		server.close()
	# Display an error message if something goes wrong.
	except Exception as e:
		print ("Error: ", e)
	else:
		print ("Email sent!")















def send_email_attach( SUBJECT, BODY, attachment ):
	import smtplib
	import email.utils
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.base import MIMEBase

	# The subject line of the email.
	# SUBJECT = 'Amazon SES Test (Python smtplib)'

	# The email body for recipients with non-HTML email clients.
	# BODY_TEXT = ("Amazon SES Test\r\n"
	# 			"This email was sent through the Amazon SES SMTP "
	# 			"Interface using the Python smtplib package."
	# 			)

	BODY_TEXT = ( BODY )
	# # The HTML body of the email.
	# BODY_HTML = """<html>
	# <head></head>
	# <body>
	# <h1>Amazon SES SMTP Email Test</h1>
	# <p>This email was sent with Amazon SES using the
	# 	<a href='https://www.python.org/'>Python</a>
	# 	<a href='https://docs.python.org/3/library/smtplib.html'>
	# 	smtplib</a> library.</p>
	# </body>
	# </html>
	# 			"""


	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = SUBJECT
	msg['From'] = email.utils.formataddr((credentials.SENDERNAME, credentials.SENDER))
	msg['To'] = credentials.RECIPIENT
	# Comment or delete the next line if you are not using a configuration set
	# msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(BODY_TEXT, 'plain')
	# part2 = MIMEText(BODY_HTML, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach( part1 )
	# msg.attach(part2)
	msg.attach( attachment )


	# Try to send the message.
	try:
		server = smtplib.SMTP(credentials.HOST, credentials.PORT)
		server.ehlo()
		server.starttls()
		#stmplib docs recommend calling ehlo() before & after starttls()
		server.ehlo()
		server.login(credentials.USERNAME_SMTP, credentials.PASSWORD_SMTP)
		server.sendmail(credentials.SENDER, credentials.RECIPIENT, msg.as_string())
		server.close()
	# Display an error message if something goes wrong.
	except Exception as e:
		print ("Error: ", e)
	else:
		print ("Email sent!")
