#!/usr/bin/python3
from projects.role import Role

class Project():
    """Project class"""
    category_list = ['Null', 'Other', 'Web', 'Desktop', 'Mobile', 'Library', 'Mod', 'Research']

    def __init__(self, title, description, owner, category, status=-1, hidden=0, hidden_reason=''):
        self.title = title
        self.description = description
        self.owner = owner
        self.category = category
        self.project_status = status
        self.is_hidden = hidden
        self.hidden_reason = hidden_reason
        # no input warning
        self.id = -1
        self.is_modified_after_hidden = 0
        self.roles = [] # role info instead of Role object in json format

    @staticmethod
    #For all users even visitors can use this query function;
    #General search for projects by project description or category;
    def search_list(conn, description, category, order_by, order):
        """Search project list by limits
        Param:
        conn -- database connection
        description -- search description
        category -- search project category
        order_by -- search order item
        order -- search order
        Return:
        Matched project list
        """
        if description != '' and category != -1:
            query = "SELECT * FROM project WHERE description LIKE \'%%" + description + "%%\' AND category = " + str(category) + " AND project_status > 0 ORDER BY " + order_by + " " + order + ";"
        elif description != '':
            query = "SELECT * FROM project WHERE description LIKE \'%%" + description + "%%\' AND project_status > 0 ORDER BY " + order_by + " " + order + ";"
        elif category != -1:
            query = "SELECT * FROM project WHERE category = " + str(category) + " AND project_status > 0 ORDER BY " + order_by + " " + order + ";"
        else:
            query = "SELECT * FROM project WHERE project_status > 0 ORDER BY " + order_by + " " + order + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        project_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
            proj.id = row['ID']
            proj.is_modified_after_hidden = row['is_modified_after_hidden']
            proj.roles = Role.get_by_proj_id(conn, proj.id)
            proj.create_time = row['create_time']
            proj.last_update = row['last_update']
            project_list.append(proj.info())
        project_list.sort(key=lambda p:p['status'])
        return {'projects': project_list, 'amount': result.rowcount}

    @staticmethod
    def check_finish(conn, proj_id):
        """Check if the project has been finished
        Param:
        conn -- database connection
        proj_id -- project digit id
        Return:
        Boolean if project is finished
        """
        proj_info = Project.get_by_id(conn, proj_id)
        return proj_info['status'] == 9

    @staticmethod
    def get_object_by_id(conn, proj_id):
        """Get project info by project id
        Param:
        conn -- database connection
        proj_id -- project digit id
        Return:
        Project info
        """
        query = "SELECT * FROM project WHERE ID = " + str(proj_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
        proj.id = row['ID']
        proj.is_modified_after_hidden = row['is_modified_after_hidden']
        proj.roles = Role.get_by_proj_id(conn, proj_id)
        proj.create_time = row['create_time']
        proj.last_update = row['last_update']
        return proj

    @staticmethod
    def get_by_id(conn, proj_id):
        """Get project info by project id
        Param:
        conn -- database connection
        proj_id -- project digit id
        Return:
        Project info
        """
        return Project.get_object_by_id(conn, proj_id).info()

    @staticmethod
    def get_by_proj_id(conn, proj_id):
        """Get another format of project info by project id
        Param:
        conn -- database connection
        proj_id -- project digit id
        Return:
        Project info
        """
        query = "SELECT * FROM project WHERE ID = " + str(proj_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
        proj.id = row['ID']
        proj.is_modified_after_hidden = row['is_modified_after_hidden']
        proj.roles = Role.get_text_by_pid(conn, proj_id)
        proj.create_time = row['create_time']
        proj.last_update = row['last_update']
        return proj

    @staticmethod
    def get_by_pid_rid(conn, proj_id, role_id):
        """Get another format of project info by project id and specific role
        Param:
        conn -- database connection
        proj_id -- project digit id
        role_id -- role digit id
        Return:
        Project text info
        """
        query = "SELECT * FROM project WHERE ID = " + str(proj_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
        proj.id = row['ID']
        proj.is_modified_after_hidden = row['is_modified_after_hidden']
        proj.roles = Role.get_text_by_id(conn, role_id)
        proj.create_time = row['create_time']
        proj.last_update = row['last_update']
        return proj.text_info()

    @staticmethod
    def get_by_pid_rid_skill(conn, proj_id, role_id, skill):
        """Get another format of project info by project id and specific role with specific skill
        Param:
        conn -- database connection
        proj_id -- project digit id
        role_id -- role digit id
        skill -- skill digit id
        Return:
        Project text info
        """
        query = "SELECT * FROM project WHERE ID = " + str(proj_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
        proj.id = row['ID']
        proj.is_modified_after_hidden = row['is_modified_after_hidden']
        proj.roles = Role.get_text_by_id(conn, role_id)
        proj.create_time = row['create_time']
        proj.last_update = row['last_update']
        return proj.info()

    @staticmethod
    #Get a project by project_title;
    def get_by_title(conn, project_title):
        """Get project info by project title
        Param:
        conn -- database connection
        proj_title -- title text
        Return:
        Project info
        """
        query = "SELECT * FROM project WHERE project_title = " + project_title.replace("'", "\\\'") + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
        proj.id = row['ID']
        proj.is_modified_after_hidden = row['is_modified_after_hidden']
        proj.roles = Role.get_by_proj_id(conn, proj.id)
        proj.create_time = row['create_time']
        proj.last_update = row['last_update']
        return proj.info()

    @staticmethod
    #Get projects by project_owner_id;
    def get_by_owner(conn, owner_id):
        """Get projects info by project owner
        Param:
        conn -- database connection
        owner_id -- dreamer digit id
        Return:
        list of Project info
        """
        query = "SELECT * FROM project WHERE dreamerID = " + str(owner_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        project_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
            proj.id = row['ID']
            proj.is_modified_after_hidden = row['is_modified_after_hidden']
            proj.roles = Role.get_by_proj_id(conn, proj.id)
            proj.create_time = row['create_time']
            proj.last_update = row['last_update']
            info = proj.info()
            info['follow'] = False
            project_list.append(info)
        own_id_list = [proj['id'] for proj in project_list]
        from users.dreamer import Dreamer
        follow_list = Dreamer.get_followed_projects(conn, owner_id)
        for proj in follow_list:
            if proj['id'] in own_id_list:
                follow_list.remove(proj)
        project_list.extend(follow_list)
        # Move finished projects to tail of the list
        project_list.sort(key=lambda p:p['status'])
        return project_list

    @staticmethod
    #Update user_level field for both dreamer and collaborator table;
    def update_user_level(conn, user_type, count, user_level, user_ID):
        """update user level
        Param:
        conn -- database connection
        user_type -- user's role
        count -- num of projects finished
        user_level -- user_level digit id
        user_ID -- user digit id
        """
        if user_type == 'D':
            table_to_update = 'dreamer'
        if user_type == 'C':
            table_to_update = 'collaborator'
        if count >= 1 and count <= 3 and user_level != 0:
            query = "UPDATE " + str(table_to_update) + " set user_level = 1 where ID = " + str(user_ID) + ";"
            conn.execute(query)
        if count > 3 and count <= 5 and user_level != 1:
            query = "UPDATE " + str(table_to_update) + " set user_level = 2 where ID = " + str(user_ID) + ";"
            conn.execute(query)
        if count > 5 and count <= 8 and user_level != 2:
            query = "UPDATE " + str(table_to_update) + " set user_level = 3 where ID = " + str(user_ID) + ";"
            conn.execute(query)
        if count > 8 and count <= 15 and user_level != 3:
            query = "UPDATE " + str(table_to_update) + " set user_level = 4 where ID = " + str(user_ID) + ";"
            conn.execute(query)
        if count > 15 and user_level != 4:
            query = "UPDATE " + str(table_to_update) + " set user_level = 5 where ID = " + str(user_ID) + ";"
            conn.execute(query)

    @staticmethod
    #Caculate the total number of projects which collaborator collaborated with;
    def total_project_finished_by_collabor(conn, collabor_ID):
        """Calculate projects finished
        Param:
        conn -- database connection
        collabor_ID -- collaborator digit id
        Return:
        Total num of finished projects
        """
        query_1 = "select count(*) as count_1 from application where status = 9 and applicant = " + str(collabor_ID) + ";"
        result_1 = conn.execute(query_1)
        row_1 = result_1.fetchone()
        query_2 = "select count(*) as count_2 from invitation where status = 9 and invitee = " + str(collabor_ID) + ";"
        result_2 = conn.execute(query_2)
        row_2 = result_2.fetchone()
        return row_1['count_1'] + row_2['count_2']

    @staticmethod
    #Finish a project and further update user_level for both dreamer and collaborator based on the number of rojects they have completed;
    def finish_a_project(conn, proj_ID, dreamer_ID):
        """Finish a project
        Param:
        conn -- database connection
        proj_ID -- project digit id
        dreamer_ID -- dreamer digit id
        Return:
        updated project info
        """
        #update project_status = 9 as finished
        query_1 = "UPDATE project set project_status = 9 where dreamerID = " + str(dreamer_ID) + " and ID = " + str(proj_ID) + ";"
        conn.execute(query_1)
        #update applicant status as finish coorporation for application table
        query_2 = "UPDATE application set status = 9 where projectID = " + str(proj_ID) + ";"
        conn.execute(query_2)
        #update invitation status as finish coorporation for invitation table
        query_3 = "UPDATE invitation set status = 9 where projectID = " + str(proj_ID) + ";"
        conn.execute(query_3)

        #further update user_level for dreamer based on the statistic count;
        query_1 = "select count(*) as count from project where dreamerID = " + str(dreamer_ID) + " and project_status = 9;"
        result_1 = conn.execute(query_1)
        row_1 = result_1.fetchone()
        query_2 = "select user_level from dreamer where ID= " + str(dreamer_ID) + ";"
        result_2 = conn.execute(query_2)
        row_2 = result_2.fetchone()
        Project.update_user_level(conn, 'D', row_1['count'], row_2['user_level'], dreamer_ID)

        #further update user_level for all collaborators of this project based on the statistic count;
        query_3 = "select applicant from application where projectID = "+ str(proj_ID) + ";"
        result_3 = conn.execute(query_3)
        for i in range(result_3.rowcount):
            row_3 = result_3.fetchone()
            count_collabor_finished_proj = Project.total_project_finished_by_collabor(conn, row_3['applicant'])
            query_4 = "select user_level from collaborator where ID= " + str(row_3['applicant']) + ";"
            result_4 = conn.execute(query_4)
            row_4 = result_4.fetchone()
            Project.update_user_level(conn, 'C', count_collabor_finished_proj, row_4['user_level'], row_3['applicant'])

        #finally return the updated project info;
        return Project.get_by_id(conn, proj_ID)
            
    @staticmethod
    #Dreamer or collaborator can follow a project;
    def follow_a_project(conn, proj_ID, user_role, user_ID):
        """Follow a project by user
        Param:
        conn -- database connection
        proj_ID -- project digit id
        user_role -- role string
        user_ID -- user digit id
        Return:
        Follow information of project id and user id
        """
        if user_role == 'Dreamer':
            #check if the user has subscribed the project or not;
            query_1 = "SELECT * FROM subscription WHERE projectID = " + str(proj_ID) + " and d_subscriber = " + str(user_ID) + ";"
            result = conn.execute(query_1)
            if result.rowcount == 0:
                #user has not subscribed this project, proceed to subscribe it;
                query = "INSERT INTO subscription (projectID, is_dreamer, d_subscriber) VALUES (" + str(proj_ID) + ", " + str(1) + ", " + str(user_ID) + ");"
                conn.execute(query)
                #query one more time to return the subscription info;
                query_2 = "SELECT * FROM subscription WHERE projectID = " + str(proj_ID) + " and d_subscriber = " + str(user_ID) + ";"
                result = conn.execute(query_2)
            row = result.fetchone()
            userid = row['d_subscriber']  
        else:
            #check if the user has subscribed the project or not;
            query_1 = "SELECT * FROM subscription WHERE projectID = " + str(proj_ID) + " and c_subscriber = " + str(user_ID) + ";"
            result = conn.execute(query_1)
            if result.rowcount == 0:
                #user has not subscribed this project, proceed to subscribe it;
                query = "INSERT INTO subscription (projectID, is_dreamer, c_subscriber) VALUES (" + str(proj_ID) + ", " + str(0) + ", " + str(user_ID) + ");"
                conn.execute(query)
                #query one more time to return the subscription info;
                query_2 = "SELECT * FROM subscription WHERE projectID = " + str(proj_ID) + " and c_subscriber = " + str(user_ID) + ";"
                result = conn.execute(query_2)
            row = result.fetchone()
            userid = row['c_subscriber']  
        return {'projectID':row['projectID'], 'user_ID':userid}

    @staticmethod
    #Dreamer or collaborator can unfollow a project;
    def unfollow_a_project(conn, proj_ID, user_role, user_ID):
        """Unfollow a project by user
        Param:
        conn -- database connection
        proj_ID -- project digit id
        user_role -- role string
        user_ID -- user digit id
        Return:
        Boolean if unfollow success
        """
        if user_role == 'Dreamer':
            query = "DELETE FROM subscription WHERE projectID = " + str(proj_ID) + " and d_subscriber = " + str(user_ID) + ";"
            conn.execute(query)
            #query one more time to return the subscription info;
            query_1 = "SELECT * FROM subscription WHERE projectID = " + str(proj_ID) + " and d_subscriber = " + str(user_ID) + ";"
            result = conn.execute(query_1)
            if result.rowcount == 0:
                return True
        else:
            query = "DELETE FROM subscription WHERE projectID = " + str(proj_ID) + " and c_subscriber = " + str(user_ID) + ";"
            conn.execute(query)
            #query one more time to return the subscription info;
            query_1 = "SELECT * FROM subscription WHERE projectID = " + str(proj_ID) + " and c_subscriber = " + str(user_ID) + ";"
            result = conn.execute(query_1)
            if result.rowcount == 0:
                return True        
        return False

    @staticmethod
    #Get all discussion records about the project;
    def get_discussion_about_one_project(conn, proj_ID):
        """Get all discussions of one project
        Param:
        conn -- database connection
        proj_ID -- project digit ID
        Return:
        list of discussions
        """
        query = "SELECT * FROM discussion WHERE projectID = " + str(proj_ID) + " ORDER BY ID;"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        discussion_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            discussion = {'discussionID':row['ID'], 'projectID':row['projectID'], 'parent_discussion_ID':row['parent_discussion_ID'], 'text':row['text'], 'is_dreamer':row['is_dreamer'], 'd_author':row['d_author'], 'c_author':row['c_author'], 'last_update_time':str(row['last_update'])}
            discussion_list.append(discussion)
        return discussion_list

    @staticmethod
    #get all discussion records of the projects which user followed;
    def get_discussion_about_followed_projects(conn, user_type, user_ID):
        """Get all discussions of user followed projects
        Param:
        conn -- database connection
        user_type -- user type string
        user_ID -- user digit ID
        Return:
        list of discussions
        """
        if user_type == 'Dreamer':
            query = "SELECT d.ID as ID, d.projectID as projectID, parent_discussion_ID, text, d.is_dreamer as is_dreamer, d_author, c_author, d.last_update as last_update FROM subscription s, discussion d WHERE s.projectID = d.projectID and s.is_dreamer = 1 and s.d_subscriber = " + str(user_ID) + " ORDER BY d.ID, d.projectID;"
            result = conn.execute(query)
        else:
            query = "SELECT d.ID as ID, d.projectID as projectID, parent_discussion_ID, text, d.is_dreamer as is_dreamer, d_author, c_author, d.last_update as last_update FROM subscription s, discussion d WHERE s.projectID = d.projectID and s.c_subscriber = " + str(user_ID) + " ORDER BY d.ID, d.projectID;"
            result = conn.execute(query)
        if result.rowcount == 0:
            return None
        discussion_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            discussion = {'discussionID':row['ID'], 'projectID':row['projectID'], 'parent_discussion_ID':row['parent_discussion_ID'], 'text':row['text'], 'is_dreamer':row['is_dreamer'], 'd_author':row['d_author'], 'c_author':row['c_author'], 'last_update_time':str(row['last_update'])}
            discussion_list.append(discussion)
        return discussion_list

    @staticmethod
    #Check if the dreamer owned the project or not;
    def check_owner(conn, proj_id, owner_id):
        """Check project owner identity
        Param:
        conn -- database connection
        proj_id -- project digit id
        owner_id -- dreamer digit id
        Return:
        boolean if owner corrent
        """
        query = "SELECT * FROM project WHERE ID = " + str(proj_id) + ";"
        result = conn.execute(query)
        if result.rowcount > 0:
            row = result.fetchone()
            if row['dreamerID'] == owner_id: return True
        return False

    @staticmethod
    #Get pending projects for further auditing process;
    def get_pending_projects(conn):
        """Get all pending status projects
        Param:
        conn -- database connection
        Return:
        list of pending projects
        """
        query = "SELECT * FROM project WHERE project_status = -1 order by create_time;"
        print(query)
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        project_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
            proj.id = row['ID']
            proj.is_modified_after_hidden = row['is_modified_after_hidden']
            proj.roles = Role.get_text_by_proj_id(conn, proj.id)
            proj.create_time = row['create_time']
            proj.last_update = row['last_update']
            project_list.append(proj.text_info())
        return project_list
    
    @staticmethod
    def hidden_projects(conn):
        """Get all projects which are in hidden status and are not modified after hidden
        Param:
        conn -- database connection
        Return:
        List of hidden projects
        """
        query = "SELECT * FROM project WHERE is_hidden = 1 AND is_modified_after_hidden = 0 order by last_update DESC;"
        result = conn.execute(query)
        project_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
            proj.id = row['ID']
            proj.is_modified_after_hidden = row['is_modified_after_hidden']
            proj.roles = Role.get_text_by_proj_id(conn, proj.id)
            proj.create_time = row['create_time']
            proj.last_update = row['last_update']
            project_list.append(proj.text_info())
        return project_list
    
    @staticmethod
    def active_projects(conn):
        """Get all active projects
        Param:
        conn -- database connection
        Return:
        list of active projects
        """
        query = "SELECT * FROM project WHERE project_status = 1 AND is_hidden = 0 order by last_update DESC;"
        result = conn.execute(query)
        project_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
            proj.id = row['ID']
            proj.is_modified_after_hidden = row['is_modified_after_hidden']
            proj.roles = Role.get_text_by_proj_id(conn, proj.id)
            proj.create_time = row['create_time']
            proj.last_update = row['last_update']
            project_list.append(proj.text_info())
        return project_list
    
    @staticmethod
    #Get projects which has been modified after hidden;
    def modified_projects_after_hidden(conn):
        """Check modified projects after hidden
        Param:
        conn -- database connection
        Return:
        list of MaH projects
        """
        query = "SELECT * FROM project WHERE is_hidden = 1 and is_modified_after_hidden = 1 order by last_update ASC;"
        print(query)
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        project_list = []
        for i in range(result.rowcount):
            row = result.fetchone()
            proj = Project(row['project_title'],row['description'],row['dreamerID'],row['category'],status=row['project_status'],hidden=row['is_hidden'],hidden_reason=row['hidden_reason'])
            proj.id = row['ID']
            proj.is_modified_after_hidden = row['is_modified_after_hidden']
            proj.roles = Role.get_text_by_proj_id(conn, proj.id)
            proj.create_time = row['create_time']
            proj.last_update = row['last_update']
            project_list.append(proj.text_info())
        return project_list
    
    @staticmethod
    #Admin can audit a project and make the project as active status if the project is legal; 
    def audit_a_project(conn, proj_ID):
        """Audit a project and put it in active status
        Param:
        conn -- database connection
        proj_ID -- project digit id
        Return:
        Boolean if activate success
        """
        query = "UPDATE project SET project_status = 1 where ID = " + str(proj_ID) + ";"
        print(query)
        conn.execute(query)
        proj = Project.get_by_proj_id(conn, proj_ID)
        if proj['status'] == 1:return True
        else:return False

    @staticmethod
    #Admin can hide a project if there is improper content about the new project;
    def hide_a_project(conn, proj_ID, hidden_reason, smtp):
        """hide a project due to improper contents and so forth
        Param:
        conn -- database connection
        proj_ID -- project digit id
        hidden_reason -- 
        Return:
        Boolean if activate success
        """
        query = "UPDATE project SET is_hidden = 1, hidden_reason = \'" + str(hidden_reason) + "\' WHERE id = " + str(proj_ID) + ";"
        print(query)
        conn.execute(query)
        #send email to project owner once it's hidden;
        Project.get_object_by_id(conn, proj_ID).notify_project_owner(conn, smtp, hide=True, hidden_reason=hidden_reason)
        proj = Project.get_by_proj_id(conn, proj_ID)
        if proj.info()['is_hidden'] == 1:return True
        else:return False

    @staticmethod
    #Admin can unhide a project if the owner has made the project content being proper and legal;
    def unhide_a_project(conn, proj_ID, smtp):
        """unhide a project and put it active status
        Param:
        conn -- database connection
        proj_ID -- project digit id
        hidden_reason
        Return:
        Boolean if activate success
        """
        query = "UPDATE project SET is_hidden = 0 WHERE id = " + str(proj_ID) + ";"
        print(query)
        conn.execute(query)
        #send email to project owner once it's unhidden;
        Project.get_object_by_id(conn, proj_ID).notify_project_owner(conn, smtp, hide=False)
        proj = Project.get_by_proj_id(conn, proj_ID)
        if proj.info()['is_hidden'] == 0:return True
        else:return False

    def notify_project_owner(self, conn, smtp, hide=True, hidden_reason=""):
        proj = Project.get_by_id(conn, self.id)
        from users.dreamer import Dreamer
        dre = Dreamer.get_by_id(conn, self.owner)
        if hidden_reason == "":
            hidden_reason = "improper or sensitive contents"
        if hide:
            subject = '[DreamMatchmaker]Your project has been hidden due to illegal or improper content, please do modifiction!'
            content = f'''<p>Hello {dre['name']},</p>
<p>   Your project - <b>{proj['title']}</b> has been hidden due to {hidden_reason}, admin will unhide your project once it's updated!</p>
<p>Dream Matchmaker Team</p>
'''
        else:
            subject = '[DreamMatchmaker]Your project has been passed audition and unhidden, please be noted!'
            content = f'''<p>Hello {dre['name']},</p>
<p>   Your project - <b>{proj['title']}</b> has been passed audition and unhidden, please be noted!</p>
<p>Dream Matchmaker Team</p>
'''
        result = smtp.send_email_html(dre['email'], content, subject)
        return result


    def info(self):
        """Return project info"""
        return {'id': self.id, 'title': self.title, 'description': self.description, 'owner': self.owner, 'category': self.category, 'status': self.project_status, 'is_hidden': self.is_hidden, 'hidden_reason': self.hidden_reason, 'is_modified_after_hidden': self.is_modified_after_hidden, "roles": self.roles, "create_time": str(self.create_time), "last_update": str(self.last_update)}

    def text_info(self):
        """Return project text info"""
        return {'id': self.id, 'title': self.title, 'description': self.description, 'owner': self.owner, 'category': self.category_list[self.category], 'status': self.project_status, 'is_hidden': self.is_hidden, 'hidden_reason': self.hidden_reason, 'is_modified_after_hidden': self.is_modified_after_hidden, "roles": self.roles, "create_time": str(self.create_time), "last_update": str(self.last_update)}

    #Check if the project which has the same title has been created or not from the same owner;
    def duplicate_check(self, conn):
        """Duplicate check of project
        Param:
        conn -- database connection
        Return:
        Boolean if project is duplicate
        """
        query = "SELECT * FROM project WHERE project_title = \'" + self.title + "\' AND dreamerID = " + str(self.owner) + ";"
        result = conn.execute(query)
        if result.rowcount > 0:
            return True
        return False
        
    #Patch the project title, description or category info, and also update the is_modified_after_hidden as 1 if it has been marked as hidden;
    def patch(self, conn):
        """Patch project info into database
        Param:
        conn -- database connection
        Return:
        patched project object
        """
        query = "select * from project WHERE id = " + str(self.id) + ";"
        result = conn.execute(query)
        if result.rowcount > 0:
            row = result.fetchone()
            #update is_modified_after_patch = 1 at the same time if the project has been hidden before patch;
            if row['is_hidden'] == 1:
                query_1 = "UPDATE project SET project_title = \'" + self.title.replace("'", "\\\'") + "\', description = \'" + self.description.replace("'", "\\\'") + "\', category = " + str(self.category) + ", is_modified_after_hidden = 1 WHERE id = " + str(self.id) + ";"
                print(query_1)
                conn.execute(query_1)
            else:
                query_2 = "UPDATE project SET project_title = \'" + self.title.replace("'", "\\\'") + "\', description = \'" + self.description.replace("'", "\\\'") + "\', category = " + str(self.category) + " WHERE id = " + str(self.id) + ";"
                print(query_2)
                conn.execute(query_2)
        return self

    #Greate a new project;
    def create(self, conn):
        """create project info into database
        Param:
        conn -- database connection
        Return:
        created project object
        """
        if self.duplicate_check(conn):
            return None
        query = "INSERT INTO project (project_title, description, category, dreamerID) VALUES (\'" + self.title.replace("'", "\\\'") + "\', \'" + self.description.replace("'", "\\\'") + "\', " + str(self.category) + ", " + str(self.owner) + ");"
        conn.execute(query)
        query = "SELECT * FROM project WHERE dreamerID = " + str(self.owner) + " ORDER BY create_time DESC;"
        result = conn.execute(query)
        row = result.fetchone()
        self.id = row['ID']
        self.create_time = row['create_time']
        self.last_update = row['last_update']
        return self

