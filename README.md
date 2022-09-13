# post_app

post_app test task

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

### API documentation

- To see post_app API documentation visit [this page](https://documenter.getpostman.com/view/12903898/2s7YYu4hMx).


### Points to discuss

- According to my solution for last user request tracking. I save every user request to database,
it means db is triggered very often. Possibly more efficient solution for prod env: save time of last request into
cache (Redis, etc.) and update field in db only if user didn't make a request for N minutes. It will
help to decrease amount of requests to db.
- **uuid** could be used instead of inc. **id**'s for production env.
