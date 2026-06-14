# BarberShop Web Application



<img width="1919" height="881" alt="image" src="https://github.com/user-attachments/assets/2d4d167d-da86-457c-a249-1b46346b33e1" />

Barber Grid is a management platform designed for barbershops that need a simple and efficient way to organize appointments, clients and business operations.
Many small barbershops still rely on paper schedules or WhatsApp messages, making customer management and business growth difficult.
Barber Grid centralizes scheduling, customer records and service management in a single platform. The current version includes the landing page and project foundation, while scheduling, authentication, and customer management features are under development.

## ✨ Current Features

- 🎨 Modern barber shop landing page
- 💈 Service showcase section
- 📱 Responsive interface
- 🗄️ Django database integration
- 🧪 User registration tests in database

## 🚧 In Development

- 📅 Appointment scheduling system
- 🔐 User authentication
- 👤 Customer management
- 💈 Barber management
- 📊 Dashboard and analytics

 ## 🛠️ Tech Stack

| Category | Technologies |
|-----------|-------------|
| Backend | Python 3.13, Django 6 |
| Database | PostgreSQL |
| Frontend | HTML5, CSS3 |
| Deployment | Gunicorn, WhiteNoise |
| Configuration | dj-database-url |
  
## 🚀 Roadmap

### Phase 1 - Core Features

- [ ] User registration form
- [ ] Login and authentication
- [ ] Appointment form
- [ ] Appointment persistence in database

### Phase 2 - Management

- [ ] Customer management
- [ ] Barber management
- [ ] Service management
- [ ] Admin dashboard

### Phase 3 - Automation

- [ ] Email notifications
- [ ] WhatsApp notifications
- [ ] Payment integration

### Phase 4 - Expansion

- [ ] REST API
- [ ] Mobile application

## 🛠️ Installation

### Clone the repository

```bash
git clone https://github.com/alvarogit-ops/barber_grid.git
cd barber_grid
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate environment

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
python manage.py migrate
```

### Start server

```bash
python manage.py runserver
```

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

### 👨‍💻 Author

Developed with ❤️ by **alvarogit-ops**

GitHub: https://github.com/alvarogit-ops
