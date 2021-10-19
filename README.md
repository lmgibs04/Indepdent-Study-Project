Documentation


Update -m mode -i input -o output -s separator -a attribute -n null -v value -t tolerance -r range -l lower -u upper -z outlier -f format -d delete 


All 

Mode (-m) – The user specifies the mode of update that they would like to use. The available options are Null, Outlier, Format, and Delete. If no option is provided, the program defaults to Null. 

Input (-i) – The input file path for the CSV that you would like to examine. Required argument. No default. 

Output (-o) – The output file path for the updated file that you will have created after running the program. Required argument. User can set a default path by modifying the program. 

Separator (-s) – The separator that is in the file. Although CSVs are comma-separated, the program is able to read files that are separated by other characters such as ‘|’ or ‘/’ if the user specifies it. This argument is not required. The program uses ‘,’ by default if not otherwise specified. 

Attribute (-a) – The specific attribute or column that you would like to examine or modify. This is a required field for the Outlier, Format, and Delete modes. In the Null mode, if a user leaves this argument blank, it will examine all columns for the specified nulls and replaced them with the specified value. 


Null

Update -m mode -i input -o output -s separator -a attribute -n null -v value 

Null (-n) – This is the values that constitutes a null. The user can input a comma-separated list of values to be recognized as nulls, such as [NaN,, Null, null, empty, N/A, NA]. If no value is specified, the program defaults to assuming that the value is empty or ‘’, which takes the form ‘,,’ in a CSV or with whichever other character if a different separator is used. 

Value (-v) – This is the value that should take the place of the specified nulls. Required argument. 


Outlier

Update -m mode -i input -o output -s separator -a attribute -t tolerance-r range -l lower -u upper -z outlier

Tolerance (-t) – This is a user specified percentage of how much they are willing to tolerate non-numerical values. The program will read through the specified column, checking where the value is characterized as a string, not a number. If the percentage of string values compared to total values exceeds the tolerance, the program will exit. Tolerance must be a decimal number between 0 and 100 inclusive. 

Range (-r) – The user can specify if they want to examine outliers based on a specified range of acceptable values or whether they would like to default to a z-score approach where the program will impute any values that exceed an α=0.05 confidence level for z-score. Required argument.  

Lower (-l) – If the user specifies a range, this is the inclusive lower bound of the range. The lower bound should be inputted in the form of an integer or decimal number. If the range mode is selected, the lower limit is required. If the user selects the z-score mode and provides a lower bound, the extraneous information will be ignored, and the program will proceed with the z-score mode. 

Upper (-u) - If the user specifies a range, this is the inclusive upper bound of the range. The upper bound should be inputted in the form of an integer or decimal number. If the range mode is selected, the upper limit is required. If the user selects the z-score mode and provides an upper bound, the extraneous information will be ignored, and the program will proceed with the z-score mode. 

Outlier (-z) – For values that the program has identified as outliers, the program will replace them according to the instruction provided in this argument, which can be one of three options: Mean, Median, or Null. 


Format

Update -m mode -i input -o output -s separator -a attribute -f format

Format (-f) – This value currently has two options: string or number. The program will assume the data type of a specific column is the selected data type and will log as an exception each row where the value is not of the specified data type. At the end, the program will return the total number of exceptions and the row number for each. 


Delete

Update -m mode -i input -o output -s separator -a attribute -v value -f format -d delete

Value (-v) – The user will select the value upon which they would like to base a deletion. The value can be either text or numeric. 

Format (-f) – The user will select whether the operation they are wanting to use for the delete is a string operation or a numeric operation. They can choose between ‘string’ and ‘number’ for this argument. 

Delete (-d) – The user will specify the condition that they would like to delete on in relation to their value. If they select ‘string’ in the -f format argument, then they can choose from the text operators Contains, Does Not Contain, Equals, or Does Not Equal in the delete argument. If they select ‘number’, they can choose from the standard numerical operators > (greater than), < (less than), >= (greater than or equal to), <= (less than or equal to), = (equals), and != (does not equal). 
