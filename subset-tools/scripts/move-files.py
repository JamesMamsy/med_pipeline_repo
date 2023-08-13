import pathlib
import shutil

def move_matching_ids(df, dest, source):
    pl_src = pathlib.Path(source)
    pl_dst = pathlib.Path(dest)
    pl_dst.mkdir(parents=True, exist_ok=True)

    for id in df['u_id']:
        sub_folder = df[df['u_id'] == id]['file_dir'].values
        pl_sub_folder = pl_src.joinpath(sub_folder[0])
        
        for file in pl_sub_folder.glob(f"**/*{id}*"):
            print(file)
            pl_patient = pl_sub_folder / file
        
            print("Searching for ID directory: " + file.as_posix())
            if file.exists():
                print("Success")    
                shutil.move(file, pl_dst / file.name)
            break
        else:
            print("File not found " + id)
