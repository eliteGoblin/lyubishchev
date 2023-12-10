# Lyubishchev

![image](https://user-images.githubusercontent.com/4377212/226231316-d0e3f8df-8ec7-43d2-a37a-579d730c0721.png)  

Personal time and metric tracking system, inspired by [Alexander Alexandrovich Lyubishchev](https://zh.wikipedia.org/wiki/%E4%BA%9A%E5%8E%86%E5%B1%B1%E5%A4%A7%C2%B7%E4%BA%9A%E5%8E%86%E5%B1%B1%E5%BE%B7%E7%BD%97%E7%BB%B4%E5%A5%87%C2%B7%E6%9F%B3%E6%AF%94%E6%AD%87%E5%A4%AB)'s personal time statistics method, illustrated in his bioriphy [This strange life](https://sudonull.com/post/171201-Granin-This-strange-life) 

> In any field, any profession, this method can help you achieve significant results!   
> Even if your talent is quite mediocre, this method can still guarantee you the greatest achievements.

## Setup

Setup venv:
```sh
sudo rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
which python
pip install -r requirements.txt
pip install -r requirements-dev.txt
```


## Run 

save following env in .dotenv/myenv

```s
export CLOCKIFY_USER_ID=xxx
export CLOCKIFY_WORKSPACE_ID=xxx
export CLOCKIFY_API_KEY=xxx
```

then run

```s
# start server in a terminal
./scripts/notebook_server_run.sh
# open browser pages in another terminal
./scripts/report.sh
# in each page, click: Restart kernal and run all cells...
```

## Develop

setup pre-commit hook

```s
cd .git/hooks
ln -s ../../scripts/precommit_check.sh  pre-commit -f
```