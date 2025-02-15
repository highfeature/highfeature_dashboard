import platform  # For getting the operating system name
import subprocess  # For executing a shell command
from time import sleep

from celery import shared_task


@shared_task(bind=True)
def ping_task(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Option for the number of packets as a function of
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Building the command. Ex: "ping -c 1 google.com"
    command = ["ping", param, "1", host]
    ret = subprocess.call(command)
    return ret


@shared_task(bind=True)
def test_task():
    for i in range(1, 11):
        print(i)
        sleep(1)
    return "Task Completed"
