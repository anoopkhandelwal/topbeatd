import logging

from flask import Flask, render_template

from Constants import Constants
from GetAllProcessInfo import get_all_process_info
from GetFileSystemInfo import get_file_system_info
from GetSystemInfo import get_system_info

app = Flask(__name__)
logging.getLogger(__name__)


@app.route('/info/system/', methods=['GET'])
def get_system_information():
    try:
        category_cpu = []
        category_cpu_p = []
        category_load = []
        category_memory = []
        category_swap = []

        cpu_io_wait = []
        cpu_system = []
        cpu_user = []
        cpu_idle = []

        cpu_system_p = []
        cpu_user_p = []

        load_1 = []
        load_5 = []
        load_15 = []

        mem_used = []
        mem_total = []
        mem_free = []

        swap_free = []
        swap_total = []
        swap_used = []

        data_points = get_system_info()
        for point in data_points:
            cpu_io_wait.append([str(point['@timestamp']), point['cpu.iowait']])
            cpu_system.append([str(point['@timestamp']), point['cpu.system']])
            cpu_user.append([str(point['@timestamp']), point['cpu.user']])
            cpu_idle.append([str(point['@timestamp']), point['cpu.idle']])

            cpu_system_p.append([str(point['@timestamp']), point['cpu.system_p']])
            cpu_user_p.append([str(point['@timestamp']), point['cpu.user_p']])

            load_1.append([str(point['@timestamp']), point['load.load1']])
            load_5.append([str(point['@timestamp']), point['load.load5']])
            load_15.append([str(point['@timestamp']), point['load.load15']])

            mem_free.append([str(point['@timestamp']), point['mem.free']])
            mem_total.append([str(point['@timestamp']), point['mem.total']])
            mem_used.append([str(point['@timestamp']), point['mem.used']])

            swap_free.append([str(point['@timestamp']), point['swap.free']])
            swap_total.append([str(point['@timestamp']), point['swap.total']])
            swap_used.append([str(point['@timestamp']), point['swap.used']])

        category_cpu.append({'name': 'CPU Usage System', 'data': cpu_system})
        category_cpu.append({'name': 'CPU IO Wait', 'data': cpu_io_wait})
        category_cpu.append({'name': 'CPU Usage User', 'data': cpu_user})
        category_cpu.append({'name': 'CPU Idle', 'data': cpu_idle})

        category_cpu_p.append({'name': 'CPU Usage System(%)', 'data': cpu_system_p})
        category_cpu_p.append({'name': 'CPU Usage User(%)', 'data': cpu_user_p})

        category_load.append({'name': 'Load 1', 'data': load_1})
        category_load.append({'name': 'Load 5', 'data': load_5})
        category_load.append({'name': 'Load 15', 'data': load_15})

        category_memory.append({'name': 'Memory Total', 'data': mem_total})
        category_memory.append({'name': 'Memory Free', 'data': mem_free})
        category_memory.append({'name': 'Memory Used', 'data': mem_used})

        category_swap.append({'name': 'Swap Total', 'data': swap_total})
        category_swap.append({'name': 'Swap Free', 'data': swap_free})
        category_swap.append({'name': 'Swap Used', 'data': swap_used})

        print category_memory
        return render_template("SystemInfo.html", category_cpu=category_cpu, category_cpu_p=category_cpu_p,
                               category_load=category_load, category_swap=category_swap,
                               category_memory=category_memory)
    except Exception as e:
        logging.info("exception {0}".format(e))


@app.route('/info/process', methods=['GET'])
def get_process_information():
    return get_all_process_info()


@app.route('/info/filesystem', methods=['GET'])
def get_filesystem_information():
    return get_file_system_info()


if __name__ == '__main__':
    app.run(host=Constants.HOSTNAME, port=Constants.PORT, threaded=True)
