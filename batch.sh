#! /bin/bash
#SBATCH -J exp2_c
#SBATCH -t 10:00
#SBATCH -p thin
#SBATCH -n 126

module load 2023
module load Python/3.11.3-GCCcore-12.3.0


module load R/4.3.2-gfbf-2023a
module load ImageMagick/7.1.1-15-GCCcore-12.3.0

SCRIPT="$HOME/home/main2PG_condor.py"

for threat in $(seq 0 5 30); do
    for probability in 0.1 0.3 0.5 0.7 0.9 1.0; do
        for replication in 1 2 3; do
            python $SCRIPT $threat $probability $replication &
        done
    done
done

wait