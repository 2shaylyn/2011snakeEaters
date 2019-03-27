###
##              Steganography Project
#                  Data Structure
#                   Spring 2019


## The program starts on the second line of the file

# You need to download the Pixels1.txt file on Wyocourses

import sys

        ## just to allows me to change the color of the output text
try:
    shell_connect = sys.stdout.shell
except AttributeError:
    print("idlecolors highlighting only works with IDLE")
    exit()

        ## decode function
    
def decode():
        ## try to open the file which name is given by the user
    while True:
        try:
            filename = input("Please, write the name of the file to decode with the extension:\n")
            file = open(filename,'r')
            break
        except:
            shell_connect.write('File does not exist, try again.\n','COMMENT')
    count = 0
    lenght = ''
    message = ''
    message2 = ''
    l=0
    d=''
    message3=''
    expt = False
    # for each line in the file, do the following:
    for line in file:
        # if it is the first two lines, take the least representative in each 'r', 'g' and 'b'
            # and take the bits in that locations
        while count<2:
            pixel = file.readline()
            lenght = lenght+pixel[3]+pixel[5]+pixel[7]
            count += 1
        # convert the number (which is in bytes) in binary to decimal and multiply it by 8 so we can know the lenght
            # of the message in bits
        l = 8*int(lenght,2)
        count = 0
        # the first channel to be looked is the 'r', so the variable channel receives 'r'
        channel = 'r'
        # this loop will run until the end of the message, so until the counter (count) is the lenght of the message in bits
        while count< l:
            pixel = file.readline()
            try:
                # in each pixel, the variable message will "append" the value in that position
                # if the channel is the red one, the bit to be decripted is the third one
                if channel == 'r':
                    message = message+pixel[3]+','
                    count += 1
                    channel = 'g'
                # if the channel is the green one, the bit to be decripted is the 5o one
                elif channel == 'g':
                    message = message+pixel[5]+','
                    count += 1
                    channel = 'b'
                # if the channel is the blue one, the bit to be decripted is the last one one
                elif channel == 'b':
                    message = message+pixel[7]+','
                    count += 1
                    channel = 'r'
                else:
                    print("Error in RGB\n")
                    break
            # if the file is not big enough to encript the message, the message will be encripted it reaches the end
            except IndexError:
                shell_connect.write("\nSorry, the file was not big enough to hide the entire message.\n\n",'COMMENT')
                expt = True
                break
        m = message.split(',')
        m.pop(-1)
        count = 0
        # this part divides the entire hex values in parts of 8 and for each set of 8 values, it takes its contribution
        # which is 0 or 1
        # so, if the hex number is even, the decode understands as a '0'
        # if the hex number is a odd number, the decode understands as a '1'
        for i in m:
            if count%8 == 0:
                message2 = message2+','
            else:
                pass
            n = int(i,16)
            if n%2 == 0:
                message2 = message2+'0'
            else:
                message2 = message2+'1'
            count +=1
        d = message2.split(',')
        d.pop(0)
        # if the file was not big enough to encript the entire message, the last element does not have 8 digits,
        # so it is not going to be possible to convert it as a letter, so, we take it off
        if expt:
            d.pop()
        for i in d:
            #convert each 8 digits into a letter
            message3 = message3+chr(int(i,2))
        if not expt:
            shell_connect.write("Decode successful!\n",'STRING')
            print ("The hidden message is: \n{}".format(message3))
        else:
            print ("The part of the hidden message that could be hidden is: \n{}".format(message3))
        break
    file.close()
                      
# hide function

