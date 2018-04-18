import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='computing')

c = conn.cursor()

countNumOfSubjects = ("SELECT COUNT(*) FROM `subjects`")
c.execute(countNumOfSubjects)

results = c.fetchall()

for row in results:
    numOfSubjects = row[0]

print("There are this many number of subjects:",numOfSubjects)

subjectID = {}
subjectName = {}
subjectLevel = {}
subjectSpaces = {}
subjectColumn = {}

subjectAttributes = [subjectID, subjectName, subjectLevel, subjectSpaces, subjectColumn]

Valid = False
counter = 0

while Valid == False:

    if counter < numOfSubjects:
        getSubjectData = ("SELECT * FROM `subjects` ORDER BY subjectName ASC;")
        c.execute(getSubjectData)
        results = c.fetchall()[counter]
        for i in range(5):
            subjectAttributes[i][counter] = results[i]

        print(results)
        print("The subject",subjectName[counter],"at level", subjectLevel[counter],"in column", subjectColumn[counter],"has subject ID", subjectID[counter])
        print("There is", subjectSpaces[counter],"spaces available.")
        counter=counter+1
    else:
        Valid = True
        print("Retrieved all subjects data.")














