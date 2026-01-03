# MealMate - Online Food Delivery Application

MealMate is a robust and user-friendly food delivery web application built with **Django**. It provides a seamless experience for both customers and administrators, featuring intuitive restaurant management, menu browsing, secure cart handling, and integrated **Razorpay** payments.

The application has been recently revamped with a **modern, responsive UI** to ensure a premium user experience across devices.

## 🚀 Features

### 👤 Customer Features
- **User Authentication**: Secure Sign Up and Sign In functionality.
- **Browse Restaurants**: View a list of available restaurants with pictures, cuisine types, and ratings.
- **Interactive Menu**: Browse restaurant menus with detailed item descriptions, prices, and vegetarian/non-veg indicators.
- **Smart Cart**: Add items to the cart, view the total price, and remove items as needed.
- **Secure Payments**: Integrated **Razorpay** payment gateway for secure and reliable checkout.
- **Order Tracking**: Order status updates (Pending, Paid, Failed) and payment success/failure screens.

### 🛠 Admin Features
- **Restaurant Management**: Add, update, and delete restaurant details (Name, Picture, Cuisine, Rating).
- **Menu Management**: Add new menu items, update descriptions/prices, and delete items from the menu.
- **Dashboard**: Centralized dashboard for easy access to all administrative tasks.

### 🎨 UI/UX Enhancements
- **Modern Design**: Fresh, professional styling using a custom design system (variables, flexbox, grid).
- **Responsive Layout**: Fully responsive interface that works on desktops, tablets, and mobiles.
- **Dynamic Elements**: Image sliders, hover effects, and interactive buttons.
- **Notification System**: User feedback for actions like adding to cart (using JavaScript alerts for now).

## 🛠 Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (Default)
- **Payment Gateway**: Razorpay
- **Version Control**: Git & GitHub

## ⚙️ Installation & Setup

Follow these steps to set up the project locally:

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Start-Ho/MealMate.git
    cd MealMate
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # Windows
    python -m venv myenv
    .\myenv\Scripts\activate

    # macOS/Linux
    python3 -m venv myenv
    source myenv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install django razorpay
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Configure Razorpay**
    - Open `Mealmate/settings.py`.
    - Add your Razorpay Key ID and Secret:
      ```python
      RAZORPAY_KEY_ID = 'your_key_id'
      RAZORPAY_KEY_SECRET = 'your_key_secret'
      ```

6.  **Create a Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

8.  **Access the App**
    - Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📂 Project Structure

```
Mealmate/
├── db.sqlite3              # Database file
├── manage.py               # Django command-line utility
├── Mealmate/               # Project configuration (settings, urls, etc.)
└── delivery/               # Main application app
    ├── migrations/         # Database migrations
    ├── static/             # Static files (CSS, Images, JS)
    │   └── styles.css      # Main stylesheet
    ├── Templates/          # HTML Templates
    │   ├── base.html       # Base template with Navbar/Footer
    │   ├── index.html      # Home page
    │   ├── ...             # Other templates
    ├── models.py           # Database models (User, Restaurant, Order, etc.)
    ├── views.py            # Application logic
    └── urls.py             # App-specific URL routing
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License.
