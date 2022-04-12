
```s
# 运行backend: TimeScaleDB, Grafana
make run
# ingest
source ./init.sh
export CLOCKIFY_API_KEY=xxx
./lyubishchev/data_ingest/ingest.py --start-date=2021-12-06 --end-date=2021-12-11
```