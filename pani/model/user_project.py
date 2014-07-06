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


    def get_project_ids(self, user_id):
        """Return the list of project IDs for the given user ID.
        """

        user_projects = db.session.query(
                    UserProject, 
                    Project.id, 
                    Project.name).\
                join(Project, Project.id==UserProject.project_id).\
                filter(UserProject.user_id == user_id)

        items = []
        for row in user_projects:
            items.append(row.id)


        return items


    