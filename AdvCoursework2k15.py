#imported modules
from tkinter import *
import traceback
import pymysql



class LoginWindow(Frame):
    username = ""
    name = ""
    password = ""
    userId = ""
    choiceID = ""
    year = int()

    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master)

        #windows attributes
        self.master.title("Course - Login")
        #self.master.wm_iconbitmap("AppIcon.ico")
        self.master.configure(bg="gray")
        self.master.resizable(0,0)

        #labels
        self.title1 = Label(self.master, text="Log in to pick your course choice\n", bg="gray", font=("Helvetica", 12))
        self.usertitle = Label(self.master, text="Username:", bg="gray")
        self.passtitle = Label(self.master, text="Password:", bg="gray")
        self.message = Label(self.master, text="Please Log In", bg="orange", width="17", height="2")

        #text entry windows and their variables
        usernameStore = StringVar()
        self.usernameStore = usernameStore
        passwordStore = StringVar()
        self.passwordStore = passwordStore
        self.usernameBox = Entry(self.master, textvariable = str(usernameStore))
        self.passwordBox = Entry(self.master, show='*', textvariable = str(passwordStore))

        #Buttons
        self.loginB = Button (self.master, text="Login", activebackground="Green", command=self.login)
        self.exitB = Button (self.master, text="Exit", activebackground="Red", command=self.exitProgram)

        #grid widgets
        self.title1.grid(row=1, column=1, columnspan=2)
        self.usertitle.grid(row=2, column=1)
        self.usernameBox.grid(row=2, column=2, sticky=W)
        self.passtitle.grid(row=3, column=1)
        self.passwordBox.grid(row=3, column=2, sticky=W)
        self.message.grid(row=4,column=1)
        self.loginB.grid(row=5, column=2, ipady=2, ipadx=50)
        self.exitB.grid(row=5, column=1, ipady=2, ipadx=50)

    def exitProgram(self):
        self.master.destroy()

    def login(self):
        ### For DEBUG ###
        print("### RUNNING LOGIN ATTEMPT ###\n")

        try:
            #Estabilishing DB connection
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
        except:
            print(" FAILED TO CONNECT TO DATABASE.")
            self.message["text"] = "Can't Connect To DB\n Try again later"
            self.message["bg"] = "Red"


        #Retrieving passwords from fields
        LoginWindow.username = self.usernameStore.get()
        LoginWindow.password = self.passwordStore.get()

        ### CHANGE THIS, TESTING PURPOSES ONLY
        #LoginWindow.username = 'admin'
        #LoginWindow.password = 'admin'
        ###

        c = conn.cursor()

        Valid = True
        Valid2 = False

        if (len(LoginWindow.username) == 0) and (len(LoginWindow.password) == 0):
            print ("No username or Password")
            Valid = False
            Valid2 = True
            self.message["text"] = "Please Enter Details"
            print("\n### DEBUG:\n"
                  " No Details Entered, Login Failed.\n")


        if (len(LoginWindow.password) == 0) and Valid2 == False:
            print ("No Password")
            Valid = False
            self.message["text"] = "Please Enter Password"


        if(c.execute("SELECT * FROM `users` WHERE username='"+ LoginWindow.username +"' AND password='"+ LoginWindow.password +"'")) and Valid == True:
            print ("Username and Password accepted.")
            self.message["text"] = "Logged In!"
            self.message["bg"] = "green"
            print("\n### DEBUG:\n"
                  " Login Succeeded! Now attempting to retrieve information from DB.")


            #prepare SQL query to get all details
            getUserInfo = ("SELECT * FROM `users` WHERE username='"+ LoginWindow.username +"'")
            #Fetch the data
            c.execute(getUserInfo)
            results = c.fetchall()
            for row in results:
                LoginWindow.userId = row[0]
                LoginWindow.username = row[1]
                LoginWindow.name = row[3]
                LoginWindow.year = row[4]
                LoginWindow.choiceID = row[5]
                permissions = row[6]

            print("Information Recieved. Displaying:\n")
            console = ("    User {user} is user {name}. They are in year {year} at Firrhill.") .format(user=LoginWindow.username, name=LoginWindow.name, year=LoginWindow.year)
            print(console)
            print("\n### DEBUG:\n"
                  " Login Completed!\n"
                  " END OF PROCEDURE!\n"
                  " ###\n"
                  "\n")

            conn.commit()
            conn.close()
            self.master.destroy()

            if permissions == 0 and LoginWindow.choiceID == 0:
                mainWindow()

            elif permissions == 0 and (LoginWindow.choiceID > 0):

                conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
                c = conn.cursor()
                print("DB connected.")

                checkChoiceIDPresent = ("SELECT * FROM `userssubjectchoice` WHERE choiceID='"+ str(LoginWindow.choiceID) +"'")

                c.execute(checkChoiceIDPresent)
                print("Executed:", checkChoiceIDPresent)

                results = c.fetchall()
                subjectCheck = {}
                ValidCoiceIDCheck = False

                for row in results:
                    for i in range(1, 5):
                        subjectCheck[i] = row[i]
                        print('subjet in slot '+ str(i) +' is '+ str(subjectCheck[i]))

                conn.commit()
                conn.close()



                for i in range(1, 5):
                    if len(subjectCheck[i]) < 7:
                        ValidCoiceIDCheck = True
                        mainWindow()
                        break

                if ValidCoiceIDCheck == False:
                    pupilsStatisticWindow()



            elif permissions == 1:
                print("Run admin menu.")
                adminWindow()


        elif Valid == True:
            print ("Username or Password incorrect.")
            self.message["text"] = "Incorrect User/Pass"
            self.message["bg"] = "Red"
            print("\n### DEBUG:\n"
                  " Login Failed!\n"
                  " END OF PROCEDURE!\n"
                  " ###\n"
                  "\n")


