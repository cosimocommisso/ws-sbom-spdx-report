import importlib
import json
import argparse
import logging
import os
import time
from ws_sdk.client import WSClient

args = None
ignored_files = {'.tgz'}

logging.basicConfig(level=logging.DEBUG if os.environ.get("DEBUG") else logging.INFO,
                    format='%(levelname)s %(asctime)s %(process)s: %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')


def parse_args():
    global args
    parser = argparse.ArgumentParser(description='Utility to import SPDX document into WS')
    parser.add_argument('-u', '--userKey', help="WS User Key", dest='ws_user_key', required=True)
    parser.add_argument('-k', '--token', help="WS Organization Token", dest='ws_token', required=True)
    parser.add_argument('-a', '--wsUrl', help="WS URL", dest='ws_url', default="saas")
    parser.add_argument('-l', '--spdxFile', help="Location of imported file", dest='spdx_file', default="saas")
    parser.add_argument('-o', '--outputDir', help="Output Directory to save update request", dest='output_dir', default=os.getcwd())
    parser.add_argument('-pj', '--projectToken', help="Project token to import data to", dest='project_token')
    parser.add_argument('-pd', '--productToken', help="Product token to import data to", dest='product_token')
    parser.add_argument('-pdn', '--productName', help="Product name to import data to", dest='product_name')
    args = parser.parse_args()

    args.target = WSClient.get_target(WSClient, args.project_token, args.product_token, args.product_name)


def create_update_request(spdx_doc) -> dict:
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
                "dependencies": get_dependencies(spdx_doc),
                "projectTags": []
             }]
            }


def parse_spdx(spdx_file: str):
    def load_parse_modules(f_name: str):
        if f_name.endswith('.json'):
            parser_name = "jsonyamlxml"
            builder_name = "jsonyamlxmlbuilders"
        # elif f_name.endswith('.rdf'):
        #     parser_name = "rdf"
        #     builder_name = "rdfbuilders"
        # elif f_name.endswith('.xml'):
        #     parser_name = "xmlparser"
        #     builder_name = "jsonyamlxmlbuilders"
        # elif f_name.endswith('.tv'):
        #     parser_name = "tagvalue"
        #     builder_name = "tagvaluebuilders"
        else:
            logging.error(f"Unsupported file format: {f_name}")
            return None

        parser_module = importlib.import_module(f"spdx.parsers.{parser_name}")
        builder_module = importlib.import_module(f"spdx.parsers.{builder_name}")
        p = getattr(parser_module, "Parser")
        b = getattr(builder_module, "Builder")

        return p, b

    with open(spdx_file, 'r', encoding="utf-8") as fp:
        from spdx.parsers.loggers import StandardLogger
        data = fp.read()
        parser, builder = load_parse_modules(spdx_file)
        doc = None

        if parser is not None:
            parser = parser(builder(), StandardLogger())
            parser.build()
            doc, error = parser.parse(data)

    return doc


def get_dependencies(doc) -> list:
    def create_dep(f) -> dict:
        d = None
        if f.chk_sum:
            if f.chk_sum.identifier != "SHA1":
                logging.warning(
                    f"File checksum of is not SHA1 ({f.chk_sum.identifier}). Chances are low that artificat will be recognized")
            d = {"artifactId": os.path.split(f.name)[-1],
                 "sha1": f.chk_sum.value,
                 "filename": f.name}
        else:
            logging.warning(f"File: {f.name} has no checksum and will be skipped")

        return d

    logging.debug("Getting Update Request Dependencies")
    dependencies = []
    for file in doc.files:
        dep = create_dep(file)
        if dep:
            dependencies.append(dep)

    return dependencies


def main():
    parse_args()
    doc = parse_spdx(args.spdx_file)
    if doc:
        update_request = create_update_request(doc)

        file_path = os.path.join(args.output_dir, f"{doc.name}-update-request.json")
        with open(file_path, 'w', encoding='utf-8') as fp:
            logging.info(f"Saved Update Request to: {os.path.join(os.getcwd(), file_path)}")
            fp.write(json.dumps(update_request))

        if args.target:
            logging.info(f"Uploading {doc.name} to WhiteSource to {args.target[0]}: {args.target[1]}")
            cl_conn = WSClient(url=args.ws_url, user_key=args.ws_user_key, token=args.ws_token)
            cl_conn.upload_offline_request(file_path, args.project_token, args.product_token, args.product_name)
        else:
            logging.info("No target is configured - scan will not be uploaded to WhiteSource")


if __name__ == '__main__':
    main()
