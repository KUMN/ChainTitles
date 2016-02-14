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


def dedup_titles(fromfilenameandpath, tofilenameandpath, frompoint):
    fromfilehandle = open(fromfilenameandpath, 'r')
    fromfilehandle.seek(frompoint)
    counter = 0    
    for from_line_read in fromfilehandle.readlines():
        '''
        dict_of_title = ast.literal_eval(line_read)
        title_list = dict_of_title['concatstr']
        title_list = dict_of_title['titles']
        '''
        line_exists = False
        tofilehandle = open(tofilenameandpath, 'r')
        for to_line_read in tofilehandle.readlines():
            if (cmp (from_line_read, to_line_read) == 0):
                line_exists = True
                counter = counter + 1
                break
        if (line_exists == False):
            writefilehandle = open(tofilenameandpath, 'a')
            writefilehandle.write(from_line_read)
            writefilehandle.close() 
    
    print ('deduped!' +  str (counter))  
        
    
    

print ("Here I am!")
if __name__ == "__main__":
    directory_base = 'C:\Namita\Official\Projects\APP\C8\Olymp\Ch\FilesToProcess'
    filenameConfigs = 'Config.txt'
    config_file_pathandname = directory_base + '\\' + filenameConfigs
    given_filename, given_file_offset, derived_filename, derived_file_offset = config_read(config_file_pathandname)
    copyfile = directory_base + '\\' + 'copyof' + derived_filename
    dedupfile = directory_base + '\\' + 'DedupedFile.txt'
        
    dedup_titles(copyfile, dedupfile, derived_file_offset)
    