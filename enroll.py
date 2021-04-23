
from zk import ZK, const
from time import sleep
import sys

device_ip = '192.168.1.201'
device_id = 4


def connection(ip, port=4370, password=0):
    zk = ZK(ip, port=port, timeout=20, password=password, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    print('Connecting ...')
    conn.disable_device()
    print('Device Disabled')
    return conn


def disconnect(conn):
    conn.enable_device()
    print('Device Enabled')
    conn.disconnect()
    print('Device Disconnected')


def exit_program(conn):
    disconnect(conn)
    sys.exit()


def after_employee_add(conn):
    while True:
        print('1- Add Another Employee')
        print('9- Back to the main menu')
        print('0- Exit the program')
        choice = input('Choice Number: ')
        if int(choice) == 1:
            add_employee(conn)
        elif int(choice) == 9:
            main_screen(conn)
        elif int(choice) == 0:
            exit_program(conn)
        else:
            print('Please Enter Correct Choice Number')


def add_employee(conn):
    name = input('Employee Name: ')
    user_id = int(input('Employee ID: '))
    # Some Operation Here
    conn.set_user(uid=user_id, name=name, privilege=const.USER_DEFAULT, password='101089', group_id='', user_id=str(user_id), card=0)
    print('Employee Added Successfully')
    after_employee_add(conn)


def main_screen(conn):
    while True:
        print('Welcome To Smart Business FinerPrint App')
        print('========================================')
        print('How Can I Help You?')
        print('1- Add Employee')
        print('2- Reboot Device')
        print('3- Ensure Date/Time')
        print('4- Show Device Serial Number')
        print('5- Show Device Mac Address')
        print('6- Download FingerPrints')
        print('0- Exit The Program')
        choice = input('Choice Number: ')
        if int(choice) == 1:
            add_employee(conn)
        elif int(choice) == 2:
            conn.restart()
        elif int(choice) == 3:
            conn.get_time()
        elif int(choice) == 4:
            conn.serialnumber()
        elif int(choice) == 5:
            conn.get_mac()
        elif int(choice) == 6:
            fingers = conn.get_templates()
            print(fingers)
        elif int(choice) == 0:
            exit_program(conn)


def main():
    while True:
        try:
            conn = connection(device_ip)
            main_screen(conn)
        except Exception as e:
            print(e)
            print('Device Connection Failed .. Please Reboot Device And Try Again Later')
            print('Do You Want To Try Again?')
            print('1- Yes')
            print('2- No, Exit The Program')
            choice = input('Choice Number: ')
            if int(choice) == 1:
                continue
            elif int(choice) == 2:
                exit_program(conn)


main()