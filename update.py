import argparse
import csv
from math import sqrt
from statistics import median
import datetime 

# user_interface uses argparse to get arguments from command line 
# https://docs.python.org/2/library/argparse.html*/

# Need to define default input and output file paths
def user_interface():
    resultlist = []
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("-m", "--mode", help="Null, Outlier,Format, or Delete")
    #parser.add_argument("-h", "--header", default='yes', help="Does your CSV have headers?")
    parser.add_argument("-i", "--input",default='C:/Users/gibso/Downloads/test.csv', help="Universal: Input file")
    parser.add_argument("-o", "--output",default='C:/Users/gibso/Downloads/output.csv', help="Universal: Output file")
    parser.add_argument("-s", "--separator",default=',', help="Universal: Value that separates attributes")
    parser.add_argument("-f", "--field", default=0, help="Universal: The attribute that you want to examine")
    parser.add_argument("-n", "--null", default='', help="Null Replacement: How nulls are represented in the document")
    parser.add_argument("-v", "--value", help="Value Conditions go Here")
    parser.add_argument("-t", "--tolerance",default='100', help="What percentage of string values with you tolerate? (Enter as a float between 1 & 100)")
    parser.add_argument("-r", "--range",default='range', help="Outlier: Do you want to set a range for the data? ('range' for yes, blank or 'z' for no)")
    parser.add_argument("-l", "--lower",help="What is the lower bound of your data?")
    parser.add_argument("-u", "--upper",help="What is the upper bound of your data?")
    parser.add_argument("-z", "--outlier",help="How do you want to handle outliers? (Mean, Median, Null)")
    parser.add_argument("-q", "--format",help="What is the data type?")
    parser.add_argument("-d", "--delete",help="What is your condition for deleting? (String: Contains, Does Not Contain, Equals Does Not Equal; Number: Greater Than, Less Than, Equal To)")
    args = parser.parse_args()
    resultlist.append(args.mode)
    resultlist.append(args.input)
    resultlist.append(args.output)
    resultlist.append(args.separator)
    resultlist.append(args.field)
    resultlist.append(args.null)
    resultlist.append(args.value)
    resultlist.append(args.tolerance)
    resultlist.append(args.range)
    resultlist.append(args.lower)
    resultlist.append(args.upper)
    resultlist.append(args.outlier)
    resultlist.append(args.format)
    return resultlist

def null_mode(arguments):
    # Force desired column number to be at least 0 for proper function behavior
    arguments[4] = max(arguments[4], 0)

    # Open file for reading and file for writing
    with open(arguments[1], 'r') as infile, open(arguments[2], 'w') as outfile:
        # Create input file reader
        reader = csv.DictReader(infile, delimiter=arguments[3])

        # get a reference to input file headers, and their indexes
        columns = reader.fieldnames
        attributes = list(range(len(columns)))

        # Create output file writer
        writer = csv.DictWriter(outfile, fieldnames=columns, delimiter=arguments[3])
        writer.writeheader()

        # Decrease desired column number input by 1, so that user can count columns from 1 instead of 0
        arguments[4] = int(arguments[4]) - 1

        # Process input list of nulls in the input file to replace in the output file
        null_list = arguments[5].split(",")

        # Loop through each row in the input file and write the processed version in the output file
        for row in reader:
                # Default behvaior is 'all' for no value in field: replace nulls in all columns
                if arguments[4] == -1:
                    # Make the replacements using the given value
                    for column in columns:
                        if row[column] in null_list:
                            row[column] = arguments[6]
                # Otherwise, single column was specified: ensure provided column number is valid
                elif arguments[4] in attributes:                      
                    # Make the replacements using the given value
                    if row[columns[arguments[4]]] in null_list:
                        row[columns[arguments[4]]] = arguments[6]
                else:
                    raise Exception("You have picked a column that is out of range.")
                # Write the processed row to the output file
                writer.writerow(row)

def outlier_mode_z_score(arguments):   
    
    a = []

    # Force desired column number to be at least 0 for proper function behavior
    arguments[4] = max(int(arguments[4]), 0)

    # Open file for reading and file for writing
    with open(arguments[1], 'r') as infile, open(arguments[2], 'w') as outfile:
        # Create input file reader
        reader = csv.DictReader(infile, delimiter=arguments[3])

        # get a reference to input file headers, and their indexes
        columns = reader.fieldnames
        attributes = list(range(len(columns)))

        # Create output file writer
        writer = csv.DictWriter(outfile, fieldnames=columns, delimiter=arguments[3])
        writer.writeheader()

        # Decrease desired column number input by 1, so that user can count columns from 1 instead of 0
        arguments[4] = int(arguments[4]) - 1

        for row in reader:
            try:
                row[columns[arguments[4]]] = int(row[columns[arguments[4]]])
                a.append(row[columns[arguments[4]]])
            except:
                # couldn't convert to int, try converting to float
                try:
                    row[columns[arguments[4]]] = float(row[columns[arguments[4]]])
                    a.append(row[columns[arguments[4]]])
                except:
                    pass

        infile.seek(0)

        n = len(a)
        mean_a = sum(a)/n
        
        std_sum = 0
        
        for i in range(len(a)):
            std_sum += abs(a[i] - mean_a)**2
        
        std_dev = sqrt(std_sum)/n

        m = 0
        for row in reader:
            try:
                if (float(row[columns[arguments[4]]]) - mean_a)/float(std_dev) > 1.96 or (float(row[columns[arguments[4]]]) - mean_a)/float(std_dev) < -1.96:
                    m += 1
                    if arguments[11] == 'null':
                        row[columns[arguments[4]]] = ''
                    elif str(arguments[11]) == 'mean':
                        row[columns[arguments[4]]] = mean_a
                    elif arguments[11] == 'median':
                        row[columns[arguments[4]]] = median_a
                    else:
                        raise Exception("Please select a valid mode. (null, mean, or median)")
            except:
                pass
            writer.writerow(row)

        if arguments[11] == 'null':
            print("There were " + str(m) + " modifications using a null value.")
        else:
            print("There were " + str(m) + " replacements using the " + str(arguments[11]) + ".")

