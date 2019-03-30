#!/usr/bin/env bash

python3 nets_spider.py
sleep 30m

python3 parse_net_lec_json.py
sleep 10m

python3 get_net_comments.py
sleep 1h

python3 write_net_to_db.py
