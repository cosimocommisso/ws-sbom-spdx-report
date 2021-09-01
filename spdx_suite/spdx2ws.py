import argparse
import json
import logging
import os
import time

from ws_sdk.client import WSClient

args = None
ignored_file_exts = ()

logging.basicConfig(level=logging.DEBUG if os.environ.get("DEBUG") else logging.INFO,
                    format='%(levelname)s %(asctime)s %(process)s: %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')


def parse_args():
    parser = argparse.ArgumentParser(description='Utility to import SPDX document into WS')
    parser.add_argument('-u', '--userKey', help="WS User Key", dest='ws_user_key', required=True)
    parser.add_argument('-k', '--token', help="WS Organization Token", dest='ws_token', required=True)
    parser.add_argument('-a', '--wsUrl', help="WS URL", dest='ws_url', default="saas")
    parser.add_argument('-l', '--spdxFile', help="Location of imported file", dest='spdx_file', default="saas")
    parser.add_argument('-o', '--outputDir', help="Output Directory to save update request", dest='output_dir', default=os.getcwd())
    parser.add_argument('-pj', '--projectToken', help="Project token to import data to", dest='project_token')
    parser.add_argument('-pd', '--productToken', help="Product token to import data to", dest='product_token')
    parser.add_argument('-pdn', '--productName', help="Product name to import data to", dest='product_name')
    arguments = parser.parse_args()
    arguments.target = WSClient.get_target(WSClient, args.project_token, args.product_token, args.product_name)

    return arguments


def create_update_request(report_files) -> dict:
    return {"updateType": "OVERRIDE",
            "type": "UPDATE",
            "agent": "fs-agent",
            "agentVersion": None,
            "pluginVersion": None,
            "orgToken": args.ws_token,
            "userKey": args.ws_user_key,
            "product": args.product_name,
            "productVersion": "",
            "timeStamp": int(time.time() * 1000.0),
            "aggregateModules": False,
            "preserveModuleStructure": False,
            "extraProperties": {},
            "projects": [{
                "coordinates": {
                    "artifactId": "TBD",
                    "version": ""
                },
                "dependencies": report_files,
                "projectTags": []
             }]
            }


def parse_spdx(spdx_file: str):
    with open(spdx_file, 'r', encoding="utf-8") as fp:
        data = fp.read()

    report_files = report_name = None
    if spdx_file.endswith('.tv'):
        report_files, report = handle_tv(data)
    elif spdx_file.endswith('.json'):
        report_files, report_name = handle_json(data)
    else:
        logging.error(f"Unsupported file format: {spdx_file}")

    return report_files, report_name


def handle_json(data):
    data_j = json.loads(data)
    report_name = data_j['Document']['name']
    packages = data_j['Document']["documentDescribes"]
    report_files = []
    for pkg in packages:
        report_files.append()

    return report_files, report_name


def handle_tv(data):
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.tagvalue import Parser
    from spdx.parsers.tagvaluebuilders import Builder

    parser = Parser(Builder(), StandardLogger())
    parser.build()
    doc, error = parser.parse(data)
    logging.debug("Getting Update Request Dependencies")
    files = []
    for file in doc.files:
        if file.chk_sum:
            files.append(create_dep(file.name, file.chk_sum.value, file.chk_sum.identifier))
        else:
            logging.warning(f"File: {file.name} has no checksum and will be skipped")

    return files, doc.name


def create_dep(f_name, f_chk_sum_value, f_chk_sum_identifier) -> dict:
    if f_name.endswith(ignored_file_exts):
        logging.info(f"Filtered out by extension file: {f_name}")
    elif f_chk_sum_identifier != "SHA1":
        logging.warning(f"File checksum of is not SHA1 ({f_chk_sum_identifier}). Low chances that the artificat will be recognized")

    return {"artifactId": os.path.split(f_name)[-1],
            "sha1": f_chk_sum_value,
            "filename": f_name}


def main():
    global args
    args = parse_args()
    report_files, report_name = parse_spdx(args.spdx_file)
    if report_files:
        update_request = create_update_request(report_files)

        file_path = os.path.join(args.output_dir, f"{report_name}-update-request.json")
        with open(file_path, 'w', encoding='utf-8') as fp:
            logging.info(f"Saved Update Request to: {os.path.join(os.getcwd(), file_path)}")
            fp.write(json.dumps(update_request))

        if args.target:
            logging.info(f"Uploading {report_name} to WhiteSource to {args.target[0]}: {args.target[1]}")
            cl_conn = WSClient(url=args.ws_url, user_key=args.ws_user_key, token=args.ws_token)
            cl_conn.upload_offline_request(file_path, args.project_token, args.product_token, args.product_name)
        else:
            logging.info("No target is configured - scan will not be uploaded to WhiteSource")


if __name__ == '__main__':
    main()
