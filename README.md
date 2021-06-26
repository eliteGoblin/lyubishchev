# lyubishchev

<img src="https://raw.githubusercontent.com/eliteGoblin/images/master/blog/img/picgo/20210617160613.png" alt="20210617160613" style="width:800px"/>  


personal time log, metric analysis tool 

# Setup

Need to first create external docker volume for Prometheus: 

```sh
docker volume create timescale_pgdata
```

# Run locally

```
docker-compose up
```

# Access Timescale data 

```sh
docker exec -it timescaledb psql postgres postgres
```



