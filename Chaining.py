import ast

def config_read(config_name):
    config_handle = open(config_name, 'r')
    config_line = config_handle.readline()
    #print config_line
    config_dict = ast.literal_eval(config_line)
    given_filename = config_dict['GivenFile']
    given_file_offset = config_dict['GivenFileOffset']
    derived_filename = config_dict['DerivedFile']
    derived_file_offset = config_dict['DerivedFileOffset']
    #dir_path = config_dict['DirectoryPath']
    return given_filename, given_file_offset, derived_filename, derived_file_offset
    
def config_write(config_name, given_file, given_file_offset, derived_file, derived_file_offset):
    config_handle = open(config_name, 'w')
    config_line = "{'GivenFile': '" + given_file + "', 'GivenFileOffset': " + str(given_file_offset) +", 'DerivedFile' : '" + derived_file + "', 'DerivedFileOffset' :" + str(derived_file_offset) +"}\n"
    #print (config_line)
    config_handle.write(config_line)
    config_handle.close()
    
def write_list_of_dicts (fullpathandname, dict_list):
    file_handle = open (fullpathandname, 'a')
    for dictitem in dict_list:
        concat_title = ' '.join(dictitem["concatstr"])
        line_to_write = "{'concatstr': \"" + concat_title + "\", 'titles': " + str(dictitem["titles"]) +"}\n"
        #print (line_to_write)
        file_handle.write(line_to_write)
    file_handle.close()
    

def read_line_titles(linetype, line_read):
    if linetype == 'original':
        title = line_read
        title_list = [line_read]
    else:
        dict_of_title = ast.literal_eval(line_read)
        title = dict_of_title['concatstr']
        title_list = dict_of_title['titles']
    return title, title_list
    
    

def is_a_match (titleOne, titleTwo):
    titleA = titleOne
    titleB = titleTwo
    split_titleA = titleA.split()
    split_titleB = titleB.split()
    lenA = len(split_titleA)
    lenB = len(split_titleB)
    concatstr = None
    #print (lenA)
    #print (lenB)
        
    startB = 0
    if lenA > lenB:
        startA = lenA - lenB
        #print ('startA is : ' + str(startA))
    else:
        startA = 0
        
    is_match = False
    i = startA
    j = startB
    nextA = 0
        
    while (is_match == False and i < lenA):
        #print split_titleA[i]
        while ((i<lenA) and (split_titleA[i] == split_titleB[j])) :
            #print i
            #print j
            #print split_titleA[i]
            #print split_titleB[j]
            i = i + 1
            j = j + 1
            #print i
            #print j
        if (i == lenA):
            is_match = True
            #store the concatenated string in a list of dicts
            #open file and write to its bottom the new string|filename
            #open filename write the string and add titleTwo
            concatstr = split_titleA[:startA+nextA] + split_titleB[0:]
            #print (concatstr)
        else:
            nextA = nextA + 1
            i = startA + nextA
            #print ('next' + str(i))
            j = startB
            #print ('next' + str(j))
            
    return (is_match, concatstr)
    #return the list of dicts {origstr:, concatstr: , titlesinstr:}

    


