import ast
import os
import shutil

def config_read(config_name):
    config_handle = open(config_name, 'r')
    config_line1 = config_handle.readline()
    #print config_line
    config_dict = ast.literal_eval(config_line1)
    print config_dict
    given_filename = config_dict['GivenFile']
    given_file_offset = config_dict['GivenFileOffset']
    derived_filename = config_dict['DerivedFile']
    derived_file_offset = config_dict['DerivedFileOffset']
    counter = config_dict['Counter']
    configline2 = config_handle.readline()
    if configline2 == '':
        offset_dict = {}
    else:
        offset_dict = ast.literal_eval(configline2)
    config_handle.close()
    #dir_path = config_dict['DirectoryPath']
    return given_filename, given_file_offset, derived_filename, derived_file_offset, counter, offset_dict
    
def config_write_line(config_name, given_file, given_file_offset, derived_file, derived_file_offset, counter, offset_dict):
    config_handle = open(config_name, 'w')
    config_line = "{'Counter': " + str(counter) + ", 'GivenFile': '" + given_file + "', 'GivenFileOffset': " + str(given_file_offset) +", 'DerivedFile' : '" + derived_file + "', 'DerivedFileOffset' :" + str(derived_file_offset) +"}\n"
    #print (config_line)
    config_handle.write(config_line)
    config_line = str(offset_dict)
    config_handle.write(config_line + '\n')    
    config_handle.close()

  
def uniqify_dict_list(inputlist):
    outputlist = []
    for item in inputlist:
        if item in outputlist:
            continue
        else:
            outputlist.append(item)
    return outputlist  
            
    
def write_list_of_dicts (fullpathandname, dict_list):
    #make dictionary list unique, its already unique when writing
    #new_dict_list = dict_list
    #dict_list = uniqify_dict_list(new_dict_list)
    #print ('with duplicates: ' + str (new_dict_list))
    #print ('without duplicates: ' + str(dict_list))
    
   
    try:
        file_handle = open(fullpathandname, 'r')
                  
        for read_line in file_handle.readlines():
            #print ('loop through file')
            dict_of_title = ast.literal_eval(read_line)
            print dict_of_title
            if (dict_of_title in dict_list):
                print ('duplicate found')
                dict_list.remove(dict_of_title)
    except:
        file_handle = open (fullpathandname, 'w+')
        file_handle.close()
    finally:    
        print ('after dedup with file')
        print  dict_list
        file_handle = open (fullpathandname, 'a')
        for dictitem in dict_list:
            #concat_title = ' '.join(dictitem["concatstr"])
            concat_title = dictitem["concatstr"]
            line_to_write = str(dictitem) + '\n'
            #line_to_write = "{'origstr': \"" + dictitem["origstr"] + "\", 'concatstr': \"" + concat_title + "\", 'titles': " + str(dictitem["titles"]) +"}\n"
            print (line_to_write)
            file_handle.write(line_to_write)
    
    str_offset = file_handle.tell()
    file_handle.close()
    return str_offset
    
'''
    file_handle = open(fullpathandname, 'r')
                
    for read_line in file_handle.readlines():
        for dictitem in dict_list:
            concat_title = ' '.join(dictitem["concatstr"])
            line_to_write = "{'concatstr': \"" + concat_title + "\", 'titles': " + str(dictitem["titles"]) +"}\n"
            if cmp (line_to_write, read_line) == 0:
                print dictitem
                print read_line
                dict_list.remove(dictitem)
            break
         
    print dict_list
    file_handle = open (fullpathandname, 'a')
    for dictitem in dict_list:
        concat_title = ' '.join(dictitem["concatstr"])
        line_to_write = "{'concatstr': \"" + concat_title + "\", 'titles': " + str(dictitem["titles"]) +"}\n"
        #print (line_to_write)
        file_handle.write(line_to_write)
    file_handle.close()
'''  


