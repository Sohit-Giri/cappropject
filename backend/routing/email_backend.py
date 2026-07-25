import os
import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

class ResendEmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        resend.api_key = os.getenv("RESEND_API_KEY") or getattr(settings, "RESEND_API_KEY", None)

    def send_messages(self, email_messages):
        num_sent = 0
        for message in email_messages:
            try:
                from_addr = message.from_email or getattr(settings, "DEFAULT_FROM_EMAIL", "RouteOptima <noreply@sohitgiri.com.np>")
                
                # Check for alternative HTML content attached to EmailMultiAlternatives or send_mail
                html_content = None
                if hasattr(message, 'alternatives'):
                    for content, mimetype in message.alternatives:
                        if mimetype == "text/html":
                            html_content = content
                            break

                params = {
                    "from": from_addr,
                    "to": message.to,
                    "subject": message.subject,
                    "text": message.body,  # Plain text version
                }

                # If HTML exists, pass it to Resend's 'html' field; otherwise use plain text
                if html_content:
                    params["html"] = html_content
                else:
                    params["html"] = message.body

                resend.Emails.send(params)
                num_sent += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e
        return num_sent