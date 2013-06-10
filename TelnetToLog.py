import telnetlib
import time
import sys
import os.path

class TelnetHost:
    def __init__(self):
        self.ip ="10.245.255.82"
        self.user ="radio"
        self.password="radio"

def SendCmd(last_reply, input, expected_reply, Timeout = 2):
    print last_reply + input
    
    input = input + "\r\n"
    tn.write(input)
    time.sleep(0.5)
    
    output = tn.read_until(expected_reply, timeout = Timeout)
    
    return output
    
def AccessToRunCmdAndOutputtoLog(host, cmd_path):
    if os.path.exists(cmd_path) == False:
        return
        
    log_path = cmd_path.rsplit('.', 1)
    log_path = log_path[0] + "_log." + log_path[1]
    
    if os.path.exists(log_path) == True:
        return

    log_file = open(log_path,'w')
    
    old_stdout = sys.stdout
    
    last_reply = tn.read_until("login: ", timeout = 2)
    
    if len(last_reply) == 0:
        return

    last_reply = SendCmd(last_reply, host.user, "Password: ")
    
    if len(last_reply) == 0:
        return
    
    last_reply = SendCmd(last_reply, host.password, "{radio} #: ")
    
    if len(last_reply) == 0:
        return
    
    cmd_file = open(cmd_path, 'r')
    
    num_of_lines = 0
    expected_reply = ""
    cmd = ""
    Timeout_f = 0
    PrintToLog = 0
    
    for line in cmd_file:
        num_of_lines += 1
        
        line = line.strip("\n")
        
        if num_of_lines % 3 == 1:
            cmd = line
            
        elif num_of_lines % 3 == 2:
            expected_reply = line
            
        elif num_of_lines % 3 == 0:
            config = line.split(';')
            
            Timeout_f = float(config[0])       
            
            if PrintToLog != 0:
                sys.stdout = log_file
            else:
                sys.stdout = old_stdout
                
            try:
                last_reply = SendCmd(last_reply, cmd, expected_reply, Timeout = Timeout_f)
                
            except ValueError, TypeError:
                last_reply = SendCmd(last_reply, cmd, expected_reply)
                
            expected_reply = ""
            cmd = ""
            Timeout_f = 0
            PrintToLog = int(config[1])
            
            if len(last_reply) == 0:
                break
    
    if len(last_reply) > 0:
        if PrintToLog != 0:
            sys.stdout = log_file
        else:
            sys.stdout = old_stdout
                
        print last_reply
    
    print tn.read_eager()

    tn.close()

    sys.stdout = old_stdout
    
    cmd_file.close()
    log_file.close()
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit()
    
    if len(sys.argv) > 3:
        sys.exit()
    
    if len(sys.argv) == 3:
        if sys.argv[2] == "-NoScreen":
            old_stdout = sys.stdout
            nul_f = open('nul', 'w')
            sys.stdout = nul_f
    
    host = TelnetHost()

    #Try to access host
    try:
        tn = telnetlib.Telnet(host.ip)
    except:
        print "Cannot open " + host.ip
        exit()
    
    AccessToRunCmdAndOutputtoLog(host, sys.argv[1])
    
    if len(sys.argv) == 3:
        if sys.argv[2] == "-NoScreen":
            sys.stdout = old_stdout
            nul_f.close()