from flask import current_app

''' 定时执行的任务
'''
class SchedulerJob(object):

    ''' 因为是独立的线程，需要传入上下文
    '''
    def __init__(self, app):
        self.app = app

    def sayHi(self):
        with self.app.app_context():
            current_app.logger.info('hi')
