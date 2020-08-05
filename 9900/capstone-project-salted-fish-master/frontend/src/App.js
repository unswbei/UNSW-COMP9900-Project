import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import HomePage from "./components/layout/HomePage";
import Narvbar from "./components/layout/Narvbar";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import Dashboard from "./components/dashboard/Dashboard";
import CreateProject from "./components/projects/createProject";
import Alert from "./components/layout/alert";
import AdminDash from "./components/dashboard/adminDash";
import AddRoleProject from "./components/projects/addRoleProject";
import ProjectList from "./components/projects/projectList";
import DreamerRecommend from "./components/dashboard/dreamerRecommend";
import projectDetails from "./components/projects/projectDetails";
import DreamerCollasCard from "./components/dashboard/dreamerCollasCard";
import ChangeRoleDetails from "./components/projects/changeRoleDetails";
import CollaProjectList from "./components/dashboard/collaProjectList";
import CollaDash from "./components/dashboard/collaDash";
import CollaOwnRecommend from "./components/dashboard/collaOwnRecommend";
import Card from "./components/dashboard/test";
import ApplicationsCard from "./components/projects/applicationsCard";
import JoinedCollaCard from "./components/projects/joinedCollaCard";
import CollaInvited from "./components/dashboard/collaInvited";
import CollaInfo from "./components/dashboard/collaInfo";
import DreamerCard from "./components/dashboard/dreamerCard";
import CollaApply from "./components/dashboard/collaApply";
import DreamerOwnCard from "./components/dashboard/dreamerOwnCard";
import ChangeProject from "./components/projects/changeProject";
import ReactApp from "./com/ReactApp"
import CollaPatch from "./components/dashboard/collaPatch";

function App() {
  return (
    <Router>
      <Narvbar />
      <Route exact path="/" component={HomePage} />
      <Alert />
      <Switch>
        <Route exact path="/dashboard" component={Dashboard} />
        <Route exact path="/colladash" component={CollaDash} />
        <Route exact path="/collaproject" component={CollaProjectList} />
        <Route exact path="/drecommend" component={DreamerRecommend} />
        <Route exact path="/crecommend" component={CollaOwnRecommend} />
        <Route exact path="/apply" component={CollaApply} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/register" component={Register} />
        <Route exact path="/create" component={CreateProject} />
        <Route exact path="/project/:id/role" component={AddRoleProject} />
        <Route exact path="/projects" component={ProjectList} />
        <Route exact path="/invited" component={CollaInvited} />
        <Route exact path="/cinfo" component={CollaInfo} />
        <Route exact path="/collapatch" component={CollaPatch}/>
        <Route exact path="/change/:id" component={ChangeProject} />
        <Route exact path="/dreamer/:id" component={DreamerCard} />
        <Route exact path="/dinfo" component={DreamerOwnCard} />
        <Route exact path="/comment" component={ReactApp} />
        <Route
          exact
          path="/project/:pid/role/:rid/collaborators/:cid/applications/:aid"
          component={ApplicationsCard}
        />
        <Route
            exact
            path="/project/:pid/role/:rid/collaborators/:cid/joined/:aid"
            component={JoinedCollaCard}
        />
        <Route exact path="/admindash" component={AdminDash} />
        <Route
          exact
          path="/project/:pid/role/:rid"
          component={ChangeRoleDetails}
        />
        <Route exact path="/projects/:id" component={projectDetails} />
        <Route
          exact
          path="/project/:pid/role/:rid/collaborators/:cid"
          component={DreamerCollasCard}
        />
        <Route exact path="/test" component={Card} />
      </Switch>
    </Router>
  );
}

export default App;