def read_line_titles(linetype, line_read):
    if linetype == 'original':
        title = line_read
        title_list = [line_read]
        #orig_str = line_read.rstrip('\n')
        print 
    else:
        dict_of_title = ast.literal_eval(line_read)
        title = dict_of_title['concatstr']
        title_list = dict_of_title['titles']
        #orig_str = dict_of_title['origstr']
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

    
'''
def compare_titles_in_files(dir_to_read, filename1, filename2):
    filepathandname = dir_to_read + '\\' + filename1
    read_filehandle_1 = open(filepathandname, 'r')
    titleOne = read_filehandle_1.readline()
    fileoffset = read_filehandle_1.tell()
    read_filehandle_1.close()
    
    read_filehandle_2 = open(filepathandname, 'r')
    read_filehandle_2.seek(fileoffset)
    lineTwo = read_filehandle_2.readline()
    
    listofdicts = []
    
    while lineTwo:
        split_line = lineTwo.split('|')
        if len(split_line) > 1:
            titleTwo = split_line[0]
            titlesinTwo = split_line[1]
        else:
            titleTwo = lineTwo
            titlesinTwo = titleTwo
        print (titleOne + ' ' + titleTwo)
        is_match, newconcatstr = is_a_match (titleOne, titleTwo)
        if (is_match == True):
            newdict = {'origstr': titleOne, 'concatstr': newconcatstr, 'titles': [titleOne, titlesinTwo]}
            print (newconcatstr)
            print (newdict)
            listofdicts.append(newdict)
         
        is_match, newconcatstr = is_a_match (titleTwo, titleOne)
        if (is_match == True):
            newdict = {'origstr': titleTwo, 'concatstr': newconcatstr, 'titles': [titlesinTwo, titleOne]}
            print (newconcatstr)
            print (newdict)
            listofdicts.append(newdict)
        
        lineTwo = read_filehandle_2.readline()
    
    print listofdicts
    #write offsets
    read_filehandle_2.close()
'''

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
    num_titlesinOne = len(titlesinOne)
    
    while lineTwo:
        titleTwo, titlesinTwo = read_line_titles(processtype, lineTwo)
        #print (titleOne + ' ' + titleTwo)
        #compare titles in One and Two - that there are no duplicates. If duplicates are there then ignore this match
        #print ('Titles in two ' + str(titlesinTwo))
        #print ('Titles in one ' + str(titlesinOne))
        #print (set(titlesinTwo).intersection(titlesinOne))
        num_titlesinCommon = len(set(titlesinTwo).intersection(titlesinOne))
        
        if ((num_titlesinCommon == 1)):
            print ('One in common')
            num_titlesinTwo = len(titlesinTwo)
            if ((num_titlesinTwo > 1) and (num_titlesinOne > 1)):
                print ('not single title list')
                if (titlesinOne[num_titlesinOne-1] == titlesinTwo[0]):
                    print ('they match at the ends')
                    is_match, newconcatstr = is_a_match (titleOne, titleTwo)
                    if (is_match == True):
                        titles = titlesinOne + titlesinTwo[1:]
                        #newdict = {'origstr': titleOne, 'concatstr': newconcatstr, 'titles': titles}
                        newconcatstr = ' '.join(newconcatstr)
                        newdict = {'concatstr': newconcatstr, 'titles': titles}
                        if newdict not in innerlistofdicts:
                            innerlistofdicts.append(newdict)
    
                if (titlesinTwo[num_titlesinTwo-1] == titlesinOne[0]):
                    print ('they match at the ends')
                    is_match, newconcatstr = is_a_match (titleTwo, titleOne)
                    if (is_match == True):
                        titles = titlesinTwo + titlesinOne[1:]
                        #newdict = {'origstr': titleTwo, 'concatstr': newconcatstr, 'titles': titles}
                        newconcatstr = ' '.join(newconcatstr)
                        newdict = {'concatstr': newconcatstr, 'titles': titles}
                        if newdict not in innerlistofdicts:
                            innerlistofdicts.append(newdict)
        if ((num_titlesinCommon == 0)):
            is_match, newconcatstr = is_a_match (titleOne, titleTwo)
            if (is_match == True):
                newconcatstr = ' '.join(newconcatstr)
                newdict = {'concatstr': newconcatstr, 'titles': titlesinOne+titlesinTwo}
                if newdict not in innerlistofdicts:
                    #print (newconcatstr)
                    #print (newdict)
                    innerlistofdicts.append(newdict)
         
            is_match, newconcatstr = is_a_match (titleTwo, titleOne)
            if (is_match == True):
                newconcatstr = ' '.join(newconcatstr)
                newdict = {'concatstr': newconcatstr, 'titles': titlesinTwo+titlesinOne}
                if newdict not in innerlistofdicts:
                    #print (newconcatstr)
                    #print (newdict)
                    innerlistofdicts.append(newdict)
        
        lineTwo = read_filehandle_2.readline()
    
    read_filehandle_2.close()
    
    #switch process type and process next file
    
    #print innerlistofdicts
    return innerlistofdicts
    #write offsets
    
