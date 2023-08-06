from tussik.email import Emailer

Emailer.setDefault("1.1.1.1")

msg = Emailer()
msg.sender("sender@domain.tld", "Sender")
msg.to("recipient@domain.tld", "Recipient")
msg.header("customtag", "1234")
msg.subject("test message")
msg.send()
