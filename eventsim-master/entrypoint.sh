#! /bin/bash
mc alias set minio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
mc mb minio/de-streaming-test
nohup bash eventsim.sh -c "examples/example-config.json" --from 365 --nusers 1000 --growth-rate 0.01 ./output > eventsim.stoud &
nohup bash eventsim.sh -c "examples/example-config.json" --from 365 --nusers 30000 --growth-rate 0.3 ./output > eventsim.stoud &
# num_threads=5  # Number of threads to create
#for ((i=0; i<num_threads; i++))
#do
#    nohup bash eventsim.sh -c "examples/example-config.json" --from 365 --nusers 1000 --growth-rate 0.01 ./output > eventsim.stoud &
#    nohup bash eventsim.sh -c "examples/example-config.json" --from 365 --nusers 30000 --growth-rate 0.3 ./output > eventsim.stoud &
#done
# wait # Wait for all threads to finish
fluentd -c ./fluent.conf