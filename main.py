#Import the modules needed for this program
import datetime 
import csv
import sys

#Initialize the variables - CSV files for the backlog and each release
BACKLOGFILE = "backlog.csv"
MVPFILE = "mvp.csv"
RELEASEONEFILE = "releaseone.csv"
RELEASETWOFILE = "releasetwo.csv"

#Main program
def main():
    print("Welcome to your Product Management Companion!") #initial welcome message
    run_mainmenu() #run the main menu display and functionality

#Display of the main menu
def display_mainmenu():
    print("-------")
    print()
    print("Please input the number of the action you would like to perform.")
    print()
    print("Actions:")
    print("1 - Add a requirement to the backlog")
    print("2 - View the backlog")
    print("3 - View the MVP release")
    print("4 - View Release 1")
    print("5 - View Release 2")
    print("0 - Exit")
    print()   

#Main menu functionality, including ending the program
def run_mainmenu():
    while True:
        display_mainmenu() #displays the main menu
        action = input("Input an action number: ") #gets user input for the action they would like to do from the menu options
        print() #adds a line break for better visual in the console
        if action == "1":
            add_requirement(backlog,BACKLOGFILE) #Adds a requirement
        elif action == "2":
            display_requirements(backlog,BACKLOGFILE) #Shows the backlog contents
        elif action == "3":
            display_requirements(mvp,MVPFILE) #Shows the MVP contents
        elif action == "4":
            display_requirements(releaseone,RELEASEONEFILE) #Shows the Release 1 contents
        elif action == "5":
            display_requirements(releasetwo,RELEASETWOFILE) #Shows the Release 2 contents     
        elif action == "0":
            exit_program() #terminates the program
        else:
            print("This is not a valid action. Please try again.\n") #catches all other inputs and allows user to input another action number

#Display of the secondary user menu
def display_secondarymenu():
    print("Please input the number of the action you would like to perform next.")
    print()
    print("Actions:")
    print("1 - Add requirement")
    print("2 - Update requirement")
    print("3 - Move requirement")
    print("0 - Exit")
    print()   

#Secondary user menu functionality
def run_secondarymenu(filenamevar,FILENAME):
    while True:    
        display_secondarymenu() #displays the secondary menu
        action = input("Input an action number: ") #gets user input for the action they would like to do from the menu options
        print() #adds a line break for better visual in the console
        if action == "1":
            add_requirement(filenamevar,FILENAME) #Adds a requirement
        elif action == "2":
            update_requirement(filenamevar,FILENAME) #Updates a requirement
        elif action == "3":
            move_requirement(filenamevar,FILENAME) #Moves a requirement
        elif action == "0":
            run_mainmenu() #Returns to the main menu
        else:
            print("This is not a valid action. Please try again.\n") #catches all other inputs and allows user to input another action number

#Display of the field options menu
def display_fieldmenu():
    print("Please input the number of the field you would like to update.")
    print()
    print("Fields:")
    print("1 - Requirement description")
    print("2 - Priority level (Highest: 1, Lowest: 5)")
    print("3 - Estimated story points")
    print("4 - Status")
    print("0 - Exit")
    print()

#Field options menu functionality
def run_fieldmenu(filenamevar,FILENAME,requirementid):
    while True:    
        display_fieldmenu() #displays the field options menu
        fieldindex = input("Input a field number: ") #gets user input for the field they would like to update from menu options
        print() #adds a line break for better visual in the console
        if (fieldindex == "1" or fieldindex == "2" or fieldindex == "3" or fieldindex == "4"): #Checks for a valid selection and then each case based on what value was input
            if fieldindex == "1":
                newfieldvalue = input("New description: ")
                update_field(filenamevar,FILENAME,requirementid,fieldindex,newfieldvalue) #Updates the field value
            elif fieldindex == "2":
                newfieldvalue = input("New priority level (Highest: 1, Lowest: 5): ")
                if (newfieldvalue == "1" or newfieldvalue == "2" or newfieldvalue == "3" or newfieldvalue == "4" or newfieldvalue == "5"):
                    update_field(filenamevar,FILENAME,requirementid,fieldindex,newfieldvalue) #Updates the field value
                else:
                    print("This is not a valid priority level. Please try again.\n") #catches all other inputs and allows user to input another priority level
            elif fieldindex == "3":
                newfieldvalue = input("New story point estimate: ")
                if is_integer(newfieldvalue): #Checks that the input is an integer
                    update_field(filenamevar,FILENAME,requirementid,fieldindex,newfieldvalue) #Updates the field value
                else:
                    print("This is not a valid story point estimate. Please try again.\n") #catches all other inputs and allows user to input another story point estimate
            elif fieldindex == "4":
                newfieldvalue = input("New status (To Do, In Progress, Done): ")
                newfieldvalue = newfieldvalue.title() #Capitalizes each word in the string
                if (newfieldvalue == "To Do" or newfieldvalue == "In Progress" or newfieldvalue == "Done"): #Validates the status is an option
                    update_field(filenamevar,FILENAME,requirementid,fieldindex,newfieldvalue) #Updates the field value
                else:
                    print("This is not a valid status. Please try again.\n") #catches all other inputs and allows user to input another status
        elif fieldindex == "0":
            run_mainmenu() #Returns to the main menu
        else:
            print("This is not a valid field number. Please try again.\n") #catches all other inputs and allows user to input another field number

