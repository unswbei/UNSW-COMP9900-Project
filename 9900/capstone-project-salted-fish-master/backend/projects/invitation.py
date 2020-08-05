#!/usr/bin/python3
from users.collaborator import Collaborator
from users.dreamer import Dreamer
from projects.project import Project
from projects.role import Role

class Invitation():
    """role invitation class"""
    def __init__(self, project_id, role_invite, invitor, invitee, general_text = '', status = -1):
        self.project_id = project_id
        self.role_invite = role_invite
        self.invitor = invitor
        self.invitee = invitee
        self.general_text = general_text
        self.status = -1
        # no input warning
        self.id = -1

    @staticmethod
    def get_object_by_id(conn, id):
        """get invitation object by id
        Param:
        conn -- database connection
        id -- digit id
        Return:
        invitation object or None
        """
        query = "SELECT * FROM invitation where ID = " + str(id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        my_invi = Invitation(row['projectID'], row['role_invited'], row['invitor'], row['invitee'], row['general_text'], row['status'])
        my_invi.id = row['ID']
        return my_invi

    @staticmethod
    def get_by_iid(conn, invitation_id):
        """get invitation info by id
        Param:
        conn -- database connection
        id -- digit id
        Return:
        invitation info or None
        """
        query = "SELECT * FROM invitation where ID = " + str(invitation_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        invitation = Collaborator.get_by_id(conn,row['invitee'])
        if len(invitation) == 0: return None
        invitation['general_text'] = row['general_text']
        invitation['invite_status'] = row['status']
        return invitation

    @staticmethod
    def get_by_pid_rid_iid(conn, project_id,role_id, invitation_ID):
        """get invitation info by id
        Param:
        conn -- database connection
        project_id -- project digit id
        role_id -- role digit id
        invitation_ID -- invitation digit id
        Return:
        invitation info or None
        """
        query = "SELECT * FROM invitation where projectID = " + str(project_id) + " AND role_invited = " + str(role_id) + " AND ID = " + str(invitation_ID) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        invitation = {"invitation_Id":row['ID'], "projectID":row['projectID'], "role_invited":row['role_invited'], "invitor":row['invitor'], "invitee":row['invitee'], "status":row['status'], "general_text":row['general_text']}
        return invitation

    @staticmethod
    def get_by_pid_rid(conn, project_id,role_id):
        """get invitatees info by project/role
        Param:
        conn -- database connection
        project_id -- project digit id
        role_id -- role digit id
        Return:
        list of invitatees info or None
        """
        query = "SELECT * FROM invitation where projectID = " + str(project_id) + " AND role_invited = " + str(role_id) + ";"
        result = conn.execute(query)
        invitees = []
        if result.rowcount == 0:
            return None
        for i in range(result.rowcount):
            row = result.fetchone()
            invitee = Collaborator.get_by_id(conn,row['invitee'])
            invitees.append(invitee)
        if len(invitees) == 0: return None
        return {'invitees': invitees, 'amount': result.rowcount}

    @staticmethod
    def get_by_invitee(conn, user_id):
        """Get all invitations for a collaborator's
        Param:
        conn -- database connection
        user_id -- collaborator digit id
        Return:
        list of invitations info
        """
        # IMPORTANT: Avoid corss import
        # This import cannot be moved up or it will cause infinite recursive import
        from projects.role import Role
        query = "SELECT * FROM invitation where invitee = " + str(user_id) + " order by ID desc;"
        result = conn.execute(query)
        invitations = []
        for i in range(result.rowcount):
            row = result.fetchone()
            if row['status'] == -1:
                invitation_status = 'Pending'
            if row['status'] == 0:
                invitation_status = 'Declined'
            if row['status'] == 1:
                invitation_status = 'Approved'
            if row['status'] == 9:
                invitation_status = 'Finished'
            invi = {'InvitationID':row['ID'], 'projectID':row['projectID'], 'Role_invited':row['role_invited'], 'Invitor':row['invitor'], 'Invitor_name': Dreamer.get_by_id(conn, row['invitor'])['name'], 'Invitee':row['invitee'], 'Invitation_status':invitation_status, 'General_text':row['general_text'], 'Role_information': Role.get_text_by_id(conn, row['role_invited']), 'Project_title': Project.get_by_id(conn, row['projectID'])['title']}
            invitations.append(invi)
        return {'invitations': invitations, 'amount': result.rowcount}

    @staticmethod
    def accept_an_invitation(conn, smtp, proj_ID, role_ID, invitation_id):
        """Accpet an invitation and further notify process
        Param:
        conn -- database connnection
        smtp -- smtp server object
        proj_ID -- project digit id
        role_ID -- role digit id
        invitation_id -- invitation digit id
        Return:
        Accpted invitation
        """
        #check the invitation status first, if not in pending(-1) status, return invitation status;
        query_pre = "select * from invitation where ID = " + str(invitation_id) + ";"
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

        # update the invitation status as 1 -  accepte the invitaiton;
        query = "UPDATE invitation set status = 1 where ID = " + str(invitation_id) + " and projectID = " + str(proj_ID) + " and role_invited = " + str(role_ID) + ";"
        conn.execute(query)
        Invitation.get_object_by_id(conn, invitation_id).notify_invitor(conn, smtp)
        #Check if more than one invitations sented for other roles of the same project;
        query_0 = "select ID as iid from invitation where projectID = " + str(proj_ID) + " and status = -1 and invitee in (select invitee from invitation where ID = " + str(invitation_id) + ");"
        result_0 = conn.execute(query_0)
        for m in range(result_0.rowcount):
            #system automatically decline all other invitations for the same project once you accept one of them;
            row_0 = result_0.fetchone()
            query_0_1 = "UPDATE invitation set status = 0 where ID = " + str(row_0['iid']) + ";"
            conn.execute(query_0_1)
            # notify both invitee and invitor about the automatically declined invitation 
            Invitation.get_object_by_id(conn, row_0['iid']).notify_invitee(conn, smtp)
            Invitation.get_object_by_id(conn, row_0['iid']).notify_invitor(conn, smtp)

        #decline all other applications/invitation for the same project role if all members have been recruited; 
        if row_1['count_1'] + row_2['count_2'] + 1 == row_3['amount']:
            query_4 = "UPDATE application set status = 0 where projectID = " + str(proj_ID) + " and role_applied = " + str(role_ID) + " and status != 1;"
            conn.execute(query_4)
            # notify applicants for result
            query_4_1 = "SELECT * from application where projectID = " + str(proj_ID) + " and role_applied = " + str(role_ID) + " and status = 0;"
            result = conn.execute(query_4_1)
            from projects.application import Application
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
            for i in range(result.rowcount):
                row = result.fetchone()
                temp_inv = Invitation(row['projectID'], row['role_invited'], row['invitor'], row['invitee'], row['general_text'], row['status'])
                temp_inv.id = row['ID']
                temp_inv.notify_invitee_auto_decline(conn, smtp)
        #return the accepted invitation;
        return Invitation.get_by_iid(conn, invitation_id)

    @staticmethod
    def decline_an_invitation(conn, smtp, proj_ID, role_ID, invitation_id):
        """Decline an invitation and further notify process
        Param:
        conn -- database connnection
        smtp -- smtp server object
        proj_ID -- project digit id
        role_ID -- role digit id
        invitation_id -- invitation digit id
        Return:
        Declined invitation
        """
        # update the invitation status as 0 -  decline the invitaiton;
        query_1 = "UPDATE invitation set status = 0 where ID = " + str(invitation_id) + " and projectID = " + str(proj_ID) + " and role_invited = " + str(role_ID) + ";"
        conn.execute(query_1)
        #return the declined invitation;
        Invitation.get_object_by_id(conn, invitation_id).notify_invitor(conn, smtp, accept=False)
        return Invitation.get_by_iid(conn, invitation_id)

    def notify_invitee(self, conn, smtp):
        """Send an email to invitee for notification
        Param:
        conn -- database connection
        smtp -- smtp server object
        Return:
        Smtp send result
        """
        proj = Project.get_by_id(conn, self.project_id)
        role = Role.get_by_id(conn, self.role_invite)
        col = Collaborator.get_by_id(conn, self.invitee)
        dre = Dreamer.get_by_id(conn, self.invitor)
        subject = '[DreamMatchmaker]You have a new project invitation'
        content = f'''<p>Hello {col['name']},</p>
<p>   <b>{dre['name']}</b> has invited you to join project <b>"{proj['title']}"</b> as <b>"{role['title']}"</b>.</p>
<p>   The following message is from the invitor:</p>
<p>      {self.general_text}<p>
<p>   You can view the invitation in your dashboard.</p>
<p>Dream Matchmaker Team</p>
'''
        result = smtp.send_email_html(col['email'], content, subject)
        return result

    def notify_invitor(self, conn, smtp, accept=True):
        """Send an email to invitor for notification
        Param:
        conn -- database connection
        smtp -- smtp server object
        accept -- boolean if invitation is accepted
        Return:
        Smtp send result
        """
        proj = Project.get_by_id(conn, self.project_id)
        role = Role.get_by_id(conn, self.role_invite)
        col = Collaborator.get_by_id(conn, self.invitee)
        dre = Dreamer.get_by_id(conn, self.invitor)
        subject = '[DreamMatchmaker]You have a invitation status update'
        if accept:
            acceptance = 'accepted'
        else:
            acceptance = 'declined'
        content = f'''<p>Hello {dre['name']},</p>
<p>   Your invitation to <b>{col['name']}</b> for project <b>"{proj['title']}"</b>, role <b>"{role['title']}"</b></p>
<p>   has been <b>{acceptance}</b>.</p>
<p>Dream Matchmaker Team</p>
'''
        result = smtp.send_email_html(dre['email'], content, subject)
        return result

    def notify_invitee_auto_decline(self, conn, smtp):
        """Send an email to invitees for auto decline notification
        Param:
        conn -- database connection
        smtp -- smtp server object
        Return:
        Smtp send result
        """
        proj = Project.get_by_id(conn, self.project_id)
        role = Role.get_by_id(conn, self.role_invite)
        col = Collaborator.get_by_id(conn, self.invitee)
        dre = Dreamer.get_by_id(conn, self.invitor)
        subject = '[DreamMatchmaker]You have a invitation status update'
        content = f'''<p>Hello {col['name']},</p>
<p>   Your invitation from <b>{dre['name']}</b> for project <b>"{proj['title']}"</b>, role <b>"{role['title']}"</b></p>
<p>   has been automaticlly cancelled due to "Role is fullfilled".</p>
<p>Dream Matchmaker Team</p>
'''
        result = smtp.send_email_html(col['email'], content, subject)
        return result

    def info(self, conn):
        """Return invitation info
        Param:
        conn -- database connection
        Return:
        invitation info
        """
        return {'id': self.id, 'project_id': self.project_id, 'role_invite': self.role_invite, 'invitor': self.invitor, 'invitee': self.invitee, 'general_text': self.general_text, 'status': self.status, 'Role_information': Role.get_text_by_id(conn, self.role_invite), 'Project_title': Project.get_by_id(conn, self.project_id)['title']}

    def duplicate_check(self, conn):
        """Check if the invitation is duplicate
        Param:
        conn -- database connection
        Return:
        Boolean if invitation is duplicate
        """
        query = "SELECT * FROM invitation where projectID = " + str(self.project_id) + " AND role_invited = " + str(self.role_invite) + " AND invitee = " + str(self.invitee)  + ";"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        query = "SELECT * FROM application where projectID = " + str(self.project_id) + " AND role_applied = " + str(self.role_invite) + " AND applicant = " + str(self.invitee)  + ";"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        return False

    def check_project_role(self,conn):
        """Check if the project role is valid
        Param:
        conn -- database connection
        Return:
        Boolean if role is valid
        """
        query = "SELECT * FROM project_role where projectID = " + str(self.project_id) + " AND ID = " + str(self.role_invite) + " ;"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        return False

    def create(self, conn):
        """Create a new Invitation into database
        Param:
        conn -- database connection
        Return:
        created invitation object
        """
        # check if all valid
        if not self.check_project_role(conn):
            return None
        if self.duplicate_check(conn):
            return None
        # store in database
        query = "INSERT INTO invitation (projectID, role_invited, invitor, invitee, general_text) VALUES (" + str(self.project_id) + ", " + str(self.role_invite) + ", " + str(self.invitor) + ", " + str(self.invitee) +  ", \'" + self.general_text.replace("'", "\\\'") + "\');"
        conn.execute(query)
        query = "SELECT * FROM invitation where projectID = " + str(self.project_id) + " ORDER BY create_time DESC;"
        result = conn.execute(query)
        row = result.fetchone()
        self.id = row['ID']
        return self
