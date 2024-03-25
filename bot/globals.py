from bot import config

SEND = True
NUMBER_FORWARD_POSTS = 6

# waiting time between sending for special groups: dict
spam_intervals = config.spam_intervals
for group in config.groups_for_rent + config.groups_for_sell:
    if group not in spam_intervals:
        spam_intervals[group] = config.spam_interval

last_send_times = {group: 0 for group in set(config.groups_for_rent+config.groups_for_sell)}