class MainWindow(Frame):
    subject = {}
    tempAllSubjectName = []
    tempAllSubjectLevel = []
    tempAllSubjectCodes = []
    subjectColumn = ["A", "B", "C", "D", "E", "F", "G", "H"]
    a = " at "
    j = 0

    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master)

        #windows attributes
        self.master.title("Course - Chooser")
        #self.master.wm_iconbitmap("AppIcon.ico")
        self.master.configure(bg="LightGray")
        #self.master.geometry("717x355")
        self.master.attributes('-topmost', 1)
        #self.master.attributes('-topmost', 0)
        self.master.resizable(0,0)

        #Labels
        greetingMessage = "Welcome "+ LoginWindow.name +". Please select the subject you'd like to study this\nyear from the choices below.\n"
        self.welcomeLabel = Label(self.master, justify=LEFT, text=greetingMessage,font=("Helvetica", 16), bg="LightGray").grid(row=1, columnspan=1+2+3+4)
        self.subjectIndicator = Label(self.master, justify=LEFT, text="Choose Subjects:       ",font=("Helvetica", 13), bg="LightGray").grid(row=2, column=3)

        #Subject Attribute Retrevial
        print("### DEBUG:\n"
              "### RUNNING SUBJECT ATTRIBUTE RETRIEVAL FROM DB.\n"
              "### MAJOR DEBUGGING FROM HERE TILL LONG LINE OF HASHES!\n"
              "### INNCOMMMMMMMING!")

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')

        c = conn.cursor()

        #Change this to self, also change it to self inside countNumOfSubjects variable
        numOfSubjectsInColumn = ["numOfSubjectsInA", "numOfSubjectsInB", "numOfSubjectsInC", "numOfSubjectsInD", "numOfSubjectsInE"]
        self.totalNumOfSubjects = 0

        for i in range(5):
            print("\n### DEBUG:\n"
                  " Checking how many subjects are in this column!\n")
            countNumOfSubjects = ("SELECT COUNT(*) FROM `subjects` WHERE `subjectColumn`='"+ MainWindow.subjectColumn[i] +"'")
            c.execute(countNumOfSubjects)

            results = c.fetchall()

            for row in results:
                numOfSubjectsInColumn[i] = row[0]


            print("There are this many subjects in column", MainWindow.subjectColumn[i],":",numOfSubjectsInColumn[i],"")

            self.totalNumOfSubjects = self.totalNumOfSubjects + numOfSubjectsInColumn[i]

        print("\nThere are this many number of subjects:",self.totalNumOfSubjects,"\n")


        print("\n### DEBUG:\n"
              " Initialising empty arrays for each columns subject attributes.")
        [subjectIDA, subjectNameA, subjectLevelA, subjectSpacesA, subjectColumnA,
        subjectIDB, subjectNameB, subjectLevelB, subjectSpacesB, subjectColumnB,
        subjectIDC, subjectNameC, subjectLevelC, subjectSpacesC, subjectColumnC,
        subjectIDD, subjectNameD, subjectLevelD, subjectSpacesD, subjectColumnD,
        subjectIDE, subjectNameE, subjectLevelE, subjectSpacesE, subjectColumnE] = [{}, {}, {}, {}, {},
                                                                                    {}, {}, {}, {}, {},
                                                                                    {}, {}, {}, {}, {},
                                                                                    {}, {}, {}, {}, {},
                                                                                    {}, {}, {}, {}, {}]
        print(" Initialised!\n")

        columnA = [subjectIDA, subjectNameA, subjectLevelA, subjectSpacesA, subjectColumnA]
        columnB = [subjectIDB, subjectNameB, subjectLevelB, subjectSpacesB, subjectColumnB]
        columnC = [subjectIDC, subjectNameC, subjectLevelC, subjectSpacesC, subjectColumnC]
        columnD = [subjectIDD, subjectNameD, subjectLevelD, subjectSpacesD, subjectColumnD]
        columnE = [subjectIDE, subjectNameE, subjectLevelE, subjectSpacesE, subjectColumnE]

        subjectAttributes = [columnA, columnB, columnC, columnD, columnE]

        Valid = False
        counter = 0


        while Valid == False:
            if counter < self.totalNumOfSubjects:
                for i in range(5):
                    for j in range(0, numOfSubjectsInColumn[i]):
                        getSubjectData = ("SELECT * FROM `subjects` WHERE subjectColumn='"+ MainWindow.subjectColumn[i] +"' ORDER BY subjectName ASC")
                        c.execute(getSubjectData)
                        results = c.fetchall()[j]


                        for k in range(5):
                            subjectAttributes[i][k][j] = results[k]
                            print(subjectAttributes[i][k][j])


                        print("Just took data from this data record:",results,"\n")
                        counter=counter+1
            else:
                    Valid = True
                    conn.commit()
                    conn.close()
                    print("Retrieved all subjects data from",counter,"subjects listed in DB.")
                    print("\n### DEBUG:\n"
                    " SUBJECT ATTRIBUTE RETRIVAEL COMPLETE!\n"
                    " #################################################################################################")







        #DropdownBox and corresponding labels
        subjectOptions = {}
        displayChoice = []



        if (LoginWindow.year == 6) or (LoginWindow.year == 5):
            MainWindow.j = 5
            print ('User is in year',LoginWindow.year,'so creating 5 subject fields.')
        elif (LoginWindow.year == 3) or (LoginWindow.year == 4):
            MainWindow.j = 8
            print ('User is in year',LoginWindow.year,'so creating 8 subject fields.')

        for i in range(MainWindow.j):
            del displayChoice[:]
            MainWindow.subject[i] = StringVar()
            MainWindow.subject[i].set ('Pick A Subject And Academic Level')


            explanation = ("Please pick a subject in column {subcolumn}:") .format(subcolumn = MainWindow.subjectColumn[i])
            subjectLabel = Label(self.master, bg="LightGray", text=explanation, font=("Helvetica", 12)).grid(row=i+3, column=1, sticky=W)


            for j in range(0, numOfSubjectsInColumn[i]):
                displayChoice.append(subjectAttributes[i][1][j] + MainWindow.a + subjectAttributes[i][2][j])
                MainWindow.tempAllSubjectName.append(subjectAttributes[i][1][j])
                MainWindow.tempAllSubjectLevel.append(subjectAttributes[i][2][j])
                MainWindow.tempAllSubjectCodes.append(subjectAttributes[i][0][j])

            subjectOptions[i] = OptionMenu(self.master, MainWindow.subject[i], *displayChoice)
            subjectOptions[i]["menu"].config(bg="DarkGray", activebackground="Red")

            subjectOptions[i].grid(row=i+3, column=3, padx=20, sticky=EW)

        #Buttons
        self.subjectCheckB = Button(self.master, text='Submit Subjects', command=self.subjectCheck).grid(row=MainWindow.j+2, column=4, sticky=E)
        self.logoutB = Button(self.master, text='Logout', command=self.logout).grid(row=MainWindow.j+2, column=5, sticky=W)

    def logout(self):
        self.exitProgram()
        loginWindow()


    def subjectCheck(self):

        subFrame = SubjectCheckWindow(self)



    def exitProgram(self):

        self.master.destroy()







