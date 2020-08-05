#!/usr/bin/python3
from users.collaborator import Collaborator
from users.dreamer import Dreamer
from projects.project import Project
from projects.role import Role

class Application():
    """role application class"""
    def __init__(self, project_id, role_apply, applicant,general_text = '',status = -1):
        self.project_id = project_id
        self.role_apply = role_apply
        self.applicant = applicant
        self.general_text = general_text
        self.status = -1
        # no input warning
        self.id = -1

    @staticmethod
    def get_object_by_aid(conn, application_id):
        """get application object by id
        Param:
        conn -- database connection
        application_id -- digit id
        Return:
        application object or None
        """
        query = "SELECT * FROM application where ID = " + str(application_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            # not exist
            return None
        row = result.fetchone()
        appli = Application(row['projectID'], row['role_applied'], row['applicant'], row['general_text'], row['status'])
        appli.id = row['ID']
        return appli

    @staticmethod
    def get_by_aid(conn, application_id):
        """get application info by id
        Param:
        conn -- database connection
        application_id -- digit id
        Return:
        applicator info with some application info or None
        """
        query = "SELECT * FROM application where ID = " + str(application_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            # not exist
            return None
        row = result.fetchone()
        # use applicator info as base instead of application info
        application= Collaborator.get_by_id(conn,row['applicant'])
        if len(application) == 0: return None
        # add application info
        application['general_text'] = row['general_text']
        application['apply_status'] = row['status']
        application['application_id'] = row['ID']
        return application

    @staticmethod
    def get_by_pid_rid(conn, project_id,role_id):
        """Get applications in specific project and role
        Param:
        conn -- database connection
        project_id -- project digit id
        role_id -- role digit id
        Return:
        list of applicatior info
        """
        # query application table by specific project/role
        query = "SELECT * FROM application where projectID = " + str(project_id) + " AND role_applied = " + str(role_id) + ";"
        result = conn.execute(query)
        all_application = {}
        application_list = []
        if result.rowcount == 0:
            # no exist
            return None
        for i in range(result.rowcount):
            row = result.fetchone()
            # fetch applicator info
            application= Collaborator.get_by_id(conn,row['applicant'])
            # append application info
            application['general_text'] = row['general_text']
            application['apply_status'] = row['status']
            application['application_id'] = row['ID']
            application_list.append(application)
        if len(application_list) == 0: return None
        # into dict for better return format
        all_application['applications'] = application_list
        return all_application

    @staticmethod
    def get_by_applicant(conn, user_ID):
        """Get all applications by a collaborator
        Param:
        conn -- database connection
        user_ID -- collaborator digit id
        Return:
        list of all application info for the collaborator
        """
        # query by applicant
        query = "SELECT * FROM application where applicant = " + str(user_ID) + " order by ID desc;"
        result = conn.execute(query)
        applications = []
        for i in range(result.rowcount):
            row = result.fetchone()
            # fetch information
            if row['status'] == -1:
                application_status = 'Pending'
            if row['status'] == 0:
                application_status = 'Declined'
            if row['status'] == 1:
                application_status = 'Approved'
            if row['status'] == 9:
                application_status = 'Finished'
            appli = {'ApplicationID':row['ID'], 'projectID':row['projectID'], 'project_title': Project.get_by_id(conn, row['projectID'])['title'], 'Role_applied':row['role_applied'], 'Role_title':Role.get_by_id(conn, row['role_applied'])['title'],'Applicant':row['applicant'], 'Application_status':application_status, 'General_text':row['general_text']}
            applications.append(appli)
        return {'applications': applications, 'amount': result.rowcount}

    @staticmethod
    def approve_an_application(conn, smtp, proj_ID, role_ID, application_id):
        """Approve application by project/role/application id
        Param:
        conn -- database connection
        smtp -- smtp server object
        proj_ID -- project digit id
        role_ID -- role digit id
        application_id -- application digit id
        Return:
        Approved application info
        """
        #check the application status first, if not in pending(-1) status, return application status;
        query_pre = "select * from application where ID = " + str(application_id) + ";"
        result_pre = conn.execute(query_pre)
        row = result_pre.fetchone()
        if row['status'] != -1:
            return row['status']

        #check if all members have been recruited or not for the same project role;
        query_1 = "select count(*) as count_1 from application where projectID = " + str(proj_ID) + " and role_applied = " + str(role_ID) + " and status = 1;"
        result_1 = conn.execute(query_1)
        row_1 = result_1.fetchone()
        query_2 = "select count(*) as count_2 from invitation where projectID = " + str(proj_ID) + " and role_invited = " + str(role_ID) + " and status = 1;"
        result_2 = conn.execute(query_2)
        row_2 = result_2.fetchone()
        query_3 = "select amount from project_role where projectID = " + str(proj_ID) + " and ID = " + str(role_ID) + ";"
        result_3 = conn.execute(query_3)
        row_3 = result_3.fetchone()
        #If all collaborators recruited for the project role, return 88 as a flag;
        if row_1['count_1'] + row_2['count_2'] == row_3['amount']:
            return 88

        # update the application status as 1 - application approved;
        query = "UPDATE application set status = 1 where ID = " + str(application_id) + ";"
        conn.execute(query)
        # notify applicant for result
        appli = Application.get_object_by_aid(conn, application_id)
        appli.notify_result(conn, smtp)
        #Check if the same applicant still applied for other roles of project;
        query_0 = "select ID as aid from application where projectID = " + str(proj_ID) + " and status = -1 and applicant in (select applicant from application where ID = " + str(application_id) + ");"
        result_0 = conn.execute(query_0)
        for m in range(result_0.rowcount):
            #systme automatically decline all other applications for the same project from same applcant;
            row_0 = result_0.fetchone()
            query_0_1 = "UPDATE application set status = 0 where ID = " + str(row_0['aid']) + ";"
            conn.execute(query_0_1)
            # notify applicant for result
            Application.get_object_by_aid(conn, application_id).notify_result(conn, smtp)

        #decline all other applications/invitations for the same project if all members have been recruited; 
        if row_1['count_1'] + row_2['count_2'] + 1 == row_3['amount']:
            query_4 = "UPDATE application set status = 0 where projectID = " + str(proj_ID) + " and role_applied = " + str(role_ID) + " and status != 1;"
            conn.execute(query_4)
            # notify applicants for result
            query_4_1 = "SELECT * from application where projectID = " + str(proj_ID) + " and role_applied = " + str(role_ID) + " and status = 0;"
            result = conn.execute(query_4_1)
            for i in range(result.rowcount):
                row = result.fetchone()
                temp_app = Application(row['projectID'], row['role_applied'], row['applicant'], row['general_text'], row['status'])
                temp_app.id = row['ID']
                temp_app.notify_result(conn, smtp, accept=False)
            query_5 = "UPDATE invitation set status = 0 where projectID = " + str(proj_ID) + " and role_invited = " + str(role_ID) + " and status != 1;"
            conn.execute(query_5)
            #notify invitees for auto cancel
            query_5_1 = "SELECT * FROM invitation where projectID = " + str(proj_ID) + " and role_invited = " + str(role_ID) + " AND status = 0;"
            result = conn.execute(query_5_1)
            from projects.invitation import Invitation
            for i in range(result.rowcount):
                row = result.fetchone()
                temp_inv = Invitation(row['projectID'], row['role_invited'], row['invitor'], row['invitee'], row['general_text'], row['status'])
                temp_inv.id = row['ID']
                temp_inv.notify_invitee_auto_decline(conn, smtp)
        #return approved application;
        return Application.get_by_aid(conn, application_id)

    @staticmethod
    def decline_an_application(conn, smtp, application_id):
        """Decline a application by application id
        Param:
        conn - database connection
        smtp - smtp server object
        application_id -- application digit id
        Return:
        declined application info
        """
        # update the application status as 0 - application declined;
        query = "UPDATE application set status = 0 where ID = " + str(application_id) + ";"
        conn.execute(query)
        # notify applicant for result
        appli = Application.get_object_by_aid(conn, application_id)
        appli.notify_result(conn, smtp, accept=False)
        #return the declined application;
        return Application.get_by_aid(conn, application_id)

    def notify_owner(self, conn, smtp):
        """Notify application to project owner through email
        Param:
        conn -- database connection
        smtp -- smtp server
        Return:
        smtp send result
        """
        proj = Project.get_by_id(conn, self.project_id)
        role = Role.get_by_id(conn, self.role_apply)
        col = Collaborator.get_by_id(conn, self.applicant)
        dre = Dreamer.get_by_id(conn, proj['owner'])
        subject = '[DreamMatchmaker]You have a new project application'
        content = f'''<p>Hello {dre['name']},</p>
<p>   <b>{col['name']}</b> has applied to join your project <b>"{proj['title']}"</b> as <b>"{role['title']}"</b></p>
<p>   The following message is from the applicant:</p>
<p>      {self.general_text}<p>
<p>   You can view and accept or decline the application on the website.</p>
<p>Dream Matchmaker Team</p>
'''
        result = smtp.send_email_html(dre['email'], content, subject)
        return result

    def notify_applicant(self, conn, smtp):
        """Notify application to applicant through email
        Param:
        conn -- database connection
        smtp -- smtp server
        Return:
        smtp send result
        """
        proj = Project.get_by_id(conn, self.project_id)
        role = Role.get_by_id(conn, self.role_apply)
        col = Collaborator.get_by_id(conn, self.applicant)
        dre = Dreamer.get_by_id(conn, proj['owner'])
        subject = '[DreamMatchmaker]You have created a new project application'
        content = f'''<p>Hello {col['name']},</p>
<p>   You have applied to join project <b>"{proj['title']}"</b> as <b>"{role['title']}"</b>.</p>
<p>   The following message is leaved to project owner:</p>
<p>      {self.general_text}<p>
<p>   The project owner will view your application. The result will be notified through email.</p>
<p>Dream Matchmaker Team</p>
'''
        result = smtp.send_email_html(col['email'], content, subject)
        return result

    def notify_result(self, conn, smtp, accept=True):
        """Notify application result to applicant through email
        Param:
        conn -- database connection
        smtp -- smtp server
        accept -- application approved or not
        Return:
        smtp send result
        """
        proj = Project.get_by_id(conn, self.project_id)
        role = Role.get_by_id(conn, self.role_apply)
        col = Collaborator.get_by_id(conn, self.applicant)
        dre = Dreamer.get_by_id(conn, proj['owner'])
        subject = '[DreamMatchmaker]You have an application status update'
        if accept:
            acceptance = 'accepted'
        else:
            acceptance = 'declined'
        content = f'''<p>Hello {col['name']},</p>
<p>   Your application to join project <b>"{proj['title']}"</b> as <b>"{role['title']}"</b></p>
<p>   has been {acceptance}.</p>
<p>Dream Matchmaker Team</p>
'''
        result = smtp.send_email_html(col['email'], content, subject)
        return result

    def info(self):
        """Return application info"""
        return {'id': self.id, 'project_id': self.project_id, 'role_apply': self.role_apply, 'applicant': self.applicant, 'general_text': self.general_text}

    def duplicate_check(self, conn):
        """Check if the application is duplicate on a role
        Param:
        conn -- database connection
        Return:
        Boolean if application is duplicate
        """
        # check application table
        query = "SELECT * FROM application where projectID = " + str(self.project_id) + " AND role_applied = " + str(self.role_apply) + " AND applicant = " + str(self.applicant)  + ";"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        # check invitation table
        query = "SELECT * FROM invitation where projectID = " + str(self.project_id) + " AND role_invited = " + str(self.role_apply) + " AND invitee = " + str(self.applicant) + ";"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        return False

    def check_project_role(self,conn):
        """Check if the role is valid(exist)
        Param:
        conn -- database connection
        Return:
        Boolean if role exist
        """
        query = f"SELECT * FROM application where projectID = {self.project_id} AND applicant = {self.applicant} AND status = 1;"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        query = f"SELECT * FROM invitation where projectID = {self.project_id} AND invitee = {self.applicant} AND status = 1;"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        return False
    
    def check_project_status(self,conn):
        """Check if the project is in active status
        Param:
        conn -- database connection
        Return:
        Boolean if project is active
        """
        query = "SELECT * FROM project where ID = " + str(self.project_id) + " AND project_status = " + str(1) + ";"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        return False


    def check_amount(self,conn):
        """Check if the role has been fullfilled
        Param:
        conn -- database connection
        Return:
        Boolean if role is fullfilled
        """
        query_1 = "select count(*) as count_1 from application where projectID = " + str(
            self.project_id) + " and role_applied = " + str(self.role_apply) + " and status = 1;"
        result_1 = conn.execute(query_1)
        row_1 = result_1.fetchone()
        query_2 = "select count(*) as count_2 from invitation where projectID = " + str(
            self.project_id) + " and role_invited = " + str(self.role_apply) + " and status = 1;"
        result_2 = conn.execute(query_2)
        row_2 = result_2.fetchone()
        query_3 = "select amount from project_role where projectID = " + str(self.project_id) + " and ID = " + str(
            self.role_apply) + ";"
        result_3 = conn.execute(query_3)
        row_3 = result_3.fetchone()
        # decline all other applications/invitations for the same project if all members have been recruited;
        if row_1['count_1'] + row_2['count_2'] == row_3['amount']:
            return True
        else:
            return False

    def create(self, conn):
        """Create a new Application into database
        Param:
        conn -- database connection
        Return:
        created application object
        """
        # check all validation
        if self.check_project_role(conn):
            return None
        if self.duplicate_check(conn):
            return None
        if self.check_amount(conn):
            return {}
        if not self.check_project_status(conn):
            return {'This project is not activated':1}
        # insert into database
        query = "INSERT INTO application (projectID, role_applied, applicant, general_text) VALUES (" + str(self.project_id) + ", " + str(self.role_apply) + ", " + str(self.applicant) + ", \'" + self.general_text.replace("'", "\\\'") + "\');"
        conn.execute(query)
        query = "SELECT * FROM application where projectID = " + str(self.project_id) + " ORDER BY create_time DESC;"
        result = conn.execute(query)
        row = result.fetchone()
        self.id = row['ID']
        return self