def compare_titles_in_files(processtype, filepathandname, fileoffset, titleOne, titlesinOne, listofdicts):
    #filepathandname = dir_to_read + '\\' + filename1
    #read_filehandle_1 = open(filepathandname, 'r')
    #titleOne = read_filehandle_1.readline()
    #fileoffset = read_filehandle_1.tell()
    #read_filehandle_1.close()
    
    read_filehandle_2 = open(filepathandname, 'r')
    read_filehandle_2.seek(fileoffset)
    lineTwo = read_filehandle_2.readline()
    innerlistofdicts = listofdicts
    
    while lineTwo:
        titleTwo, titlesinTwo = read_line_titles(processtype, lineTwo)
        #print (titleOne + ' ' + titleTwo)
        #compare titles in One and Two - that there are no duplicates. If duplicates are there then ignore this match
        #print ('Titles in two ' + str(titlesinTwo))
        #print ('Titles in one ' + str(titlesinOne))
        #print (set(titlesinTwo).intersection(titlesinOne))
        if (len(set(titlesinTwo).intersection(titlesinOne)) == 0):
            is_match, newconcatstr = is_a_match (titleOne, titleTwo)
            if (is_match == True):
                
                newdict = {'origstr': titleOne, 'concatstr': newconcatstr, 'titles': titlesinOne+titlesinTwo}
                #print (newconcatstr)
                #print (newdict)
                innerlistofdicts.append(newdict)
         
            is_match, newconcatstr = is_a_match (titleTwo, titleOne)
            if (is_match == True):
                #compare titles in One and Two - that there are no duplicates. If duplicates are there then ignore this match
                newdict = {'origstr': titleTwo, 'concatstr': newconcatstr, 'titles': titlesinTwo+titlesinOne}
                #print (newconcatstr)
                #print (newdict)
                innerlistofdicts.append(newdict)
        
        lineTwo = read_filehandle_2.readline()
    
    read_filehandle_2.close()
    
    #switch process type and process next file
    
    #print innerlistofdicts
    return innerlistofdicts
    #write offsets
    
    
def start_chaining(dir_path, filename_config):
    
    given_filename = None
    given_file_offset = 0
    derived_filename = None
    derived_file_offset = 0
    yes_to_loop = True
    
    config_file_pathandname = (dir_path + '/' + filename_config)
    given_filename, given_file_offset, derived_filename, derived_file_offset = config_read(config_file_pathandname)
    new_given_file_offset = given_file_offset
    new_derived_file_offset = derived_file_offset
    
    derived_file_pathandname = dir_path + '/' + derived_filename
    given_file_pathandname = dir_path + '/' + given_filename
    
    while (yes_to_loop):
        
        derived_filehandle = open(derived_file_pathandname, 'r')
        derived_filehandle.seek(derived_file_offset)
        lineOne = derived_filehandle.readline()
        new_derived_file_offset = derived_filehandle.tell()
        derived_filehandle.close()
        listofdicts = []
    
        if (lineOne == ''):   
            #print ('read given file')
            processtype = 'original'
            given_filehandle = open(given_file_pathandname, 'r')
            given_filehandle.seek(given_file_offset)
            lineOne = given_filehandle.readline()
            new_given_file_offset = given_filehandle.tell()
            filepathandname = given_file_pathandname
            fileoffset = new_given_file_offset
        
            if lineOne != '':
                titleOne, titlesinOne = read_line_titles(processtype, lineOne)
            else:
                print('EOF Given File')
                given_filehandle.close()
                yes_to_loop = False
                break
        else:
            #print (lineOne)
            processtype = 'derived'
            filepathandname = derived_file_pathandname
            fileoffset = new_derived_file_offset
            titleOne, titlesinOne = read_line_titles(processtype, lineOne)
    
        listofdicts = compare_titles_in_files(processtype, filepathandname, fileoffset, titleOne, titlesinOne, listofdicts)
        if processtype == 'derived':
            processtype = 'original'
            filepathandname = given_file_pathandname
            fileoffset = new_given_file_offset
            listofdicts = compare_titles_in_files(processtype, filepathandname, fileoffset, titleOne, titlesinOne, listofdicts)
    
        write_list_of_dicts(derived_file_pathandname, listofdicts)
        #write to config 
        config_write(config_file_pathandname, given_filename, new_given_file_offset, derived_filename, new_derived_file_offset)
    
        #loop to next line
        given_file_offset = new_given_file_offset
        derived_file_offset = new_derived_file_offset
    
    
    
    


print ('I am here')  
if __name__ == "__main__":
    ide = 'Mars'
    print("Hello World Namita! " + ide)
    directory_base = '/home/local/ANT/namitak/Official/Olymp/FilesToProcess'
    filenameConfigs = 'Config.txt'
    
    start_chaining(directory_base, filenameConfigs)
    
    print ('Done!')
    #is_a_match(titleOn