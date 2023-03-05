# goodwe-connector

![image](https://user-images.githubusercontent.com/53972851/221367514-63997c8c-b491-467b-996b-0407ff98ffba.png)


A python library to connect with Goodwe API Rest and get production data of solar panels.

## A. How to use it.

### A.1. The JSON file **goodwe_config.json**:

Create **goodwe_config.json** file in the root path of the repository with the following fields:

Field  | Field meaning
------------- | -------------
system_id  | Unique device identifier (you can get it after login in the application: [GOODWE SEMS PORTAL](https://www.semsportal.com/home/login)). It's presenting in the base URL after login it.
account  | User email. Used into the application: [GOODWE SEMS PORTAL](https://www.semsportal.com/home/login)
password  | User password. Used into the application: [GOODWE SEMS PORTAL](https://www.semsportal.com/home/login)

Example of **goodwe_config.json**:

```
{
    "goodwe_api_connection":{
        "system_id":"",
        "account":"",
        "password":""
    }
}
```
### A.2. Run it! 

Open **example.py** and edit to call the **goodew_connector** package functions. Run the **example.py** with python:

Script execution: 
```
python3 example.py
```

Similar ouput like this (for the selected method):
```
Day 14/02/2023	Power Generated: 9.1 kW
```
## B. Generate documentation.

- Build documentation:

```
mkdocs build
```

- Serve:

```
mkdocs serve
```

## C. Extra information: Goodwe Api

Goodwe SEMS portal: 

- [GOODWE SEMS PORTAL](https://www.semsportal.com/home/login)

Documentation about goodwe api:

- [http://www.goodwe-power.com:82/Help](http://www.goodwe-power.com:82/Help)
- [http://www.goodwe-power.com:82/swagger/ui/index](http://www.goodwe-power.com:82/swagger/ui/index)