#Read the requirements from the CSV file and return as a list that can be stored later into a variable to be used in the program - used for backlog and all releases
def read_file(FILENAME):
    try:
        filenamevar = [] #Create the list
        with open(FILENAME, newline="") as file: #Opens the file
            reader = csv.reader(file) #Read the file contents
            for row in reader: #Iterate through all rows in the file
                filenamevar.append(row) #Add each row in the file to the list
        return filenamevar #Returns the list to be used as an output
    except FileNotFoundError as error: #Case when the file cannot be found
        print(f"Could not find {FILENAME} file.") 
        exit_program() #Terminates the program
    except Exception as e: #Catch any exceptions
        print(type(e), e)
        exit_program() #Terminates the program

#Write requirements to the CSV file to store for later use - used for backlog and all releases
def write_requirements(filenamevar,FILENAME):
    try:
        with open(FILENAME, "w", newline="") as file: #Opens the file
            writer = csv.writer(file)
            writer.writerows(filenamevar) #Writes the requirements to the file
    except Exception as e: #Catch any exceptions
        print(type(e), e)
        exit_program() #Terminates the program
    
#Add requirement to the list end of the list - used for backlog and all releases
def add_requirement(filenamevar,FILENAME):
    requirementid = str(len(filenamevar) + 1) #Set the requirement ID by default based on the length of the existing list, adding one, and converting to a string
    description = input("Enter the requirement description: ") 
    while True:
        priority = input("Enter the priority level (Highest: 1, Lowest: 5): ")
        if (int(priority) <= 5 and int(priority) > 0): #Check that the priority was an integer and in the range
            break #Continue if the input was valid
        else:
            print("This is not a valid priority level. Please try again.\n") #catches all other inputs and allows user to input another priority level
    while True:
        storypoints = input("Enter the estimated story points: ")
        if is_integer(storypoints): #Check that the input was an integer
            break #Continue if the input was valid
        else:
            print("This is not a valid story point estimate. Please try again.\n") #catches all other inputs and allows user to input another story point estimate
    status = "To Do" #Set the status by default
    dateadded = str(datetime.date.today()) #Get the current date as a string
    requirementtoadd = [requirementid,description,priority,storypoints,status,dateadded] #Create the list of the new requirement to be added to the file list
    filenamevar.append(requirementtoadd) #Add the requirement to the end of the list
    write_requirements(filenamevar,FILENAME) #Saves the requirements to the CSV file
    print(f"Requirement {requirementid} was added.") #Confirm the requirement was added
    print()

#Display requirements - used for backlog and all releases
def display_requirements(filenamevar,FILENAME):
    if len(filenamevar) > 0: #Checks that the list contains at least one requirement
        print("Current Requirements: ")
        for i, req in enumerate(filenamevar, start=1): #Loop through all requirements in the list
            print(f"Requirement ID: {req[0]} \t Requirement: {req[1]}") #Display the requirement ID and description for each
    else:
        print("There are no requirements at this time.") #Displays if there were no requirements
    print("-------")
    print()
    run_secondarymenu(filenamevar,FILENAME) #run the main menu display and functionality

#Update requirement
def update_requirement(filenamevar,FILENAME):
    while True:
        requirementid = input("Input the Requirement ID: ")
        print() #adds a line break for better visual in the console
        if int(requirementid) <= len(filenamevar): #Checks to make sure the requirement falls within the length of the list of existing requirements
            requirementid = int(requirementid) #Converts the ID to an integer
            print("Current Requirement Information:") #Displays all current values using the position of each in the list
            print(f"Requirement ID: {requirementid}")
            print(f"Requirement Description: {filenamevar[requirementid-1][1]}")
            print(f"Priority Level: {filenamevar[requirementid-1][2]}")
            print(f"Estimated Story Points: {filenamevar[requirementid-1][3]}")
            print(f"Status: {filenamevar[requirementid-1][4]}")
            print(f"Date Added: {filenamevar[requirementid-1][5]}")
            print("-------")
            print() #adds a line break for better visual in the console
            run_fieldmenu(filenamevar,FILENAME,requirementid) #Displays the field menu and functionality
        else:
            print("This is not a valid Requirement ID. Please try again.\n") #catches all other inputs and allows user to input another Requirement ID

