from pathlib import Path
from requests import head
from tqdm import tqdm
import boto3
from tdw.librarian import ModelLibrarian

private_models = ['camera_box', 'iron_box', 'coffeemug', 'b04_ramlosa_bottle_2015_vray', 'moet_chandon_bottle_vray',
                  'b04_whiskeybottle', '102_pepsi_can_12_fl_oz_vray', 'candlestick1', 'golf', 'b03_toothbrush',
                  'b05_calculator', 'b05_tag_heuer_max2014', 'b05_executive_pen', 'f10_apple_iphone_4']
lib_full = ModelLibrarian("models_full.json")
lib_core = ModelLibrarian("models_core.json")
objects_csv_path = Path('D:/Github/').joinpath("tdw/Python/tdw/py_impact/objects.csv")
if not objects_csv_path.exists:
    print(f"Not found: {objects_csv_path}")
objects_csv_txt = objects_csv_path.read_text(encoding="utf-8")
objects_csv_lines = objects_csv_txt.split("\n")

session = boto3.Session(profile_name="tdw")
s3 = session.resource("s3")

pbar = tqdm(total=len(private_models) * 3)
for private_model in private_models:
    pbar.set_description(private_model)
    record_full = lib_full.get_record(private_model)
    if record_full is None:
        print(f"WARNING: No record for {private_model}")
        pbar.update(3)
        continue
    if record_full.do_not_use:
        print(f"SKIPPING {private_model} because it's flagged as do_not_use: {record_full.do_not_use_reason}")
        pbar.update(3)
        continue
    record_core = lib_core.get_record(private_model)
    if record_core is not None:
        print(f"SKIPPING {private_model} because it's already in the public bucket.")
        pbar.update(3)
        continue
    urls = dict()
    for platform in record_full.urls:
        # Download the model.
        key = record_full.urls[platform].split("https://tdw-private.s3.amazonaws.com/")[1]
        resp = s3.meta.client.get_object(Bucket='tdw-private', Key=key)
        # Upload the asset bundle.
        s3_object = s3.Object("tdw-public", key)
        s3_object.put(Body=resp["Body"].read())
        s3_object.Acl().put(ACL="public-read")
        # Update the URLs.
        url =  f"https://tdw-public.s3.amazonaws.com/{key}"
        resp = head(url)
        if resp.status_code != 200:
            print(f"WARNING: Got code {resp.status_code} for {url}")
        urls[platform] = url
        pbar.update(1)
    record_full.urls = urls
    # Add the record.
    lib_core.add_or_update_record(record=record_full, overwrite=False, write=True)
    # Update the record.
    lib_core.add_or_update_record(record=record_full, overwrite=True, write=True)
    # Update objects.csv
    for line in objects_csv_lines:
        if line.startswith(record_full.name) and "models_full.json" in line:
            objects_csv_txt = objects_csv_txt.replace(line, line.replace("models_full.json", "models_core.json"))
            objects_csv_path.write_text(objects_csv_txt, encoding="utf-8")
            break
