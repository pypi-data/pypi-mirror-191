import os,time;from colorama import Fore

class color:
    positive = Fore.GREEN
    negative = Fore.RED
    reset = Fore.RESET
def nlog(arguments=None):

    localtime = time.localtime();date = time.strftime('%Y/%m/%d', localtime)

    path = date;path = f'logs/{path}'

    if not os.path.exists(path):
        os.makedirs(path)
    path = open(f'{path}/log.txt', 'a')
    path.write(f'[{time.strftime("%Y-%m-%d %H:%M:%S", localtime)}] {arguments}\n' if arguments else f'[{time.strftime("%Y-%m-%d %H:%M:%S", localtime)}]\n')
    return (f'[{color.positive}{time.strftime("%Y-%m-%d %H:%M:%S", localtime)}{color.reset}] {arguments}\n' if arguments else f'[{time.strftime("%Y-%m-%d %H:%M:%S", localtime)}]\n')