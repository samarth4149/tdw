from tdw.librarian import ModelLibrarian
import os
from tqdm import tqdm

if __name__ == '__main__':
    orig_lib_path = '/data/samarth/tdw_shapenet_core_res100/records.json'
    m = ModelLibrarian(orig_lib_path)
    for r in tqdm(m.records):
        if not os.path.exists(r.get_url()[8:]):
            r.do_not_use = True
            m.add_or_update_record(r, overwrite=True, write=False)
    
    m.library = '/data/samarth/tdw_shapenet_core_res100/records_interm.json'
    m.write(pretty=False)