#Check if story point estimate is an integer value, returns True if it is an integer and False otherwise
def is_integer(newfieldvalue):
    try:
        int(newfieldvalue)
        return True
    except ValueError:
        return False

#Update field
def update_field(filenamevar,FILENAME,requirementid,fieldindex,newfieldvalue):
    fieldindex = int(fieldindex) #Get the integer form of the index
    requirementindex = int(requirementid)-1 #Get the requirement index from the ID and subtracting one, making sure to convert to an integer
    filenamevar[requirementindex][fieldindex] = newfieldvalue #Replaced the value in the specified location with the new value
    write_requirements(filenamevar,FILENAME) #Saves the requirements to the CSV file
    print("Field has been updated.")
    print("-------")
    print()

#Move requirement
def move_requirement(filenamevar,FILENAME):
    requirementid = input("What is the Requirement ID of the requirement to be moved: ") #Get the ID of the requirement to be moved
    print()
    requirementindex = int(requirementid)-1 #Gets the index of the requirement based on its ID
    requirementtomove = filenamevar.pop(requirementindex) #Finds the requirement by the index, removes it, and stores the content in a temporary variable
    write_requirements(filenamevar,FILENAME) #Saves the requirements to the CSV file
    print("Where should the requirement be moved to: Backlog, MVP, Release 1, or Release 2?")
    print()
    while True:
        newreleaselocation = input("Where to move to: ").title() #Capitalizes each word in the string
        if newreleaselocation == "Backlog": #If the requirement is moving to the backlog
            requirementtomove[0] = str(len(backlog)+1) #Get the length of the existing list, add one to get the right new index, and add this total as a string to the list to be appended
            backlog.append(requirementtomove) #Add the requirement list to the end
            write_requirements(backlog,BACKLOGFILE) #Saves the requirements to the CSV file
            print("Requirement was moved to the backlog.")
            print()
            run_mainmenu() #Returns to the main menu
        elif newreleaselocation.upper() == "MVP": #If the requirement is moving to the MVP, Capitalizes the whole string
            requirementtomove[0] = str(len(mvp)+1) #Get the length of the existing list, add one to get the right new index, and add this total as a string to the list to be appended
            mvp.append(requirementtomove) #Add the requirement list to the end
            write_requirements(mvp,MVPFILE) #Saves the requirements to the CSV file
            print("Requirement was moved to the MVP.")
            print()
            run_mainmenu() #Returns to the main menu
        elif newreleaselocation == "Release 1": #If the requirement is moving to Release 1
            requirementtomove[0] = str(len(releaseone)+1) #Get the length of the existing list, add one to get the right new index, and add this total as a string to the list to be appended
            releaseone.append(requirementtomove) #Add the requirement list to the end
            write_requirements(releaseone,RELEASEONEFILE) #Saves the requirements to the CSV file
            print("Requirement was moved to Release 1.")
            print()
            run_mainmenu() #Returns to the main menu
        elif newreleaselocation == "Release 2": #If the requirement is moving to Release 2
            requirementtomove[0] = str(len(releasetwo)+1) #Get the length of the existing list, add one to get the right new index, and add this total as a string to the list to be appended
            releasetwo.append(requirementtomove) #Add the requirement list to the end
            write_requirements(releasetwo,RELEASETWOFILE) #Saves the requirements to the CSV file
            print("Requirement was moved to Release 2.")
            print()
            run_mainmenu() #Returns to the main menu
        else:
            print("This is not a valid location. Please try again.\n") #catches all other inputs and allows user to input another location
    
    
#User inputs "0" in the main menu to exit the program
def exit_program():
    print("You have chosen to exit the program.")
    print("Thank you and goodbye!")
    print("You may now close this window.")
    sys.exit() #terminates the program

#Read the CSV files for the backlog and all releases into global variables
backlog = read_file(BACKLOGFILE)
mvp = read_file(MVPFILE)
releaseone = read_file(RELEASEONEFILE)
releasetwo = read_file(RELEASETWOFILE)

#Runs the program
main()
