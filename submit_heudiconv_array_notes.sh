#!/bin/bash

#purpose: run heudiconv  

# THIS SCRIPT IS INTENDED TO BE RUN THROUGH THE WRAPPER SCRIPT submit_heudiconv_array.sh 
# THE JOB ARRAY WRAPPER SCRIPT TAKES IDENTICAL ARGUMENTS AND CAN ALSO BE USED FOR SINGLE SUBJECT

#inputs:
# 	 (1+) a list of subject IDs in their original format from dicoms/ directory (e.g. SAXE_EMOfd_20 )
#         if not provided, will run for ALL subjects in dicoms/

#example usage: ./submit_heudiconv_array.sh SAXE_EMOfd_20 SAXE_EMOfd_32 
# 	    or...   ./submit_heudiconv_array.sh 


# note: assumes heuristics file is in this dir within: heuristic_files/heudi.py 
heudifile=heuristic_files/heudi.py  
    ### heudifile variable as the python script which contains naming templates and file organization (see github link -> saxe_heudi_notes.py)
    ### as said by the note, should belong in the heursitic_files folder and named heudi.py

proj=`cat ../PATHS.txt` 
    ### path to specific project directory (according to Saxe lab README)

subjs=("${@}") 
    ### array that holds all arguments (subjects) as separate elements

if [[ $# -eq 0 ]]; then     ### if number of arguments in subjs is 0 (none in argument), then...

    # first go to data directory, grab all subjects,
    # and assign to an array
    pushd $proj/data/dicoms 
        ### push directory of project dicoms to current directory (saving original directory)

    # including pilots
    subjs=($(ls SAX* -d)) 
        ### list all directories starting with SAX (with more potentially following) and then redefine subj array
    # excluding pilots
    #subjs=($(ls sub-leap[0-9]* -d)) 
        ### NOT considering those starting with SAX (includes pilots), but starting with  

    popd 
        ### brings us back to our original directory
fi


# take the length of the array for indexing job
len=$(expr ${#subjs[@]} - 1) 
    ### length of array given by the number of subjects in subj subtracted by one (since indexing starts at 0). expr needed to treat #subjs[@]} - 1 as a math expression

echo Spawning ${#subjs[@]} sub-jobs. 
    ### echo will print out "Spawning (NUMBER OF SUBJECTS) sub-jobs"; a good check to know we're considering the right files

# submit the jobs
sbatch --array=0-$len $proj/scripts/1_heudiconv_scripts/heudiconv_single_subject.sh $heudifile ${subjs[@]} 
    ### submitting job array using single subject script (bash) and heuristic script (py) to SLURM
    ### --array=0-$len: start and end index ($len defined above) of each job (participant)
    ### $proj/.../heudiconv_single_subject.sh: in the project path defined by PATHS.txt, it will perform the single subject script for EACH subject in array
    ### $heudifile: will run the heuristic python script for each participant
    ### ${subjs[@]}: ALL elements of subject array
