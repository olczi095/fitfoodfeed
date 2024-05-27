# FitFoodFeed
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white])

**FitFoodFeed is a Django-based web application** (Django e-commerce website project) focused on fit food products, promoting a healthy and active lifestyle.  

### Current Segments:
- 📝 a blog designed for food reviews

### Upcoming Segments:
- 🛒 e-commerce platform
- 👩‍💻 mini social networking site
  
The implementation incorporates type hints and unit tests written with unittest, but the tests will be modified with Faker and Factory Boy.

<br />

#### Project History
The code has been written according to TDD principles since commit 5acc9d4 from 19-07-23 until commit 2d9586a from 20-11-23

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

### **<p align="center">HOMEPAGE</p>**

![homepage](https://github.com/olczi095/fitfoodfeed/assets/114907948/0be93307-f056-4023-acc0-eda1986791b5)
![homepage2](https://github.com/olczi095/fitfoodfeed/assets/114907948/b1f3e121-67db-4669-beec-bda4b5c84b69)
<br /><br />

### **<p align="center">HOMEPAGE IN DARK MODE</p>**

![homepage-darkmode](https://github.com/olczi095/fitfoodfeed/assets/114907948/d5fd3359-dd33-46bb-b40c-212dc538846d)
![homepage2-darkmode](https://github.com/olczi095/fitfoodfeed/assets/114907948/5b4bb44c-d617-44f5-8412-9e0fcb560235)
<br /><br />

### **<p align="center">PAGE WITH CUSTOM REVIEW</p>**
   <p align="center">Click on tags to navigate, view related posts, and participate in the comment section.</p>
   
![review-detail](https://github.com/olczi095/fitfoodfeed/assets/114907948/5def7be2-43fc-4dcc-95c7-b9d48922560c)
<br /><br />
  <p align="center">Smart multilevel Commenting System (non-superuser comments require approval).</p>
  
![comment-section](https://github.com/olczi095/fitfoodfeed/assets/114907948/a3698ddc-3229-4824-974e-4e40bbf65b2f)
<br /><br />

### **<p align="center">MAIN PAGE FOR AUTHORS</p>**
   <p align="center">Featuring additional functionalities like edit and delete buttons for reviews.</p>
   
![homepage-for-authors](https://github.com/olczi095/fitfoodfeed/assets/114907948/56894399-0fdb-4521-8198-88850c11fafd)
<br /><br />


### **<p align="center">UPDATE REVIEW FORM</p>**
   <p align="center">One of the available review forms for authors</p>
   
![review-edit-form](https://github.com/olczi095/fitfoodfeed/assets/114907948/beb27b88-4350-4df1-8a22-4754fb5dd0c1)
<br /><br />


### **<p align="center">REGISTRATION FORM</p>**
  
![registration-form](https://github.com/olczi095/fitfoodfeed/assets/114907948/82bfa61d-b834-4630-bfc3-e7960cca763a)
<br /><br />


### **<p align="center">ADMIN PANEL (POST)</p>**
   <p align="center">Default admin panel page for the Post model with associated, clickable and linked Author, Category and Tags models</p>
   
![adminpanel](https://github.com/olczi095/fitfoodfeed/assets/114907948/64b186fb-5cd0-4811-b9d3-f18902963fa3)
<br /><br />


## Authors

- [@olczi095](https://github.com/olczi095/olczi095)

✌️ If you have any ideas for improving or modifying my project, feel free to contact me.


### Icon Attribution

The icons used in this project were created by [mim_studio](https://www.flaticon.com/authors/mim-studio) from [Flaticon](https://www.flaticon.com/), and are available under the [CC BY 3.0](http://creativecommons.org/licenses/by/3.0/) license.
