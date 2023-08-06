import requests
from subprocess import check_output
from cryptography.fernet import Fernet
from socket import gethostname


class Serialation:
    '''
    A class to manage users authorization of Dabour Scripts.
    '''

    def __init__(self, delimiter='XXX', base_url=None, token=None):
        self.delimiter = delimiter
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Token {token}'})
        self.machine_name = gethostname()
        self.machine_token = self.__serial_token_complex()

        self.original_hd_serial = None
        self.original_proc_id = None
        self.remote_hd_serial = None
        self.remote_proc_id = None

        self.first_time_run = None
        self.__check_machine_sub()

        if self.first_time_run == True:
            self.__create_subscription()

    def __check_machine_sub(self):
        resp = self.session.get(
            f"{self.base_url}/api/v1/subscriptions/{self.machine_name}")

        if resp.status_code == 404:
            self.first_time_run = True
        else:
            self.first_time_run = False

        return resp.status_code

    def __get_serials(self):
        '''
        This function will get the hd serials and procID serial.
        Then it compine it with the delimmiter to add more security layer.
        '''
        hardserial = 'wmic diskdrive get serialnumber'
        processorid = 'wmic cpu get processorid'
        hardserial = check_output(
            hardserial, shell=True).decode().split('\n')[1].strip()

        processorid = check_output(
            processorid, shell=True).decode().split('\n')[1].strip()
        return f"{hardserial}{self.delimiter}{processorid}"

    def __encrypt_serial(self, serial: str):
        '''
        This function will encrypt the machine serials to secure requests.
        '''
        key = Fernet.generate_key()
        fnt = Fernet(key)
        token = fnt.encrypt(serial.encode())
        phone = self.delimiter.encode()
        return token + phone + key

    def __serial_token_complex(self):
        '''
        This function response will go through the network 
        then our server will recieve it's response as a request
        with encrypted tokens.

        >>> user = Serialation()
        >>> serial = user.serial_token_complex()
        '''
        complex_serials = self.__get_serials()
        serial_token_complex = self.__encrypt_serial(complex_serials)
        return serial_token_complex

    def __calculate_serial(self, clean_serial):
        '''
        This function can calculate a complex serial number
        that we got from the server.

        It extracts information from the response of the request
        and then calculate it based on the return value

        Then it will return True if the client machine has the same
        serials as in the request from the begining.

        >>> user = Serialation()
        >>> serial = user.serial_token_complex()

        >>> is_authorized = user.calculate_serial(serial)
        '''
        key = clean_serial.split(
            self.delimiter.encode())[1]
        token = clean_serial.split(
            self.delimiter.encode())[0]
        fnt = Fernet(key)
        serial = fnt.decrypt(token)
        hard_desk_serial = serial.decode().split(self.delimiter)[0]
        processor_serial = serial.decode().split(self.delimiter)[1]

        original_serials = self.__get_serials().split(self.delimiter)
        original_serial_hard = original_serials[0]
        original_serial_proc = original_serials[1]

        self.original_hd_serial = original_serial_hard
        self.original_proc_id = original_serial_proc

        self.remote_hd_serial = hard_desk_serial
        self.remote_proc_id = processor_serial

        return True

    def __clean_serial_from_json(self, complex_serial):
        '''
        This function can clean serial when it comes dirty.
        '''
        clean = str(complex_serial).removesuffix(
            "'").removeprefix("b'").encode()
        return clean

    def get_auth_token(self, username, password):
        data = {
            'username': f'{username}',
            'password': f'{password}',
        }
        if self.base_url:
            resp = requests.post(f'{self.base_url}/api/v1/token/', data=data)
            return resp.json()['token']
        else:
            raise Exception(
                "\n\n====> You have to pass a base_url \n====> client = Serialation(base_url='yourapi.com')\n\n")

    def __create_subscription(self, name=None):
        '''
        This function will create new client and send it to the server.
        You have to go to the server panel and activate this user.

        This function must run one time ever.
        '''
        if not name:
            name = self.machine_name
        data = {'serial_number': self.machine_token,
                'subscriper_name': name, 'machinename': self.machine_name}
        resp = self.session.post(
            f"{self.base_url}/api/v1/subscriptions/", data=data)
        return resp.status_code

    def __get_sub_info(self):
        subs = self.session.get(
            f"{self.base_url}api/v1/subscriptions/{self.machine_name}")
        return subs.json()

    def check_sub_serial(self):
        '''
        This function can compares the remote serials to machine one.
        It returns True if everything is OK else it returns False.
        '''
        sub_serial = self.__get_sub_info()['serial_number']
        calc = self.__calculate_serial(sub_serial.encode())
        if calc:
            if (self.original_hd_serial == self.remote_hd_serial) and (self.original_proc_id == self.remote_proc_id):
                return True
            else:
                return False

    def check_sub_active(self):
        info = self.__get_sub_info()['is_active']
        return info

    def check_sub_paid(self):
        info = self.__get_sub_info()['is_paid']
        return info

    def get_sub_days_left(self):
        '''
        How many days before expired
        '''
        num_days = self.__get_sub_info()['number_of_days']
        check_expiration_days = self.__get_sub_info()['check_expiration_days']
        days_left = num_days - check_expiration_days
        return days_left

    def check_expired(self):
        '''
        Check if subscription is expired
        '''
        num_days = self.__get_sub_info()['number_of_days']
        delta_days = self.__get_sub_info()['check_expiration_days']
        if delta_days >= num_days:
            return True
        else:
            return False
