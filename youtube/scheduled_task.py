from celery import shared_task


@shared_task(bind=True)
def celery_test(self):
    for i in range(5):
        print(f"*********************************** {i}th print *********************")
    return "working"
