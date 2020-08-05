#!/usr/bin/python3

'''
UNSW COMP9900 20T2
Capstone Project
Team Salted Fish
Members
Xiaowei Zhou    z5108173
Keyu Yang       z5177443
Lisha Jing      z5243620
Nan Zhao        z5225777
Qingbei Wu      z5222641

This file does not have Python doc, but using
Swagger automatic doc for documentation.
'''

# PyPi libraries
import json, yaml, os
from functools import wraps
from flask import Flask, request, send_from_directory
from flask_restplus import Api, abort, fields, reqparse
from werkzeug.datastructures import FileStorage

# Own libraries
from db import DB
from auth_token import AuthToken
from util import check_email, allowed_file, CorsResource
from smtp import SMTP

from users.admin import Admin
from users.dreamer import Dreamer
from users.collaborator import Collaborator

from projects.project import Project
from projects.role import Role
from projects.application import Application
from projects.invitation import Invitation
from projects.discussion import Discussion

# Load config
f = open('projects/project.config', 'r', encoding='utf-8')
config = yaml.load(f.read(), Loader=yaml.FullLoader)

# Other config
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files')
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except:
    pass
IMAGE_FOLDER = os.path.join(os.getcwd(), 'images')
try:
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
except:
    pass

# Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
api = Api(app, authorizations={
    'API-KEY': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'AUTH_KEY'
    },
}, security='API-KEY', default='Dream_Matchmaker', title='Dream Matchmaker', description='Dream Matchmaker, a project posting and collaborator finding system')

# Auth Token
SECRET = "DREAM MATCHMAKER, POWERED BY TEAM SALTED FISH"
expires = 3600
auth = AuthToken(SECRET, expires)

# Auth decorator
def require_auth(f):
    @wraps(f)
    def func(*args, **kwargs):
        token = request.headers.get('AUTH_KEY')
        if not token:
            abort(401, 'Auth Token Missing')
        try:
            userinfo = auth.validate(token)
        except Exception as e:
            abort(401, e)
        return f(*args, **kwargs)

    return func

# Get Parsers
projects_parser = reqparse.RequestParser()
projects_parser.add_argument('description', type=str, default='')
projects_parser.add_argument('category', type=int, default=-1) # -1 for all categories
projects_parser.add_argument('order_by', choices=['last_update','project_title'], default='last_update')
projects_parser.add_argument('sorting', choices=['ASC','DESC'], default='DESC')

collaborator_parser = reqparse.RequestParser()
collaborator_parser.add_argument('applied_role', type=int, default=-1) # -1 for no request on this

# Put Parsers
resume_parser = reqparse.RequestParser()
resume_parser.add_argument('file', type=FileStorage, location='files')

# Post Models
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Your email address'),
    'password': fields.String(required=True, description='Your password', min_length=8),
    'role': fields.String(required=True, description='Admin, Dreamer, Collaborator', enum=['Admin','Dreamer','Collaborator'])
})

dreamer_register_model = api.model('Dreamer_Register', {
    'name': fields.String(required=True, description='Your name'),
    'email': fields.String(required=True, description='Your email address'),
    'password': fields.String(required=True, description='Your password', min_length=8),
    'repeat_password': fields.String(required=True, description='Repeat your password', min_length=8),
    'phone_no': fields.String(required=False, description='Phone number (optional)')
})

collaborator_register_model = api.model('Collaborator_Register', {
    'name': fields.String(required=True, description='Your name'),
    'email': fields.String(required=True, description='Your email address'),
    'password': fields.String(required=True, description='Your password', min_length=8),
    'repeat_password': fields.String(required=True, description='Repeat your password', min_length=8),
    'phone_no': fields.String(required=False, description='Phone number (optional)'),
    'education': fields.Integer(required=False, description='Education, 1=Other, 2=Bachelor, 3=Master, 4=PhD'),
    'skills': fields.String(required=False, description='skills(as integer). Format: skill1,skill2,skill3,...', example='2,3,1'),
    'experience': fields.String(required=False, description='experience (in years). Format: exp1,exp2,exp3,...', example='3,2,1')
})

admin_hide_project_model = api.model('Hide_Project', {
    'hidden_reason': fields.String(required=True, description='Hide reason')
})

project_post_model = api.model('Project_Post', {
    'title': fields.String(required=True, description='Project title'),
    'description': fields.String(required=True, description='Project description'),
    'category': fields.Integer(required=False, description='Project Category ID')
})

role_post_model = api.model('Role_Post', {
    'title': fields.String(required=True, description='Role title'),
    'amount': fields.Integer(required=True, description='Amount required'),
    'skill': fields.String(required=True, description='Skill ids list divide by comma "," e.g. 2,3,4'),
    'experience': fields.Integer(required=True, description='Experience required in years.'),
    'education': fields.Integer(required=True, description='Education required'),
    'general_enquiry': fields.String(required=False, description='other enquiry')
})

project_patch_model = api.model('Project_Patch', {
    'project_title': fields.String(required=False, description='project title'),
    'description': fields.String(required=False, description='project description'),
    'category': fields.Integer(required=False, description='project category'),
})

role_patch_model = api.model('Role_Patch', {
    'title': fields.String(required=False, description='Role title'),
    'amount': fields.Integer(required=False, description='Amount required'),
    'skill': fields.String(required=False, description='Skill ids list divide by comma "," e.g. 2,3,4'),
    'experience': fields.Integer(required=False, description='Experience required in years.'),
    'education': fields.Integer(required=False, description='Education required'),
    'general_enquiry': fields.String(required=False, description='other enquiry')
})