def outlier_mode_range(arguments):

    a = []

     # Force desired column number to be at least 0 for proper function behavior
    arguments[4] = max(int(arguments[4]), 0)

    # Open file for reading and file for writing
    with open(arguments[1], 'r') as infile, open(arguments[2], 'w') as outfile:
        # Create input file reader
        reader = csv.DictReader(infile, delimiter=arguments[3])

        # get a reference to input file headers, and their indexes
        columns = reader.fieldnames
        attributes = list(range(len(columns)))

        # Create output file writer
        writer = csv.DictWriter(outfile, fieldnames=columns, delimiter=arguments[3])
        writer.writeheader()

        # Decrease desired column number input by 1, so that user can count columns from 1 instead of 0
        arguments[4] = int(arguments[4]) - 1

        # Verify that the provided lower bound is numeric
        try:
            arguments[9] = int(arguments[9])
        except:
            try:
                arguments[9] = float(arguments[9])
            except:
                raise Exception("You need to enter valid a valid number for the lower bound of the range.")

        # Verify that the provided upper bound is numeric
        try:
            arguments[10] = int(arguments[10])
        except:
            try:
                arguments[10] = float(arguments[10])
            except:
                raise Exception("You need to enter a valid number for the upper bound of the range.")

        # Ensure user-provided tolerance is valid
        if float(arguments[7]) < 0 or float(arguments[7]) > 100:
            raise Exception("Please enter a tolerance level between 1 and 100.")

        # Exclude string data types from outlier calculations, end program if strings above tolerance level
        n =  0
        for row in reader:
            n += 1
            try:
                row[columns[arguments[4]]] = int(row[columns[arguments[4]]])
                a.append(row[columns[arguments[4]]])
            except:
                # couldn't convert to int, try converting to float
                try:
                    row[columns[arguments[4]]] = float(row[columns[arguments[4]]])
                    a.append(row[columns[arguments[4]]])
                except:
                    pass

        # Stop the program if the attribute has no numeric data values
        if a == []:
            raise Exception("You have chosen an attribute with no numerical values. Please select an attribute with some numerial values.")

        if float(1 - len(a)/n) > float(arguments[7])/100:
            print("There were " + str(n-len(a)) + " errors in the selected column out of " + str(n) + " rows. The error percentage was " + str(round(float(1 - len(a)/n)*100,2)) + "%.")
            raise Exception("The number of errors in this attribute has exceeded your tolerance.")

        if (n-len(a)) == 1:
            print("There was " + str(n-len(a)) + " error in the selected column out of " + str(n) + " rows. The error percentage was " + str(round(float(1 - len(a)/n)*100,2)) + "%.")
        else:
            print("There were " + str(n-len(a)) + " errors in the selected column out of " + str(n) + " rows. The error percentage was " + str(round(float(1 - len(a)/n),2)*100) + "%.")

        median_a = median(a)
        mean_a = sum(a)/len(a)

        infile.seek(0)

        m = 0
        for row in reader:
            try:
                if float(row[columns[arguments[4]]]) < float(arguments[9]) or float(row[columns[arguments[4]]]) > float(arguments[10]):
                    m += 1
                    if arguments[11] == 'null':
                        row[columns[arguments[4]]] = ''
                    elif str(arguments[11]) == 'mean':
                        row[columns[arguments[4]]] = mean_a
                    elif arguments[11] == 'median':
                        row[columns[arguments[4]]] = median_a
                    else:
                        raise Exception("Please select a valid mode. (null, mean, or median)")
            except:
                pass
            writer.writerow(row)

        if arguments[11] == 'null':
            print("There were " + str(m) + " modifications using a null value.")
        else:
            print("There were " + str(m) + " replacements using the " + str(arguments[11]) + ".")

