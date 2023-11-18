# FitFoodFeed
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white])

**FitFoodFeed is a Django-based web application** focused on fit food products, promoting a healthy and active lifestyle.  

### Current Segments:
- 📝 a blog designed for food reviews

### Upcoming Segments:
- 🛒 e-commerce platform
- 👩‍💻 mini social networking site
  
The implementation incorporates type hints and unit tests written with unittest, but the tests will be modified with Faker and Factory Boy.

_The code has been written according to TDD principles since commit 5acc9d4 from 19-07-23_

## Features
<br />

- **User Accounts** - registration and authentication, login/logout.
- **Enhanced User Profile** - fields include an avatar (code has validators for it).
- **Blog Reviews Management** - forms for creating, updating and deleting blog reviews, available only for the author of the particular review or admins.
- **Review Models** - each review can be associated with categories and tags, used in navbars and some other website sections.
- **Like Button for Reviews** - created with AJAX, fully accessible for authenticated users, read-only for unauthenticated users.
- **Comments Section** - default name for guests, automatically connected with authenticated users for a more convenient and nicer usage.
- **Responsive Styles for Screens** - different styles for various screen sizes.
<br />

## Requirements

This project is developed with **Python 3.11.4**.

_While it may work with lower Python versions, it's recommended to use Python 3.11.4 for optimal compatibility. Using versions below Python 3.6 is not guaranteed to work properly._

## Installation
**Note:** Depending on your operating system, you may need to use `python3` instead of `python` - mainly on MacOS and Linux.
<br />
<br/>

1. **Clone the Repository and navigate to the project directory**
```bash
git clone https://github.com/olczi095/fitfoodfeed.git
cd fitfoodfeed
```
<br />

2. **Create and activate Virtual Environment(optional):**
```bash
python -m venv venv  # or your own venv name

# On MacOS and Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```
<br />

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```
Optionally, install additional developer dependencies:
    
```bash
pip install -r requirements-dev.txt
```
<br />

4. **Configure Environment Variables:**

Create an ".env" file with your unique secret key and set DEBUG to "True" or "False":

```bash
SECRET_KEY=your_unique_secret_key_here
# Generate your unique secret key, for instance using get_random_secret_key() from django.core.management.utils

DEBUG=true_or_false
# Set to "True" for development mode with detailed errors pages.
```
<br />

5. **Apply Migrations for initialize database:**

```bash
python manage.py migrate
```
<br />

6. **Create a Superuser for admin panel access:**

```bash
python manage.py createsuperuser
```
<br />

7. **Run Development Server:**

```bash
python manage.py runserver
```
<br />


**The website will be available in browsers at:**

```bash
http://localhost:8000/
```

## Screenshots

**<p align="center">MAIN PAGE</p>**

![main-page](https://github.com/olczi095/fitfoodfeed/assets/114907948/512ba949-1c2c-44ff-81c3-fb8c527b9c4e)
![main-page2](https://github.com/olczi095/fitfoodfeed/assets/114907948/52a96833-52c7-4aef-bcc0-aa427199e578)
<br /><br />

**<p align="center">PAGE WITH CUSTOM REVIEW</p>**
   <p align="center">Click on tags to navigate, view related posts, and participate in the comment section.</p>
   
![review](https://github.com/olczi095/fitfoodfeed/assets/114907948/a2124689-2dbc-4106-8ce7-17e60b458760)
<br /><br />


**<p align="center">MAIN PAGE FOR AUTHORS</p>**
   <p align="center">Featuring additional functionalities like edit and delete buttons for reviews.</p>
   
![page-for-authors](https://github.com/olczi095/fitfoodfeed/assets/114907948/6644ba8a-aba1-44ef-964f-b65484da4b6f)
<br /><br />


**<p align="center">UPDATE REVIEW FORM</p>**
   <p align="center">One of the available review forms for authors</p>
   
![edit-review](https://github.com/olczi095/fitfoodfeed/assets/114907948/b01d5676-7437-4b9b-ad8b-de1d5a1f34e0)
<br /><br />


**<p align="center">REGISTRATION FORM</p>**
  
![registration](https://github.com/olczi095/fitfoodfeed/assets/114907948/424212d5-7753-40d3-bba3-9fb233df2ac7)
<br /><br />


**<p align="center">ADMIN PANEL (POST)</p>**
   <p align="center">Default admin panel page for the Post model with associated, clickable and linked Author, Category and Tags models</p>
   
![admin-panel](https://github.com/olczi095/fitfoodfeed/assets/114907948/a945c4fa-14a6-47e7-b41b-dabadc74e035)
<br /><br />


## Authors

- [@olczi095](https://github.com/olczi095/olczi095)

✌️ If you have any ideas for improving or modifying my project, feel free to contact me.
