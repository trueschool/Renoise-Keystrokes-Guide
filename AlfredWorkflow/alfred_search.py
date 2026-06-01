import json
import os
import sys
import xml.etree.ElementTree as ET


def search_bindings(xml_file, query):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    items = []
    # Split query into words to allow fuzzy multi-word matching (e.g. "clone block")
    query_words = query.lower().split()

    for category in root.findall(".//Category"):
        cat_id_elem = category.find("Identifier")
        cat_name = cat_id_elem.text if cat_id_elem is not None else "Unknown"

        for keybinding in category.findall(".//KeyBinding"):
            topic_elem = keybinding.find("Topic")
            binding_elem = keybinding.find("Binding")
            key_elem = keybinding.find("Key")

            if (
                topic_elem is not None
                and binding_elem is not None
                and key_elem is not None
            ):
                topic = topic_elem.text
                binding = binding_elem.text
                key = key_elem.text

                if not key or not key.strip():
                    continue

                search_string = f"{cat_name} {topic} {binding} {key}".lower()

                # Check if ALL query words are in the search string
                if all(word in search_string for word in query_words):
                    items.append(
                        {
                            "title": binding,
                            "subtitle": f"{key}   |   [{cat_name} ➔ {topic}]",
                            "arg": key,  # This is what gets copied to clipboard if you hit Enter
                            "valid": True,
                            "text": {"copy": key, "largetype": key},
                        }
                    )

    # If no results, show a placeholder
    if not items:
        items.append(
            {
                "title": "No shortcuts found",
                "subtitle": "Try a different search term...",
                "valid": False,
            }
        )

    print(json.dumps({"items": items}))


if __name__ == "__main__":
    # Alfred passes the query as the first argument
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    xml_path = os.path.join(os.path.dirname(__file__), "KeyBindings-Whitelabel.xml")
    search_bindings(xml_path, query)
