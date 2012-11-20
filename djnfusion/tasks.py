try:
    from celery.task import Task
    from celery.registry import tasks
except ImportError:
    pass


from djnfusion import sync_user, optin_user, daily_statistics


class SyncUserTask(Task):
    def run(self, user=None, user_id=None):
        sync_user(user=user, user_id=user_id)
tasks.register(SyncUserTask)


class OptinUserTask(Task):
    def run(self, user=None, user_id=None):
        sync_user(user=user, user_id=user_id)
        optin_user(user=user, user_id=user_id)
tasks.register(OptinUserTask)


class DailyStatisticsTask(Task):
    def run(self, user=None, user_id=None):
        daily_statistics(user=user, user_id=user_id)
tasks.register(DailyStatisticsTask)