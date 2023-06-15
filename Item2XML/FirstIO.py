import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import ParseError


def generate_schema_type(element):
    """Determine the schema type of an XML element based on its content."""
    if element is None:
        return "None"
    if element.text and ("\\" in element.text or "/" in element.text):
        return "FilePath"
    if element.text and element.text.lower() in ["true", "false"]:
        return "Bool"
    try:
        if element.text:
            int(element.text)
        return "Int"
    except ValueError:
        pass
    return "String"  # Default to string if none of the above conditions are met


def get_element_name(tag):
    """Remove namespace from tag, if present, and return only the tag name."""
    return tag.split("}")[-1] if "}" in tag else tag


def get_parent_map(tree):
    return {c: p for p in tree.iter() for c in p}


def get_element_family(element, root, parent_map):
    """Get the family information of an XML element."""
    if element == root:
        return "Root"
    elif len(element) > 0:
        children = [child.tag for child in element]
        return f"Parent (Children: {', '.join(children)})"
    else:
        parent = parent_map[element].tag
        return f"Child (Parent: {parent})"


def load_xml_file(xml_file):
    """Load XML file and return two pandas dataframes: one for the XML data and one for custom values."""
    try:
        tree = ET.parse(xml_file)
    except ParseError as e:
        print(f"Failed to parse XML: {e}")
        import traceback

        traceback.print_exc()  # Print the stack trace
        return pd.DataFrame(), pd.DataFrame(), None, None, None
    root = tree.getroot()

    parent_map = get_parent_map(tree)

    rows = []
    custom_values = []
    for elem in tree.iter():
        tag = elem.tag
        default_value = elem.text if elem.text else ""
        schema_type = generate_schema_type(elem)
        element_name = "<" + get_element_name(tag) + ">"
        element_family = get_element_family(root, elem, parent_map)
        rows.append([tag, default_value, schema_type, element_name, element_family])
        custom_values.append([tag, default_value, ""])

    df_xml = pd.DataFrame(
        rows, columns=["Tag", "Default Values", "Schema", "Element Name", "Relations"]
    )
    df_custom_values = pd.DataFrame(
        custom_values, columns=["Tag", "Default Value", "Custom Value"]
    )
    return df_xml, df_custom_values, tree, root, element_family


def process_element(element, df_custom_values):
    """Update the text of an XML element with the corresponding custom value from the DataFrame."""
    tag = element.tag
    custom_value_row = df_custom_values[df_custom_values["Tag"] == tag]
    if not custom_value_row.empty:
        custom_value = custom_value_row.iloc[0]["Custom Value"]
        if custom_value != "":
            element.text = custom_value
    for child in element:
        process_element(child, df_custom_values)


def save_xml_file(df_custom_values, tree, xml_file):
    """Save the XML file with any custom values that have been added."""
    root = tree.getroot()
    process_element(root, df_custom_values)
    tree_string = ET.tostring(root, encoding="utf-8")
    pretty_tree_string = minidom.parseString(tree_string).toprettyxml(indent="\t")
    with open(xml_file, "w") as f:
        f.write(pretty_tree_string)
