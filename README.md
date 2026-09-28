# CommDir — Community Directory

A membership management web app for organizing community records by family — built for use cases like a church/parish membership directory. Tracks members grouped into families, each with a registration number and shared family login, with separate admin and member access levels.

## Features

**Admin**
- Register new families and add/edit member records
- View the full member directory
- Activate / deactivate members
- Reset member passwords
- Change their own password

**Member**
- View the member directory
- Change their own password

Member records include registration number, name, family name, zone/unit, address, and active/inactive status. Admins and members log in through separate portals with separate credentials.

## Tech Stack

- Python 3 / [Flask](https://flask.palletsprojects.com/)
- SQLite (via `cs50`'s `SQL` wrapper) — table: `members`
- `flask-session` for server-side sessions
- `werkzeug.security` for password hashing
- Jinja2 templates + plain CSS for the UI

This follows the structure of a CS50-style Flask project (`helpers.py` provides `apology`, `login_required`, `lookup`, and `usd` helpers).

## Structure

```
application.py        # Flask app: routes for index, login, register, directory, editing, etc.
helpers.py             # apology(), login_required, lookup(), usd()
styles.css

homepage.html
register.html
logina.html / loginm.html         # admin / member login
layouta.html / layoutm.html       # admin / member page layout
layoutn.html / layoutv.html
directory.html / directorym.html  # directory views
portfolioa.html / portfoliom.html # admin / member profile ("portfolio") pages
add.html / edit.html / editor.html
change_password_a.html / change_password_m.html
deactivate.html
apology.html
```

## Setup

```bash
pip install flask flask-session cs50 werkzeug
```

The app expects a SQLite database at `members.db` with a `members` table (columns referenced in `application.py` include `RegnNo`, `MemberId`, `Name`, `DateofBirth`, `FamilyName`, `Password`, address, zone/unit, and status fields) — this schema needs to be created before first run, as the `.db` file isn't checked into the repo.

Run the app with Flask's development server:

```bash
export FLASK_APP=application.py
flask run
```

## Note

Field names in the registration form (native diocese, native parish, family unit) reflect the specific community this was originally built for; adapt the schema/forms if reusing for a different organization.
