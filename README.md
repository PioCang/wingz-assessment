# wingz-assessment

## 0 Foreword: Some Design choices
1. In the spec, primary keys take on the format `id_<model_name>`. I've simplified them to use `id` that's readily supplied by Django to be the default primary key on any table.
2. Similarly, Foreign Keys will use just `<model_name>` as the foreign key (but under the hood Django uses `<model_name>_id`).
3. The instructions' wording leads me to believe that a majority of the optimization concerns center around the Ride List API. Therefore, I want to make it clear that my approach to this coding assessment places utmost emphasis towards the performance and optimization efforts of the **Ride List API**. With that said, far behind is the level of care expended towards the rest of the CRUD operations on the rest of the models.
4. I've decided to use the Haversine formula to compute for geo-distance.
5. I made the decision to have `lat` and `lon` be required inputs for the Ride List API, with the rationale being: someone looking for a ride would likely want to see distance-to-pickup even if their sort preference is by pickup_time.

## 1 Preparations
Let's prep a virtual env, I assume you have *pyenv* installed.
For a small application, I want to avoid the memory overhead involved with Docker containers.

1. Create the virtual env to sandbox all PIP changes. Needs [pyenv](https://formulae.brew.sh/formula/pyenv) and [pyenv-virtualenv](https://formulae.brew.sh/formula/pyenv-virtualenv) installed.
```
pyenv virtualenv 3.11.3 wingz
pyenv activate wingz
```

2. Clone the repository
```
git clone https://github.com/PioCang/wingz-assessment.git
```

3. We run everything inside this folder
```
cd wingz-assessment/wingz/
mkdir static
```

4. Install the requirements. (Ensure the `wingz` virtual env is activated.)
```
pip install -r requirements.txt
```

5. Run the migrations
```
python manage.py migrate
```

6. Let's create the `static` folder for profiling the queries.
```
python manage.py collectstatic
```

7. Create a superuser by following the prompts
```
python manage.py createsuperuser
```

8. Run the server
```
python manage.py runserver 8000
```

The server will be hosted on http://localhost:8000/

9. Grant the superuser you just created with Admin role in [Users Admin page](http://localhost:8000/admin/rideshare/user/1/change/) and save.


## 2 Using the app's APIs
To use the API and endpoints, you must first Login your user. Please refer to [ENDPOINTS.md](./ENDPOINTS.md)

An HTTP Archive file [requests.har](./requests.har) is provided for you but you have to provide the auth Token yourself.



---
### Profiling using Silk
You can access the SQL profiling of the requests in
http://localhost:8000/silk/requests/

The proof that only 3 SQL queries were done for the Rides List API is in [sql_profile_proof.png](sql_profile_proof.png)


## 3 Teardown
1. Stop the Django server with `Ctrl + C`
2. Delete the environment with
```
pyenv deactivate
pyenv virtualenv-delete wingz
```
3. Delete the `wingz-assessment` folder

## 4 Bonus SQL question
This CTE query is written in BigQuery flavor of SQL
```sql
--- Pair up pickup timestamps with dropoff timestamps that belong to the same
--- ride_id. The HAVING clause ensures that we only consider completed trips
WITH
all_completed_trips AS (
    SELECT
        ride_id
        , MAX(
            CASE
                WHEN description = 'Status changed to pickup'
                    THEN created_at
                END
            ) AS pickup_time
        , MAX(
            CASE
                WHEN description = 'Status changed to dropoff'
                    THEN created_at
                END
        ) AS dropoff_time
    FROM rideshare.ride_event
    GROUP BY ride_id
    HAVING pickup_time IS NOT NULL
        AND dropoff_time IS NOT NULL
),

--- Filter out the trips that took less than or equal to one hour.
--- 1) MILLISECOND is the granularity needed here because the DATE_DIFF function
--- employs an implied floor() function thereby making values such as 1.0005
--- be resolved to 1.0000
--- 2) Dropoff_time is used to signal the termination of the trip, so it is
--- used as the basis for which month a trip falls under. For example, if a
--- trip crossed over Jan 31st to Feb 1st, that trip counts towards February.
all_completed_trips_gt_1_hr AS (
    SELECT DISTINCT
        FORMAT_TIMESTAMP('%Y-%m', all_completed_trips.dropoff_time) AS month
        , CONCAT(user.first_name, ' ', LEFT(user.last_name, 1)) AS driver
        , all_completed_trips.ride_id
    FROM all_completed_trips
    INNER JOIN rideshare.ride
        ON ride.ride_id = all_completed_trips.ride_id
    INNER JOIN rideshare.user
        ON user.user_id = ride.user_id
    WHERE DATE_DIFF(
        all_completed_trips.dropoff_time, all_completed_trips.pickup_time, MILLISECOND
    ) / 3600000 > 1
)

--- Main result
--- Caveat: the naming convention in the example consolidates people having the
--- same first name and first letter of surname e.g. John P and John P
SELECT
    month
    , driver
    , COUNT(DISTINCT ride_id) AS count_of_trips_gt_1hr
FROM all_completed_trips_gt_1_hr
GROUP BY month, driver
ORDER BY month, driver
```

# -- END
