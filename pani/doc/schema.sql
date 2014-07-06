CREATE TABLE users (
    id INTEGER PRIMARY KEY ASC,
    username TEXT NOT NULL,
    password TEXT NULL,
    public_key TEXT NULL
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY ASC,
    name TEXT NOT NULL,
    description TEXT NULL
);

CREATE TABLE users_projects (
    user_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    PRIMARY KEY(user_id, project_id)
);


/* Default data
*/
INSERT INTO users (username, password) VALUES ('admin', 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86');


