# Ecommerce-fero-task

build an e-commerce API using Django Rest Framework along with frontend in Vuejs to manage customers, orders, and products . The system should be able to handle multiple customers, each having multiple orders, and each order containing multiple products with corresponding quantities.

Click the link to see the problem statement in detail: https://github.com/virenribadiya/Ecommerce-fero-task/blob/main/Ecommerce%20Problem%20Statement.pdf

## Usage Instructions

Note: Python and Node.js must be installed in the system.

Steps:

1. Clone the repository.

2. Navigate to the project directory in terminal.

3. Install virtual environment by following command.

    reference: https://virtualenv.pypa.io/en/latest/user_guide.html
    ```
    pip install virtualenv
    ```
4. Create python virtual environment.

   In Linux or Mac, create the new python virtual environment
   ```
    virtualenv venv
    ```

   Or in Windows
   ```
    python -m virtualenv venv
    ```
   
5. Activate the environment.

   In Linux or Mac, activate the new python environment
   ```
    source venv/bin/activate
    ```

   Or in Windows
   ```
    .\venv\Scripts\activate
    ```

6. install dependacies for python virtual environment.
    ```
    pip install -r requirements.txt
    ``` 

7. Start the backend server:

   - Navigate to "server" directory in terminal.
   
   - Start the backend server by following command.
        ```
        python manage.py runserver
        ```

8. Start the frontend server:

    - Open a new terminal and naviagate to the "client" directory in terminal.

    - Install dependacies for frontend server by following command.
        ```
        npm install
        ```
    
    - Start the frontend server by following command.
        ```
        npm run dev
        ```

## Tech stack and dependencies:

#### Backend:

- Django : https://www.djangoproject.com/
    - External dependecies:
        - Django REST Framework : https://www.django-rest-framework.org/
        - django-cors-headers : https://pypi.org/project/django-cors-headers/

#### Frontend:

- Vue.js : https://vuejs.org/
    - External dependecies:
        - vue-router : https://router.vuejs.org/
        - Vuetify : https://vuetifyjs.com/en/
        - Vuelidate : https://vuelidate-next.netlify.app/
        

## Preview

[preview-fero.webm](https://github.com/virenribadiya/Ecommerce-fero-task/assets/108461765/7c53310b-c70b-4a68-81a3-03445c169bac)


