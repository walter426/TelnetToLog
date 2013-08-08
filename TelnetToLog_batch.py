import time
import sys
import os.path
import subprocess

def TelnetToLogFromTemplate_batch(log_dir_path, template_dir_path):
    #Verify input
    if os.path.exists(log_dir_path) == False:
        print "Log directory does not exist!"
        return
    
    if os.path.exists(template_dir_path) == False:
        print "Template directory does not exist!"
        return
    
    log_list_path = log_dir_path + "\list.txt"

    if os.path.exists(log_list_path) == False:
        print "'list.txt' does not exist in the log directory!"
        return

    #add template paths
    template_paths = []
    
    for dirname, dirnames, filenames in os.walk(template_dir_path):
        #for subdirname in dirnames:
        #    print os.path.join(dirname, subdirname)
        
        for filename in filenames:
            template_paths.append(filename)
            #print template_paths
            #print os.path.join(dirname, filename)
    
    #Create script from the template and run it
    log_list_file = open(log_list_path, 'r')
    idx = 0
     
    for ArgList in log_list_file:
        idx += 1
        str_ArgList = ArgList.strip("\n")
        ArgList = str_ArgList.split(",")
        
        for arg_idx in range(len(ArgList)):
            ArgList[arg_idx] = ArgList[arg_idx].strip().rstrip()
            
        
        #Create cmd file from the template
        cmd_path_group = []
        process_group = []
        
        for template_path in template_paths:
            template_file = open(os.path.join(template_dir_path, template_path), 'r')
            
            template_name = template_path.rsplit('.', 1)
            template_name = template_name[0]

            cmd_path = os.path.join(log_dir_path, str(idx).zfill(3)+ "_" + "_".join(ArgList) + "_" + template_name + ".txt")
            cmd_path_group.append(cmd_path)
            
            cmd_file = open(cmd_path, 'w')
            
            for line in template_file:
                for arg_idx in range(len(ArgList)):
                    line = line.replace("arg_" + str(arg_idx), str(ArgList[arg_idx]))
   
                cmd_file.write(line)

            cmd_file.close()
            
            process_group.append(subprocess.Popen(os.getcwd() + "\TelnetToLog.py " + cmd_path + " -NoScreen", shell = True)) 
            
            template_file.close()
            
        for process in process_group:
            process.wait()

        for cmd_path in cmd_path_group:
            os.remove(cmd_path)
            
        print str_ArgList + " done!"
            
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit()
    
    TelnetToLogFromTemplate_batch(sys.argv[1], sys.argv[2])
