#!/usr/bin/env bash

python3 nets_spider.py
python3 mooc_spider.py
sleep 30m

python3 parse_net_lec_json.py
python3 parse_mooc_lec_json.py
sleep 10m

python3 get_net_comments.py
python3 get_mooc_commets.py
sleep 1h

python3 write_net_to_db.py
python3 write_mooc_to_db.py
