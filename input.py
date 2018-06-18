from context.py import create_context_area

#given a few files of example data it should generate things for itself
def gen_data(num, file_name):
    #num is number of things to generate, and file name is the name of the file that hold the info

    f = open(file_name, "r")

