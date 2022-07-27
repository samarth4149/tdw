from tdw.librarian import ModelLibrarian
import os

if __name__ == '__main__':
    orig_lib_path = '/data/samarth/tdw_shapenet_core_res100/records.json'
    m = ModelLibrarian(orig_lib_path)
    m.library = '/data/samarth/tdw_shapenet_core_res100/records_interm.json'
    for r in m.records:
        if not os.path.exists(r.get_url()[8:]):
            r.do_not_use = True
            
    m.write(pretty=False)