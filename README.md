# **Social and Musical Chambers Trust – Management System**

## **Overview**  
The **Social and Musical Chambers Trust Management System** is a platform designed to streamline the activities and operations of a trust dedicated to promoting music and social causes. The system allows efficient management of events, memberships, donations, and announcements while fostering community engagement through a user-friendly interface.

---

## **Key Features**  
- **Membership Management**: Keep track of trust members and their participation in events and initiatives.  
- **Event Scheduling**: Plan and organize musical and social events with ease.  
- **Donation Tracking**: Monitor and manage donations received for various causes.  
- **Announcements and Updates**: Share important updates, newsletters, and events with members.  
- **Content Management**: Maintain a gallery and blog section to showcase events and initiatives.  

---

## **Technologies Used**  
- **Frontend**: HTML, CSS, Bootstrap  
- **Backend**: Python, Django  
- **Database**: SQLite (or MySQL for production)  
- **Additional Tools**: Django Admin Panel for easy backend management  

---

## **Installation Instructions**  

### **Prerequisites**  
1. Python 3.x installed on your system  
2. SQLite (pre-installed with Python) or MySQL for database support  
3. Virtual environment setup (recommended)  

### **Steps to Run the Project**  

#### **Backend Setup**  
1. **Clone the Repository**  
   ```bash  
   git clone https://github.com/your-repo/social-musical-chambers-trust.git  
   cd social-musical-chambers-trust  
   ```  

2. **Set Up Virtual Environment**  
   ```bash  
   python -m venv venv  
   source venv/bin/activate   # On Windows: venv\Scripts\activate  
   ```  

3. **Install Dependencies**  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Configure the Database**  
   - Modify `settings.py` to configure the database (SQLite for development, MySQL for production).  
   - Run migrations to create the database schema:  
     ```bash  
     python manage.py migrate  
     ```  

5. **Run the Development Server**  
   ```bash  
   python manage.py runserver  
   ```  
   Access the application at `http://127.0.0.1:8000/`.

---

## **Usage**  

### **Admin Portal**  
- Manage trust members and their event participation.  
- Plan and schedule events with detailed descriptions.  
- Monitor donations and generate financial reports.  
- Update the gallery and blog sections with event highlights.

### **Member Portal**  
- View upcoming events and announcements.  
- Make donations directly through the platform (future enhancement).  
- Access blog posts, galleries, and newsletters.

---

## **Future Enhancements**  
- Integration with payment gateways for online donations.  
- Implementation of real-time notifications for events and updates.  
- Multi-language support for broader community engagement.  
- Advanced analytics for donation tracking and event participation.  

---

## **Contributing**  
Contributions are welcome! Feel free to fork the repository and submit pull requests.  

---

## **License**  
This project is licensed under the MIT License.  

---

## **Contact**  
**Developer**: Vigneshwaran J  
- **Email**: [venerablevignesh@gmail.com](mailto:venerablevignesh@gmail.com)  
- **GitHub**: [https://github.com/Vijayadhi](https://github.com/Vijayadhi)
- **Portfolio**: [https://portfolio-vigneshwaran.netlify.app
](https://portfolio-vigneshwaran.netlify.app
)
