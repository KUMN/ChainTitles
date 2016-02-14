
import shutil
import ast

def config_read(config_name):
    config_handle = open(config_name, 'r')
    config_line = config_handle.readline()
    print config_line
    config_dict = ast.literal_eval(config_line)
    given_filename = config_dict['GivenFile']
    given_file_offset = config_dict['GivenFileOffset']
    derived_filename = config_dict['DerivedFile']
    derived_file_offset = config_dict['DerivedFileOffset']
    #dir_path = config_dict['DirectoryPath']
    return given_filename, given_file_offset, derived_filename, derived_file_offset

def write_list_of_titles (fullpathandname, title_list):
    file_handle = open (fullpathandname, 'w')
    for title in title_list:
        file_handle.write(title)
    file_handle.close()

def get_max_titles(fromfilenameandpath, tofilenameandpath):
    filehandle = open(fromfilenameandpath, 'r')
    max_num_of_titles = 0
    max_title_list = []
    counter = 0
    for line_read in filehandle.readlines():
        counter = counter + 1
        dict_of_title = ast.literal_eval(line_read)
        title_list = dict_of_title['titles']
        if (len(title_list) > max_num_of_titles):
            max_num_of_titles = len(title_list)
            max_title_list = title_list
            print max_num_of_titles
            print max_title_list
            #print counter
    write_list_of_titles(tofilenameandpath, max_title_list)
    
    

print ("Here I am!")
if __name__ == "__main__":
    directory_base = 'C:\Namita\Official\Projects\APP\C8\Olymp\Ch\FilesToProcess'
    filenameConfigs = 'Config.txt'
    config_file_pathandname = directory_base + '\\' + filenameConfigs
    given_filename, given_file_offset, derived_filename, derived_file_offset = config_read(config_file_pathandname)
    maxtitlesfile = directory_base + '\\' + 'MaxTitles.txt'
    
    sourcefile = directory_base + '\\' + derived_filename
    destinationfile = directory_base + '\\' + "copyof" + derived_filename 
    shutil.copyfile(sourcefile, destinationfile)
    get_max_titles(destinationfile, maxtitlesfile)
    