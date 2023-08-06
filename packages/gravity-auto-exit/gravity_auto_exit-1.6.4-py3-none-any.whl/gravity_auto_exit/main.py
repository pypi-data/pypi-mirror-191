import datetime
import threading
import time
import uuid
from cad.main import CAD
from whikoperator.main import Wpicoperator
import requests
from gravity_auto_exit.logger import logger
from neurocore_worker.main import NeuroCoreWorker


class AutoExit:
    def __init__(self, cam_host, cam_login, cam_password,
                 neurocore_login, neurocore_password,
                 auth_method='Digest', engine_callback=None,
                 reload_time=15, debug=False,
                 detection_amount=4, failed_callback=None,
                 fail_callback_react_amount=2, fail_reload_time=1.5,
                 active=True, resize_photo: tuple = False, cam_port=80,
                 catch_event='Line Crossing',
                 simple_callback_func=None,
                 sleep_before=1):
        self.simple_callback_func = simple_callback_func
        self.sleep_before = sleep_before
        self.neurocore_worker = NeuroCoreWorker(
            api_login=neurocore_login,
            api_password=neurocore_password,
            plate_frame_size=resize_photo)
        self.cad = CAD(host=cam_host, port=cam_port, login=cam_login,
                       password=cam_password,
                       callback_func=self.cad_callback_func,
                       delay_time=0,
                       logger=logger,
                       catch_event=catch_event)
        cam_ip = cam_host.replace('http://', '')
        cam_ip = f"{cam_ip}:{cam_port}"
        self.reload_time = reload_time
        if not logger:
            logger.getLogger(type(self).__name__)
        else:
            logger.name = type(self).__name__
        self.active = active
        self.resize_photo = resize_photo
        self.fail_callback_react_amount = fail_callback_react_amount
        self.fail_reload_time = fail_reload_time
        self.cam = Wpicoperator(
            cam_ip=cam_ip,
            cam_login=cam_login,
            cam_pass=cam_password,
            auth_method=auth_method)
        self.callback_request_url = None
        self.debug = debug
        self.count = 0
        self.last_take = datetime.datetime.now()
        self.can_wait_others = False
        self.failed_callback = failed_callback
        self.engine_callback = engine_callback
        self.wait_started = False
        logger.debug('AUTO_EXIT has started successfully')

    def set_active(self, activity_bool: bool):
        self.active = activity_bool

    def set_can_wait_others(self, boolean: bool):
        self.can_wait_others = boolean

    def start(self):
        self.cad.mainloop()

    def save_pic(self, pic_name, pic_body, frmt='.jpg'):
        logger.debug(f'Saving picture {pic_name}')
        with open(pic_name + frmt, 'wb') as fobj:
            fobj.write(pic_body)
        logger.debug("Success!")

    def cad_callback_func(self, data=None):
        logger.debug("=====CAD func started=====")
        if self.simple_callback_func:
            threading.Thread(target=self.simple_callback_func).start()
        if not self.active:
            logger.debug("---It is not active---")
            if self.can_wait_others and not self.wait_started:
                self.wait_started = True
                logger.debug("But it is a another car in order")
                while not self.active:
                    time.sleep(0.5)
                logger.debug('Active again')
            else:
                return
        self.active = False
        logger.debug(f'Sleeping before: {self.sleep_before}')
        time.sleep(self.sleep_before)
        #if datetime.datetime.now() - self.last_take > datetime.timedelta(
        #        seconds=self.reload_time):
        logger.debug("Recognise cycle has been started")
        for i in range(5):
            logger.debug(f"Recognise cycle {i} of 5")
            time.sleep(i + 0.2)
            response = self.camera_and_recognise()
            if 'error' in response:
                logger.error(f"{response['error']}: {response['info']}")
            else:
                result, photo = response
                if result:
                    self.last_take = datetime.datetime.now()
                    logger.debug(f"Success recognise. Number {result}")
                    self.can_wait_others = False
                    self.wait_started = False
                    self.active = True
                    return result
                else:
                    logger.error(
                        f"Unknown Error! Number {result}")
            if self.failed_callback and i == 2:
                logger.debug(f'Failed callbaсk working photo...')
                self.failed_callback()
        self.active = True
        self.wait_started = False

    def camera_and_recognise(self):
        result = self.try_recognise_plate()
        if 'error' in result:
            return result
        photo, result = result['photo'], result['number']
        if result:
            if self.debug:
                self.save_pic(f"{str(uuid.uuid4())}.jpg", photo)
            if self.engine_callback:
                threading.Thread(target=self.engine_callback,
                                 args=(result, photo)).start()
            if self.callback_request_url:
                threading.Thread(target=self.http_callback,
                                 kwargs={'number': result}).start()
        return result, photo

    def http_callback(self, number):
        requests.post(self.callback_request_url,
                      params={'number': number})

    def try_recognise_plate(self):
        logger.debug(f'Taking photo...')
        photo = self.cam.take_shot()
        result = self.neurocore_worker.get_car_number(photo)
        return result

    def set_post_request_url(self, url):
        self.callback_request_url = url
        return url


class CADEntrance(AutoExit):
    """ Детекция автомобиля на брутто """
    pass


if __name__ == '__main__':
    def engine_callback(*args, **kwargs):
        print('MAIN')


    inst = AutoExit(  #
        'http://127.0.0.1',
        # 'http://172.16.6.176',
        'admin',
        'Assa+123',
        debug=True,
        #        cam_port=80,
        # 1920*1080
        resize_photo=(250, 100, 1200, 1100),
        cam_port=82,
        neurocore_login='admin',
        neurocore_password='admin',
        engine_callback=engine_callback
    )
    # inst.set_post_request_url('http://127.0.0.1:8080/start_auto_exit')
    res = inst.try_recognise_plate()
    # print(res.keys())
    # if 'error' in res:
    #    print(res)
    inst.start()
