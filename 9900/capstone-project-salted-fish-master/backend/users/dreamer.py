#!/usr/bin/python3

from users.util import sha256
from projects.project import Project
from users.collaborator import Collaborator

class Dreamer():
    """Dreamer user class"""
    def __init__(self, name, email, password_plain='', password_encrypted='', id='', create_time='', last_update='', phone_no='', user_level=0, description=''):
        self.name = name
        self.email = email.lower()
        if password_encrypted == '':
            self.password_encrypted = sha256(password_plain)
        else:
            self.password_encrypted = password_encrypted
        self.id = id
        self.phone_no = phone_no
        self.user_level = user_level
        self.description = description
        self.create_time = create_time
        self.last_update = last_update
        self.level_text='Entry'
        if self.user_level == 4: self.level_text='Expert'
        elif self.user_level == 3: self.level_text='Professional'
        elif self.user_level == 2: self.level_text='Senior'
        elif self.user_level == 1: self.level_text='Medium'

    @staticmethod
    def login(conn, email, password_plain='', password_encrypted=''):
        """Dreamer login function
        Param:
        conn -- database connection
        email -- collaborator email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        Return:
        Dreamer info or None
        """
        # ignore case
        email = email.lower()
        query = "select * from dreamer where email = \'" + email + "\';"
        result = conn.execute(query)
        if result.rowcount == 0:
            # not exist
            return None
        row = result.fetchone()
        # use sha256 encrypted password to compare
        if password_encrypted == '':
            enc_pass = sha256(password_plain)
        else:
            enc_pass = password_encrypted
        if enc_pass == row['password']:
            return Dreamer(row['name'], row['email'], password_encrypted=row['password'], id=row['ID'], create_time=row['create_time'], last_update=row['last_update'], phone_no=row['phone_no'], user_level=row['user_level'], description=row['description']).info()
        return None

    @staticmethod
    def get_followed_projects(conn, id):
        """Get projects user followed by user id
        Param:
        conn -- database connection
        id -- dreamer digital id
        Return:
        followed project info list
        """
        # query subscription table
        query = f"SELECT * FROM subscription WHERE is_dreamer=1 AND d_subscriber={id};"
        result = conn.execute(query)
        project_list = []
        for i in range(result.rowcount):
            # fetch project information
            row = result.fetchone()
            pid = row['projectID']
            proj_info = Project.get_by_id(conn, pid)
            proj_info['follow'] = True
            project_list.append(proj_info)
        return project_list

    @staticmethod
    def get_follow_ids(conn, user_ID):
        """Get dreamer's followed project id list by user id
        Param:
        conn -- database connection
        user_ID -- collaborator digital id
        Return:
        List of followed project info
        """
        projects_followed = []
        # query subscription tabale
        query = f"SELECT * FROM subscription WHERE is_dreamer=1 AND d_subscriber={user_ID}"
        result = conn.execute(query)
        for i in range(result.rowcount):
            row = result.fetchone()
            projects_followed.append(row['projectID'])
        return projects_followed

    @staticmethod
    def is_email_exist(conn, email):
        """Check if a email exist in dreamers
        Param:
        conn -- database connection
        email -- user email address
        Return:
        Boolean if email exist
        """
        # ignore case
        email = email.lower()
        query = "select * from dreamer where email = \'" + email + "\';"
        result = conn.execute(query)
        return result.rowcount

    @staticmethod
    def getObject(conn, email):
        """Get dreamer object by email
        Param:
        conn -- database connection
        email -- user email address
        Return:
        Dreamer object or None
        """
        # ignore case
        email = email.lower()
        query = "select * from dreamer where email = \'" + email + "\';"
        result = conn.execute(query)
        if result.rowcount == 0:
            # not exist
            return None
        row = result.fetchone()
        return Dreamer(row['name'], row['email'], password_encrypted=row['password'], id=row['ID'], create_time=row['create_time'], last_update=row['last_update'], phone_no=row['phone_no'], user_level=row['user_level'], description=row['description'])

    @staticmethod
    def get_by_id(conn, id):
        """Get dreamer info by id
        Param:
        conn -- database connection
        id -- draemer digital id
        Return:
        Dreamer info or None
        """
        query = "select * from dreamer where ID = " + str(int(id)) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            # not exist
            return None
        row = result.fetchone()
        return Dreamer(row['name'], row['email'], password_encrypted=row['password'], id=row['ID'], create_time=row['create_time'], last_update=row['last_update'], phone_no=row['phone_no'], user_level=row['user_level'], description=row['description']).info()

    def collaborators_recommdation(self, conn):
        """Recommend collaborators for dreamer owned projects' roles
        Param:
        conn -- database connection
        Return:
        collaborators list by recommendation project/role
        """
        owner = self.id
        #fetch all project owned by dreamer;
        query_1 = "SELECT ID as proj_ID, project_title, description, category, dreamerID, project_status, is_hidden, hidden_reason, is_modified_after_hidden FROM project WHERE dreamerID = " + str(owner) + " and project_status = 1 ORDER BY ID;"
        result_1 = conn.execute(query_1)
        if result_1.rowcount == 0:
            return None
        project_role_recomm_collabors_list = []
        for i in range(result_1.rowcount):
            row_1 = result_1.fetchone()
            #fetch roles for each project;
            query_2 = "SELECT ID as role_ID, title, amount, skill, experience, education, general_enquiry FROM project_role pr, role_skill rs WHERE pr.ID = rs.roleID and projectID = " + str(row_1['proj_ID']) + " ORDER BY ID, skill;"
            result_2 = conn.execute(query_2)
            if result_2.rowcount == 0:
                continue
            #macthing collabors based on the requirements of each role;
            else:
                role_recomm_collabors_list = []
                for j in range(result_2.rowcount):
                    row_2 = result_2.fetchone()
                    collaborator_list = [] 
                    strict_matching_count = 0
                    relaxing_matching_count = 0
                    #1.strict matching
                    query_3 = "select collaborator.ID as ID, name, email, phone_no, education, skill, experience, user_level, description from collaborator, skills where collaborator.ID = skills.collaboratorID and skill = " + str(row_2['skill']) + " and experience = " + str(row_2['experience']) + " and education = " + str(row_2['education']) + " ORDER BY ID;"
                    result_3 = conn.execute(query_3)
                    if result_3.rowcount != 0:
                        for k in range(result_3.rowcount):
                            row_3 = result_3.fetchone()
                            collabor = {'CollaboratorID':row_3['ID'],'Name':row_3['name'],'Email':row_3['email'],'Phone_no':row_3['phone_no'],'Skill':row_3['skill'],'Experience':row_3['experience'],'Education':row_3['education'],'User_level':row_3['user_level'],'Description':row_3['description']}
                            collaborator_list.append(collabor)
                            strict_matching_count += 1
                    #2.relaxing matching
                    query_4 = "select collaborator.ID as ID, name, email, phone_no, education, skill, experience, user_level, description from collaborator, skills where collaborator.ID = skills.collaboratorID and skill = " + str(row_2['skill']) + " and experience >= " + str(row_2['experience'] - 1) + " and education >= " + str(row_2['education'] - 1) + " ORDER BY ID;"
                    result_4 = conn.execute(query_4)
                    if result_4.rowcount != 0:
                        for l in range(result_4.rowcount):
                            row_4 = result_4.fetchone()
                            collabor = {'CollaboratorID':row_4['ID'],'Name':row_4['name'],'Email':row_4['email'],'Phone_no':row_4['phone_no'],'Skill':row_4['skill'],'Experience':row_4['experience'],'Education':row_4['education'],'User_level':row_4['user_level'],'Description':row_4['description']}
                            if collabor not in collaborator_list:
                                collaborator_list.append(collabor)
                                relaxing_matching_count += 1
                    #role info + recommendation collabor list
                    role_recomm_collabors = {'Role_ID':row_2['role_ID'], 'Title':row_2['title'], 'Amount':row_2['amount'], 'Skill':row_2['skill'], 'Experience':row_2['experience'], 'Education':row_2['education'], 'General_enquiry':row_2['general_enquiry'],'Strict_matching_count':strict_matching_count, 'Relaxing_matching_count':relaxing_matching_count, 'Collaborator_list':collaborator_list}
                    role_recomm_collabors_list.append(role_recomm_collabors)
            #project info + role info + recommendation collabor list
            project_role_recomm_collabors = {'Project_ID':row_1['proj_ID'], 'Project_title':row_1['project_title'], 'Description':row_1['description'], 'Category':row_1['category'], 'DreamerID':row_1['dreamerID'], 'Project_status':row_1['project_status'], 'Is_hidden':row_1['is_hidden'], 'Hidden_reason':row_1['hidden_reason'], 'Is_modified_after_hidden':row_1['is_modified_after_hidden'], 'Role_recomm_collabors_list':role_recomm_collabors_list}
            project_role_recomm_collabors_list.append(project_role_recomm_collabors)
        if len(project_role_recomm_collabors_list) == 0: return None
        return project_role_recomm_collabors_list

    @staticmethod
    def check_password(conn, email, password_plain='', password_encrypted=''):
        """Check if the password of dreamer is correct
        Param:
        conn -- database connection
        email -- dreamer email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        Return:
        Boolean if password is correct
        """
        email = email.lower()
        query = "select * from dreamer where email = \'" + email + "\';"
        result = conn.execute(query)
        row = result.fetchone()
        if password_encrypted == '':
            enc_pass = sha256(password_plain)
        else:
            enc_pass = password_encrypted
        if enc_pass == row['password']:
            return True
        return False
    
    @staticmethod
    def commit_newpassword(conn, email, password_plain='', password_encrypted=''):
        """Commit new password into database
        Param:
        conn -- database connection
        email -- dreamer email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        """
        email = email.lower()
        if password_encrypted == '':
            new_pass = sha256(password_plain)
        else:
            new_pass = password_encrypted
        query = "UPDATE dreamer set password = \'" + new_pass + "\' where email = \'" + email + "\';"
        conn.execute(query)
    

    def info(self):
        """Return dreamer info"""
        return {'role': 'Dreamer', 'name': self.name, 'email': self.email, 'id': self.id, 'creation_time': str(self.create_time), 'last_update': str(self.last_update), 'phone_no': self.phone_no, 'user_level': self.level_text, 'description': self.description}


    def commit(self, conn):
        """Commit dreamer info into database"""
        query = "INSERT INTO dreamer (name, email, password, phone_no, user_level, description) VALUES (\'" + self.name.replace("'", "\\\'") + "\', \'" + self.email + "\', \'" + self.password_encrypted + "\', \'" + self.phone_no.replace("'", "\\\'") + "\', " + str(self.user_level) + ", \'" + self.description.replace("'", "\\\'") + "\') ON DUPLICATE KEY UPDATE `name`= \'" + self.name.replace("'", "\\\'") + "\', `password` = \'" + self.password_encrypted + "\', `phone_no` = \'" + self.phone_no.replace("'", "\\\'") + "\', `user_level` = " + str(self.user_level) + ", `description` = \'" + self.description.replace("'", "\\\'") + "\';"
        conn.execute(query)