'''    
def start_chaining(dir_path, filename_config):
    
    given_filename = None
    given_file_offset = 0
    derived_filename = None
    derived_file_offset = 0
    yes_to_loop = True
    
    config_file_pathandname = (dir_path + '\\' + filename_config)
    given_filename, given_file_offset, derived_filename, derived_file_offset = config_read(config_file_pathandname)
    new_given_file_offset = given_file_offset
    new_derived_file_offset = derived_file_offset
    
    derived_file_pathandname = dir_path + '\\' + derived_filename
    given_file_pathandname = dir_path + '\\' + given_filename
    
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
                titleOne, titlesinOne, origstrOne = read_line_titles(processtype, lineOne)
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
            titleOne, titlesinOne, origstrOne = read_line_titles(processtype, lineOne)
    
        listofdicts = compare_titles_in_files(processtype, filepathandname, fileoffset, titleOne, titlesinOne, listofdicts, origstrOne)
        if processtype == 'derived':
            processtype = 'original'
            filepathandname = given_file_pathandname
            fileoffset = new_given_file_offset
            listofdicts = compare_titles_in_files(processtype, filepathandname, fileoffset, titleOne, titlesinOne, listofdicts, origstrOne)
    
        write_list_of_dicts(derived_file_pathandname, listofdicts)
        #write to config 
        config_write(config_file_pathandname, given_filename, new_given_file_offset, derived_filename, new_derived_file_offset)
    
        #loop to next line
        given_file_offset = new_given_file_offset
        derived_file_offset = new_derived_file_offset
    
'''    
def process_titles_in_file(dir_path, filename_config):
    given_filename = None
    given_file_offset = 0
    derived_filename = None
    derived_file_offset = 0
    yes_to_loop = True
    
    config_file_pathandname = (dir_path + '\\' + filename_config)
     
    while yes_to_loop:
        given_filename, given_file_offset, derived_filename, derived_file_offset, round_counter, offsetdict = config_read(config_file_pathandname)
        
        if (round_counter == 0):
            processtype = 'original'   
        else:
            processtype = 'derived'
        
        new_derived_filename = str(round_counter) + derived_filename   
        derived_file_pathandname = dir_path + '\\' + new_derived_filename
        given_file_pathandname = dir_path + '\\' + given_filename
        new_given_file_offset = given_file_offset
        #new_derived_file_offset = derived_file_offset
    
        given_filehandle = open(given_file_pathandname, 'r')
        given_filehandle.seek(given_file_offset)
        lineOne = given_filehandle.readline()
        listofdicts = []
        titlestr_offset_dict = {}
        filepathandname = given_file_pathandname
   
        while lineOne:
            new_given_file_offset = given_filehandle.tell()
            fileoffset = new_given_file_offset
            titleOne, titlesinOne = read_line_titles(processtype, lineOne)
            '''
            if (processtype == 'original'):
                fileoffset = new_given_file_offset
            else:
                fileoffset = new_given_file_offset
            ''' 
            listofdicts = compare_titles_in_files(processtype, filepathandname, fileoffset, titleOne, titlesinOne, listofdicts)
            write_list_of_dicts(derived_file_pathandname, listofdicts)
            #titlestr_offset_dict[origstrOne] = origstrOffset
            #new_derived_file_offset = origstrOffset
            #config_write_line(config_file_pathandname, given_filename, new_given_file_offset, derived_filename, new_derived_file_offset, round_counter, titlestr_offset_dict)
        
            lineOne = given_filehandle.readline()
        
        given_filehandle.close()
        fstat = os.stat(derived_file_pathandname)
        filesize = fstat.st_size
        if filesize == 0:
            yes_to_loop = False
        else:
            #os.remove(given_file_pathandname)
            round_counter = round_counter + 1
            config_write_line(config_file_pathandname, new_derived_filename, 0, derived_filename, 0, round_counter, titlestr_offset_dict)
    


print ('I am here')  
if __name__ == "__main__":
    ide = 'Mars'
    print("Hello World Namita! " + ide)
    directory_base = 'C:\Namita\Official\Projects\APP\C8\Olymp\Ch\FilesToProcess'
    filenameConfigs = 'ConfigF1.txt'
    
    process_titles_in_file(directory_base, filenameConfigs)
    
    print ('Done!')
    #is_a_match(titleOne, titleTwo)