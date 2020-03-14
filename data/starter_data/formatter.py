import re, os

class Formatter():

    """
        Class Formatter takes out duplicate spaces in a line of text in a file
    """

    def __init__(self, fn):
        self.filename = fn

    def condense(self):
        """
            condenses the strings in file using regular expressions and rewrites to the file
            WARNING: MAKE SURE TO CHANGE ANY '-' FOR GAMES PLAYED OR GAMES STARTED TO NA BEFORE RUNNING SCRIPT
        """

        try:
            text = []
            with open(self.filename, 'r') as file:
                for line in file:
                    try:
                        line = line.strip()
                        if '\t-\t' in line:
                            index_of_dash = line.rindex('\t-\t')
                            line = line[0:index_of_dash] + '-' + line[index_of_dash+3:] #no space in gamesplayed-gamestarted

                        line = re.sub('\t', ' ', line)
                        line = " ".join(line.split())
                        line = self.strip(line)
                        line += '\n'
                    except Exception as e:
                        print('Error in formatter.py: condense', e)
                    text.append(line)

            with open(self.filename, 'w') as file:
                file.writelines(text)

        except Exception as e:
            print('Error opening file:', self.filename, e)

    def strip(self, line):
        """
            strips the line of extraneous data after gp-gs
            returns the striped line
            rtype: string
        """
        try:
            ending_index_of_gpgs = re.search('\d+-\d+', line).end() #ending index of gp-gs
            if ending_index_of_gpgs is not None:
                return line[:ending_index_of_gpgs]
        except:
            return line


def main():
    file_list = os.listdir('.')

    for file in file_list:
        if '.txt' in file:
            formatter = Formatter(file)
            formatter.condense()

def run_single(fn):
    """
     runs condense for a single file
    """
    formatter=Formatter(fn)
    formatter.condense()

def run_single_swap_fn_ln(fn):
    """
     runs condense for a single file and reverse the position of first name and last name
    """
    run_single(fn)
    lines = []
    with open(fn, 'r') as file:
        for line in file:
            if ',' in line: #there is a format lastname, firstname that we want to make firstname lastname
                line = re.sub(',', '', line)
                split_line = line.split(' ')
                if(split_line[1].isupper() and '.' not in split_line[1] and '-' not in split_line[1]):
                    split_line[1] = split_line[1].capitalize()
                if(split_line[2].isupper() and '.' not in split_line[2] and '-' not in split_line[2]):
                    split_line[2] = split_line[2].capitalize()
                if(split_line[1].isupper() and '-' in split_line[1]):
                    split = split_line[1].split('-')
                    for i in range(0, len(split)):
                        split[i] = split[i].capitalize()
                    split_line[1] = "-".join(split)
                if(split_line[2].isupper() and '-' in split_line[2]):
                    split = split_line[2].split('-')
                    for i in range (0, len(split)):
                        split[i] = split[i].capitalize()
                    split_line[2] = "-".join(split)

                __swap(split_line, 1, 2) #last name is at position 1, first name at position 2
                line = " ".join(split_line)
            lines.append(line)

    with open(fn, 'w') as file:
        file.writelines(lines)


def __swap(array, index1, index2):
    temp = array[index1]
    array[index1] = array[index2]
    array[index2] = temp