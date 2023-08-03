# goodwe-connector
![image](https://user-images.githubusercontent.com/53972851/221367514-63997c8c-b491-467b-996b-0407ff98ffba.png)

A python library to connect with Goodwe API Rest and get production data of solar panels.

## A. How to use...

### A.1. Developer environment: Create virtual environment and install requirements.txt

1. Create virtual envinroment:

```
python -m venv .\venv
```
2. Install requirements.txt.

```
 pip install -r requirements.txt
```

### A.2. Create JSON file 'goodwe_config.json' like this (base repository path), with the following fields:

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
### A.3. Open example.py and edit to call the goodew_connector package functions:

Run the sample.py with python:

Define the extrategy that you want launch and running python script file:
```
python3 sample.py
```

Similar ouput like this:
```
{
    "2023-08-02": 10.7
}
Generated 36.70 kWh (avg. 12.23 kWh per day) in 3 days.
{
    "2023-08-01": 14.5,
    "2023-08-02": 10.7,
    "2023-08-03": 11.5
}
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
