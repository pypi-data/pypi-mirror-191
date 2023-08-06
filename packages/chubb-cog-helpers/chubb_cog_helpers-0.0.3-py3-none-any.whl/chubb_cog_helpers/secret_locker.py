import os
import json
import base64

def sl_encode(text):
    return base64.b64encode(text.encode()).decode()

def sl_decode(text):
    return base64.b64decode(text.encode()).decode()

class SecretLocker:
    file_path = ''
    name = ''
    json = ''

    def __init__(self, locker_name):
        self.name = locker_name

        secret_lp = os.path.abspath(os.getcwd()) + '\\.secrets'
        secret_fp = secret_lp + '\\' + locker_name + '.b64'

        self.file_path = secret_fp

        if not os.path.exists(secret_lp):
            os.mkdir(secret_lp)

            secret_file = open(secret_fp, 'x')
            secret_file.close()
        else:
            if not os.path.exists(secret_fp):
                print('Creating new Locker')
                
                secret_file = open(secret_fp, 'x')
                secret_file.close()
            else:
                print('Opening existing Locker')

                with open(self.file_path, 'r') as f:
                    self.json = sl_decode(f.read()).replace('\n', '')

    def add_secret(self, secret_name, secret):
        if self.json == '':
            secret_dict = {}
        else:
            secret_dict = json.loads(self.json)

        try:
            secret_dict[secret_name]
            print('The secret already exists in the locker')
        except KeyError as error:
            secret_dict[secret_name] = secret

            self.json = json.dumps(secret_dict)

            with open(self.file_path, 'w') as f:
                f.write(sl_encode(self.json))
                f.close()

    def change_secret(self, secret_name, secret):
        try:
            secret_dict = json.loads(self.json)

            try:
                secret_dict[secret_name] = secret

                self.json = json.dumps(secret_dict)

                with open(self.file_path, 'w') as f:
                    f.write(sl_encode(self.json))
                    f.close()
            except KeyError as error:
                print('The secret does not exist in the locker')
        except:
            print('Locker contains no secrets')

    def drop_secret(self, secret_name):
        try:
            secret_dict = json.loads(self.json)

            try:
                del secret_dict[secret_name]

                self.json = json.dumps(secret_dict)

                with open(self.file_path, 'w') as f:
                    f.write(sl_encode(self.json))
                    f.close()
            except KeyError as error:
                print('The secret does not exist in the locker')
        except:
            print('Locker contains no secrets')
            
    def get_secret(self, secret_name):
        try:
            secret_dict = json.loads(self.json)
            
            try:
                return secret_dict[secret_name]
            except:
                print('The secret does not exist in the locker')
        except:
            print('Locker contains no secrets')