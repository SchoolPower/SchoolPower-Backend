from apns2.client import APNsClient
from apns2.payload import Payload

token_hex = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'
payload = Payload(alert="Hello World!", sound="default", badge=1)
topic = 'com.example.App'
client = APNsClient('aps.pem', use_sandbox=True, use_alternative_port=False)
client.send_notification(token_hex, payload, topic)