class SubjectCheckWindow(Toplevel):

    def __init__(self, master):

        self.master_frame = master
        Toplevel.__init__(self)

        self.grab_set()

        #windows attributes
        self.title("Confirm Choice?")
        #self.master.wm_iconbitmap("AppIcon.ico")
        self.configure(bg="LightGray")
        #self.master.geometry("717x355")
        self.attributes('-topmost', 1)
        #self.master.attributes('-topmost', 0)
        self.resizable(0,0)

        #Labels
        confirmMessage = "Confirm Choice?"
        self.confirmMessage = Label(self, justify=LEFT, text=confirmMessage,font=("Helvetica", 12), bg="LightGray").grid(row=0, columnspan=0+1)
        self.confirm = Button(self, text='Yes', command=self.subjectCheck).grid(row=2, column=0, sticky="NWES")
        self.decline = Button(self, text='No', command=self.closeConfirmWindow).grid(row=2, column=1, sticky="NWES")
        self.columnconfigure(0, weight=1)


    def closeConfirmWindow(self):
        self.grab_release()
        self.destroy()



    def subjectCheck(self):

        tempHoldOfNamePosition = []
        tempHoldOfLevelPosition = []
        validArray = {}



        print ("User's Choice ID is:",LoginWindow.choiceID)
        if LoginWindow.choiceID == 0: #This is setting up initial choiceID if one isn't set up already
            #Estabilish DB connection
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
            c = conn.cursor()
            findMaxChoiceID = ("SELECT COUNT(*) FROM `usersSubjectChoice`")
            c.execute(findMaxChoiceID)

            results = c.fetchall()
            for row in results:
                numOfRecords = row[0]

            LoginWindow.choiceID = numOfRecords+1
            print('There is this many columns of data:',numOfRecords)
            print('Therefore, the Choice ID for this pupil will be,', LoginWindow.choiceID)
            insertChoiceID = ("INSERT INTO `userssubjectchoice`(`choiceID`, `ID`) VALUES ("+ str(LoginWindow.choiceID) +", "+ str(LoginWindow.userId) +")")
            updateUserDetailsChoiceID = ("UPDATE `users` SET choiceID='"+ str(LoginWindow.choiceID) +"' WHERE ID="+ str(LoginWindow.userId) +"")

            print('Execeuting this query into database: "', insertChoiceID,'"')
            c.execute(insertChoiceID)
            print('Execeuting this query into database: "', updateUserDetailsChoiceID,'"')
            c.execute(updateUserDetailsChoiceID)


            conn.commit()
            conn.close()

        else:
            print("Since user already has choiceID, no need to set it up.")




        chosenSubjectName = []
        chosensubjectLevel = []

        noSpaceInSubjectBoolean = False


        del chosenSubjectName[:]
        del chosensubjectLevel[:]
        matchingSubjectBoolean = False
        evenChosenASubjectBoolean = True

        try:
            for i in range(MainWindow.j):
                validArray[i] = False



                #This Finds the subject ID by searching the lists tempAllSubjectName, tempAllSubjectLevel, tempAllSubjectCodes.
                tempHold=(""+ MainWindow.subject[i].get() +"")
                if tempHold == 'Pick A Subject And Academic Level':
                    evenChosenASubjectBoolean = False
                    break


                print("PRINTING TEMPHOLD",tempHold)
                #if tempHold.find(MainWindow.a) >= 0:
                numTillAt = tempHold.find(MainWindow.a)
                tempHold = tempHold.replace(MainWindow.a, "")
                choiceName = tempHold[0:numTillAt]
                choiceLevel = tempHold[numTillAt:len(tempHold)]
                chosenSubjectName.append(choiceName)
                chosensubjectLevel.append(choiceLevel)
                print("chosenSubjectName[",i,"] is",chosenSubjectName[i])
                print(choiceLevel)



            if evenChosenASubjectBoolean == True:
                for a in range(MainWindow.j):
                    for b in range(MainWindow.j):
                        if a == b and a != MainWindow.j-1:
                            b = b+1
                        elif a == b and a == MainWindow.j-1:
                            b = b-1
                        print("Does",chosenSubjectName[a],"=",chosenSubjectName[b],"?")
                        if chosenSubjectName[a] == chosenSubjectName[b]:
                            print("You have picked two", chosenSubjectName[a])
                            confirmMessage = ("ERROR: You picked {subjectName} twice.\nPlease check and try again.").format(subjectName=chosenSubjectName[a])
                            self.confirmMessage = Label(self, justify=LEFT, text=confirmMessage,font=("Helvetica", 12), bg="red").grid(row=0, columnspan=0+1)
                            self.configure(bg="red")
                            matchingSubjectBoolean = True
                            break




                for i in range(MainWindow.j):
                    del tempHoldOfLevelPosition[:]
                    del tempHoldOfNamePosition[:]



                    if matchingSubjectBoolean == True:
                        break


                    else:
                        for l, m in enumerate(MainWindow.tempAllSubjectName):
                            if m == (chosenSubjectName[i]):
                                tempHoldOfNamePosition.append(l)
                        print(*tempHoldOfNamePosition)

                        for n, o in enumerate(MainWindow.tempAllSubjectLevel):
                            if o == (chosensubjectLevel[i]):
                                for x in range(len(tempHoldOfNamePosition)):
                                    if n == tempHoldOfNamePosition[x]:
                                        tempHoldOfLevelPosition.append(n)
                        print(*tempHoldOfLevelPosition)


                        for p, q in enumerate(MainWindow.tempAllSubjectCodes):
                            if q[6] == (MainWindow.subjectColumn[i]):
                                for x in range(len(tempHoldOfLevelPosition)):
                                    if p == tempHoldOfLevelPosition[x]:
                                        tempCodeArrayPos = p
                        print(tempCodeArrayPos)
                        print(MainWindow.tempAllSubjectCodes[tempCodeArrayPos])



                        #Estabilish DB connection
                        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
                        c = conn.cursor()

                        print ('For Subject', MainWindow.subjectColumn[i],'you have selected,', MainWindow.subject[i].get() )
                        print ('Attempting to add subject to DB now in corresponding column.')


                        checkSpaceForSubjectQuery = ("SELECT * FROM `subjects` WHERE subjectID='"+ MainWindow.tempAllSubjectCodes[tempCodeArrayPos] +"'")
                        print("Executing", checkSpaceForSubjectQuery)
                        c.execute(checkSpaceForSubjectQuery)

                        results = c.fetchall()

                        for row in results:
                            spaceInSubject = row[3]
                        print("Space in subject is", spaceInSubject)

                        minusAspaceInSubjectQuery = ("UPDATE `subjects` SET `Amount`='"+ str(spaceInSubject) +"' WHERE subjectID='"+ MainWindow.tempAllSubjectCodes[tempCodeArrayPos] +"'")

                        if spaceInSubject > 0:
                            spaceInSubject = spaceInSubject -1
                            c.execute(minusAspaceInSubjectQuery)

                        elif spaceInSubject == 0:
                            noSpaceInSubjectBoolean = True
                            print("Made it thi far")


                        if noSpaceInSubjectBoolean == False:
                            query = ("UPDATE `userssubjectchoice` SET Subject"+ MainWindow.subjectColumn[i] +"ID='"+ MainWindow.tempAllSubjectCodes[tempCodeArrayPos] +"' WHERE ID="+ str(LoginWindow.userId) +" AND choiceID="+ str(LoginWindow.choiceID) +"")
                            print('Execeuting this query into database: "', query,'"')

                            try:
                                c.execute(query)

                                conn.commit()
                                conn.close()

                                print("Database Update Successful.")
                                validArray[i] = True
                            except:
                                print("Database Update Failed.")
                                conn.rollback()

                        elif noSpaceInSubjectBoolean == True:
                            confirmMessage = ("ERROR: No space left in\nsubject "+chosenSubjectName[i]+". Choose\ndifferent subject.")
                            self.confirmMessage = Label(self, justify=LEFT, text=confirmMessage,font=("Helvetica", 12), bg="red").grid(row=0, columnspan=2)
                            break

            elif evenChosenASubjectBoolean == False:
                confirmMessage = ("ERROR: You have not selected\na choice in every drop down box")
                self.confirmMessage = Label(self, justify=LEFT, text=confirmMessage,font=("Helvetica", 12), bg="red").grid(row=0, columnspan=2)




        except:
            tb = traceback.format_exc()
            print(tb)

        valid = True
        for i in range(len(validArray)):
            if validArray[i] == False:
                valid = False

        if valid == True:
            self.destroy
            MainWindow.exitProgram(self)
            pupilsStatisticWindow()



