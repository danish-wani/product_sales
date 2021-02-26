# Product Sales

**Heroku URL**:   https://


**Login Page** (Email/Username based authentication)

**Dashboard** (Monthly Sales data Graph, Product-Line and Quantity Tabular Data, and Month input based Graph representation of sales vs product line data.)

How to run:

`pip install pipenv`

`cd mercados_em`

`pipenv shell`

`pipenv install`

`python manage.py runserver`

(set DEBUG=False and ALLOWED_HOSTS = [] in product_sales/settings.py  if you are running on local machine)

To load a CSV sales data in future with predefined column headers you can run

`python manage.py load_sales_data path-to-csv`

**For email authentication:**
I have created a custom backend in dashboard/backends.py which authenticates the user on both email and username.





**P.S:**
The other two approaches which I could have also used for the implementation are as follows:
1. Instead of storing CSV data in Order model, I could have kept the CSV data in pandas data frame and queried the same for every operation.
2. Graph plotting could have been also done using matplotlib(python library) on the above data frame, and the html result of the same could have been used to show the graphs on the UI.
