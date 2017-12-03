###################################################
# SE2017/student/views.py: Consists of all the valid methods of student module of SAMS-IIITS
#__authors__ = "David", "Sri Harsha","Sajas"
#__copyright__ = "Copyright 2017, SE2017 Course"
#__Team__ = ["Likhith", "David", "Sri Harsha","Sajas", "Koushik", "Rajeev"]
#__license__ = "MIT"
#__version__ = "1.2"
#__maintainer__ = "Likhith"
#__email__ = "likhith.l15@iiits.in"
#__status__ = "Development"
####################################################


from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from home.models import *


@login_required(login_url="/login/")
def dashboard(request):
    '''
    This function finds out the summary reports of attendance and Pending assignments

    '''
    user = request.user

    try:
        user = request.user
        userPersonnelObj = Personnel.objects.filter(LDAP=user)
        MyCourses = Students_Courses.objects.filter(Student_ID=userPersonnelObj[0].Person_ID)
        CourseAttendanceContext = []

        for course in MyCourses:
            AttendanceSessions = Attendance_Session.objects.filter(Course_Slot=course.Course_ID.Course_ID)
            classesPresent = 0
            totalClasses = 0
            absentDays = []
            totalClassesIncurrentMonth = 0
            totalClassesPresentInCurrentMonth = 0
            for sessions in AttendanceSessions:
                try:
                    attendanceObject = Attendance.objects.filter(Student_ID=userPersonnelObj[0].Person_ID).filter(
                        ASession_ID=sessions.Session_ID)

                    totalClasses += 1

                    if (attendanceObject[0].Marked == 'P'):
                        classesPresent += 1
                        if (datetime.datetime.now().month == attendanceObject[0].Date_time.month):
                            totalClassesIncurrentMonth += 1
                            totalClassesPresentInCurrentMonth += 1


                    elif (attendanceObject[0].Marked == 'A'):
                        absentDays.append(attendanceObject[0].Date_time)
                        if (datetime.datetime.now().month == attendanceObject[0].Date_time.month):
                            totalClassesIncurrentMonth += 1

                except:
                    pass
            if (totalClasses == 0):
                retObj = dict(course=course, totalAttendance="N.A", monthAttendance="N.A")
            elif (totalClassesIncurrentMonth == 0):
                retObj = dict(course=course, totalAttendance=(classesPresent * 100.0 / totalClasses),
                              monthAttendance="N.A")
            else:
                retObj = dict(course=course, totalAttendance=(classesPresent * 100.0 / totalClasses),
                              monthAttendance=(totalClassesPresentInCurrentMonth * 100.0 / totalClassesIncurrentMonth))
            CourseAttendanceContext.append(retObj)
        attendanceContext = dict(CourseAttendanceContext=CourseAttendanceContext)
    except:
        attendanceContext = dict(ErrorMessage="No Registered Classes")
    pendingAssignments = []
    StudentObject = Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID=course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID=assignment).filter(
                Student_ID=StudentObject[0].Person_ID)
            if (submissionsByStudent.count() == 0):
                now = timezone.now()
                if (assignment.End_Time > now):
                    assignContextObject = dict(Course=course, assignment=assignment)
                    pendingAssignments.append(assignContextObject)

    return render(request, "student/index.html",
                  dict(name=user, attendanceContext=attendanceContext, assignmentContext=pendingAssignments))



@login_required(login_url="/login/")
def viewattendance(request):
    #print("HErE")
    
        user = request.user # getting data of the username
        userPersonnelObj = Personnel.objects.filter(LDAP=user) # getting the data from the table Personnel where LDAP is the username that we got earlier

        #the userPersonnelObj contains Person_ID, LDAP, Role 
        
        MyCourses = Students_Courses.objects.filter(Student_ID=userPersonnelObj[0].Person_ID)

        #we now are taking data from Students_Courses table using the Person_ID that we got in the userPersonnelObj and putting it in MyCourses
        #MyCourses contains Student_ID, Course_ID, Reg_Date
	AttendanceSessions = Attendance_Session.objects.all()
        CourseAttendanceContext = []
        #classesPresent = 0
	#print(MyCourses)
	#for c in MyCourses:
	 #   print(c)
	i=1
        for course in MyCourses:
	    print(i)
	    #print(course)
	    #print("courses check",course.Course_ID)
	    classesPresent = 0
            #AttendanceSessions = Attendance_Session.objects.all()#filter(Course_Slot=course.Course_ID)
	    #print("enterCheck1")
            #print("check attendance sessions for ",course,AttendanceSessions)
            #We are taking data from Attendance_Session table using the course_ID that we got earlier.
            totalClasses = 0
            absentDays = []
	    
            for sessions in AttendanceSessions:
		#print (sessions, sessions.Session_ID) #looping in AttendanceSessions
	        #print("enterCheck2",sessions.Course_Slot.Course_ID.Course_Name)
		#print("course.Course_ID",course.Course_ID)
		#try:
		if str(sessions.Course_Slot.Course_ID.Course_Name) == str(course.Course_ID):
		    print(i)
		    i+=1
                    attendanceObject = Attendance.objects.filter(Student_ID=userPersonnelObj[0].Person_ID).filter(ASession_ID=sessions.Session_ID)
		    #print ("check2",attendanceObject)
                    #Select alll the data in Attendance table where Sudent_ID is the Person_ID that is available in  UserPersonnelObj and  ASession_ID is the Session_ID s that are available in AttendanceSessions
		    print(attendanceObject[0])
                    totalClasses += 1                    

                    if (attendanceObject[0].Marked == 'P'):
                        classesPresent += 1
                    elif (attendanceObject[0].Marked == 'A'):
                        absentDays.append(attendanceObject[0].Date_time)
		#else:
		    #print("passing",sessions.Course_Slot.Course_ID.Course_Name,course.Course_ID)
	   	    #pass
	    percent = 0
	    if totalClasses:	  
                percent = classesPresent*100/totalClasses     
	    retObj = dict(course=course, present=classesPresent, total=totalClasses, absentDays=absentDays, absent = totalClasses-classesPresent, percent=percent)
            CourseAttendanceContext.append(retObj)
	    #print (CourseAttendanceContext)
        context = dict(CourseAttendanceContext=CourseAttendanceContext)
    #except:
     #   context = dict(ErrorMessage="No Registered Classes")
    	#print context
    	return render(request, "student/ViewAttendance.html", context)  #rendering the attendance page from templates   

