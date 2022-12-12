/* Skills and Knowledge Assessment Database
   Database definition for SQLite3
*/

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS levels (
    id INTEGER PRIMARY KEY ASC,
    weight INT NOT NULL UNIQUE,
    level TEXT NOT NULL UNIQUE,
    description TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS hardware (
    id INTEGER PRIMARY KEY ASC,
    product TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS software (
    id INTEGER PRIMARY KEY ASC,
    product TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS processes (
    id INTEGER PRIMARY KEY ASC,
    process TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tasks_hw (
    id INTEGER PRIMARY KEY ASC,
    task TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tasks_sw (
    id INTEGER PRIMARY KEY ASC,
    task TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY ASC,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skills_hw (
    id INTEGER PRIMARY KEY ASC,
    timestamp TEXT,
    employee INT NOT NULL,
    product INT NOT NULL,
    task INT NOT NULL,
    level INT NOT NULL,
    FOREIGN KEY (employee) REFERENCES employees(id),
    FOREIGN KEY (product) REFERENCES hardware(id),
    FOREIGN KEY (task) REFERENCES tasks_hw(id),
    FOREIGN KEY (level) REFERENCES levels(id)
);

CREATE TABLE IF NOT EXISTS skills_sw (
    id INTEGER PRIMARY KEY ASC,
    timestamp TEXT,
    employee INT NOT NULL,
    product INT NOT NULL,
    task INT NOT NULL,
    level INT NOT NULL,
    FOREIGN KEY (employee) REFERENCES employees(id),
    FOREIGN KEY (product) REFERENCES software(id),
    FOREIGN KEY (task) REFERENCES tasks_sw(id),
    FOREIGN KEY (level) REFERENCES levels(id)
);

CREATE TABLE IF NOT EXISTS skills_pr (
    id INTEGER PRIMARY KEY ASC,
    timestamp TEXT,
    employee INT NOT NULL,
    process INT NOT NULL,
    level INT NOT NULL,
    FOREIGN KEY (employee) REFERENCES employees(id),
    FOREIGN KEY (process) REFERENCES processes(id),
    FOREIGN KEY (level) REFERENCES levels(id)
);

INSERT INTO levels VALUES
(NULL, 0, "None", "Have no knowledge on product, technology or process"),
(NULL, 1, "Basic", "Have general knowledge on product, technology or process; can follow prepared instructions"),
(NULL, 2, "Middle", "Have experience with product, technology or process; can find instructions and follow them"),
(NULL, 3, "Professional", "Navigate freely in product, technology or process; can provide instructions and advise to customer"),
(NULL, 4, "Expert", "Know all quircks of product, technology or process; can provide instructions, advise to customer and deliver trainings");
