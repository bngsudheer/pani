from pani import db
from pani.model.user import User
from pani.model.project import Project

class UserProject(db.Model):
    __tablename__ = 'users_projects'

    user_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, primary_key=True)


    def get_choices_form(self, user_id):
        """Return the choices list suitable to inject as default values in 
        the form.
        """
        user_projects = db.session.query(
                    UserProject, 
                    Project.id, 
                    Project.name).\
                filter(UserProject.user_id==user_id).\
                join(Project, Project.id==UserProject.project_id)
        items = []
        for row in user_projects:
            items.append((row.id, row.name))


        return items

    @classmethod
    def get_project_users_choices_form(cls, user_id):
        """Return the choices list suitable to inject as default values in 
        the form.
        """
        user_projects = db.session.query(
                    UserProject, 
                    User.id, 
                    User.username).\
                filter(UserProject.user_id==user_id).\
                join(User, User.id==UserProject.user_id)
        items = []
        for row in user_projects:
            items.append((row.id, row.username))


        return items






    def get_project_ids(self, user_id):
        """Return the list of project IDs for the given user ID.
        """
        
        items = []
        for row in self.get_projects(user_id):
            items.append(row.id)

        return items


    def get_user_ids(self, project_id):
        """Return the list of User IDs for the given user ID.
        """
        
        items = []
        for row in self.get_users_by_project_id(project_id):
            items.append(row.id)

        return items

    def get_users_by_project_id(self, project_id):
        user_projects = db.session.query(
                    UserProject, 
                    User.id, 
                    User.username).\
                join(User, User.id==UserProject.user_id).\
                filter(UserProject.project_id == project_id)


        return user_projects
 

    def get_projects(self, user_id):
        user_projects = db.session.query(
                    UserProject, 
                    Project.id, 
                    Project.name).\
                join(Project, Project.id==UserProject.project_id).\
                filter(UserProject.user_id == user_id)


        return user_projects
    