def hide():
    ## try to open the file which name is given by the user
    while True:
        try:
            filename = input("Please, write the name of the file to hide with the extension:\n")
            fileR = open(filename,'r')
            break
        except:
            shell_connect.write('File does not exist, try again.\n','COMMENT')
    ## User write a message to be encripted
    message_str = input("Write a message to be encrypted: ")
    ## The message which is a String item, has to be written in its binary representation
    message_bin = [bin(ord(k))[2:].zfill(8) for k in message_str]
    ## The next step is to create a new file that will going to have the encripted message
    fileW = open(filename[:-4]+'_hidden.txt','w')
    count = 0
    channel ='r'
    count1 = 0
    count2 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count0 = 0
    new_line = ''
    expt = False
    ## The first two pixels is going to have in its least bits the lenght of the message
    # So, first, let's figure what is the lenght of the message in binary
    len_bin = bin(len(message_str))
    # We need that this binary lenght number has 6 bits, in order to use all 6 least significant bits of the 2 first pixels
    len_bin = len_bin[2:].zfill(6)
    for line in fileR:
        if count != 0:
            # So, the first two bits will have the lenght of the message
            while count0<2:
                pixel = fileR.readline()
                new_line = ''
                pin = [3,5,7]
                count4 = 0
                for i in pixel:
                    if count4 in pin:
                        new_line = new_line + len_bin[count5]
                        count5 += 1
                    else:
                        new_line = new_line + i
                    count4 += 1
                fileW.write(new_line)
                count0 += 1
            else:
                # The rest of the pixels will have the message encripted
                # this try is only because the file could not be big enough to ecript the entire message, so
                # if the file is not big enough to hide the entire message, the message will be hidden until the file permits
                try:
                    if count <= 8*len(message_str):
                        # if the channel is 'r', the bit to be decripted is the third one
                        if channel == 'r':
                            count3=0
                            pixeln = int(line[3],16)
                            message_comp = int(message_bin[count1][count2])
                            new_line = ''
                            # we will modify the bit that already exists there, only if we need
                            # pixel2n is the decimal number of the third position of the currently hex number in the file
                            # message_comp is the decimal number of the position that we want to encript of the message
                            ## the logic is message_comp has to be 0 or 1, 
                            # if the bit of the message is a '0' and the hex bit of the file is a '8', the decode will understand as a '0' in order to decode it
                            # so, if the hex number is even, the decode understands as a '0'
                            # if the hex number is a odd number, the decode understands as a '1'
                            # so, we will change in the file only if the message has an even number on the position i and the file has an odd number in that position
                            if pixeln%2 != message_comp:
                                for i in line:
                                    if count3 == 3:
                                        ## so, like I said, if one number is odd and the other is even,
                                        # we will change the number in the file by adding one, and the rest bits of the pixel, remains the same
                                        new_hex = hex(pixeln+1)
                                        new_hex = new_hex[2:]
                                        new_line = new_line + new_hex
                                    else:
                                        new_line = new_line+i
                                    count3 += 1
                                fileW.write(new_line)
                            else:
                                fileW.write(line)
                                # at the end, the next channel is the 'g', so, channel receives 'g'
                            channel = 'g'
                        # the logic is exactly the same for the other channels
                        elif channel == 'g':
                            count3=0
                            pixeln = int(line[5],16)
                            message_comp = int(message_bin[count1][count2])
                            new_line = ''
                            if pixeln%2 != message_comp:
                                for i in line:
                                    if count3 == 5:
                                        new_hex = hex(pixeln+1)
                                        new_hex = new_hex[2:]
                                        new_line = new_line + new_hex
                                    else:
                                        new_line = new_line+i
                                    count3 += 1
                                fileW.write(new_line)
                            else:
                                fileW.write(line)
                            channel = 'b'
                        elif channel == 'b':
                            count3=0
                            pixeln = int(line[7],16)
                            message_comp = int(message_bin[count1][count2])
                            new_line = ''
                            if pixeln%2 != message_comp:
                                for i in line:
                                    if count3 == 7:
                                        new_hex = hex(pixeln+1)
                                        new_hex = new_hex[2:]
                                        new_line = new_line + new_hex
                                    else:
                                        new_line = new_line+i
                                    count3 += 1
                                fileW.write(new_line)
                            else:
                                fileW.write(line)
                            channel = 'r'
                        count += 1
                        count2 += 1
                        count6 += 1
                        if count6%8 == 0:
                            count1 += 1
                            count2 = 0
                    else:
                        # if the message is smaller than the file, after ecripting the message, the rest pixels will remain the same
                        fileW.write(line)
                        count+=1
                except IndexError:
                    shell_connect.write("\nWarning: the file was not big enough to hide the entire message.\n\n",'COMMENT')
                    expt = True
        else:
            fileW.write(line)
            count+=1
    fileW.close()
    fileR.close()
    if not expt:
        shell_connect.write("Hide successful!\n",'STRING')
    else:
        shell_connect.write("Because of the size of the {} file, it was possible to hide only {} characters.".format(filename,(count-2)//8),'COMMENT')

print('\t-------------------------------------------------------------')
print("\t    Hello, Welcome to the Steganography Project")
print('\t-------------------------------------------------------------')
while True:
    choice = input("\nPlease choose 'h' to hide or 'd' to decode or 'e' to exit:\n")
    # you can write 'h', 'H', 'Hide', 'd' , 'Decode'...
    choice = choice[0]
    choice = choice.lower()
    choice_dic = {'h':'hide','d':'decode','e':'exit'}
    if choice in choice_dic:
        print("You chose to {}.\n".format(choice_dic[choice]))
        if choice == 'h':
            hide()
        elif choice == 'd':
            decode()
        elif choice == 'e':
            print("\nThank you.\nGood Bye.\n")
            break
    else:
        shell_connect.write("Sorry, please try again.\nRemember to choose 'h','d' or 'e'.\n",'KEYWORD')