def AssgnSubStatusPending(request):
    '''
    function returns Pending Assignments list
    '''
    user = request.user
    pendingAssignments = []
    StudentObject = Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID=course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID=assignment).filter(
                Student_ID=StudentObject[0].Person_ID)
            if (submissionsByStudent.count() == 0):
                now = timezone.now()
                if (assignment.End_Time > now):
                    assignContextObject = dict(Course=course, assignment=assignment)
                    pendingAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusPending.html', dict(pendingAssignments=pendingAssignments))


def AssgnSubStatusOverdue(request):
    '''
    This function returns Overdue Assignments list
    '''
    user = request.user
    overdueAssignments = []
    StudentObject = Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID=course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID=assignment).filter(
                Student_ID=StudentObject[0].Person_ID)
            if (submissionsByStudent.count() == 0):
                now = timezone.now()
                if (assignment.End_Time < now):
                    assignContextObject = dict(Course=course, assignment=assignment)
                    overdueAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusOverdue.html', dict(overdueAssignments=overdueAssignments))


def AssgnSubStatusSubmitted(request):
    '''
    This function lists all the submitted Assignments
    '''
    user = request.user
    submittedAssignments = []
    StudentObject = Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID=course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID=assignment).filter(
                Student_ID=StudentObject[0].Person_ID)
            if (submissionsByStudent.count() != 0):
                assignContextObject = dict(Course=course, assignment=assignment, submission=submissionsByStudent)
                submittedAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusSubmitted.html', dict(submittedAssignments=submittedAssignments))


def addDropCourses(request):
    '''
    Just returns all the courses available for students to take
    '''
    user = request.user
    StudentObject = Personnel.objects.filter(LDAP=user.id)

    courses = Courses.objects.all()
    courseSelectionOption = []
    for course in courses:
        CourseByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID).filter(
            Course_ID=course.Course_ID)
        selected = True
        if CourseByStudent.count() == 0:
            selected = False
        FacultyForCourse = Instructors_Courses.objects.filter(Course_ID=course.Course_ID)
        if (FacultyForCourse.count() != 0):
            faculty = FacultyForCourse[0].Inst_ID
        else:
            faculty = "Yet To Be Decided"
        courseSelectionObj = dict(course=course, selected=selected, faculty=faculty)
        courseSelectionOption.append(courseSelectionObj)
    return render(request, 'student/CourseRegistration.html', dict(courses=courseSelectionOption))


def registerCourses(request):
    '''
    This function allows add/drop a course for a student
    '''
    print (request.POST)
    user = request.user
    StudentObject = Personnel.objects.filter(LDAP=user.id)
    courses = Courses.objects.all()
    for course in courses:
        CourseByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID).filter(
            Course_ID=course.Course_ID)
        if (request.POST.get(str(course.Course_ID)) and CourseByStudent.count() == 0):
	    registerStudent = CourseByStudent.create(Student_ID=StudentObject[0], Course_ID=course,
                                                     Reg_Date=datetime.datetime.now())
	    registerStudent.save()
	    print(registerStudent)
        elif (CourseByStudent.count() != 0 and not request.POST.get(str(course.Course_ID))):
            CourseByStudent.delete()
#	    registerStudent = CourseByStudent.create(Student_ID=StudentObject[0], Course_ID=course,
#                                                     Reg_Date=datetime.datetime.now())

    return render(request, "student/index.html", {})

@login_required(login_url="/login/")
def upcoming_events(request):
    '''
    This function lists all the events
    '''
    events= Events.objects.all()
    #events.sort(key=lambda r: r.event.Event_Date)
    return render(request, "student/events.html", {'events':events})