def format_mode(arguments):
    # Force desired column number to be at least 0 for proper function behavior
    arguments[4] = max(int(arguments[4]), 0)

    # Open file for reading and file for writing
    with open(arguments[1], 'r') as infile, open(arguments[2], 'w') as outfile:
        # Create input file reader
        reader = csv.DictReader(infile, delimiter=arguments[3])

        # get a reference to input file headers, and their indexes
        columns = reader.fieldnames
        attributes = list(range(len(columns)))

        # Create output file writer
        writer = csv.DictWriter(outfile, fieldnames=columns, delimiter=arguments[3])
        #writer.writeheader()

        # Decrease desired column number input by 1, so that user can count columns from 1 instead of 0
        arguments[4] = int(arguments[4]) - 1

        if arguments[12] == 'number':
            n = 0
            exceptions = []
            for row in reader:
                n += 1
                try:
                    row[columns[arguments[4]]] = float(row[columns[arguments[4]]])
                except:
                    exceptions.append(n)
        elif arguments[12] == 'string':
            n = 0
            exceptions = []
            for row in reader:
                n += 1
                try:
                    row[columns[arguments[4]]] = int(row[columns[arguments[4]]])
                    exceptions.append(n)
                except:
                    pass
        else:
            raise Exception("You must input a valid data type (number or string).")
        
        if len(exceptions) == 1:
            outfile.write("There was 1 row that did not match the specified data type.")
            outfile.write('\n')
            outfile.write("There was an error on line " + str(exceptions[0]) + ".")
        else:
            outfile.write("There were " + str(len(exceptions)) + " rows that did not match the specified data type.")
            outfile.write('\n')
            for i in range(len(exceptions)):
                outfile.write("There was an error on line " + str(exceptions[i]) + ".")
                outfile.write('\n')
        
        # Add Date Formatting

def delete_mode(arguments):
    # Force desired column number to be at least 0 for proper function behavior
    arguments[4] = max(int(arguments[4]), 0)

    # Open file for reading and file for writing
    with open(arguments[1], 'r') as infile, open(arguments[2], 'w') as outfile:
        # Create input file reader
        reader = csv.DictReader(infile, delimiter=arguments[3])

        # get a reference to input file headers, and their indexes
        columns = reader.fieldnames
        attributes = list(range(len(columns)))

        # Create output file writer
        writer = csv.DictWriter(outfile, fieldnames=columns, delimiter=arguments[3])
        #writer.writeheader()

        # Decrease desired column number input by 1, so that user can count columns from 1 instead of 0
        arguments[4] = int(arguments[4]) - 1

        # Create deletions list for deleted line #'s
        deletions = []

        if arguments[12] == 'string':
            n = 0 
            for row in reader:
                n += 1
                try:
                    if arguments[13] == "Contains":
                        if str(arguments[6]) in str(row[columns[arguments[4]]]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    elif arguments[13] == "Does Not Contain":
                        if str(arguments[6]) not in str(row[columns[arguments[4]]]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    elif arguments[13] == "Equals":
                        if str(arguments[6]) == str(row[columns[arguments[4]]]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    elif arguments[13] == "Does Not Equal":
                        if str(arguments[6]) != str(row[columns[arguments[4]]]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    else:
                        raise Exception("You must enter a valid mode for deletion (Contains, Does not Contain, Equals, Does not Equal, Greater Than, Less Than, Equal To)")
                except:
                    writer.write(row)
        elif arguments[12] == 'number':
            try:
                float(arguments[6])
            except:
                raise Exception("Your value must be a number.")
            n = 0
            for row in reader:
                n += 1
                try:
                    if arguments[13] == ">":
                        if float(row[columns[arguments[4]]]) > float(arguments[6]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    elif arguments[13] == "<":
                        if float(row[columns[arguments[4]]]) < float(arguments[6]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    elif arguments[13] == "=":
                        if float(row[columns[arguments[4]]]) == float(arguments[6]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    elif arguments[13] == ">=":
                        if float(row[columns[arguments[4]]]) >= float(arguments[6]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    elif arguments[13] == "<=":
                        if float(row[columns[arguments[4]]]) <= float(arguments[6]):
                            deletions.append(n)
                            pass
                        else:
                            intentionally_except
                    elif arguments[13] == "!=":
                        if float(row[columns[arguments[4]]]) != float(arguments[6]):
                            pass
                        else:
                            intentionally_except
                    else:
                        raise Exception("You must enter a valid mode for deletion (Contains, Does not Contain, Equals, Does not Equal, >, <, =, >=, <=, !=)")
                except:
                    writer.writerow(row)
        else:
            raise Exception("You must input a valid data type (number or string).")


def select_mode(arguments):
    if arguments[0] == 'null':
        null_mode(arguments)
    elif arguments[0] == 'outlier':
        if arguments[8] == 'range':
            outlier_mode_range(arguments)
        elif arguments[8] == 'z-score':
            outlier_mode_z_score(arguments)
        else:
            raise Exception("Please enter a valid mode for outlier type.")
    elif arguments[0] == 'format':
        format_mode(arguments)
    elif arguments[0] == 'delete':
        delete_mode(arguments)
    else:
        raise Exception("Please enter a valid mode.")


# main program starts here
def main():
    arguments = user_interface()
    select_mode(arguments)


if __name__ == "__main__":
    main()