collaborator_patch_model = api.model('Collaborator_Patch', {
    'phone_no': fields.String(required=False, description='Phone number (optional)'),
    'education': fields.Integer(required=False, description='Education required'),
    'skill': fields.String(required=False, description='Skill ids list divide by comma "," e.g. 2,3,4'),
    'experience': fields.String(required=False, description='Experience required in years.')
})



change_password_model = api.model('Change_Password', {
    'original_password': fields.String(required=True, description='Your original password', min_length=8),
    'new_password': fields.String(required=True, description='Your new password', min_length=8)
})

apply_role_model = api.model('Apply_Role', {
    'general_text': fields.String(required=True, description='Apply description')
})

invite_role_model = api.model('Invite_Role', {
    'collaborator_id': fields.Integer(required=True, description='Invitee ID'),
    'general_text': fields.String(required=True, description='Invite description')
})

post_discussion_model = api.model('Post_Discussion', {
    'parent_id': fields.Integer(required=False, description='reply discussion'),
    'discuss_content': fields.String(required=True, description='content of discussion')
})

# API
@api.route('/admin')
class AdminAPI(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description="Get Admin data")
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        admin_email = userinfo['email']
        admin_id = userinfo['id']
        admin_role = userinfo['role']
        if admin_role != 'Admin':
            return {'message': 'You are not logged in as admin'}, 401
        return {'email': admin_email}, 200

@api.route('/admin/hidden_projects')
class GetAllHiddenProjects(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description="Get all hidden projects")
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        admin_role = userinfo['role']
        if admin_role != 'Admin':
            return {'message': 'You are not logged in as admin'}, 401
        conn = db.conn()
        result = Project.hidden_projects(conn)
        conn.close()
        return {"hidden_projects": result}, 200
        
@api.route('/admin/modified_after_hidden_projects')
class GetModifiedAfterHiddenProjects(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description="Get all hidden projects")
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        admin_role = userinfo['role']
        if admin_role != 'Admin':
            return {'message': 'You are not logged in as admin'}, 401
        conn = db.conn()
        result = Project.modified_projects_after_hidden(conn)
        conn.close()
        return {"modified_after_hidden_projects": result}, 200

@api.route('/admin/pending_projects')
class GetAllPendingProjects(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'No pending projects found')
    @api.response(401, 'Auth Failed')
    @api.doc(description="Get all pending projects")
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        #admin_email = userinfo['email']
        #admin_id = userinfo['id']
        admin_role = userinfo['role']
        if admin_role != 'Admin':
            return {'message': 'You are not logged in as admin'}, 401
        conn = db.conn()
        result = Project.get_pending_projects(conn)
        conn.close()
        if result is None:
            return {'message': 'No pending projects are found now!'}, 400
        return {"pending_projects": result}, 200
        
@api.route('/admin/active_projects')
class GetAllActiveProjects(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'No active projects found')
    @api.response(401, 'Auth Failed')
    @api.doc(description="Get all active projects")
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        #admin_email = userinfo['email']
        #admin_id = userinfo['id']
        admin_role = userinfo['role']
        if admin_role != 'Admin':
            return {'message': 'You are not logged in as admin'}, 401
        conn = db.conn()
        result = Project.active_projects(conn)
        conn.close()
        if result is None:
            return {'message': 'No pending projects are found now!'}, 400
        return {'active_projects': result}, 200

'''@api.route('/admin/<int:id>')
class AuditAProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.response(402, 'Failed to audit the project')
    @api.doc(description="Audit a project")
    @require_auth
    def get(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        #admin_email = userinfo['email']
        #admin_id = userinfo['id']
        admin_role = userinfo['role']
        if admin_role != 'Admin':
            return {'message': 'You are not logged in as admin'}, 401
        conn = db.conn()
        result = Project.audit_a_project(conn, int(id))
        conn.close()
        if result:return {'message': 'Audit the project successfully!'}, 200
        else:return {'message': 'Fail to udit the project!'}, 402'''

