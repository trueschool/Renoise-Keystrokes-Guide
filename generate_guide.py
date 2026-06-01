import xml.etree.ElementTree as ET
import re
import os

def update_guide():
    # You can point this to the Whitelabel or your custom Keybindings XML
    xml_path = "KeyBindings-Whitelabel.xml"
    html_path = "RenoiseKeys.html"

    if not os.path.exists(xml_path) or not os.path.exists(html_path):
        print(f"Error: Make sure {xml_path} and {html_path} are in the same folder.")
        return

    print("Parsing Keybindings XML...")
    tree = ET.parse(xml_path)
    root = tree.getroot()

    categories = {}

    # 1. Parse XML and group by Category -> Topic -> Binding
    for category in root.findall(".//Category"):
        identifier = category.find("Identifier")
        if identifier is None or not identifier.text:
            continue
        cat_name = identifier.text.strip()

        for keybinding in category.findall(".//KeyBinding"):
            key_tag = keybinding.find("Key")
            # Only include bindings that actually have a keyboard mapping
            if key_tag is None or not key_tag.text:
                continue

            topic_tag = keybinding.find("Topic")
            binding_tag = keybinding.find("Binding")

            topic_name = topic_tag.text.strip() if topic_tag is not None and topic_tag.text else "Uncategorized"
            binding_name = binding_tag.text.strip() if binding_tag is not None and binding_tag.text else "Unknown"
            key_combo = key_tag.text.strip()

            if cat_name not in categories:
                categories[cat_name] = {}
            if topic_name not in categories[cat_name]:
                categories[cat_name][topic_name] = []

            categories[cat_name][topic_name].append({
                'name': binding_name,
                'key': key_combo
            })

    # 2. Generate the Table of Contents HTML
    toc_lines = ['    <nav id="toc">\n']
    for cat_name in categories.keys():
        anchor_id = cat_name.replace(" ", "_")
        toc_lines.append(f'        <a href="#{anchor_id}">{cat_name}</a>')
    toc_lines.append('    </nav>')
    toc_html = '\n'.join(toc_lines)

    # 3. Generate the Cards HTML container
    cards_lines = ['    <div class="container" id="cardsContainer">\n']
    for cat_name, topics in categories.items():
        anchor_id = cat_name.replace(" ", "_")
        cards_lines.append(f'        <div class="card" id="{anchor_id}">')
        cards_lines.append(f'            <h2 class="category-title">{cat_name}</h2>')

        for topic_name, bindings in topics.items():
            cards_lines.append(f'            <div class="topic-group">')
            cards_lines.append(f'                <div class="topic-title">&gt;&gt; {topic_name}</div>')

            for b in bindings:
                # Format the key combination (e.g. "Command + Shift + K")
                parts = b['key'].split(' + ')
                key_html_parts = [f'<kbd>{p}</kbd>' for p in parts]
                key_html = ' <span class="key-plus">+</span> '.join(key_html_parts)

                cards_lines.append(f'                <div class="binding-row">')
                cards_lines.append(f'                    <div class="binding-name">{b["name"]}</div>')
                cards_lines.append(f'                    <div class="binding-key key-combo">{key_html}</div>')
                cards_lines.append(f'                </div>')
            cards_lines.append(f'            </div>')
        cards_lines.append(f'        </div>')
    cards_html = '\n'.join(cards_lines)

    new_html_content = toc_html + '\n' + cards_html + '\n'

    # 4. Inject the new HTML content directly into the existing file
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Regex to match everything from the start of <nav id="toc"> down to the noResults div
    pattern = re.compile(r'(^[ \t]*<nav id="toc">.*?\n)[ \t]*<div class="no-results" id="noResults">', re.DOTALL | re.MULTILINE)

    if pattern.search(html):
        # Substitute the new content while keeping the Search JS and styling intact
        updated_html = pattern.sub(f'{new_html_content}        <div class="no-results" id="noResults">', html, count=1)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(updated_html)
        print("Success! RenoiseKeys.html has been updated with the whitelabel keybindings.")
    else:
        print("Error: Could not find the target HTML structure to replace.")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    update_guide()
