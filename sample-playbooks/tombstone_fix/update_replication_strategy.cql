update keyspace Locks
with placement_strategy = 'NetworkTopologyStrategy'
and strategy_options = {dc-1:3}
and durable_writes = false;