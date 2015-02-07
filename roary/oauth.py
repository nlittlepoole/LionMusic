import pxssh
import getpass




def login(host,psswd):
    '''
    Auther: @niger
    Take in a uni and password and check cunix for succesful login
    use lookup unix command to pull department
    '''
    s = pxssh.pxssh()
    try:
        if not s.login ('cunix.cc.columbia.edu', host, psswd):
            return None
        else:
            user = {'uni':host}
            s.sendline ('lookup ' + host )
            s.prompt()         # match the prompt
            data = str(s.before )    # contains everything before the prompt.
            s.logout()

            # make indexes for string splitting
            start = data.find('Dept:') +5 if data.find('Dept:')>0 else -1
            end  = data.find('Address:') if data.find('Address:')>0 else -1
            res  = data.find('Residence:') +10 if data.find('Address:')>0 else -1


            if start + end >0:
                user['dept'] =data[start:end].strip()
            if res > 0:
                user['dorm'] = ' '.join(data[res:].strip().split(' ')[1:]) # removes white space and remove room # from residence adress

            return user
    except Exception as e:
        return None

if __name__ == '__main__':
    host = raw_input('username\n')
    print "password:\n"
    psswd = getpass.getpass()
    print login(host,psswd)
