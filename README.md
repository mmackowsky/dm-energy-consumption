# DeviceMinder - Energy Consumption Service

## Description
<p>
    This service is a simulation of retrieving energy data from external energy meters in a building/home, allowing for data retrieval from the device, displaying it, and deleting it. Measurement generation is handled by Celery tasks, which, when invoked, asynchronously add records to the PostgreSQL database. The user's logged-in ID, which is saved along with the measurement, is retrieved from the request header, decoded from the JWT Token.
</p>

## Technologies
<ul>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/8cc0785a-7f2c-4efd-8891-7f796c934ad8" width=15> Python 3.11</li>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/0dbf9713-295d-4395-93b5-0ebe471d4238" width=20> Celery</li>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/9ffb3ef3-76a6-48da-acf2-787e8062d05e" width=20> PostgreSQL 15</li>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/3ab3f47d-b088-4473-bec4-330882f78bfb" width=15> Docker</li>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/fd90329c-e363-430a-8593-952ac694c1be" width="15"> Poetry</li>
</ul>
