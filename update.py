begin_time = datetime.now()

import argparse
import csv
from math import sqrt
from statistics import median
import datetime 

# user_interface uses argparse to get arguments from command line 
# https://docs.python.org/2/library/argparse.html*/

# We set up the various arguments that we will receive. We can assign them default values, a default data type, or set them to required.
# For questions about the different arguments, see the attached description or consult the readme. 
def user_interface():
    resultlist = []
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("-m", "--mode", help="Null, Outlier,Format, or Delete")
    #parser.add_argument("-h", "--header", default='yes', help="Does your CSV have headers?")
    parser.add_argument("-i", "--input",default='C:/Users/gibso/Downloads/test.csv', help="Universal: Input file")
    parser.add_argument("-o", "--output",default='C:/Users/gibso/Downloads/output.csv', help="Universal: Output file")
    parser.add_argument("-s", "--separator",default=',', help="Universal: Value that separates attributes")
    parser.add_argument("-a", "--attribute", default=0, help="Universal: The attribute that you want to examine")
    parser.add_argument("-n", "--null", default='', help="Null Replacement: How nulls are represented in the document")
    parser.add_argument("-v", "--value", help="Value Conditions go Here")
    parser.add_argument("-t", "--tolerance",default='100', help="What percentage of string values with you tolerate? (Enter as a float between 1 & 100)")
    parser.add_argument("-r", "--range",default='range', help="Outlier: Do you want to set a range for the data? ('range' for yes, blank or 'z' for no)")
    parser.add_argument("-l", "--lower",help="What is the lower bound of your data?")
    parser.add_argument("-u", "--upper",help="What is the upper bound of your data?")
    parser.add_argument("-z", "--outlier",help="How do you want to handle outliers? (Mean, Median, Null)")
    parser.add_argument("-f", "--format",help="What is the data type?")
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

