# ALX Backend Python – Generators and Data Streaming

This project explores **Python generators**, **database streaming**, and **memory-efficient data processing** using MySQL.
It focuses on building scalable backend logic capable of handling large datasets without exhausting system resources.

### Objectives

* Understand how **Python generators** enable lazy data evaluation.
* Connect to a MySQL database and **fetch rows in batches** using `fetchmany()`.
* Implement **streaming ETL-like workflows**, where data is processed iteratively instead of being fully loaded into memory.
* Simulate **pagination** using `LIMIT` and `OFFSET` while maintaining a single query loop.
* Compute aggregate values (e.g., average user age) efficiently using generators instead of SQL aggregate functions.

### Key Files

* `seed.py` – Handles database connection setup to `ALX_prodev`.
* `0-stream_users.py` – Streams user data row by row.
* `1-batch_processing.py` – Fetches and filters users in batches.
* `2-lazy_paginate.py` – Simulates lazy pagination with generators.
* `3-average_age.py` – Computes aggregate statistics from streamed data.

### Learning Outcomes

You’ll learn to design **backend systems that scale**, reduce **database load**, and perform **on-the-fly computations** efficiently — critical skills for backend engineering and data-driven systems design.

---

Would you like me to add a **short setup section** (e.g., MySQL config + how to run each script)?
