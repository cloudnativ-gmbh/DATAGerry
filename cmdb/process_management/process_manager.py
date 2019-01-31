import importlib
import multiprocessing
import threading
import re

class ProcessManager:

    def __init__(self):
        # service definitions (in correct order)
        self.__service_defs = []
        self.__service_defs.append(CmdbProcess("exampleservice1", "cmdb.process_management.example_service.ExampleService"))
        self.__service_defs.append(CmdbProcess("webapp", "cmdb.interface.gunicorn.WebCmdbService"))

        # processlist
        self.__process_list = []

        # process controller
        self.__process_controllers = []

        # shutdown flag
        self.__flag_shutdown = threading.Event()

    def start_app(self):
        # start all services from service definitions
        for service_def in self.__service_defs:
            service_class = self.__load_class(service_def.get_class())
            process = multiprocessing.Process(target=service_class().start)
            process.start()
            self.__process_list.append(process)
            # start process controller
            proc_controller = ProcessController(process, self.__flag_shutdown, self.stop_app)
            proc_controller.start()
            self.__process_controllers.append(proc_controller)

        # wait for process controllers
        for proc_controller in self.__process_controllers:
            proc_controller.join()


    def stop_app(self):
        self.__flag_shutdown.set()
        # go through processes in different order
        for process in reversed(self.__process_list):
            process.terminate()

    def __load_class(self, classname):
        """ load and return the class with the given classname """
        # extract class from module
        pattern = re.compile("(.*)\.(.*)")
        match = pattern.fullmatch(classname)
        if match is None:
            raise Exception("Could not load class {}".format(classname,))
        module_name = match.group(1)
        class_name = match.group(2)
        loaded_module = importlib.import_module(module_name)
        loaded_class = getattr(loaded_module, class_name)
        return loaded_class


class CmdbProcess:

    def __init__(self, name, classname):
        self.__name = name
        self.__classname = classname

    def get_name(self):
        return self.__name

    def get_class(self):
        return self.__classname


class ProcessController(threading.Thread):

    def __init__(self, process, flag_shutdown, cb_shutdown):
        super(ProcessController, self).__init__()
        self.__process = process
        self.__flag_shutdown = flag_shutdown
        self.__cb_shutdown = cb_shutdown

    def run(self):
        self.__process.join()
        # terminate app, if process crashed
        if not self.__flag_shutdown.is_set():
            self.__cb_shutdown()


