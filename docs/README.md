# goodwe-connector
![image](https://user-images.githubusercontent.com/53972851/221367514-63997c8c-b491-467b-996b-0407ff98ffba.png)

A python library to connect with Goodwe API Rest and get production data of solar panels.

## A. How to use.

### A.1. Create JSON file 'goodwe_config.json' like this, with the following fields:

- System Id
- Account
- Password

Example of goodwe_config.json

```
{
    "goodwe_api_connection":{
        "system_id":"",
        "account":"",
        "password":""
    }
}
```
### A.2. Open example.py and edit to call the goodew_connector package functions:

Run the example.py with python:

Script execution with linux file:
```
python3 example.py
```

Similar ouput like this:
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

## C. Extra information: Goodew Api

Goodwe Api information:

- [http://www.goodwe-power.com:82/Help](http://www.goodwe-power.com:82/Help)
- [http://www.goodwe-power.com:82/swagger/ui/index](http://www.goodwe-power.com:82/swagger/ui/index)
