## Deployment procedure

### 👉 Step 1: Start all of the containers [🔝](#-table-of-contents)

> I have to remind again in case you missed 😊
> If you need to set cluster with keyfile authentication, [check here](https://github.com/minhhungit/mongodb-cluster-docker-compose/tree/Feature/Auth/with-keyfile-auth)

Clone this repository, open powershell or cmd on the repo folder and run:

```bash
docker-compose up -d
```

### 👉 Step 2: Initialize the replica sets (config servers and shards) [🔝](#-table-of-contents)

Run these command one by one:

```bash
docker-compose exec oltp-config-1 sh -c "mongosh < /scripts/oltp-config.js"
docker-compose exec olap-config-1 sh -c "mongosh < /scripts/olap-config.js"

docker-compose exec oltp-node-1 sh -c "mongosh < /scripts/oltp-master-node.js"
docker-compose exec olap-node-1 sh -c "mongosh < /scripts/olap-master-node.js"
```

### 👉 Step 3: Initializing the router [🔝](#-table-of-contents)

>Note: Wait a bit for the config server and shards to elect their primaries before initializing the router

```bash
docker-compose exec oltp-router sh -c "mongosh < /scripts/oltp-router.js"
docker-compose exec olap-router sh -c "mongosh < /scripts/olap-router.js"
```

### 👉 Step 4: Enable sharding and setup sharding-key [🔝](#-table-of-contents)
```bash
docker-compose exec oltp-node-1 mongosh --port 27017

// Enable sharding for database `bda_oltp`
sh.enableSharding("bda_oltp")

// Check sharding status
sh.status()

exit()

docker-compose exec olap-node-1 mongosh --port 27017

// Enable sharding for database `bda_olap`
sh.enableSharding("bda_olap")

// Check sharding status
sh.status()

exit()
```

```

---
### ✔️ Done !!!
