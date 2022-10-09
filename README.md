# Customer Relationship Management System

Customer Relationship Management System for a small/meduim sales team. Allowing them to track key customer contacts and record their individual sales, giving management/admins further insight into the teams performance.

<div>
  <p>
    <a href="https://github.com/SeanConroy01/qa-application/issues">Report Bug</a>
    ·
    <a href="https://github.com/SeanConroy01/qa-application/issues">Request Feature</a>
  </p>
</div>


## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [License](#license)
- [Support](#support)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## Prerequisites

This project requires Python. Install instructions can be found below:

- [Python](https://www.python.org/downloads/)

**Note:** If you are new to Python, you may find
[Learn Python - Full Course for Beginners](https://www.youtube.com/watch?v=rfscVS0vtbw)
helpful for learning the basics. Alternatively, here is an excellent Udemy course that I used to learn Python - [100 Days of Code: The Complete Python Pro Bootcamp for 2022)](https://www.udemy.com/course/100-days-of-code/?src=sac&kw=100+days).

## Getting Started

The easiest way to get a local copy up and running is to clone the repository:

1. Clone the repository.
```
git clone https://github.com/SeanConroy01/qa-application.git
```
2. Change directory.
```
cd qa-application
```
3. Create environment and install required pip packages.
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
4. Create a .env file or export teh following as environment variables
```
PORT=5000
SECRET_KEY=8BYlSihBXox27C0sKR6bTrfE4EFhy5terRFr5f
DATABASE_URI=sqlite:///data.db
```
5. Start the application
```
python3 app.py
```
6. Go to localhost:5000/create-admin, this will create default a default admin and user account. which can then be used the create additional accounts
```
Admin
Username: admin@cisco.com
Password: 1234567890

User
Username: user@cisco.com
Password: 1234567890
```

## License

This project is distributed under the MIT License. See [LICENSE.md](LICENSE.md) for more details.

## Support

If you are having problems, please let us know by [raising a new issue](https://github.com/SeanConroy01/qa-application/issues/new/choose).

## Contact

Contributors names and contact info

Sean Conroy ([@ImSeanConroy](https://twitter.com/ImSeanConroy)) - [hello@imseanconroy.com](hello@imseanconroy.com)

## Acknowledgments

During development, the below items were either found useful or directly used in within the application: 

* [Choose an Open Source License](https://choosealicense.com)
* [Bootstrap](https://getbootstrap.com)
* [Font Awesome](https://fontawesome.com)

<p align="right">(<a href="#top">back to top</a>)</p>
