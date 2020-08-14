# COMP47360-Research Practicum (MSc Conv)-2019/20 Summer

## Background

Bus companies produce schedules which contain generic travel times. There are many variables which determine how long the actual journey will take.  Traffic conditions which are affected by the time of day, the day of the week, the month of the year and the weather play an important role in determining how long the journey will take.  

This project involves analyzing historic Dublin Bus data and weather data in order to create dynamic travel time estimates. Based on data analysis of historic Dublin Bus data, a system which when presented with any bus route, departure time, the day of the week, current weather condition, produces an accurate estimate of travel time for the complete route and sections of the route.  

This system can produce and display via the interface an accurate estimate of travel time for the selected journey, which is based on real-time. This project can provide more accurate time for users' journey.

## Prerequisites

#### Git

Clone the project by it

#### Anaconda

Anaconda is popular because it brings many of the tools used in data science and machine learning with just one install.

#### MySQL

MySQL is used with other programs to implement applications that need relational database capability.

#### mange.py Configuration

![Configuration](https://raw.githubusercontent.com/junyi-z/COMP47360/master/image/K9AH%601%7DHRDXWDU%5DI0HS2EL5.png)

#### model_files

https://drive.google.com/file/d/1DaWRS5d_7RkhxjqP3dSmg18TICjv0xWR/view

![model](https://raw.githubusercontent.com/junyi-z/COMP47360/master/image/model.png)

You should download it and unzip to 'dublin_bus_summer/model_files'. Because the model files are too large to upload to GitHub.

#### data_files

https://drive.google.com/file/d/1Impyfv-tbxZNE0o5hhrODQqPNmsdRpAu/view

![data](https://raw.githubusercontent.com/junyi-z/COMP47360/master/image/data.png)

You should download it and unzip to 'dublin_bus_summer/data_files'. Because the data files are too large to upload to GitHub.

## Install

1. Install django

   ```
   conda install django
   ```

2. Install joblib

   ```
   conda install joblib
   ```

3. Install pandas

   ```
   conda install pandas
   ```

4. Install requests

   ```
   conda install requests
   ```

5. Install datetime

   ```
   conda install datetime
   ```

6. Install os

   ```
   conda install os
   ```

7. Install json

   ```
   conda install json
   ```

8. Install sys

   ```
   conda install sys
   ```

9. Install pymysql

   ```
   conda install pymysql
   ```

10. Install sshtunnel

    ```
    conda install sshtunnel
    ```

11. Clone the git repository

    ```
    git clone https://csgitlab.ucd.ie/group_15/dublin_bus_summer.git
    ```


## Usage

Consider that the bus route stations in the BrightSpace data are not exactly the same as the current real-time bus route stations. 

We did two things.

The bus stop selection for the Home page is based on existing bus stops.

The bus routes and stops on Advanced Planner are derived from BrightSpace data.

## Contributors

- [x] Yuhao Wang
- [x] Junyi Zhang
- [x] Junhong Xu

