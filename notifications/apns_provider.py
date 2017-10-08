from apns2.client import APNsClient
from apns2.payload import Payload

token_hex = ''
payload = Payload(content_available=1, custom={'updated-subjects': {
    "English 11": [{"name": "Poem","score": "1/10"},
                    {"name": "Essay","score": "10/10"}],
    "Chemistry 11": [{"name": "Memrise","score": "--"},
                    {"name": "Quiz","score": "9/10"}]
}})
topic = 'studio.schoolpower.SchoolPower'
client = APNsClient('apns.pem', use_sandbox=True, use_alternative_port=False)
client.send_notification(token_hex, payload, topic)
