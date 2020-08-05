#!/usr/bin/python3

from users.util import sha256
from projects.project import Project

class Collaborator():
    """Collaborator user class"""
    def __init__(self, name, email, password_plain='', password_encrypted='', id='', create_time='', last_update='', phone_no='', user_level=0, description='', education=-1, skill_dict={}):
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
        self.education = education
        self.education_text='Default'
        if self.education == 1: self.education_text='Other'
        elif self.education == 2: self.education_text='Bachelor'
        elif self.education == 3: self.education_text='Master'
        elif self.education == 4: self.education_text='PhD'
        self.skill_dict = skill_dict

    @staticmethod
    def get_all(conn):
        """Get list of all collaborators
        Param:
        conn -- database connection
        Return:
        A list of collaborator
        """
        query = "select id from collaborator ORDER BY id ASC;"
        result = conn.execute(query)
        co_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            # update: use info_2 for text education
            co_list.append(Collaborator.get_object_by_id(conn, row['id']).info_2())
        return co_list

    @staticmethod
    def get_by_id(conn, id):
        """Get a collaborator user info by his id
        Param:
        conn -- database connection
        id -- collaborator digit id
        Return:
        A collaborator user info
        """
        # query for collaborator id
        query = "select * from collaborator where ID = " + str(id) + ";"
        result = conn.execute(query)
        row = result.fetchone()
        my_col = Collaborator(row['name'], row['email'], password_encrypted=row['password'], id=row['ID'], create_time=row['create_time'], last_update=row['last_update'], phone_no=row['phone_no'], user_level=row['user_level'], description=row['description'], education=row['education'])
        # add skill dict info
        my_col.skill_dict = Collaborator.getSkills(conn, row['ID'])
        my_col_info = my_col.info()
        # remove useless information
        del my_col_info['creation_time']
        del my_col_info['last_update']
        return my_col_info

    @staticmethod
    def get_object_by_id(conn, id, applied_role=-1):
        """Get a collaborator user object by his id
        Param:
        conn -- database connection
        id -- collaborator digit id
        applied_role -- role digit id -- Optional
        Return:
        A collaborator user info
        Optional - if the user applied for specific role
        """
        # query for collaborator id
        query = "select * from collaborator where ID = " + str(id) + ";"
        result = conn.execute(query)
        row = result.fetchone()
        my_col = Collaborator(row['name'], row['email'], password_encrypted=row['password'], id=row['ID'], create_time=row['create_time'], last_update=row['last_update'], phone_no=row['phone_no'], user_level=row['user_level'], description=row['description'], education=row['education'])
        # add skill dict info
        my_col.skill_dict = Collaborator.getSkills(conn, row['ID'])
        # Optional - check if user applied for role
        if applied_role != -1:
            query_2 = "SELECT * FROM application where role_applied = " + str(applied_role) + " AND applicant = " + str(id) + " AND status = -1;"
            result = conn.execute(query_2)
            return my_col, result.rowcount
        return my_col

    def info_2(self):
        """Get a collaborator user info with education in text"""
        return {'Name': self.name, 'Email': self.email, 'collaboratorID': self.id, 'Phone_no': self.phone_no, 'User_level': self.user_level, 'Description': self.description, 'Education': self.education_text, 'Skills': self.skill_dict}

    @staticmethod
    def getSkills(conn, id):
        """Get a collaborator's skill/exp dictionary from database
        Param:
        conn -- database connection
        id -- collaborator digit id
        Return:
        skill-exp dict
        """
        skills = {}
        # query skills table by collaborator id
        query = "select skill, experience from skills where collaboratorID = " + str(id) + ";"
        result = conn.execute(query)
        if result.rowcount != 0:
            for i in range(result.rowcount):
                row = result.fetchone()
                skills[row['skill']] = row['experience']
        return skills

    @staticmethod
    def is_email_exist(conn, email):
        """Check a collaborator email exist
        Param:
        conn -- database connection
        email -- collaborator email address
        Return:
        Boolean if the email address exist
        """
        # ignore case
        email = email.lower()
        query = "select * from collaborator where email = \'" + email + "\';"
        result = conn.execute(query)
        return result.rowcount

    @staticmethod
    def login(conn, email, password_plain='', password_encrypted=''):
        """Collaborator Login
        Param:
        conn -- database connection
        email -- collaborator email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        Return:
        Collaborator info or None
        """
        # ignore case
        email = email.lower()
        query = "select * from collaborator where email = \'" + email + "\';"
        result = conn.execute(query)
        if result.rowcount == 0:
            # user email not exist
            return None
        row = result.fetchone()
        # use sha256 encrypted password to compare
        if password_encrypted == '':
            enc_pass = sha256(password_plain)
        else:
            enc_pass = password_encrypted
        if enc_pass == row['password']:
            # password match, fetch information to return
            skills = Collaborator.getSkills(conn, row['ID'])
            return Collaborator(row['name'], row['email'], password_encrypted=row['password'], id=row['ID'], create_time=row['create_time'], last_update=row['last_update'], phone_no=row['phone_no'], user_level=row['user_level'], description=row['description'], education=row['education'], skill_dict=skills).info()
        return None

    @staticmethod
    def getObject(conn, email):
        """Get collaborator object by email
        Param:
        conn -- database connection
        email -- collaborator email
        Return:
        Collaborator object or None
        """
        # ignore case
        email = email.lower()
        query = "select * from collaborator where email = \'" + email + "\';"
        result = conn.execute(query)
        if result.rowcount == 0:
            # user email not exist
            return None
        row = result.fetchone()
        skills = Collaborator.getSkills(conn, row['ID'])
        return Collaborator(row['name'], row['email'], password_encrypted=row['password'], id=row['ID'], create_time=row['create_time'], last_update=row['last_update'], phone_no=row['phone_no'], user_level=row['user_level'], description=row['description'], education=row['education'], skill_dict=skills)

    @staticmethod
    def check_password(conn, email, password_plain='', password_encrypted=''):
        """Check collaborator password correctness
        Param:
        conn -- database connection
        email -- collaborator email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        Return:
        Boolean if email match or not
        """
        # ignore case
        email = email.lower()
        query = "select * from collaborator where email = \'" + email + "\';"
        result = conn.execute(query)
        row = result.fetchone()
        # use sha256 encrypted password to compare
        if password_encrypted == '':
            enc_pass = sha256(password_plain)
        else:
            enc_pass = password_encrypted
        if enc_pass == row['password']:
            return True
        return False

    @staticmethod
    def commit_newpassword(conn, email, password_plain='', password_encrypted=''):
        """Update new password into database
        Param:
        conn -- database connection
        email -- collaborator email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        """
        # ignore case
        email = email.lower()
        if password_encrypted == '':
            new_pass = sha256(password_plain)
        else:
            new_pass = password_encrypted
        # update password in database
        query = "UPDATE collaborator set password = \'" + new_pass + "\' where email = \'" + email + "\';"
        conn.execute(query)

    @staticmethod
    def get_my_followed_projects(conn, user_ID):
        """Get collaborator's followed project list by user id
        Param:
        conn -- database connection
        user_ID -- collaborator digital id
        Return:
        List of followed project info
        """
        projects_followed = []
        # query subscription tabale
        query = f"SELECT * FROM subscription WHERE is_dreamer=0 AND c_subscriber={user_ID}"
        result = conn.execute(query)
        proj_list = []
        # fetch project information
        for i in range(result.rowcount):
            row = result.fetchone()
            proj_info = Project.get_by_proj_id(conn, row['projectID']).text_info()
            proj_info['follow'] = True
            proj_list.append(proj_info)
        return proj_list

    @staticmethod
    def get_follow_ids(conn, user_ID):
        """Get collaborator's followed project id list by user id
        Param:
        conn -- database connection
        user_ID -- collaborator digital id
        Return:
        List of followed project info
        """
        projects_followed = []
        # query subscription tabale
        query = f"SELECT * FROM subscription WHERE is_dreamer=0 AND c_subscriber={user_ID}"
        result = conn.execute(query)
        for i in range(result.rowcount):
            row = result.fetchone()
            projects_followed.append(row['projectID'])
        return projects_followed

    @staticmethod
    def get_my_projects(conn, user_ID):
        """Get collaborator's engaged project list by user id
        Param:
        conn -- database connection
        user_ID -- collaborator digital id
        Return:
        List of engaged+followed project info
        """
        projects_joined = []
        # query application table for active/finished project
        query_1 = "SELECT projectID, role_applied FROM application WHERE applicant = " + str(user_ID) + " AND (status = 1 or status = 9) ORDER BY projectID;"
        result_1 = conn.execute(query_1)
        for i in range(result_1.rowcount):
            row_1 = result_1.fetchone()
            # prepare fetch engaged project information
            if (row_1['projectID'], row_1['role_applied']) not in projects_joined:
                projects_joined.append((row_1['projectID'], row_1['role_applied']))
        # query invitation table for active/finished project
        query_2 = "SELECT projectID, role_invited FROM invitation WHERE invitee = " + str(user_ID) + " AND (status = 1 or status = 9) ORDER BY projectID;"
        result_2 = conn.execute(query_2)
        for j in range(result_2.rowcount):
            row_2 = result_2.fetchone()
            # prepare fetch engaged project information
            if (row_2['projectID'], row_2['role_invited']) not in projects_joined:
                projects_joined.append((row_2['projectID'], row_2['role_invited']))
        follow_list = Collaborator.get_my_followed_projects(conn, user_ID)
        # merge list - remove duplicate
        joined_projects = [a[0] for a in projects_joined]
        # engaged project has larger priority
        for proj in follow_list:
            if proj['id'] in joined_projects:
                follow_list.remove(proj)
        myproject_list = []
        # fetch project information with specific role
        for k in range(len(projects_joined)):
            proj = Project.get_by_pid_rid(conn, projects_joined[k][0], projects_joined[k][1])
            proj['follow'] = False
            myproject_list.append(proj)
        # final merge of project info list
        myproject_list.extend(follow_list)
        # move finished projects to bottom
        myproject_list.sort(key=lambda p:p['status'])
        return {'my_projects': myproject_list, 'amount': len(myproject_list)}

    def search_list(self, conn, description, category, order_by, order):
        """Search whole project list with matching of collaborator's info
        Param:
        conn -- database connection
        description -- search for project description
        category -- project category
        order_by -- order item
        order -- order (ASC/DESC)
        Return:
        project list based on limits
        """
        skills = self.skill_dict
        edu = self.education
        project_list = []
        # match with each skill-exp pair
        for skill, exp in skills.items():
            # query project table
            if category == -1:
                query = "SELECT project.ID as pID, project_role.ID as rID, project_title, project.last_update as last_update FROM project, project_role, role_skill WHERE project.ID = projectID AND description LIKE \'%%" + description + "%%\' AND skill = " + str(skill) + " AND experience <= " + str(exp) + " AND education <= " + str(edu) + " ORDER BY " + order_by + " " + order + ";"
            else:
                query = "SELECT project.ID as pID, project_role.ID as rID, project_title, project.last_update as last_update FROM project, project_role, role_skill WHERE project.ID = projectID AND description LIKE \'%%" + description + "%%\' AND category = " + str(category) + " AND skill = " + str(skill) + " AND experience <= " + str(exp) + " AND education <= " + str(edu) + " ORDER BY " + order_by + " " + order + ";"
            result = conn.execute(query)
            for i in range(result.rowcount):
                row = result.fetchone()
                # append info without duplicate
                proj = Project.get_by_id(conn, row['pID'])
                is_exist = False
                for project in project_list:
                    if project['id'] == proj['id']: is_exist = True
                if not is_exist:
                    project_list.append(proj)
        if len(project_list) == 0: return None
        project_list.sort(key=lambda p:p['status'])
        return {'projects': project_list, 'amount': result.rowcount}

    def projects_recommdation(self, conn):
        """Recommend projects for collaborator based on skill/exp/edu
        Param:
        conn -- database connection
        Return:
        recommendation projects and roles
        """
        skills = self.skill_dict
        edu = self.education
        project_list = []
        #strict matching
        strict_matching_count = 0
        # query on each skill/exp pair
        for skill, exp in skills.items():
            # match on role
            query = "SELECT projectID as proj_id, ID as role_id, skill FROM project_role pr, role_skill rs WHERE pr.ID = rs.roleID and skill = " + str(skill) + " AND experience = " + str(exp) + " AND education = " + str(edu) + " ORDER BY ID, projectID, skill;"
            result = conn.execute(query)
            for i in range(result.rowcount):
                row = result.fetchone()
                proj = Project.get_by_pid_rid_skill(conn, row['proj_id'], row['role_id'], row['skill'])
                is_exist = False
                # append without duplicate
                for project in project_list:
                    if project['id'] == proj['id']: is_exist = True
                if not is_exist:
                    project_list.append(proj)
                    strict_matching_count += 1
        #relaxing matching
        relaxing_matching_count = 0
        for skill, exp in skills.items():
            query = "SELECT projectID as proj_id, ID as role_id, skill FROM project_role pr, role_skill rs WHERE pr.ID = rs.roleID and skill = " + str(skill) + " AND experience <= " + str(exp - 1) + " AND education >= " + str(edu - 1) + " ORDER BY ID, projectID, skill;"
            result = conn.execute(query)
            for i in range(result.rowcount):
                row = result.fetchone()
                proj = Project.get_by_pid_rid_skill(conn, row['proj_id'], row['role_id'], row['skill'])
                is_exist = False
                for project in project_list:
                    if project['id'] == proj['id']: is_exist = True
                if not is_exist:
                    project_list.append(proj)
                    relaxing_matching_count += 1
        if len(project_list) == 0: return None
        return {'projects': project_list, 'strict matching count': strict_matching_count, 'relaxing matching count': relaxing_matching_count}

    def info(self):
        """Return collaborator info"""
        return {'role': 'Collaborator', 'name': self.name, 'email': self.email, 'id': self.id, 'creation_time': self.create_time, 'last_update': self.last_update, 'phone_no': self.phone_no, 'user_level': self.level_text, 'description': self.description, 'education': self.education_text, 'skills': self.skill_dict}

    def commit_skills(self, conn):
        """Write collaborator's skill-exp into database
        Param:
        conn -- database connection
        """
        query = "DELETE FROM skills where `collaboratorID` = " + str(self.id) + ";"
        conn.execute(query)
        for k, v in self.skill_dict.items():
            query = "INSERT INTO skills (skill, experience, collaboratorID) VALUES (" + str(k) + ", " + str(v) + ", " + str(self.id) + ");"
            conn.execute(query)

    def commit(self, conn):
        """Write collaborator information into database
        Param:
        conn -- database connection
        """
        query = "INSERT INTO collaborator (name, email, password, phone_no, education, user_level, description) VALUES (\'" + self.name.replace("'", "\\\'") + "\', \'" + self.email + "\', \'" + self.password_encrypted + "\', \'" + self.phone_no + "\', " + str(self.education) + ", " + str(self.user_level) + ", \'" + self.description.replace("'", "\\\'") + "\') ON DUPLICATE KEY UPDATE `name`= \'" + self.name.replace("'", "\\\'") + "\', `password` = \'" + self.password_encrypted + "\', `phone_no` = \'" + self.phone_no + "\', `education` = " + str(self.education) + ", `user_level` = " + str(self.user_level) + ", `description` = \'" + self.description.replace("'", "\\\'") + "\';"
        conn.execute(query)
        # register check - ID error
        if self.id == '':
            query = "select ID from collaborator where `email` = \'" + self.email + "\';"
            result = conn.execute(query)
            row = result.fetchone()
            self.id = row['ID']
        # register skills
        self.commit_skills(conn)
    
    
    def patch(self, conn):
        query = "UPDATE collaborator SET phone_no = \'" + self.phone_no + "\',education = \'" + str(self.education) + "\' WHERE ID = " + str(self.id) + ";"
        conn.execute(query)
        if self.education == 1: self.education_text='Other'
        elif self.education == 2: self.education_text='Bachelor'
        elif self.education == 3: self.education_text='Master'
        elif self.education == 4: self.education_text='PhD'
        # update skills/experience requirement
        if len(self.skill_dict) == 0:  # cannot delete requirements and put nothing there - skip if no provided
            print("skill_dict is empty")
            return self
        query = f"DELETE FROM skills where collaboratorID = {self.id};"
        conn.execute(query)
        for i,j in self.skill_dict.items():
            query = f"INSERT INTO skills (skill, experience, collaboratorID) VALUES ({str(i)}, {str(j)}, {str(self.id)});"
            print(query)
            conn.execute(query)
        return self
