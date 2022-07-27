from tdw.librarian import ModelLibrarian
import os
from tqdm import tqdm

if __name__ == '__main__':
    orig_lib_path = '/data/samarth/tdw_shapenet_core_res100/records.json'
    m = ModelLibrarian(orig_lib_path)
    m.library = '/data/samarth/tdw_shapenet_core_res100/records_interm.json'
    for i, r in enumerate(m.records):
        if not os.path.exists(r.get_url()[8:]):
            m.records[i].do_not_use = True
            
    m.write(pretty=False)