class PupilsStatisticWindow(LoginWindow):
    subjectName = {}
    subjectLevel = {}

    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master)
        print("Running this window")


        #windows attributes
        self.master.title("Subjects Chosen")
        #self.master.wm_iconbitmap("AppIcon.ico")
        self.master.configure(bg="LightGray")
        #self.master.geometry("717x355")
        self.master.attributes('-topmost', 1)
        #self.master.attributes('-topmost', 0)
        self.master.resizable(0,0)

        #Labels
        username = ("User: "+ LoginWindow.name)
        self.usernameLabel = Label(self.master, justify=LEFT, text=username,font=("Helvetica", 14), bg="LightGray").grid(row=0, column=0, sticky="W")

        space = ("           ")
        self.spaceLabel = Label(self.master, text=space, bg="LightGray").grid(row=0, column=1)

        year = ("Year: S"+ str(LoginWindow.year))
        self.yearLabel = Label(self.master, justify=LEFT, text=year,font=("Helvetica", 16), bg="LightGray").grid(row=0, column=2, sticky="W")



        if (LoginWindow.year == 6) or (LoginWindow.year == 5):
            j = 5
            print ('User is in year',LoginWindow.year,'so user has 5 subjects.')
        elif (LoginWindow.year == 3) or (LoginWindow.year == 4):
            j = 8
            print ('User is in year',LoginWindow.year,'so user has 8 subjects.')


        #Buttons
        self.timtableButtom = Button(self.master, text='Construct Timetable', command=self.makeTimetable).grid(row=j+2, column=0)
        self.decline = Button(self.master, text='Logout', command=self.logout).grid(row=j+2, column=2, sticky=E)


        subjectChosenText = {}
        levelChosenText = {}
        choiceID = {}



        for i in range(j):
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
            c = conn.cursor()

            retrieveSubjectIDQuery = ("SELECT * FROM `userssubjectchoice` WHERE choiceID="+ str(LoginWindow.choiceID) +" AND ID="+ str(LoginWindow.userId) +"")
            print('Execeuting this query into database: "', retrieveSubjectIDQuery, '"')
            c.execute(retrieveSubjectIDQuery)

            results = c.fetchall()
            for row in results:
                choiceID[i] = row[i+1]

            conn.close()


            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
            c = conn.cursor()

            retrieveSubjectNameAndLevelQuery = ("SELECT * FROM `subjects` WHERE subjectID='"+ choiceID[i] +"'")
            print('Execeuting this query into database: "', retrieveSubjectNameAndLevelQuery, '"')
            c.execute(retrieveSubjectNameAndLevelQuery)

            results = c.fetchall()
            for row in results:
                PupilsStatisticWindow.subjectName[i] = row[1]
                PupilsStatisticWindow.subjectLevel[i] = row[2]

            conn.close()



        for i in range(j):
            subjectChosenText[i] = ("Subject chosen in "+ MainWindow.subjectColumn[i] +": ", PupilsStatisticWindow.subjectName[i])
            levelChosenText[i] = ("Level: ", PupilsStatisticWindow.subjectLevel[i])

            #tempSubjectChosenText = subjectChosenText[i]
            tempSubjectChosenText = "".join(str(x) for x in subjectChosenText[i])
            #tempLevelChosenText = levelChosenText[i]]
            tempLevelChosenText = "".join(str(x) for x in levelChosenText[i])

            self.subjectChosenDisplayLabel = Label(self.master, justify=LEFT, text=tempSubjectChosenText,font=("Helvetica", 12), bg="LightGray").grid(row=i+2, column=0, sticky="W")
            self.levelChosenDisplayLabel = Label(self.master, justify=LEFT, text=tempLevelChosenText,font=("Helvetica", 12), bg="LightGray").grid(row=i+2, column=2, sticky="W")

    def logout(self):
        self.master.destroy()
        loginWindow()

    def makeTimetable(self):
        subFrame = TimeTable(self)


