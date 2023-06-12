#FirstIO.py
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import ParseError

# Generate the schema type based on the content of the XML element
def generate_schema_type(element):
    if element is None:
        return 'None'
    if element.text and ('\\' in element.text or '/' in element.text):
        return 'FilePath'
    if element.text and element.text.lower() in ['true', 'false']:
        return 'Bool'
    try:
        if element.text:
            int(element.text)
            return 'Int'
    except ValueError:
        pass
    return 'String'  # Default to string if none of the above conditions are met

def get_element_name(tag):
    # Some XML files use namespaces, which are included in the tag as "{namespace}tagname".
    # This function removes the namespace and returns only the tagname.
    return tag.split('}')[-1] if '}' in tag else tag


# Adjust the names of the elements to include namespaces (if any) and brackets
def adjust_element_names(root, tags):
    element_names = []
    for tag in tags:
        element = root.find('.//'+tag)  # find with './/' to get elements at any level
        element_names.append(f"<{element.tag}>" if element is not None else "")
    return element_names

# Load XML file and return two pandas dataframes: one for the XML data and one for custom values
def load_xml_file(xml_file):
    try:
        tree = ET.parse(xml_file)
    except ParseError as e:
        print(f"Failed to parse XML: {e}")
        return pd.DataFrame(), pd.DataFrame(), None
    root = tree.getroot()

    tags = []
    default_values = []
    for elem in tree.iter():
        tags.append(elem.tag)
        default_values.append(elem.text if elem.text else '')
    element_names = adjust_element_names(root, tags)

    df_xml = pd.DataFrame({
        'Row': range(1, len(tags) + 1),
        'Element Name': element_names,
        'Tag': tags,
        'Type': ['Element'] * len(tags),
        'Schema': [''] * len(tags),
        'Default Values': default_values
    })
    df_xml['Schema'] = df_xml.apply(lambda row: generate_schema_type(root.find('.//'+row['Tag'])), axis=1)  # calculate Schema type for each row

    df_custom_values = pd.DataFrame({
        'Row': range(1, len(tags) + 1),
        'Element Name': element_names,
        'Default Value': default_values,
        'Custom Value': ['']*len(tags),
        'Tag': tags
    })
    return df_xml, df_custom_values, tree

# Save the XML file with any custom values that have been added
def save_xml_file(df_custom_values, tree, xml_file):
    root = tree.getroot()

    def process_element(element):
        tag = element.tag
        custom_value_row = df_custom_values[df_custom_values['Tag'] == tag]
        if not custom_value_row.empty:
            custom_value = custom_value_row.iloc[0]['Custom Value']
            if custom_value != '':
                element.text = custom_value
        for child in element:
            process_element(child)

    process_element(root)
    tree_string = ET.tostring(root, encoding="utf-8")
    pretty_tree_string = minidom.parseString(tree_string).toprettyxml(indent="\t")
    with open(xml_file, "w") as f:
        f.write(pretty_tree_string)

# Reset the 'Custom Value' column in the dataframe to be empty strings
def reset_xml_values(df):
    df['Custom Value'] = ''
    return df
