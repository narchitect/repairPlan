import ifcopenshell
print(ifcopenshell.__version__)
import ifcopenshell.util.element


# Load the IFC file
ifc_file = "/Users/nayunkim/Documents/GitHub/thesis/data/models/Library_Borrmann_alex_Leica_v6_Exteneded_ModifiedCOR.ifc"


def get_object_info_by_guid(ifc_file_path, guid):
    # Load the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Get the element by GUID
    element = ifc_file.by_guid(guid)

    if not element:
        print(f"No element found with GUID: {guid}")
        return

    # Get basic information
    print(f"Element Type: {element.is_a()}")
    print(f"Global ID: {element.GlobalId}")
    print(f"Name: {element.Name}")

    # Get properties
    psets = ifcopenshell.util.element.get_psets(element)
    print("\nProperty Sets:")
    for pset_name, props in psets.items():
        print(f"  {pset_name}:")
        for prop_name, prop_value in props.items():
            print(f"    {prop_name}: {prop_value}")

    # Get quantities
    qtos = ifcopenshell.util.element.get_psets(element, qtos_only=True)
    print("\nQuantities:")
    for qto_name, quantities in qtos.items():
        print(f"  {qto_name}:")
        for quantity_name, quantity_value in quantities.items():
            print(f"    {quantity_name}: {quantity_value}")

    # Get material
    material = ifcopenshell.util.element.get_material(element)
    if material:
        print(f"\nMaterial: {material.Name}")

    # Get type (if applicable)
    element_type = ifcopenshell.util.element.get_type(element)
    if element_type:
        print(f"\nType: {element_type.Name}")

    # Get container
    container = ifcopenshell.util.element.get_container(element)
    if container:
        print(f"\nContainer: {container.is_a()} - {container.Name}")

# Usage example

guid = "3ieRYLDdzA7A223TPufELQ"  # Replace with the GUID you want to query


print(get_object_info_by_guid(ifc_file, guid))