class TimeTable(Toplevel):

    def __init__(self, master):

        self.master_frame = master
        Toplevel.__init__(self)

        #windows attributes
        self.title("Timetable")
        self.configure(bg="LightGray")
        self.attributes('-topmost', 1)
        self.resizable(0,0)

        plainLabel = Label(self, text=(LoginWindow.name+"'s\nTimetable"),bg="white", width=15, height=4, relief=GROOVE).grid(row=0, column=0)
        mondayLabel = Label(self, text="Monday",bg="white", width=15, height=4, relief=GROOVE).grid(row=1, column=0)
        tuesdayLabel = Label(self, text="Tuesday",bg="white", width=15, height=4, relief=GROOVE).grid(row=2, column=0)
        wednesdayLabel = Label(self, text="Wednesday",bg="white", width=15, height=4, relief=GROOVE).grid(row=3, column=0)
        thursdayLabel = Label(self, text="Thursday",bg="white", width=15, height=4, relief=GROOVE).grid(row=4, column=0)
        fridayLabel = Label(self, text="Friday",bg="white", width=15, height=4, relief=GROOVE).grid(row=5, column=0)

        periodLabels = ["Registration","Period 1", "Period 2", "Period 3", "Period 4", "Period 5", "Period 6"]
        for i in range(len(periodLabels)):
            (periodLabels[i]) = Label(self, text=periodLabels[i],bg="white", width=20, height=4, relief=GROOVE).grid(row=0, column=i+1)

        regiLabels = ["regi1", "regi2", "regi3", "regi4", "regi5"]
        for i in range(len(regiLabels)):
            (regiLabels[i]) = Label(self, text="Registration",bg="white", width=20, height=4, relief=GROOVE)
            (regiLabels[i]).grid(row=i+1, column=1)

        columnALabels = ["firstA", "secondA", "thirdA", "forthA", "fifthA"]
        for i in range(len(columnALabels)):
            (columnALabels[i]) = Label(self, text=(PupilsStatisticWindow.subjectName[0]+"\n"+PupilsStatisticWindow.subjectLevel[0]),bg="white", justify=LEFT,  width=20, height=4, relief=GROOVE)
        columnALabels[0].grid(row=1, column=3, sticky=W)
        columnALabels[1].grid(row=1, column=4, sticky=W)
        columnALabels[2].grid(row=3, column=7, sticky=W)
        columnALabels[3].grid(row=4, column=5, sticky=W)
        columnALabels[4].grid(row=5, column=2, sticky=W)

        columnBLabels = ["firstB", "secondB", "thirdB", "forthB", "fifthB"]
        for i in range(len(columnBLabels)):
            (columnBLabels[i]) = Label(self, text=(PupilsStatisticWindow.subjectName[1]+"\n"+PupilsStatisticWindow.subjectLevel[1]),bg="white", justify=LEFT, width=20, height=4, relief=GROOVE)
        columnBLabels[0].grid(row=1, column=7, sticky=W)
        columnBLabels[1].grid(row=2, column=3, sticky=W)
        columnBLabels[2].grid(row=2, column=4, sticky=W)
        columnBLabels[3].grid(row=4, column=2, sticky=W)
        columnBLabels[4].grid(row=5, column=3, sticky=W)

        columnCLabels = ["firstC", "secondC", "thirdC", "forthC", "fifthC"]
        for i in range(len(columnCLabels)):
            (columnCLabels[i]) = Label(self, text=(PupilsStatisticWindow.subjectName[2]+"\n"+PupilsStatisticWindow.subjectLevel[2]),bg="white", justify=LEFT, width=20, height=4, relief=GROOVE)
        columnCLabels[0].grid(row=1, column=5, sticky=W)
        columnCLabels[1].grid(row=2, column=2, sticky=W)
        columnCLabels[2].grid(row=3, column=5, sticky=W)
        columnCLabels[3].grid(row=3, column=6, sticky=W)
        columnCLabels[4].grid(row=5, column=4, sticky=W)

        columnDLabels = ["firstD", "secondD", "thirdD", "forthD", "fifthD"]
        for i in range(len(columnDLabels)):
            (columnDLabels[i]) = Label(self, text=(PupilsStatisticWindow.subjectName[3]+"\n"+PupilsStatisticWindow.subjectLevel[3]),bg="white", justify=LEFT, width=20, height=4, relief=GROOVE)
        columnDLabels[0].grid(row=1, column=6, sticky=W)
        columnDLabels[1].grid(row=2, column=5, sticky=W)
        columnDLabels[2].grid(row=3, column=2, sticky=W)
        columnDLabels[3].grid(row=4, column=3, sticky=W)
        columnDLabels[4].grid(row=4, column=4, sticky=W)

        columnELabels = ["firstE", "secondE", "thirdE", "forthE", "fifthE"]
        for i in range(len(columnELabels)):
            (columnELabels[i]) = Label(self, text=(PupilsStatisticWindow.subjectName[4]+"\n"+PupilsStatisticWindow.subjectLevel[4]),bg="white", justify=LEFT, width=20, height=4, relief=GROOVE)
        columnELabels[0].grid(row=1, column=2, sticky=W)
        columnELabels[1].grid(row=2, column=6, sticky=W)
        columnELabels[2].grid(row=2, column=7, sticky=W)
        columnELabels[3].grid(row=4, column=6, sticky=W)
        columnELabels[4].grid(row=4, column=7, sticky=W)







