# UrbanVibe - Premium Clothing
Store

UrbanVibe is a modern E-commerce platform dedicated to high-quality footwear. Built with Django, it features a sleek, responsive design and robust backend functionality.

## Features

- **Storefront**: Browse collections and products with high-quality visuals.
- **Enhanced Registration**: Comprehensive user registration collecting Name, Email, Address, Contact No, and Pincode.
- **Email Notifications**: Automated welcome emails sent to users upon registration using SMTP.
- **User Profiles**: Personalized profiles storing delivery details for a smoother checkout experience.
- **Admin Dashboard**: Powerful administrative tools for managing products, users, and sales reports.
- **OTP Verification**: Integrated OTP generation and email verification for secure access.

## Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **Database**: SQLite (Default)
- **Email**: SMTP (Gmail)

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shuaibahmad00/UrbanVibe.git
   cd UrbanVibe
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Environment Configuration**:
   Update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `Factory/settings.py` (or use an `.env` file) for email functionality.

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

## Contributing

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed as part of the Factory project.*
