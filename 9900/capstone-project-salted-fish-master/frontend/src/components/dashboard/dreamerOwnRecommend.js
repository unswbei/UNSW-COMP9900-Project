import React from "react";
import { Redirect } from "react-router-dom";
import { Link } from "react-router-dom";
import { connect } from "react-redux";

class DreamerOwnRecommend extends React.Component {
  render() {
    if (!this.props.isAuthenticated) {
      return <Redirect to="/login" />;
    }
    if (this.props.authRole !== "Dreamer") {
      return <Redirect to="/colladash" />;
    }

    const skill_list = [
      "Web Development",
      "Java",
      "Python",
      "PHP",
      "Script Language",
      "Database Management",
      "Computer Vision",
      "Security Engineering",
      "Testing",
      "Algorithm Design",
      "Operating System",
      "Data Science",
      "Human Computer Interaction",
      "Deep Learning/Neural Network",
      "Distribution System",
    ];

    const education_list = ["Other", "Bachelor", "Master", "Phd"];
    const url =
      "https://source.unsplash.com/collection/" +
      Math.floor(Math.random() * 200) +
      "/800x600";
    const projectUrl = "./projects/" + this.props.each.Project_ID;

    return (
      <div className="row">
        <div className="col s12 m12 l12">
          <div className="card horizontal small">
            <div className="card-stacked">
              <div className="card-content" style={{ overflowY: "scroll" }}>
                <h4>
                  <Link to={projectUrl}>{this.props.each.Project_title}</Link>
                </h4>
                {this.props.each.Role_recomm_collabors_list.map(
                  (res, index) => {
                    return (
                      <div key={index}>
                        <p style={{ fontFamily: "Cherry Swash" }}>
                          Form your requirements,
                          <br /> Skill:{skill_list[res.Skill-1]}, Title:
                          {res.Title}
                        </p>
                        <p style={{ fontFamily: "Cherry Swash" }}>
                          experience: at least {res.Experience} years,
                          Education:
                          {education_list[res.Education - 1]},
                        </p>

                        {res.Collaborator_list.length > 0 ? (
                          res.Collaborator_list.map((colla, index) => {
                            const collaboratorUrl =
                              "/project/" +
                              this.props.each.Project_ID +
                              "/role/" +
                              res.Role_ID +
                              "/collaborators/" +
                              colla.CollaboratorID;

                            return (
                              <div
                                key={index}
                                className="collection"
                                style={{ transform: "scale(1)" }}
                              >
                                <Link
                                  to={collaboratorUrl}
                                  className="collection-item"
                                >
                                  {colla.Name}
                                </Link>
                              </div>
                            );
                          })
                        ) : (
                          <p style={{ fontFamily: "Bungee" }}>
                            NO Recommendation yet
                          </p>
                        )}
                        <br></br>
                      </div>
                    );
                  }
                )}
              </div>
            </div>

            <div className="card-image right">
              <img src={url} />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  authRole: state.auth.role,
  isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, null)(DreamerOwnRecommend);
