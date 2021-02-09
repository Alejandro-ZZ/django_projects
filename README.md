# Django web applications

Online web sites using Django and the service of PythonAnywhere so that it is available over the Internet. In this applications the following features are involved:

**1.** Usage of sqlite3 database through Object-Relational Mapping (ORM) access which is implemented with model objects of Django.

**2.** Database modeling, including one-to-many and many-to-many relationships.

**3.** Usage of cookies, sessions, and authentication processes.

**4.** Navigation into the Django applications with some crispy forms to make advanced/custom forms rendering.

**5.** Basic code of JavaScript and the Jquery library used for in-browser manipulation of the Document Object Model (DOM) and event handling.

**6.** Usage of JavaScript Object Notation (JSON) used as a syntax to exchange data between code running on the Django server and code running in the browser (JavaScript/jQuery).

## Runing in your PC

**1. Clone the repository** <br/>
Open a bash/command console where you want to save the copy of this repository, clone it and open the folder.

    git clone https://github.com/Alejandro-ZZ/django_projects.git
    cd django_projects  
    
**2. Install requirements**

    pip install -r requirements.txt
    python manage.py check

`manage.py check` uses the system check framework to inspect the entire Django project for common problems. By default, all apps will be checked. This is the normal output of running check:

    System check identified no issues (0 silenced).

If the check identifies errors, stop until there are no errors. 

**3. Migrations**<br/>
Only take the next steps once check sees no errors. Once the check works do:

    python manage.py makemigrations

Then run:

    python manage.py migrate
