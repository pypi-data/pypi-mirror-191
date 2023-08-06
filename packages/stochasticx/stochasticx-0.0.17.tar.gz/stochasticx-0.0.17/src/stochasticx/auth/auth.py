import os
import requests
from stochasticx.constants.urls import CloudRoutes, get_cloud_url
from stochasticx.utils.auth_utils import AuthUtils, LoginUtils
import ipywidgets as widgets
from IPython.display import display


class UsageQuota:
    """Class to get your current usage quota and your limits"""

    def __init__(
        self,
        concurrentJobLimit: int,
        monthlyJobLimit: int,
        storageUsed: int,
        storageLimit: int,
    ):
        """Initializer

        Args:
            concurrentJobLimit (int): concurrent job limit
            monthlyJobLimit (int): monthly job limit
            storageUsed (int): storage used
            storageLimit (int): storage limit
        """

        self.concurrentJobLimit = concurrentJobLimit
        self.monthlyJobLimit = monthlyJobLimit
        self.storageUsed = storageUsed
        self.storageLimit = storageLimit

    def __str__(self):
        """Convert the object to a string

        Returns:
            str
        """
        return """
    Concurrent job limit {} 
    Monthly job limit: {} 
    Storage used: {} 
    Storage limit: {}
""".format(
            self.concurrentJobLimit,
            self.monthlyJobLimit,
            self.storageUsed,
            self.storageLimit,
        )


class Company:
    """Class to store information about the company of the user"""

    def __init__(self, id: str, name: str, website: str):
        """Initializer

        Args:
            id (str): ID
            name (str): company name
            website (str): website
        """

        self.id = id
        self.name = name
        self.website = website

    def __str__(self):
        """Method to convert the object to a string

        Returns:
            str
        """
        return """
    Id: {} 
    Company name: {} 
    Website: {}
""".format(
            self.id, self.name, self.website
        )


class User:
    """Class to store information about the user"""

    def __init__(self, id: str, first_name: str, last_name: str, email: str, role: str):
        """Initializer

        Args:
            id (str): ID
            first_name (str): first name
            last_name (str): last name
            email (str): email
            role (str): role
        """

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role

    def __str__(self):
        """Method to conver the object to a string

        Returns:
            str
        """
        return """
    Id: {} 
    First name: {} 
    Last name: {} 
    Email: {} 
    Role: {}
""".format(
            self.id, self.first_name, self.last_name, self.email, self.role
        )


class Stochastic:
    """Class to do login and store the information of the current user"""

    def __init__(self):
        """Initializer"""

        self.username = os.getenv("STOCHASTIC_USER")
        self.password = os.getenv("STOCHASTIC_PASSWORD")
        self.company_info = None
        self.usage_quota = None
        self.user_info = None

    def login(self):
        """Do login"""

        LoginUtils.login_request(self.username, self.password)

    def login(self, username, password):
        os.environ["STOCHASTIC_USER"] = username
        LoginUtils.login_request(username, password)

    def link_login(self):
        LoginUtils.link_login_request()

    def notebook_login(self):
        """Allows you to login in a Jupyter Notebook"""

        username = widgets.Text(description="Username")
        password = widgets.Password(description="Password")
        output = widgets.Output()
        login_button = widgets.Button(description="Login")

        display(username, password, login_button, output)

        def on_button_clicked(b):
            with output:
                logged_in = LoginUtils.login_request(username.value, password.value)
                if logged_in:
                    print("Login successfully")
                else:
                    print("Username or password is not correct")

        login_button.on_click(on_button_clicked)

    def _initilize_profile(self):
        """Populate the profile with data"""

        auth_header = AuthUtils.get_auth_headers()

        response = requests.get(get_cloud_url(CloudRoutes.ME_URL), headers=auth_header)
        data = response.json()

        if data.get("company") is not None:
            self.company_info = Company(
                id=data.get("company").get("id"),
                name=data.get("company").get("name"),
                website=data.get("company").get("website"),
            )

            self.usage_quota = UsageQuota(
                concurrentJobLimit=data.get("company").get("concurrentJobLimit"),
                monthlyJobLimit=data.get("company").get("monthlyJobLimit"),
                storageUsed=data.get("company").get("storageUsed"),
                storageLimit=data.get("company").get("storageLimit"),
            )

        self.user_info = User(
            id=data.get("id"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            email=data.get("email"),
            role=data.get("role"),
        )

    def get_profile(self):
        """Returns profile information

        Returns:
            User: user information
        """
        self._initilize_profile()
        return self.user_info

    def get_company(self):
        """Returns the company information

        Returns:
            Company: company information
        """
        self._initilize_profile()
        return self.company_info

    def get_usage_quota(self):
        """Return the usage quota

        Returns:
            UsageQuota: usage quota
        """
        self._initilize_profile()
        return self.usage_quota
