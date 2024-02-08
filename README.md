# Habit Tracker

### App made in Flask to track your daily routine.
![img_tracker](./static/img/habit_tracker.png)

---
### Run the app
1. Deploy a mongodb database and replace the parameters in .env file
2. Create a virtual environment and install dependencies
```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
3. Run in the command line
```bash
$ gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

4. Run in docker
```bash
$ docker build -t habits_tracker:latest .
$ docker run -it -p 5000:5000 -e MONGODB_URI="mongodb://<YOUR_USER>:<YOUR_PASSWORD>@<YOUR_MONGODB>:27017/habits" -e DB_NAME="habits" habits_tracker:latest
```

5. Run with docker-compose

a. create .env file or set env variables
```bash
$ export DB_USERNAME=mongoadmin
$ export DB_PASSWORD=<your_password>
```
b. run docker-compose
```bash
$ docker-compose up -d
```