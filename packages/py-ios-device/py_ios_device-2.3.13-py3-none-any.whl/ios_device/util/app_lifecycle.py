from collections import namedtuple
from dataclasses import dataclass

from ios_device.util.kperf_data import KDBG_EVENTID_MASK, KDBG_FUNC_MASK, kdbg_extract_class, kdbg_extract_subclass, \
    kdbg_extract_code, KdBufParser

AppLifeEvent = namedtuple('AppLifeEvent', ['period', 'sub_state', 'time', 'thread', 'kind'])


class Node:
    # 初始化一个节点
    def __init__(self, val=None):
        self.val = val  # 节点值
        self.l_child = []  # 子节点列表

    # 添加子节点
    def add_child(self, node):
        self.l_child.append(node)


class AppLifeCycle:

    def __init__(self):
        self.events = []
        self.process = None

    def app_launching(self, process):
        self.process = process

    def update_app_period(self, data: AppLifeEvent):
        print(data)
        self.events.append(data)

    def decode_app_lifecycle(self, event: KdBufParser, thread):
        """ 判断顺序非常重要，同一个 kdcode 可能值一样，但是根据顺序表述不一样，且事件会重复出现多次
        """

        if event.class_code == 0x1f:  # dyld-init
            if event.subclass_code == 0x7 and event.final_code == 13:
                self.update_app_period(AppLifeEvent('Initializing',
                                                    'System Interface Initialization', event.timestamp, thread, 'BEGIN'))
            elif event.subclass_code == 0x7 and event.final_code == 1:
                self.update_app_period(AppLifeEvent('Initializing',
                                                    'System Interface Initialization', event.timestamp, thread, 'END'))
                self.update_app_period(AppLifeEvent('Initializing',
                                                    'Static Runtime Initialization', event.timestamp, thread, 'END'))

        elif event.class_code == 0x31 and event.subclass_code == 0xca and event.final_code == 1 and event.func_code == 2:  # AppKit/UIKit common application launch phases
            self.update_app_period(AppLifeEvent('Launching',
                                                'Initial Frame Rendering', event.timestamp, thread, 'END'))

        elif event.class_code == 0x2b:
            if event.subclass_code == 0xd8:  # appkit-init
                if event.final_code == 1:
                    #     (not (main-ui-thread (thread ?thread)))
                    #     ?a <- (main-ui-thread (thread ?thread) (kind UIKIT))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'System Interface Initialization', event.timestamp, thread, 'END'))
                elif event.final_code == 12 and event.func_code == 0:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'AppKit Initialization', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'AppKit Scene Creation', event.timestamp, thread, 'BEGIN'))
                elif event.final_code == 12 and event.func_code == 1:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'AppKit Scene Creation', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'applicationWillFinishLaunching()', event.timestamp, thread, 'BEGIN'))
                elif event.final_code == 12 and event.func_code == 2:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'applicationWillFinishLaunching()', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'AppKit Scene Creation', event.timestamp, thread, 'BEGIN'))
                elif event.final_code == 11 and event.func_code == 1:
                    #     (main-ui-thread (thread ?thread) (kind MARZIPAN))

                    self.update_app_period(AppLifeEvent('Launching',
                                                        'AppKit Scene Creation', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'applicationDidFinishLaunching()', event.timestamp, thread, 'BEGIN'))

                elif event.final_code == 11 and event.func_code == 2:
                    #     (main-ui-thread (thread ?thread) (kind APPKIT))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'applicationDidFinishLaunching()', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'Initial Frame Rendering', event.timestamp, thread, 'BEGIN'))
            elif event.subclass_code == 0x87:  # UIKit application launch phases
                if event.final_code == 90:
                    #     (assert (main-ui-thread (thread ?thread) (kind UIKIT)))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Initialization', event.timestamp, thread, 'BEGIN'))
                elif event.final_code == 21:
                    #     (main-ui-thread (thread ?thread) (kind UIKIT))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Initialization', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'BEGIN'))

                    #     (main-ui-thread (thread ?thread) (kind MARZIPAN))
                    # self.update_app_period(AppLifeEvent('Initializing',
                    #                                     'AppKit Scene Creation', time, thread, 'END'))
                    # self.update_app_period(AppLifeEvent('Initializing',
                    #                                     'UIKit Scene Creation', time, thread, 'BEGIN'))

                elif event.final_code == 23:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'willFinishLaunchingWithOptions()', event.timestamp, thread, 'BEGIN'))
                elif event.final_code == 24:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'willFinishLaunchingWithOptions()', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'BEGIN'))

                elif event.final_code == 25:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'didFinishLaunchingWithOptions()', event.timestamp, thread, 'BEGIN'))

                elif event.final_code == 26:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'didFinishLaunchingWithOptions()', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'BEGIN'))

                elif event.final_code == 300:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'sceneWillConnectTo()', event.timestamp, thread, 'BEGIN'))
                elif event.final_code == 301:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'sceneWillConnectTo()', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'BEGIN'))
                elif event.final_code == 312:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'sceneWillEnterForeground()', event.timestamp, thread, 'BEGIN'))

                elif event.final_code == 313:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'sceneWillEnterForeground()', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'BEGIN'))

                elif event.final_code == 12:
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'UIKit Scene Creation', event.timestamp, thread, 'END'))
                    self.update_app_period(AppLifeEvent('Launching',
                                                        'Initial Frame Rendering', event.timestamp, thread, 'BEGIN'))
