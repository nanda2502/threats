#! /bin/bash
#SBATCH -J exp2_c
#SBATCH -t 10:00
#SBATCH -p thin
#SBATCH -n 90

module load 2023
module load Python/3.11.3-GCCcore-12.3.0

SCRIPT="$HOME/home/main2PG_condor.py"


for threat in $(seq 35 5 60); do
    for probability in 0.1 0.3 0.5 0.7 0.9; do
        for replication in 1 2 3; do
            python $SCRIPT $threat $probability $replication &
        done
    done
done

wait