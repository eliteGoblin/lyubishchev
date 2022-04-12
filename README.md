# lyubishchev

<img src="https://raw.githubusercontent.com/eliteGoblin/images/master/blog/img/picgo/20210617160613.png" alt="20210617160613" style="width:800px"/>  


personal time log, metric analysis tool 

# Run backend locally

```
make run
```

# Ingest 

```
source ./init.sh
make ingest-xx
```

# Access Timescale data 

```sh
docker exec -it timescaledb psql postgres postgres
```

# View in Grafana



# TODO

* add step to ingest
* record design idea: use postgres to record all data, create separate tool to generate plot, reports. then automatically generate Markdown report.