# Define Null Mode
def null_mode(arguments):
    # Force desired column number to be at least 0 for proper function behavior
    # This is related to allowing users to select column numbers from 1 to n, rather than selecting from 0 to n - 1, which is more intuitive for most users. 
    arguments[4] = max(arguments[4], 0)

    # Open file for reading and file for writing
    with open(arguments[1], 'r') as infile, open(arguments[2], 'w') as outfile:
        # Create input file reader
        reader = csv.DictReader(infile, delimiter=arguments[3])

        # Get a reference to input file headers, and their indexes
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
    
    # Define 'a', the list where we will keep all numeric values 
    a = []

    # Force desired column number to be at least 0 for proper function behavior
    arguments[4] = max(int(arguments[4]), 0)

    # Open file for reading and file for writing
    with open(arguments[1], 'r') as infile, open(arguments[2], 'w') as outfile:
        # Create input file reader
        reader = csv.DictReader(infile, delimiter=arguments[3])

        # Get a reference to input file headers, and their indexes
        columns = reader.fieldnames
        attributes = list(range(len(columns)))

        # Create output file writer
        writer = csv.DictWriter(outfile, fieldnames=columns, delimiter=arguments[3])
        writer.writeheader()

        # Decrease desired column number input by 1, so that user can count columns from 1 instead of 0
        arguments[4] = int(arguments[4]) - 1

        # We will check which rows have numeric values and which have string values. We will collect the numeric values in a list
        for row in reader:
            try:
                # Try converting to integer type first
                row[columns[arguments[4]]] = int(row[columns[arguments[4]]])
                a.append(row[columns[arguments[4]]])
            except:
                # Couldn't convert to int, try converting to float
                try:
                    row[columns[arguments[4]]] = float(row[columns[arguments[4]]])
                    a.append(row[columns[arguments[4]]])
                except:
                    # If a row is a string, it is left out the list
                    pass

        # Reset cursor to original position after loop
        infile.seek(0)

        # Define number of elements of a in order to calculate the mean of a without using pre-built functions
        n = len(a)
        mean_a = sum(a)/n
        
        std_sum = 0
        
        # Iterate through a to calculate and add the squared variance of each value in order to find the standard deviation
        for i in range(len(a)):
            std_sum += abs(a[i] - mean_a)**2
        
        # Use the sumer of squared variances to get the standard deviation
        std_dev = sqrt(std_sum)/n

        # Check to see if the z-score of each value falls within the acceptable 95% CI range
        m = 0
        for row in reader:
            try:
                # If the calculation can be performed, and the value falls outside the z-score interval, it will be replaced with either the mean of a, the median of a, or a null
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

        # Tell the users which replacement mode was used and how many outlier replacements occurred 
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

        # Ensure user-provided tolerance is a valid number between 0 and 100
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
                try:
                    row[columns[arguments[4]]] = float(row[columns[arguments[4]]])
                    a.append(row[columns[arguments[4]]])
                except:
                    pass

        # Stop the program if the attribute has no numeric data values
        if a == []:
            raise Exception("You have chosen an attribute with no numerical values. Please select an attribute with some numerial values.")

        # End the program if the uppper bound of the tolerance level was exceded and explain to the user why the program was terminated with specific information 
        if float(1 - len(a)/n) > float(arguments[7])/100:
            print("There were " + str(n-len(a)) + " errors in the selected column out of " + str(n) + " rows. The error percentage was " + str(round(float(1 - len(a)/n)*100,2)) + "%.")
            raise Exception("The number of errors in this attribute has exceeded your tolerance.")

        # Return the number of non-numeric values in the specified column that could not be considered
        if (n-len(a)) == 1:
            print("There was " + str(n-len(a)) + " error in the selected column out of " + str(n) + " rows. The error percentage was " + str(round(float(1 - len(a)/n)*100,2)) + "%.")
        else:
            print("There were " + str(n-len(a)) + " errors in the selected column out of " + str(n) + " rows. The error percentage was " + str(round(float(1 - len(a)/n),2)*100) + "%.")

        median_a = median(a)
        mean_a = sum(a)/len(a)

        # Set the cursor back to 0 for another pass
        infile.seek(0)

        m = 0
        for row in reader:
            try:
                # Check to see if the value is greater than the upper bound or less than the lower bound
                if float(row[columns[arguments[4]]]) < float(arguments[9]) or float(row[columns[arguments[4]]]) > float(arguments[10]):
                    # If so, increase the count by 1 and then perform the relevant replacement
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

        # Give users a summary of how many outliers were replaced and which replacement mode was used
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

        # Create logic line for if 'number' is chosen as data type
        if arguments[12] == 'number':
            n = 0
            # Record the row number of the excepted values in a list
            exceptions = []
            for row in reader:
                n += 1
                try:
                    # Check to see if the value can be treated as numeric, otherwise except and add row number
                    row[columns[arguments[4]]] = float(row[columns[arguments[4]]])
                except:
                    exceptions.append(n)
        
        elif arguments[12] == 'string':
            n = 0
            exceptions = []
            for row in reader:
                n += 1
                try:
                    # We perform the same operation as above but reversed in how we except and record. 
                    # I did it this way because it's not possible to float(string) but it is possible to str(number)
                    row[columns[arguments[4]]] = float(row[columns[arguments[4]]])
                    exceptions.append(n)
                except:
                    pass
        
        else:
            raise Exception("You must input a valid data type (number or string).")
        
        # Put the total number of exceptions and their line numbers in the output file
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

        # Create logic line for if the column is specified to be full of strings
        if arguments[12] == 'string':
            n = 0 
            for row in reader:
                n += 1
                # Create different logical operators for string/text values
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
                            # Here we cause an intentional exception in order to force the reader to write the row
                            # If there is no exception, the row is not written into the output file. Thus, it is effectively 'deleted'. 
                            intentionally_except
                    else:
                        raise Exception("You must enter a valid mode for deletion (Contains, Does not Contain, Equals, Does not Equal, Greater Than, Less Than, Equal To)")
                except:
                    writer.write(row)
        
        # Create logic line for if the column is specified to be full of numbers
        elif arguments[12] == 'number':
            try:
                float(arguments[6])
            except:
                raise Exception("Your value must be a number.")
            n = 0
            for row in reader:
                n += 1
                # Implement various numerical operators
                try:
                    if arguments[13] == ">":
                        if float(row[columns[arguments[4]]]) > float(arguments[6]):
                            deletions.append(n)
                            # If the given value meets the condition, it moves to the pass line and is effectively passed over from being written
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
                            # Here we cause an intentional exception in order to force the reader to write the row
                            # If there is no exception, the row is not written into the output file. Thus, it is effectively deleted. 
                            intentionally_except
                    else:
                        raise Exception("You must enter a valid mode for deletion (Contains, Does not Contain, Equals, Does not Equal, >, <, =, >=, <=, !=)")
                except:
                    writer.writerow(row)
        else:
            raise Exception("You must input a valid data type (number or string).")

# Part of the program that reads the user-specified mode and directs to the appropriate function and sub-function
# Raises an exception if the mode is not recognized
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


# Main program starts here
# We initialize the arguments and then pass along to the mode-handling function
def main():
    arguments = user_interface()
    select_mode(arguments)


if __name__ == "__main__":
    main()

time = datetime.now() - begin_time
print("The runtime was: " + str(time))
