#! /bin/bash
#SBATCH -J exp3_b
#SBATCH -t 0:10:00
#SBATCH -p thin
#SBATCH -n 16

module load 2023
module load Python/3.11.3-GCCcore-12.3.0

SCRIPT="$HOME/home/main2PG_condor.py"

for threat in $(seq 0 5 30); do
        for replication in 1 2 3; do
            python $SCRIPT $threat $replication &
        done
    done

wait