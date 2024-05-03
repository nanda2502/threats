#! /bin/bash
#SBATCH -J generate_figures
#SBATCH -t 2:00
#SBATCH -p thin 
#SBATCH -n 1 

module load 2023
module load R/4.3.2-gfbf-2023a
module load ImageMagick/7.1.1-15-GCCcore-12.3.0 

export R_LIBS=$HOME/rpackages:$R_LIBS

# Run the R script
Rscript $HOME/home/analysis_scripts/create_figures.R