@api.route('/categories')
class Categories(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.doc(description="Get project categories list")
    def get(self):
        return {"categories": config['Project']['Categories'], "description": config['Project']['Categories_description']}, 200

@api.route('/skills')
class Skills(CorsResource):
    @api.response(200, 'Success')
    @api.doc(description="Get collaborator skills list")
    def get(self):
        return {"skills": config['Role']['Skills']}, 200

@api.route('/projects')
class ProjectsList(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.doc(description="Get projects list filtered by arguments")
    @api.expect(projects_parser, validate=True)
    def get(self):
        args = projects_parser.parse_args()
        desc = args.get('description')
        category = args.get('category')
        order_by = args.get('order_by')
        sorting = args.get('sorting')
        conn = db.conn()
        result = Project.search_list(conn, desc, category, order_by, sorting)
        conn.close()
        if result is None:
            return {'projects': [], 'message': 'No matching projects were found.'}, 200
        return result, 200

@api.route('/dreamer/my_projects')
class DreamerOwnProjectsList(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        conn = db.conn()
        my_user_id = Dreamer.getObject(conn, userinfo['email']).info()['id']
        result = Project.get_by_owner(conn, my_user_id)
        conn.close()
        if result is None:
            return {'projects': [], 'message': 'You have not create any projects'}, 200
        return {'projects': result}, 200

@api.route('/collaborators')
class CollaboratorsList(CorsResource):
    @api.response(200, 'Success')
    @api.doc(Description='Get all collaborators information')
    def get(self):
        conn = db.conn()
        co_list = Collaborator.get_all(conn)
        conn.close()
        return {'Collaborator_list': co_list}, 200

@api.route('/collaborator/resume')
class UploadResume(CorsResource):
    @api.response(201, 'Created')
    @api.response(400, 'Validation Error')
    @api.response(401, 'Auth Failed')
    @api.doc(Description='Upload a pdf resume')
    @api.expect(resume_parser)
    @require_auth
    def post(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 401
        conn = db.conn()
        user = Collaborator.get_by_id(conn, userinfo['id'])
        conn.close()
        args = resume_parser.parse_args()
        uploaded_file = args['file']
        if uploaded_file.filename == '':
            return {'message': 'No file selected'}, 400
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = f"Resume_{user['id']}_{'_'.join(user['name'].split())}.pdf"
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'message': 'File saved'}, 201
        return {'message': 'File format error'}, 400

@api.route('/collaborator/<int:id>/resume')
class FindResume(CorsResource):
    @api.response(200, 'Success')
    @api.response(404, 'Resume Not Found')
    @api.doc(Description='Get the resume download URL')
    def get(self, id):
        conn = db.conn()
        user = Collaborator.get_by_id(conn, int(id))
        conn.close()
        filename = f"Resume_{user['id']}_{'_'.join(user['name'].split())}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            return {'filename': filename}, 200
        else:
            return {'message': 'Resume not found'}, 404

# Note. This is NOT a restful API!
@app.route('/download/<path:filename>')
def downloader(filename):
    dirpath = app.config['UPLOAD_FOLDER']
    return send_from_directory(dirpath, filename, as_attachment=True)

@api.route('/collaborator/<int:id>')
class CollaboratorInfo(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.doc(Description='Get single collaborator information')
    @api.expect(collaborator_parser, validate=True)
    def get(self, id):
        args = collaborator_parser.parse_args()
        role_id = args.get('applied_role')
        conn = db.conn()
        appli = 0
        if role_id != -1:
            colla, appli = Collaborator.get_object_by_id(conn, int(id), role_id)
        else:
            colla = Collaborator.get_object_by_id(conn, int(id))
        conn.close()
        result = colla.info_2()
        result['role_applied'] = role_id
        result['wait_approve'] = bool(appli)
        return result, 200

@api.route('/collaborator/projects')
class CollaboratorProjectsList(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.response(401, 'Auth Failed')
    @api.expect(projects_parser, validate=True)
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 401
        email = userinfo['email']
        conn = db.conn()
        my_user = Collaborator.getObject(conn, email)
        args = projects_parser.parse_args()
        desc = args.get('description')
        category = args.get('category')
        order_by = args.get('order_by')
        sorting = args.get('sorting')
        result = my_user.search_list(conn, desc, category, order_by, sorting)
        conn.close()
        if result is None:
            return {'projects': [], 'message': 'No matching projects were found.'}, 200
        return result, 200

@api.route('/collaborator/recommendation')
class ProjectsRecommendation(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.response(401, 'Auth Failed')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 401
        email = userinfo['email']
        conn = db.conn()
        my_user = Collaborator.getObject(conn, email)
        result = my_user.projects_recommdation(conn)
        conn.close()
        if result is None:
            return {'projects': [], 'message': 'No matching projects were found.'}, 200
        return result, 200

@api.route('/dreamer/<int:id>')
class DreamerInfo(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Dreamer can not be found')
    @api.response(401, 'Auth Failed')
    @api.doc(Description='Get information of a dreamer')
    def get(self, id):
        conn = db.conn()
        result = Dreamer.get_by_id(conn, int(id))
        conn.close()
        if result:return {'Dreamer_Info': result}, 200
        else:return {'message':'The queried dreamer can not be found!'}, 400

@api.route('/dreamer/recommendation')
class CollaboratorsRecommendation(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.response(401, 'Auth Failed')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        email = userinfo['email']
        conn = db.conn()
        my_user = Dreamer.getObject(conn, email)
        result = my_user.collaborators_recommdation(conn)
        conn.close()
        if result is None:
            return {'collaborators': [], 'amount': 0, 'message': 'No matching collaborators were found.'}, 200
        return {'collaborators': result, 'amount': len(result), 'message': 'Some matching collaborators were found for your projects.'}, 200

@api.route('/project/<int:id>/hide')
@api.param('id', 'The project id')
class AdminHideProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Failed to hide')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Hide a project')
    @api.expect(admin_hide_project_model, validate=True)
    @require_auth
    def post(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Admin':
            return {'message': 'You are not logged in as admin'}, 401
        conn = db.conn()
        info = request.json
        result = Project.hide_a_project(conn, int(id), info['hidden_reason'], smtp)
        if not result:
            return {'message': 'Failed to hide the project'}, 400
        return {'message': 'Successfully hide the project!', 'Project_ID':int(id)}, 200
        
@api.route('/project/<int:id>/unhide')
@api.param('id', 'The project id')
class AdminUnhideProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Failed to hide')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Unhide a project')
    @require_auth
    def get(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Admin':
            return {'message': 'You are not logged in as admin'}, 401
        conn = db.conn()
        result = Project.unhide_a_project(conn, int(id), smtp)
        if not result:
            return {'message': 'Failed to unhide the project'}, 400
        return {'message': 'Successfully unhide the project!', 'Project_ID':int(id)}, 200

@api.route('/project/<int:id>/finish')
@api.param('id', 'The project id')
class DreamerFinishProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Failed to finish the project')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'Project not found')
    @api.doc(description='Finish a project')
    @require_auth
    def get(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        dreamer_id = userinfo['id']
        conn = db.conn()
        result1 = Project.get_by_id(conn, int(id))
        if result1 is None:
            conn.close()
            return {'message': 'Requesting non-existing project information'}, 404
        result = Project.finish_a_project(conn, int(id), dreamer_id)
        conn.close()
        if result['status'] != 9:
            return {'message': 'Failed to finish the project'}, 400
        return {'message': 'Successfully finish the project!', 'Project_ID':result['id']}, 200

@api.route('/project/<int:id>/follow')
@api.param('id', 'The project id')
class FollowAProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Failed to follow the project')
    @api.doc(description='Follow a project')
    @require_auth
    def get(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        user_ID = userinfo['id']
        conn = db.conn()
        if userinfo['role'] == 'Dreamer':
            result = Project.follow_a_project(conn, int(id), 'Dreamer', user_ID)
        else:
            result = Project.follow_a_project(conn, int(id), 'Collaborator', user_ID)
        conn.close()
        if result:
            return {'message': 'Successfully follow the project!'}, 200
        else:
            return {'message': 'Fail to follow the project!'}, 400

@api.route('/project/<int:id>/unfollow')
@api.param('id', 'The project id')
class UnfollowAProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Failed to unfollow the project')
    @api.doc(description='Unfollow a project')
    @require_auth
    def get(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        user_ID = userinfo['id']
        conn = db.conn()
        if userinfo['role'] == 'Dreamer':
            result = Project.unfollow_a_project(conn, int(id), 'Dreamer', user_ID)
        else:
            result = Project.unfollow_a_project(conn, int(id), 'Collaborator', user_ID)
        conn.close()
        if result:
            return {'message': 'Successfully unfollow the project!'}, 200
        else:
            return {'message': 'Fail to unfollow the project!'}, 400

@api.route('/collaborator/invitations')
class InvitationsReceived(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Show invitations I received')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        collaborator_id = userinfo['id']
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 401
        conn = db.conn()
        result = Invitation.get_by_invitee(conn, collaborator_id)
        conn.close()
        return result, 200

@api.route('/collaborator/my_projects')
class CollaboratorJoinedProjects(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description='All projects I collaborated')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        user_ID = userinfo['id']
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 401
        conn = db.conn()
        result = Collaborator.get_my_projects(conn, user_ID)
        conn.close()
        return result, 200

@api.route('/collaborator/my_applications')
class ApplicationsOfCollaborator(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description='All applications that collaborator has applied')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        user_ID = userinfo['id']
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 401
        conn = db.conn()
        result = Application.get_by_applicant(conn, user_ID)
        conn.close()
        return result, 200

@api.route('/project/<int:pid>/role/<int:rid>/invitation')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
class InviteRole(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Invite a collaborator for a role')
    @api.expect(invite_role_model, validate=True)
    @require_auth
    def post(self, pid, rid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        invite_info = request.json
        try:
            general_text = invite_info['general_text']
        except:
            general_text = ''
        conn = db.conn()
        new_invite = Invitation(int(pid), int(rid), dreamer_id, invite_info['collaborator_id'], general_text=general_text).create(conn)
        if new_invite == None:
            conn.close()
            return {'message': 'invite role duplicate'}, 400
        new_invite.notify_invitee(conn, smtp)
        invi_id = new_invite.info(conn)['id']
        conn.close()
        return {'message': 'role invite success', 'project_id': int(pid), 'project_role_id': int(rid), 'invitation_id': invi_id}, 200

@api.route('/project/<int:pid>/role/<int:rid>/invitation/<int:iid>/accept')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
@api.param('iid', 'The invitation id')
class AcceptAnInvitation(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Auth Failed')
    @api.response(404, 'Invitation not found')
    @api.doc(description='Accept an invitation')
    @require_auth
    def get(self, pid, rid, iid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 400
        conn = db.conn()
        invitation = Invitation.get_by_pid_rid_iid(conn, int(pid), int(rid), int(iid))
        if invitation['invitee'] != userinfo['id']:
            conn.close()
            return {'message': 'You are not authorized to accept this invitation'}, 400
        if Project.check_finish(conn, int(pid)):
            conn.close()
            return {'message': 'The project has been finished.'}, 400
        if invitation['status'] == 0:
            conn.close()
            return {'message': 'This invitation has been declined'}, 400
        result_1 = Invitation.get_by_iid(conn, int(iid))
        if result_1 is None:
            conn.close()
            return {'message': 'Invitation not found'}, 404
        result = Invitation.accept_an_invitation(conn, smtp, int(pid), int(rid), int(iid))
        conn.close()
        if result == 0:
            return {'message': 'This invitation has been declined already!'}, 400
        if result == 1:
            return {'message': 'This invitation has been accepted already!'}, 400
        if result == 9:
            return {'message': 'The related project of this invitation has been finished.'}, 400
        if result == 88:
            return {'message': 'This project role has been fullfilled, no more collaborator needed!'}, 400
        if result['invite_status'] != 1:
            return {'message': 'Failed to accept an invitation'}, 400
        return {'message': 'Accept invitation successfully','Invitation':result}, 200

@api.route('/project/<int:pid>/role/<int:rid>/invitation/<int:iid>/decline')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
@api.param('iid', 'The invitation id')
class DeclineAnInvitation(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'Invitation not found!')
    @api.doc(description='Decline an invitation')
    @require_auth
    def get(self, pid, rid, iid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 400
        conn = db.conn()
        invitation = Invitation.get_by_pid_rid_iid(conn, int(pid), int(rid), int(iid))
        if invitation['invitee'] != userinfo['id']:
            conn.close()
            return {'message': 'You are not authorized to decline this invitation'}, 400
        if invitation['status'] == 1:
            conn.close()
            return {'message': 'This invitation has been accepted already!'}, 400
        if Project.check_finish(conn, int(pid)):
            conn.close()
            return {'message': 'The project has been finished.'}, 400
        result_1 = Invitation.get_by_iid(conn, int(iid))
        if result_1 is None:
            conn.close()
            return {'message': 'Invitation not found'}, 404
        result = Invitation.decline_an_invitation(conn, smtp, int(pid), int(rid), int(iid))
        if result['invite_status'] != 0:
            conn.close()
            return {'message': 'Failed to decline an invitation'}, 400
        invite = Invitation.get_object_by_id(conn, iid)
        invite.notify_invitor(conn, smtp, accept=False)
        conn.close()
        return {'message': 'Invitation has been declined successfully!','Invitation':result}, 200

@api.route('/project/<int:pid>/role/<int:rid>/joined_collabors')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
class JoinedCollabors(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Get joined collaborators')
    @require_auth
    def get(self, pid, rid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        collaborator_id = userinfo['id']
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        conn = db.conn()
        result = Role.get_joined_collaborators(conn, rid)
        conn.close()
        return {"collaborators": result}, 200

@api.route('/project/<int:pid>/role/<int:rid>/appllication')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
class ApplyRole(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Apply a new role for the project')
    @api.expect(apply_role_model, validate=True)
    @require_auth
    def post(self, pid, rid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        collaborator_id = userinfo['id']
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 401
        apply_info = request.json
        try:
            general_text = apply_info['general_text']
        except:
            general_text = ''
        conn = db.conn()
        if Project.check_finish(conn, int(pid)):
            conn.close()
            return {'message': 'The project has been finished.'}, 400
        new_apply = Application(int(pid), int(rid), collaborator_id,general_text=general_text).create(conn)
        if new_apply == None:
            conn.close()
            return {'message': 'apply role duplicate'}, 400
        if new_apply == {}:
            conn.close()
            return {'message': 'All collaborators have been recruited'}, 400
        if new_apply == {'This project is not activated': 1}:
            conn.close()
            return {'message': 'This project is not activated'}, 400
        new_apply.notify_owner(conn, smtp)
        new_apply.notify_applicant(conn, smtp)
        conn.close()
        return {'message': 'role apply success', 'project_id': int(pid),'project_role_id': int(rid), 'apply_id': new_apply.info()['id']}, 200

@api.route('/project/<int:pid>/role/<int:rid>/application/<int:aid>')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
@api.param('aid', 'The application id')
class ViewSingleApplication(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'Application not found')
    @api.doc(description=' View applications for each role')
    @require_auth
    def get(self, pid,rid,aid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        conn = db.conn()
        if not Project.check_owner(conn, pid, dreamer_id):
            conn.close()
            return {'message': 'You are not the owner of the project'}, 400
        result = Application.get_by_aid(conn, int(aid))
        conn.close()
        if result is None:
            return {'message': 'Application not found'}, 404
        return result, 200

@api.route('/project/<int:pid>/role/<int:rid>/applications')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
class ViewAllApplication(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'Application not found')
    @api.doc(description=' View applications for each role')
    @require_auth
    def get(self, pid,rid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        conn = db.conn()
        if not Project.check_owner(conn, pid, dreamer_id):
            conn.close()
            return {'message': 'You are not the owner of the project'}, 400
        result = Application.get_by_pid_rid(conn,int(pid),int(rid))
        conn.close()
        if result is None:
            return {'message': 'Application not found'}, 404
        return result, 200

    
@api.route('/project/<int:pid>/discussion/<int:did>')
@api.param('pid', 'The project id')
@api.param('did', 'The discussion id')
class ViewSingleDiscussion(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'Discussion not found')
    @api.response(405, 'Wrong project ID was given for the searching discussion!')
    @api.doc(description=' View single discussion for a project')
    @require_auth
    def get(self ,pid,did):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Dreamer' and userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as dreamer or collaborator'}, 401
        conn = db.conn()
        result = Discussion.get_by_did(conn,int(did))
        conn.close()
        if result is None:
            return {'message': 'Discussion not found'}, 404
        if result['projectID'] != pid:
            return {'message': 'Wrong project ID was given for the searching discussion!'}, 405
        return result, 200


@api.route('/project/<int:id>/discussions')
@api.param('id', 'The project id')
class ViewAllDiscussion(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'Discussion not found')
    @api.doc(description=' View all discussions for a project')
    @require_auth
    def get(self ,id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        if userinfo['role'] != 'Dreamer' and userinfo['role'] != 'Collaborator' :
            return {'message': 'You are not logged in as dreamer or collaborator'}, 401
        conn = db.conn()
        result = Discussion.get_by_pid(conn,int(id))
        conn.close()
        if result is None:
            return {'message': 'Discussion not found'}, 404
        return result, 200   

    
@api.route('/notification')
class ViewNotification(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'notification not found')
    @api.doc(description=' View notification for user')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        user_id = userinfo['id']
        user_role = userinfo['role']
        if user_role != 'Dreamer' and user_role != 'Collaborator':
            return {'message': 'You are not logged in as dreamer or collaborator'}, 401
        conn = db.conn()
        result = Discussion.get_notification_by_id(conn,int(user_id),user_role)
        conn.close()
        if result is None:
            return {'message': 'notification not found'}, 404
        return result, 200

@api.route('/project/<int:pid>/role/<int:rid>/application/<int:aid>/approve')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
@api.param('aid', 'The application id')
class ApproveAnApplication(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'Application not found')
    @api.doc(description='Approve an application')
    @require_auth
    def get(self, pid, rid, aid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        conn = db.conn()
        if not Project.check_owner(conn, int(pid), dreamer_id):
            conn.close()
            return {'message': 'You are not the owner of the project'}, 400
        if Project.check_finish(conn, int(pid)):
            conn.close()
            return {'message': 'The project has been finished.'}, 400
        result_1 = Application.get_by_aid(conn, int(aid))
        if result_1 is None:
            conn.close()
            return {'message': 'Application not found'}, 404
        result = Application.approve_an_application(conn, smtp, int(pid), int(rid), int(aid))
        conn.close()
        if result == 0:
            return {'message': 'This apploication has been declined already!'}, 400
        if result == 1:
            return {'message': 'This apploication has been approved already!'}, 400
        if result == 9:
            return {'message': 'The related project of this application has been finished.'}, 400
        if result == 88:
            return {'message': 'This project role has been fullfilled, no more collaborator needed!'}, 400
        if result['apply_status'] != 1:
            return {'message': 'Failed to approve an application'}, 400
        return {'message': 'Approve application successfully','Application':result}, 200

@api.route('/project/<int:pid>/role/<int:rid>/application/<int:aid>/decline')
@api.param('pid', 'The project id')
@api.param('rid', 'The project_role id')
@api.param('aid', 'The application id')
class DeclineAnApplication(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(404, 'Application not found')
    @api.doc(description='Decline an application')
    @require_auth
    def get(self, pid, rid, aid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        conn = db.conn()
        if not Project.check_owner(conn, pid, dreamer_id):
            conn.close()
            return {'message': 'You are not the owner of the project'}, 400
        if Project.check_finish(conn, int(pid)):
            conn.close()
            return {'message': 'The project has been finished.'}, 400
        result_1 = Application.get_by_aid(conn, int(aid))
        if result_1 is None:
            conn.close()
            return {'message': 'Application not found'}, 404
        result = Application.decline_an_application(conn, smtp, int(aid))
        conn.close()
        if result == 0:
            return {'message': 'This application has been declined already!'}, 400
        if result == 1:
            return {'message': 'This application has been approved already!'}, 400
        if result == 9:
            return {'message': 'The related project of this application has been finished.'}, 400
        if result == 88:
            return {'message': 'This project role has been fullfilled, no more collaborator needed!'}, 400
        if result['apply_status'] != 0:
            return {'message': 'Failed to decline an application'}, 400
        return {'message': 'Decline the application successfully','Application':result}, 200

@api.route('/project/<int:id>')
@api.param('id', 'The project id')
class GetProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(404, 'Project not found')
    @api.doc(description='Get project information')
    def get(self, id):
        conn = db.conn()
        result = Project.get_by_id(conn, int(id))
        conn.close()
        if result is None:
            return {'message': 'Requesting non-existing project information'}, 404
        return result, 200

    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Project is not in active status, no update is allowed!')
    @api.doc(description='Update the information of a project')
    @api.expect(project_patch_model, validate=True)
    @require_auth
    def patch(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        conn = db.conn()
        if not Project.check_owner(conn, int(id), dreamer_id):
            conn.close()
            return {'message': 'You are not the owner of the project'}, 400
        proj = Project.get_by_id(conn, int(id))
        if proj['status'] != 1:
            return {'message': 'This project is not in active status, no update is allowed!'}, 401            
        project_info = request.json
        cursor_project = Project.get_by_proj_id(conn, int(id))
        try:
            cursor_project.title = project_info['project_title']
        except:
            pass
        try:
            cursor_project.description = project_info['description']
        except:
            pass
        try:
            cursor_project.category = project_info['category']
        except:
            pass
        result = cursor_project.patch(conn).info()
        conn.close()
        return {'message': 'Patch success', 'info': result}, 200

@api.route('/project/<int:id>/discussionAboutOneProject')
@api.param('id', 'The project id')
class GetDiscussionAboutOneProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'No discussion records')
    @api.doc(description='Get discussion records about one project')
    def get(self, id):
        conn = db.conn()
        result = Project.get_discussion_about_one_project(conn, int(id))
        conn.close()
        if result:
            return result, 200
        else:
            return {'message': 'No discussion records found about this project'}, 400

@api.route('/project/<int:id>/discussionAboutFollowedProjects')
@api.param('id', 'The project id')
class GetDiscussionAboutFollowedProjects(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'No discussion records')
    @api.doc(description='Get discussion records about one project')
    @require_auth
    def get(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        user_id = userinfo['id']
        conn = db.conn()
        if userinfo['role'] == 'Dreamer':
            result = Project.get_discussion_about_followed_projects(conn, 'Dreamer', user_id)
        else:
            result = Project.get_discussion_about_followed_projects(conn, 'Collaborator', user_id)
        conn.close()
        if result:
            return result, 200
        else:
            return {'message': 'No discussion records found about your followed project'}, 400

        
@api.route('/project/<int:id>/discussion')
@api.param('id', 'The project id')
class PostDiscussion(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(402, 'Project not found')
    @api.doc(description='Post a discussion for a project')
    @api.expect(post_discussion_model, validate=True)
    @require_auth
    def post(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        user_id = userinfo['id']
        if userinfo['role'] != 'Dreamer' and userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as dreamer or collaborator'}, 401
        discussion_info = request.json
        discuss_content = discussion_info['discuss_content']
        parent_id = discussion_info['parent_id']
        conn = db.conn()
        if userinfo['role'] == 'Dreamer':
            if Project.check_owner(conn, int(id), user_id):
                new_discuss = Discussion(int(id),parent_id,is_dreamer = 2,d_author = user_id,text = discuss_content).create_by_dreamer(conn)
            else:
                new_discuss = Discussion(int(id),parent_id,is_dreamer = 1,d_author = user_id,text = discuss_content).create_by_dreamer(conn)
        else:
            new_discuss = Discussion(int(id),parent_id,is_dreamer = 0,c_author = user_id,text = discuss_content).create_by_collaborator(conn)
        if new_discuss == None:
            conn.close()
            return {'message': 'Project not found'}, 402
        discussion_id = new_discuss.info()['id']
        if new_discuss.info()['is_dreamer'] == 2:
            role = 'owner of this project'
        elif new_discuss.info()['is_dreamer'] == 1:
            role = 'other dreamer'
        else:
            role = 'collaborator'
        conn.close()
        return {'message': 'post discussion success', 'project_id': int(id), 'parent_discussion_id': parent_id, 'discussion_id': discussion_id,'post_by':role,'post_time':new_discuss.info()['create_time']}, 200

@api.route('/project/<int:id>/role')
@api.param('id', 'The project id')
class PostRole(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Post a new role for the project')
    @api.expect(role_post_model, validate=True)
    @require_auth
    def post(self, id):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        conn = db.conn()
        if not Project.check_owner(conn, int(id), dreamer_id):
            conn.close()
            return {'message': 'You are not the owner of the project'}, 400
        role_info = request.json
        try:
            general_enquiry = role_info['general_enquiry']
        except:
            general_enquiry = ''
        skills = [int(i.strip()) for i in role_info['skill'].split(',') if i != '']
        new_role = Role(int(id), role_info['title'], role_info['amount'], skills, role_info['experience'], role_info['education'], general_enquiry=general_enquiry).create(conn)
        conn.close()
        if new_role == None:
            return {'message': 'role create duplicate'}, 400
        return {'message': 'role create success', 'project_id': int(id), 'role_id': new_role.info()['id']}, 200

@api.route('/project/<int:pid>/role/<int:rid>')
@api.param('pid', 'The project id')
@api.param('rid', 'The role id')
class PatchRole(CorsResource):
    @api.response(200, 'Success')
    @api.response(404, 'Role is not found!')
    @api.doc(description='Fetch a role information')
    def get(self, pid, rid):
        conn = db.conn()
        result = Role.get_by_id(conn, int(rid))
        if result == None:
            return {'message': 'Role is not found!'}, 404
        return result, 200

    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.response(402, 'Project is not in active status, no update is allowed!')
    @api.response(403, 'Project is not found!')
    @api.doc(description='Update a role information')
    @api.expect(role_patch_model, validate=True)
    @require_auth
    def patch(self, pid, rid):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        conn = db.conn()
        if not Project.check_owner(conn, int(pid), dreamer_id):
            conn.close()
            return {'message': 'You are not the owner of the project'}, 400
        if Project.check_finish(conn, int(pid)):
            conn.close()
            return {'message': 'The project has been finished.'}, 401
        role_info = request.json
        cursor_role = Role.get_object_by_id(conn, int(rid))
        try:
            cursor_role.title = role_info['title']
        except:
            pass
        try:
            cursor_role.amount = role_info['amount']
        except:
            pass
        try:
            skills = [int(i.strip()) for i in role_info['skill'].split(',') if i != '']
            cursor_role.skill = skills
        except:
            pass
        try:
            cursor_role.experience = role_info['experience']
        except:
            pass
        try:
            cursor_role.education = role_info['education']
        except:
            pass
        try:
            cursor_role.general_enquiry = role_info['general_enquiry']
        except:
            pass
        result = cursor_role.patch(conn).info()
        conn.close()
        if result == None:
            return {'message': 'This project is not found!', 'info': result}, 403
        if result == 99:
            return {'message': 'This project is not in active status, no update is allowed!', 'info': result}, 402
        return {'message': 'Patch success', 'info': result}, 200

@api.route('/collaborator/patch')
class PatchCollaborator(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Update a collaborator information')
    @api.expect(collaborator_patch_model, validate=True)
    @require_auth
    def patch(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        collaborator_id = userinfo['id']
        conn = db.conn()
        if userinfo['role'] != 'Collaborator':
            conn.close()
            return {'message': 'You are not logged in as collaborator'}, 400
        collaborator_info = request.json
        cursor_collaborator = Collaborator.get_object_by_id(conn, int(collaborator_id))
        skills = collaborator_info['skill'].split(',')
        skills = [0 if i=="" else int(i.strip()) for i in skills]
        exps = collaborator_info['experience'].split(',')
        exps = [0 if i=="" else int(i.strip()) for i in exps]
        try:
            cursor_collaborator.phone_no = collaborator_info['phone_no']
        except:
            pass
        try:
            cursor_collaborator.education = collaborator_info['education']
        except:
            pass
        try:
            skill_dict = {i: j for i,j in zip(skills,exps)}
            cursor_collaborator.skill_dict = skill_dict
        except:
            pass
        result = cursor_collaborator.patch(conn).info_2()
        conn.close()
        return {'message': 'Patch success', 'info': result}, 200
    
    
@api.route('/project')
class PostProject(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Post a new project')
    @api.expect(project_post_model, validate=True)
    @require_auth
    def post(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        project_info = request.json
        conn = db.conn()
        new_project = Project(project_info['title'], project_info['description'], dreamer_id, project_info['category']).create(conn)
        conn.close()
        if new_project == None:
            return {'message': 'project create request duplicate'}, 400
        return {'message': 'project create success', 'project_id': new_project.info()['id']}, 200

@api.route('/collaborator/my_follows_id')
class CollaboratorFollowsID(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Get a list of followed projects id')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        collaborator_id = userinfo['id']
        if userinfo['role'] != 'Collaborator':
            return {'message': 'You are not logged in as collaborator'}, 401
        conn = db.conn()
        follow_list = Collaborator.get_follow_ids(conn, collaborator_id)
        conn.close()
        return {'follows': follow_list}, 200
        

@api.route('/dreamer/my_follows_id')
class DreamerFollowsID(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Get a list of followed projects id')
    @require_auth
    def get(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        dreamer_id = userinfo['id']
        if userinfo['role'] != 'Dreamer':
            return {'message': 'You are not logged in as dreamer'}, 401
        conn = db.conn()
        follow_list = Dreamer.get_follow_ids(conn, dreamer_id)
        conn.close()
        return {'follows': follow_list}, 200

@api.route('/collaborator/register')
class CollaboratorRegister(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Register Failed')
    @api.doc(description='Register a new collaborator')
    @api.expect(collaborator_register_model, validate=True)
    def post(self):
        register_info = request.json
        name = register_info['name']
        email = register_info['email']
        if not check_email(email):
            return {'message': 'Email not valid.'}, 400
        conn = db.conn()
        if Collaborator.is_email_exist(conn, email):
            conn.close()
            return {'message': 'Email already registered.'}, 400
        password = register_info['password']
        if password != register_info['repeat_password']:
            conn.close()
            return {'message': 'Passwords not match.'}, 400
        try:
            phone_no = register_info['phone_no']
        except:
            phone_no = ''
        try:
            education = register_info['education']
        except:
            education = -1
        skill_dict = {}
        try:
            skills = register_info['skills'].split(',')
            skills = [0 if i=="" else int(i.strip()) for i in skills]
            exps = register_info['experience'].split(',')
            exps = [0 if i=="" else int(i.strip()) for i in exps]
            print(skills, exps)
            if not (len(skills) == len(exps)): return {'message': 'Skills and experience have different length.'}, 400
            for i in range(len(skills)):
                skill_dict[skills[i]]=exps[i]
        except:
            skill_dict = {}
        print(skill_dict)
        Collaborator(name, email, password_plain=password, phone_no=phone_no, education=education, skill_dict=skill_dict).commit(conn)
        conn.close()
        return {'message': 'Register success'}, 200

@api.route('/dreamer/register')
class DreamerRegister(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Register Failed')
    @api.doc(description='Register a new dreamer')
    @api.expect(dreamer_register_model, validate=True)
    def post(self):
        register_info = request.json
        name = register_info['name']
        email = register_info['email']
        if not check_email(email):
            return {'message': 'Email not valid.'}, 400
        conn = db.conn()
        if Dreamer.is_email_exist(conn, email):
            return {'message': 'Email already registered.'}, 400
        password = register_info['password']
        if password != register_info['repeat_password']:
            return {'message': 'Passwords not match.'}, 400
        try:
            phone_no = register_info['phone_no']
        except:
            phone_no = ''
        Dreamer(name, email, password_plain=password, phone_no=phone_no).commit(conn)
        conn.close()
        return {'message': 'Register success'}, 200

@api.route('/login')
class Login(CorsResource):
    @api.response(200, 'Success')
    @api.response(401, 'Login Failed')
    @api.doc(description='Login with email and password, receive an auth token')
    @api.expect(login_model, validate=True)
    def post(self):
        login_info = request.json
        email = login_info['email']
        password = login_info['password']
        # try login based on role
        role = login_info['role']
        conn = db.conn()
        if role == 'Admin':
            user = Admin.login(conn, email, password)
        elif role == 'Dreamer':
            user = Dreamer.login(conn, email, password)
        elif role == 'Collaborator':
            user = Collaborator.login(conn, email, password)
        conn.close()
        # login failed
        if user is None:
            return {'message': 'Login failed for incorrect credentials.'}, 401
        else:
            token = auth.token(user).decode()
            return {'token': token, 'role': user['role'], 'id': user['id'], 'name': user['name']}, 200

@api.route('/changepassword')
class ChangePassword(CorsResource):
    @api.response(200, 'Success')
    @api.response(400, 'Validate Failed')
    @api.response(401, 'Auth Failed')
    @api.doc(description='Change your password')
    @api.expect(change_password_model, validate=True)
    @require_auth
    def post(self):
        token = request.headers.get('AUTH_KEY')
        userinfo = auth.decode(token)
        role = userinfo['role']
        email = userinfo['email']
        password_info = request.json
        original_password = password_info['original_password']
        new_password = password_info['new_password']
        if original_password == new_password:
            return {'message': 'new password should be different'}, 400
        conn = db.conn()
        if role == 'Admin':
            if not Admin.check_password(conn, email, original_password):
                return {'message': 'Your original_password is incorrect'}, 400
            Admin.commit_newpassword(conn,email,new_password)
        elif role == 'Dreamer':
            if not Dreamer.check_password(conn, email, original_password):
                return {'message': 'Your original_password is incorrect'}, 400
            Dreamer.commit_newpassword(conn,email,new_password)
        elif role == 'Collaborator':
            if not Collaborator.check_password(conn, email, original_password):
                return {'message': 'Your original_password is incorrect'}, 400
            Collaborator.commit_newpassword(conn,email,new_password)
        conn.close()
        return {'message': 'change password success'}, 200


if __name__ == '__main__':
    smtp = SMTP()
    db = DB()
    app.run(debug=True, host='0.0.0.0')
