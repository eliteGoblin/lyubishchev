# Lyubishchev

Personal time and metric tracking system, following Lyubishchev's method, mentioned in his bioriphy [This strange life](https://sudonull.com/post/171201-Granin-This-strange-life)
## Setup

Setup venv:
```sh
sudo rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
which python
```

## Run CI locally

```sh
# skip integration test
./local.sh
```

## Run 

```s
export CLOCKIFY_USER_ID=xxx    
export CLOCKIFY_WORKSPACE_ID=xxx
export CLOCKIFY_API_KEY=xxx
python -m lyubishchev dayrange 2023-03-12 2023-03-18
```