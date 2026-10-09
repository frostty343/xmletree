import xml.etree.ElementTree as ET

#namespaces
NS = {
    "ns": "http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01",
    "ach": "http://fsrar.ru/WEGAIS/ActChargeOn_v2",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance" ,
    "aif": "http://fsrar.ru/WEGAIS/ActInventoryF1F2Info",
    "oref": "http://fsrar.ru/WEGAIS/ClientRef_v2",
    "pref": "http://fsrar.ru/WEGAIS/ProductRef_v2" 
}

#USER_FSRAR_ID
user_fsrar_id = str(input("fsrar_id: "))
if not user_fsrar_id.isdigit():
    raise ValueError("FSRAR_ID должен содержать только цифры.")
if len(user_fsrar_id) != 12:
    raise ValueError(f"FSRAR_ID должен состоять ровно из 12 символов (получено {len(user_fsrar_id)}).")

#identity
act_identity = "..."

#header_info
act_number = "..."
act_date = "..."
act_type = "..."
act_note = "..."


def qd(tag: str) -> str:
    prefix, name = tag.split(":", 1)
    uri = NS[prefix]
    return f"{{{uri}}}{name}"

def generateXmlResult(root, doc_name: str, fsrar_id: str):
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  " ,level=0)
    tree.write(f"{doc_name}_{fsrar_id}.xml", encoding="UTF-8" , xml_declaration=True)


def structureXMLgenerator(
        NS,
        user_fsrar_id,
        act_identity,
        act_number,
        act_date,
        act_type,
        act_note
):
    for prefix, uri in NS.items():
        ET.register_namespace(prefix, uri)

    #XML STRUCTURE
    root = ET.Element(qd("ns:Documents"), {"Version": "1.0"})

    owner = ET.SubElement(root, qd("ns:Owner"))
    fsrar_id_block = ET.SubElement(owner, qd("ns:FSRAR_ID"))
    fsrar_id_block.text = user_fsrar_id

    document = ET.SubElement(root, qd("ns:Document"))
    act = ET.SubElement(document, qd("ns:ActChargeOn_v2"))
    ET.SubElement(act, qd("ach:Identity")).text = act_identity
    header = ET.SubElement(act, qd("ach:Header"))
    ET.SubElement(header, qd("ach:Number")).text = act_number
    ET.SubElement(header, qd("ach:ActDate")).text = act_date
    ET.SubElement(header, qd("ach:TypeChargeOn")).text = act_type
    ET.SubElement(header, qd("ach:Note")).text = act_note

    return root


generated_doc = structureXMLgenerator(
        NS,
        user_fsrar_id,
        act_identity,
        act_number,
        act_date,
        act_type,
        act_note
)

if __name__ == "__main__":
    generateXmlResult(generated_doc, "ActChargeOn_v2", user_fsrar_id)