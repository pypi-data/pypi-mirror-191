# Airflow Data Query Plugin

A user-friendly data query tool for Apache Airflow. With this plugin, you can execute SQL queries against databases
connected in your Airflow environment and view the results directly on the Airflow UI.

![image](https://user-images.githubusercontent.com/55907021/218151699-40922bf8-8b22-4bad-afeb-5b896a402587.png)

## Features

- Connect to databases using existing Airflow connections.
- Execute SQL queries and view results directly on the Airflow UI.
- Save query results as CSV files.

## Usage

1. Install the plugin using pip:

```bash
pip install airflow-data-query
```

2. Add the plugin to the Airflow plugins folder:

```bash
cp -r airflow_data_query $AIRFLOW_HOME/plugins
```

Navigate to the Airflow UI,and click on "Data Query".

Connect to a database using an existing Airflow connection and start executing your SQL queries.

## Thanks

- [Apache Airflow](https://github.com/apache/airflow)
- [Base on this](https://github.com/apache/airflow/pull/3718)

## License

This project is licensed under the Apache 2.0 License.