class AdminWindow(LoginWindow, Listbox):

    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master)

        #windows attributes
        self.master.title("Admin Menu")
        #self.master.wm_iconbitmap("AppIcon.ico")
        self.master.configure(bg="white")
        #self.master.geometry("717x355")
        self.master.attributes('-topmost', 1)
        #self.master.attributes('-topmost', 0)
        self.master.resizable(0,0)

        #Labels
        self.nameLabel = Label(self.master, text="Name:", bg="white").grid(row=0, column=0, sticky=W)
        self.yearLabel = Label(self.master, text="Year:", bg="white").grid(row=0, column=1, sticky=W)
        self.subjectALabel = Label(self.master, text="Column A:", bg="white").grid(row=0, column=2, sticky=W)
        self.subjectBLabel = Label(self.master, text="Column B:", bg="white").grid(row=0, column=3, sticky=W)
        self.subjectCLabel = Label(self.master, text="Column C:", bg="white").grid(row=0, column=4, sticky=W)
        self.subjectDLabel = Label(self.master, text="Column D:", bg="white").grid(row=0, column=5, sticky=W)
        self.subjectELabel = Label(self.master, text="Column E:", bg="white").grid(row=0, column=6, sticky=W)

        self.sortAlphabeticalltLabel = Label(self.master, text=" Sort Alphabetically:", bg="white").grid(row=2, column=0, sticky=E)
        self.searchNamesLabel = Label(self.master, text=" Search Names:", bg="white").grid(row=2, column=3, sticky=W)

        #Buttons
        self.sortNamesAlphabetically = Button(self.master, text="Sort", command=self.bubbleSortListAlphabetically).grid(row=2,ipadx=5, column=1, sticky=N+W+E)
        self.logoutB = Button(self.master, text='Logout', command=self.logout).grid(row=2, column=6, sticky=E)





        self.scrollbar = Scrollbar(master)
        self.scrollbar.grid(sticky=N+E+S, column=7, row=1)

        self.listboxName = Listbox(master, yscrollcommand=self.scrollbar.set, font=("Helvetica", 7))
        self.listboxName.grid(sticky=N+E+S+W, column=0, row=1)

        self.listboxYear = Listbox(master, width=10, yscrollcommand=self.scrollbar.set, font=("Helvetica",7))
        self.listboxYear.grid(sticky=N+E+S+W, column=1, row=1)

        self.listboxSubjectA = Listbox(master, width=37, yscrollcommand=self.scrollbar.set, font=("Helvetica", 7))
        self.listboxSubjectA.grid(sticky=N+E+S+W, column=2, row=1)

        self.listboxSubjectB = Listbox(master, width=37, yscrollcommand=self.scrollbar.set, font=("Helvetica", 7))
        self.listboxSubjectB.grid(sticky=N+E+S+W, column=3, row=1)

        self.listboxSubjectC = Listbox(master, width=37, yscrollcommand=self.scrollbar.set, font=("Helvetica", 7))
        self.listboxSubjectC.grid(sticky=N+E+S+W, column=4, row=1)

        self.listboxSubjectD = Listbox(master, width=37, yscrollcommand=self.scrollbar.set, font=("Helvetica", 7))
        self.listboxSubjectD.grid(sticky=N+E+S+W, column=5, row=1)

        self.listboxSubjectE = Listbox(master, width=37, yscrollcommand=self.scrollbar.set, font=("Helvetica", 7))
        self.listboxSubjectE.grid(sticky=N+E+S+W, column=6, row=1)


        #Search bar
        self.searchBarVariable = StringVar()
        self.searchBarVariable.trace("w", lambda name, index, mode: self.update_list())
        self.searchBarEntry = Entry(master, textvariable=self.searchBarVariable, width=16).grid(row=2, column=3, sticky=E)




        #Keybinds
        self.listboxYear.bind("<MouseWheel>", self.mouseWheel)
        self.listboxName.bind("<MouseWheel>", self.mouseWheel)
        self.listboxSubjectA.bind("<MouseWheel>", self.mouseWheel)
        self.listboxSubjectB.bind("<MouseWheel>", self.mouseWheel)
        self.listboxSubjectC.bind("<MouseWheel>", self.mouseWheel)
        self.listboxSubjectD.bind("<MouseWheel>", self.mouseWheel)
        self.listboxSubjectE.bind("<MouseWheel>", self.mouseWheel)

        self.listboxYear.bind("<Up>", self.upArrowKey)
        self.listboxName.bind("<Up>", self.upArrowKey)
        self.listboxSubjectA.bind("<Up>", self.upArrowKey)
        self.listboxSubjectB.bind("<Up>", self.upArrowKey)
        self.listboxSubjectC.bind("<Up>", self.upArrowKey)
        self.listboxSubjectD.bind("<Up>", self.upArrowKey)
        self.listboxSubjectE.bind("<Up>", self.upArrowKey)

        self.listboxYear.bind("<Down>", self.downArrowKey)
        self.listboxName.bind("<Down>", self.downArrowKey)
        self.listboxSubjectA.bind("<Down>", self.downArrowKey)
        self.listboxSubjectB.bind("<Down>", self.downArrowKey)
        self.listboxSubjectC.bind("<Down>", self.downArrowKey)
        self.listboxSubjectD.bind("<Down>", self.downArrowKey)
        self.listboxSubjectE.bind("<Down>", self.downArrowKey)





        #This populates the list box with text.
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
        c = conn.cursor()

        #prepare SQL query to get all details
        countUsers = ("SELECT COUNT(*) FROM `users` WHERE `permissions`=0")
        getAllUsersInfo = ("SELECT * FROM `users` WHERE permissions=0")

        #Fetch the data
        c.execute(countUsers)

        resultsNumOfUsers = c.fetchall()
        for rowNum in resultsNumOfUsers:
            self.numOfUsers = rowNum[0]

        print("There are:" ,self.numOfUsers)


        self.name = {}
        self.year = {}
        self.choiceID = {}

        for i in range(self.numOfUsers):
            c.execute(getAllUsersInfo)
            results = c.fetchall()[i]
            print(results)

            self.name[i] = results[3]
            self.year[i] = results[4]
            self.choiceID[i] = results[5]

        conn.close()

        self.usersChoiceID = {}
        self.subjectNameAndLevelA = {}
        self.subjectNameAndLevelB = {}
        self.subjectNameAndLevelC = {}
        self.subjectNameAndLevelD = {}
        self.subjectNameAndLevelE = {}
        self.subjectChosenAttributes = [self.subjectNameAndLevelA, self.subjectNameAndLevelB, self.subjectNameAndLevelC,
                                        self.subjectNameAndLevelD, self.subjectNameAndLevelE]



        for j in range(self.numOfUsers):
            for i in range(5):
                self.usersChoiceID[i] = ""

                conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
                c = conn.cursor()

                retrieveSubjectIDQuery = ("SELECT * FROM `userssubjectchoice` WHERE choiceID="+ str(self.choiceID[j]) +"")
                print('Execeuting this query into database: "', retrieveSubjectIDQuery, '"')
                c.execute(retrieveSubjectIDQuery)

                results = c.fetchall()
                for row in results:
                    if row[i+1] == 0:
                        row[i+1] = ""
                    self.usersChoiceID[i] = row[i+1]
                    print("User ChoiceID", self.usersChoiceID[i])

                conn.close()

                if self.usersChoiceID[i] == "":
                    print("No subjectID found so no subject chosen yet in column.")
                    self.subjectChosenAttributes[i][j] = "N/A"

                else:
                    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')
                    c = conn.cursor()

                    retrieveSubjectNameAndLevelQuery = ("SELECT * FROM `subjects` WHERE subjectID='"+ self.usersChoiceID[i] +"'")
                    print('Execeuting this query into database: "', retrieveSubjectNameAndLevelQuery, '"')
                    c.execute(retrieveSubjectNameAndLevelQuery)

                    results = c.fetchall()
                    for row in results:
                        tempSubjectName = row[1]
                        tempSubjectLevel = row[2]
                        self.subjectChosenAttributes[i][j] = (""+tempSubjectName+" at "+tempSubjectLevel+"")
                        print(self.subjectChosenAttributes[i][j])


                    conn.close()

        for i in range(self.numOfUsers):
            self.listboxName.insert(END, self.name[i])
            self.listboxYear.insert(END, self.year[i])
            self.listboxSubjectA.insert(END, self.subjectChosenAttributes[0][i])
            self.listboxSubjectB.insert(END, self.subjectChosenAttributes[1][i])
            self.listboxSubjectC.insert(END, self.subjectChosenAttributes[2][i])
            self.listboxSubjectD.insert(END, self.subjectChosenAttributes[3][i])
            self.listboxSubjectE.insert(END, self.subjectChosenAttributes[4][i])




        self.scrollbar.config(command=self.onScrollbar)
        # Function for updating the list/doing the search.
        # It needs to be called at the end to dynamically populate the listbox.
        self.update_list()


    def logout(self):
            self.exitProgram()
            loginWindow()


    def update_list(self):

        #Used with the search bar
        search_term = self.searchBarVariable.get()

        (tempNamelist, tempYearlist, tempSubAlist, tempSubBlist,
        tempSubClist, tempSubDlist, tempSubElist) = ([],[],[],[],[],[],[])
        #Populating temp lists due to technicallities of language
        for i in range(self.numOfUsers):
            tempNamelist.append(self.name[i])
            tempYearlist.append(self.year[i])
            tempSubAlist.append(self.subjectChosenAttributes[0][i])
            tempSubBlist.append(self.subjectChosenAttributes[1][i])
            tempSubClist.append(self.subjectChosenAttributes[2][i])
            tempSubDlist.append(self.subjectChosenAttributes[3][i])
            tempSubElist.append(self.subjectChosenAttributes[4][i])



        self.listboxName.delete(0, END)
        self.listboxYear.delete(0, END)
        self.listboxSubjectA.delete(0, END)
        self.listboxSubjectB.delete(0, END)
        self.listboxSubjectC.delete(0, END)
        self.listboxSubjectD.delete(0, END)
        self.listboxSubjectE.delete(0, END)


        for item in tempNamelist:
            if search_term.lower() in item.lower():
                print(item)
                self.listboxName.insert(END, item)
                for i in range(self.numOfUsers):
                    if item == self.name[i]:
                        self.listboxYear.insert(END, self.year[i])
                        self.listboxSubjectA.insert(END, self.subjectChosenAttributes[0][i])
                        self.listboxSubjectB.insert(END, self.subjectChosenAttributes[1][i])
                        self.listboxSubjectC.insert(END, self.subjectChosenAttributes[2][i])
                        self.listboxSubjectD.insert(END, self.subjectChosenAttributes[3][i])
                        self.listboxSubjectE.insert(END, self.subjectChosenAttributes[4][i])




    def bubbleSortListAlphabetically(self):
        #This is the bubble sort for sorting the names in alphabetical order.
        for i in range(self.numOfUsers):
            for j in range(self.numOfUsers-1):
                if self.name[j] > self.name[j+1]:
                    self.name[j], self.name[j+1] = self.name[j+1], self.name[j]
                    self.year[j], self.year[j+1] = self.year[j+1], self.year[j]
                    self.subjectChosenAttributes[0][j], self.subjectChosenAttributes[0][j+1] = self.subjectChosenAttributes[0][j+1], self.subjectChosenAttributes[0][j]
                    self.subjectChosenAttributes[1][j], self.subjectChosenAttributes[1][j+1] = self.subjectChosenAttributes[1][j+1], self.subjectChosenAttributes[1][j]
                    self.subjectChosenAttributes[2][j], self.subjectChosenAttributes[2][j+1] = self.subjectChosenAttributes[2][j+1], self.subjectChosenAttributes[2][j]
                    self.subjectChosenAttributes[3][j], self.subjectChosenAttributes[3][j+1] = self.subjectChosenAttributes[3][j+1], self.subjectChosenAttributes[3][j]
                    self.subjectChosenAttributes[4][j], self.subjectChosenAttributes[4][j+1] = self.subjectChosenAttributes[4][j+1], self.subjectChosenAttributes[4][j]

                    print(self.name)



        #This displays the sorted names
        for i in range(self.numOfUsers):
            self.listboxName.delete(i)
            self.listboxName.insert(i, self.name[i])

            self.listboxYear.delete(i)
            self.listboxYear.insert(i, self.year[i])

            self.listboxSubjectA.delete(i)
            self.listboxSubjectA.insert(i, self.subjectChosenAttributes[0][i])

            self.listboxSubjectB.delete(i)
            self.listboxSubjectB.insert(i, self.subjectChosenAttributes[1][i])

            self.listboxSubjectC.delete(i)
            self.listboxSubjectC.insert(i, self.subjectChosenAttributes[2][i])

            self.listboxSubjectD.delete(i)
            self.listboxSubjectD.insert(i, self.subjectChosenAttributes[3][i])

            self.listboxSubjectE.delete(i)
            self.listboxSubjectE.insert(i, self.subjectChosenAttributes[4][i])



    def onScrollbar(self, *args):
        """connect the yview action together"""
        self.listboxYear.yview(*args)
        self.listboxName.yview(*args)
        self.listboxSubjectA.yview(*args)
        self.listboxSubjectB.yview(*args)
        self.listboxSubjectC.yview(*args)
        self.listboxSubjectD.yview(*args)
        self.listboxSubjectE.yview(*args)


    def mouseWheel(self, event):
        self.listboxYear.yview("scroll", -(event.delta), "units")
        self.listboxName.yview("scroll", -(event.delta), "units")
        self.listboxSubjectA.yview("scroll", -(event.delta), "units")
        self.listboxSubjectB.yview("scroll", -(event.delta), "units")
        self.listboxSubjectC.yview("scroll", -(event.delta), "units")
        self.listboxSubjectD.yview("scroll", -(event.delta), "units")
        self.listboxSubjectE.yview("scroll", -(event.delta), "units")

        """This prevents default bindings from firing twice"""
        return "break"

    def upArrowKey(self, event):
        self.listboxYear.yview_scroll(-1, "units")
        self.listboxName.yview_scroll(-1, "units")
        self.listboxSubjectA.yview_scroll(-1, "units")
        self.listboxSubjectB.yview_scroll(-1, "units")
        self.listboxSubjectC.yview_scroll(-1, "units")
        self.listboxSubjectD.yview_scroll(-1, "units")
        self.listboxSubjectE.yview_scroll(-1, "units")

        """This prevents default bindings from firing twice"""
        return "break"

    def downArrowKey(self, event):
        self.listboxYear.yview_scroll(1, "units")
        self.listboxName.yview_scroll(1, "units")
        self.listboxSubjectA.yview_scroll(1, "units")
        self.listboxSubjectB.yview_scroll(1, "units")
        self.listboxSubjectC.yview_scroll(1, "units")
        self.listboxSubjectD.yview_scroll(1, "units")
        self.listboxSubjectE.yview_scroll(1, "units")

        """This prevents default bindings from firing twice"""
        return "break"




def adminWindow():
    adminWindowRoot = Tk()
    app = AdminWindow(adminWindowRoot)
    adminWindowRoot.mainloop()


def pupilsStatisticWindow():
    pupilsStatisticWindowRoot = Tk()
    app = PupilsStatisticWindow(pupilsStatisticWindowRoot)
    pupilsStatisticWindowRoot.mainloop()


def mainWindow():
    mainWindowRoot = Tk()
    app = MainWindow(mainWindowRoot)
    mainWindowRoot.mainloop()


def loginWindow():
    loginWindowRoot = Tk()
    app = LoginWindow(loginWindowRoot)
    loginWindowRoot.mainloop()


if __name__ == '__main__':
    loginWindow()
