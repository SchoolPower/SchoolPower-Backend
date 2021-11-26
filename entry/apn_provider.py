import asyncio
import collections
import logging
import time
import json

from apns2.client import APNsClient
from apns2.payload import Payload

from config.config import PEM_FILE_PATH, TOPIC
from db import db

Notification = collections.namedtuple('Notification', ['token', 'payload'])

SEND_INTERVAL = 3
N_BATCH = 20
logging.getLogger('apns2').setLevel(logging.WARNING)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def handle_async():
    time_start = time.time()
    await db.init()
    client = APNsClient(PEM_FILE_PATH, use_sandbox=False, use_alternative_port=False)
    tokens = await db.get_all_tokens()

    notifications = [Notification(payload=Payload(content_available=True), token=str(token.token)) for token in tokens]
    batch_size = int(len(notifications) / N_BATCH) + 1
    invalid_tokens = []
    results = {}
    for i, chunk in enumerate(chunks(notifications, batch_size)):
        print("Sending batch " + str(i) + " of size " + str(len(chunk)))
        result = client.send_notification_batch(notifications=chunk, topic=TOPIC)
        results.update(result)
        time.sleep(SEND_INTERVAL)

    invalid_tokens.extend([token for token, result in results.items() if result != "Success"])
    await asyncio.gather(*[db.remove_token(token) for token in invalid_tokens])
    await db.close()
    print(json.dumps({
        "processed": len(results),
        "removed": len(invalid_tokens),
        "duration": time.time() - time_start,
        "results_set": list(set(res for res in results.values())),
        "batch_size": batch_size,
    }))


def handle(event, context):
    asyncio.get_event_loop().run_until_complete(handle_async())


if __name__ == '__main__':
    handle(None, None)
