#!/usr/bin/python3
from users.collaborator import Collaborator
from users.dreamer import Dreamer
from projects.project import Project

class Discussion():
    """Discussion class under project"""
    def __init__(self, projectID, parent_discussion_ID, is_dreamer, d_author = '',c_author = '',text = ''):
        self.projectID = projectID
        self.parent_discussion_ID = parent_discussion_ID
        self.is_dreamer = is_dreamer
        self.d_author = d_author
        self.c_author = c_author
        self.text = text
        # no input warning
        self.id = -1

    @staticmethod
    def get_notification_by_id(conn, user_id,user_role):
        """get notifications for specific user
        Param:
        conn -- database connection
        user_id -- user digit id
        user_role -- role of user, 'Dreamer' or 'Collaborator'
        Return:
        notification list
        """
        # read role
        if user_role == 'Dreamer':
            query = "SELECT * FROM dreamer_notification where dreamer_ID = " + str(user_id) + " and is_viewed = " + str(0) + ";"
        if user_role == 'Collaborator':
            query = "SELECT * FROM collaborator_notification where collaborator_ID = " + str(user_id) + " and is_viewed = " + str(0) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        notification_dict = {}
        notification_list = []
        # fetch notifications
        for i in range(result.rowcount):
            row = result.fetchone()
            id = row['ID']
            notification = {'notification_id': row['ID'], 'notification_content': row['notification_text']}
            notification_list.append(notification)
            if user_role == 'Dreamer':
                query = "UPDATE dreamer_notification set is_viewed = " + str(1) + " where ID = " + str(id) + ";"
            if user_role == 'Collaborator':
                query = "UPDATE collaborator_notification set is_viewed = " + str(1) + " where ID = " + str(id) + ";"
            conn.execute(query)
        notification_dict['notification'] = notification_list
        return notification_dict

    @staticmethod
    def get_by_did(conn, discussion_id):
        """Get discussion info by id
        Param:
        conn -- database connection
        discussion_id -- discussion digit id
        Return:
        discussion info dict
        """
        query = "SELECT * FROM discussion where ID = " + str(discussion_id) + ";"
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        row = result.fetchone()
        discussion_info = {'discussion_id':discussion_id,'projectID':row['projectID'],'parent_id':row['parent_discussion_ID'],'content':row['text'],'create_time':str(row['create_time'])}
        if row['is_dreamer'] == 2:
            author = Dreamer.get_by_id(conn,row['d_author'])
            discussion_info['is_owner'] = 'Yes'
            discussion_info['author_id'] = author['id']
            discussion_info['author_name'] = author['name']
            discussion_info['author_role'] = 'dreamer'
        elif row['is_dreamer'] == 1:
            author = Dreamer.get_by_id(conn, row['d_author'])
            discussion_info['is_owner'] = 'No'
            discussion_info['author_id'] = author['id']
            discussion_info['author_name'] = author['name']
            discussion_info['author_role'] = 'dreamer'
        else:
            author = Collaborator.get_by_id(conn, row['c_author'])
            discussion_info['is_owner'] = 'No'
            discussion_info['author_id'] = author['id']
            discussion_info['author_name'] = author['name']
            discussion_info['author_role'] = 'collaborator'
        return discussion_info

    @staticmethod
    def get_by_pid(conn, project_id):
        """Get all discussions under a specific project
        Param:
        conn -- database connection
        project_id -- project digit id
        Return:
        discussion list of a project
        """
        query = "SELECT * FROM discussion where projectID = " + str(project_id) + ";"
        result = conn.execute(query)
        all_discussion = {}
        discussion_list = []
        if result.rowcount == 0:
            return None
        for i in range(result.rowcount):
            row = result.fetchone()
            discussion_info = {'discussion_id':row['ID'],'parent_id': row['parent_discussion_ID'], 'content': row['text'], 'create_time':str(row['create_time'])}
            if row['is_dreamer'] == 2:
                author = Dreamer.get_by_id(conn, row['d_author'])
                discussion_info['is_owner'] = 'Yes'
                discussion_info['author_id'] = author['id']
                discussion_info['author_name'] = author['name']
                discussion_info['author_role'] = 'dreamer'
            elif row['is_dreamer'] == 1:
                author = Dreamer.get_by_id(conn, row['d_author'])
                discussion_info['is_owner'] = 'No'
                discussion_info['author_id'] = author['id']
                discussion_info['author_name'] = author['name']
                discussion_info['author_role'] = 'dreamer'
            else:
                author = Collaborator.get_by_id(conn, row['c_author'])
                discussion_info['is_owner'] = 'No'
                discussion_info['author_id'] = author['id']
                discussion_info['author_name'] = author['name']
                discussion_info['author_role'] = 'collaborator'
            discussion_list.append(discussion_info)
        all_discussion['discussion_info'] = discussion_list
        return all_discussion


    def info(self):
        """Return discussion info dict"""
        return {'id': self.id, 'project_id': self.projectID, 'parent_discussion_id': self.parent_discussion_ID,'content': self.text, 'is_dreamer': self.is_dreamer, 'create_time': str(self.create_time)}

    def owner_reply(self, conn):
        """Discussion reply by project owner
        Param:
        conn -- database connection
        """
        query = "SELECT * FROM discussion where ID = " + str(self.parent_discussion_ID) + " ;"
        result = conn.execute(query)
        row = result.fetchone()
        if row['is_dreamer'] == 2 or row['is_dreamer'] == 1:
            query = "INSERT INTO dreamer_notification (dreamer_ID, notification_text, is_viewed) VALUES (" + str(row['d_author']) + ", \'" + self.text.replace("'", "\\\'") + "\', " + str(0) + ");"
            conn.execute(query)
        else:
            query = "INSERT INTO collaborator_notification (collaborator_ID, notification_text, is_viewed) VALUES (" + str(row['c_author']) + ", \'" + self.text.replace("'", "\\\'") + "\', " + str(0) + ");"
            conn.execute(query)


    def create_by_dreamer(self, conn):
        """Discussion reply by a dreamer
        Param:
        conn -- database connection
        Return:
        discussion object
        """
        if self.parent_discussion_ID == 0:
            query = "INSERT INTO discussion (projectID, text, is_dreamer, d_author) VALUES (" + str(self.projectID) + ", \'" + self.text.replace("'", "\\\'") + "\', " + str(self.is_dreamer) + ", " + str(self.d_author) + ");"
        else:
            query = "INSERT INTO discussion (projectID, parent_discussion_ID, text, is_dreamer, d_author) VALUES (" + str(self.projectID) + ", " + str(self.parent_discussion_ID) + ", \'" + self.text.replace("'", "\\\'") + "\', " + str(self.is_dreamer) + ", " + str(self.d_author) + ");"
            if self.is_dreamer == 2:
                self.owner_reply(conn)
        conn.execute(query)
        query = "SELECT * FROM discussion where projectID = " + str(self.projectID) + " ORDER BY create_time DESC;"
        result = conn.execute(query)
        row = result.fetchone()
        self.id = row['ID']
        self.create_time = row['create_time']
        return self

    def create_by_collaborator(self, conn):
        """Discussion reply by a collaborator
        Param:
        conn -- database connection
        Return:
        discussion object
        """
        if self.parent_discussion_ID == 0:
            query = "INSERT INTO discussion (projectID, text, is_dreamer, c_author) VALUES (" + str(self.projectID) + ", \'" + self.text.replace("'", "\\\'") + "\', " + str(self.is_dreamer) + ", " + str(self.c_author) + ");"
        else:
            query = "INSERT INTO discussion (projectID, parent_discussion_ID, text, is_dreamer, c_author) VALUES (" + str(self.projectID) + ", " + str(self.parent_discussion_ID) + ", \'" + self.text.replace("'", "\\\'") + "\', " + str(self.is_dreamer) + ", " + str(self.c_author) + ");"
        conn.execute(query)
        query = "SELECT * FROM discussion where projectID = " + str(self.projectID) + " ORDER BY create_time DESC;"
        result = conn.execute(query)
        row = result.fetchone()
        self.id = row['ID']
        self.create_time = row['create_time']
        return self
