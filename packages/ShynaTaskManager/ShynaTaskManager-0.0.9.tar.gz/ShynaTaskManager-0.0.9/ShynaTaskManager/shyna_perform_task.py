from Shynatime import ShTime
from ShynaDatabase import Shdatabase
import os
from ShynaTelegramBotNotification import BotNotify
from Shyna_speaks import Shyna_speaks


class ShynaPerformTask:
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    s_bot = BotNotify.BotShynaTelegram()
    s_speak = Shyna_speaks.ShynaSpeak()
    result = False

    def get_task_from_table(self):
        try:
            self.s_data.default_database = os.environ.get('taskmanager_db')
            self.s_data.query = "Select * from Task_Manager where task_date='" + str(self.s_time.now_date) + \
                                "' and task_status in ('True', 'running')"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                print("No Task to process")
            else:
                for item in self.result:
                    task_id = item[3]
                    task_time = item[5]
                    task_type = item[6]
                    speak = item[7]
                    snooze_duration = item[9]
                    snooze_duration_status = item[8]
                    self.perform_task(task_id, task_time, task_type, speak, snooze_duration, snooze_duration_status)
        except Exception as e:
            self.s_bot.message = "Exception at task manager get task from table " + str(e)
            self.s_bot.bot_send_msg_to_master()
            print(e)

    def perform_task(self, task_id, task_time, task_type, speak, snooze_duration, snooze_duration_status):
        try:
            if str(task_type).lower().__eq__('alarm'):
                self.s_speak.priority = [0, 1, 2]
                self.s_speak.shyna_speaks(msg=str(speak))
                if str(self.is_this_is_the_first_alarm(task_time=task_time)).lower().__eq__('true'):
                    if str(self.is_shivam_in_front_of_camera()).lower().__eq__('true'):
                        self.s_speak.priority = [0, 1, 2]
                        self.s_speak.shyna_speaks(msg="Good Morning Boss!")
                        self.s_data.default_database = os.environ.get('taskmanager_db')
                        self.s_data.query = "Update Task_Manager set task_status='False' where task_id='" \
                                            + str(task_id) + "'"
                        self.s_data.create_insert_update_or_delete()
                    else:
                        pass
                else:
                    if str(self.is_shivam_in_front_of_camera()).lower().__eq__('true'):
                        self.s_speak.priority = [0, 1, 2]
                        self.s_speak.shyna_speaks(msg="Good Morning Boss!")
                        self.s_data.default_database = os.environ.get('taskmanager_db')
                        self.s_data.query = "Update Task_Manager set task_status='False' where task_id='" \
                                            + str(task_id) + "'"
                        self.s_data.create_insert_update_or_delete()
                    else:
                        if str(snooze_duration_status).lower().__eq__('true') and int(snooze_duration) > 0:
                            snooze_duration = int(snooze_duration) - 1
                            self.s_data.default_database = os.environ.get('taskmanager_db')
                            self.s_data.query = "Update Task_Manager set snooze_duration = '" + str(snooze_duration) + \
                                                "', task_status='running' where task_id='" + str(task_id) + "'"
                            self.s_data.create_insert_update_or_delete()
                        else:
                            self.s_data.default_database = os.environ.get('taskmanager_db')
                            self.s_data.query = "Update Task_Manager set task_status='False' where task_id='" \
                                                + str(task_id) + "'"
                            self.s_data.create_insert_update_or_delete()
            else:
                pass
        except Exception as e:
            self.s_bot.message = "Exception at task manager perform task " + str(e)
            self.s_bot.bot_send_msg_to_master()
            print(e)

    def is_this_is_the_first_alarm(self, task_time):
        self.result = False
        task_time_sequence = []
        try:
            self.s_data.default_database = os.environ.get('alarm_db')
            self.s_data.query = "Select alarm_time from alarm where alarm_date='" + str(self.s_time.now_date) + "'"
            results = self.s_data.select_from_table()
            if str(results[0]).lower().__eq__('empty'):
                self.result = False
            else:
                for item in results:
                    task_time_sequence.append(item[0])
                task_time_sequence = sorted(task_time_sequence)
                if self.s_time.string_to_time(str(task_time_sequence[0])) == self.s_time.string_to_time(task_time):
                    self.result = True
                else:
                    self.result = False
        except Exception as e:
            print(e)
            self.result = False
        finally:
            return self.result

    def is_shivam_in_front_of_camera(self):
        self.result = False
        try:
            self.s_data.default_database = os.environ.get('twelve_db')
            self.s_data.query = "Select new_status,check_status from shyna_is where question_is = " \
                                "'is_shivam_at_home' and task_date='" + str(self.s_time.now_date) + "'"
            results = self.s_data.select_from_table()
            if str(results[0][1]).lower().__eq__('true') and str(results[0][0]).lower().__eq__('true'):
                self.s_data.query = "Select new_status,check_status from shyna_is where question_is = " \
                                    "'shivam_front_of_camera' and task_date='" + str(self.s_time.now_date) + "'"
                results = self.s_data.select_from_table()
                if str(results[0]).lower().__eq__('empty'):
                    self.result = "flag"
                else:
                    if str(results[0][1]).lower().__eq__('false'):
                        self.result = "flag"
                    else:
                        if str(results[0][0]).lower().__eq__('true'):
                            self.result = True
                        else:
                            self.result = False
            else:
                self.result = False
        except Exception as e:
            print(e)
            self.result = False
        finally:
            return self.result


if __name__ == '__main__':
    ShynaPerformTask().get_task_from_table()
