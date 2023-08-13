import pathlib
from joblib import Parallel, delayed
import sys
import os


#Renames file based off path, assuming structure  subset/subPID/PID/SID/img
#Path must be given as pathLib object
def rename_matching_ids(df,path,dataset,subset,view,file_type=".jpg", useSubPath = True):
    pl_path = pathlib.Path(path)

    for id in df['u_id']:
        
        sub_path = df[df['u_id'] == id]['file_dir'].values
        index = df[df['u_id'] == id].index.values[0]
        
        newName = str(index) + "_" + dataset + "_" + subset + "_" + view + "_" + str(id) + file_type
        if(useSubPath):
            img_sub_path = pl_path.joinpath(sub_path[0])
        else:
            img_sub_path = pl_path
        

        regex =  f"**/*{id}*"
        matching_files = img_sub_path.glob(regex)


        if(matching_files):
            for file in matching_files:
                print(file)
                pl_patient = img_sub_path / file
                if pl_patient.exists():
                    
                    newPath = img_sub_path / newName
                    print("Renaming:" + pl_patient.as_posix() + "-> " + newPath.as_posix()) 
                    os.rename(pl_patient, newPath)
                    renamed = True
                else:
                    print("Error: Cannot find file- " + pl_patient.as_posix())
        else:
            print("Error: Cannot find ID " + id)


def driver(parentDirectory,path,dataset,subset,view, nThreads):
    pathLib_parent = pathlib.Path(parentDirectory)

    #Parallel
    if(nThreads != 1):
        Parallel(n_jobs=nThreads)(delayed(rename_matching_ids)(path,dataset,subset,view) for path in pathLib_parent.rglob(f"*.png"))
        
    #Serial Execution
    else:
        for img_path in pathLib_parent.rglob(f"*.png"):
            rename_matching_ids(img_path)


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python3 rename_files.py path_of_png_folder dataset_name subset view nThreads")
    else:
        driver(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5], sys.argv[6])