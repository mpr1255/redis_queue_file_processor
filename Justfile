default: generate_requirements resolve_versions build_environment start_redis populate_queue run_parallel snapshot_processed_files stop_redis

generate_requirements:
    pipreqs . --force

resolve_versions:
    python resolve_versions.py

build_environment:
    pip install -r requirements.txt

start_redis:
    redis-server &

populate_queue:
    python populate_queue.py

run_parallel:
    parallel -j 4 python process_file.py 

snapshot_processed_files:
    python snapshot_processed_files.py

stop_redis:
    redis-cli shutdown

