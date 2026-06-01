# RenoiseKeys 🎹

A beautifully formatted, searchable, and printable HTML cheat sheet for [Renoise](https://www.renoise.com/) tracker keyboard shortcuts. 

This repository includes a generic "whitelabel" version using Renoise's default keybindings, an **Alfred Workflow** (for macOS), and a **Python generator script** so you can build a custom guide from your own modified Renoise keybindings!

## Features
* 🎨 **Interactive HTML Guide**: A cyberpunk-themed, searchable, categorised cheat sheet.
* 🖨 **Print-Ready**: Includes CSS optimized for printing a physical copy.
* 🔍 **Alfred Workflow (macOS)**: Instantly search your shortcuts system-wide using the `rk` keyword.
* 🛠 **Customizable**: Feed it *your* custom Renoise keybindings to create a personalized guide.

---

## 🚀 Getting Started (Default Keybindings)

If you use the default Renoise keybindings, you don't need to generate anything! 

1. Simply open `RenoiseKeys.html` in any web browser.
2. Use the search bar at the top to filter for specific shortcuts, or click the categories to jump around.

---

## 🔍 RenoiseKeys for Alfred (macOS)

If you use [Alfred](https://www.alfredapp.com/) on a Mac, you can search your Renoise shortcuts without leaving your workflow!

1. Download or locate the `RenoiseKeys for Alfred.alfredworkflow` file in this repository.
2. Double-click the file to import the workflow into Alfred.
3. Bring up Alfred and type `rk <search term>` (e.g., `rk render pattern`) to instantly find the keyboard shortcut. 
4. Press `Enter` on any result to copy the shortcut directly to your clipboard!

---

## 🛠 Generate Your Own Custom Guide

If you heavily customize your Renoise shortcuts, the default guide won't match your workflow. You can use the included Python script to regenerate the HTML file using your own personal `KeyBindings.xml`.

### Prerequisites
* Python 3 installed on your machine.

### Instructions

1. **Locate your custom `KeyBindings.xml`**
   * **macOS:** `~/Library/Preferences/Renoise/V3.x.x/KeyBindings.xml`
   * **Windows:** `%appdata%\Renoise\V3.x.x\KeyBindings.xml`
   * **Linux:** `~/.renoise/V3.x.x/KeyBindings.xml`
   *(You can also export this directly from within Renoise's preferences).*

2. **Copy the XML file to this folder**
   Place your `KeyBindings.xml` in the same directory as the script.

3. **Update the Python Script**
   Open `generate_guide.py` in a text editor and ensure the `xml_path` matches your file name. If you named it `KeyBindings.xml`, change line 7 to:
   ```python
   xml_path = "KeyBindings.xml"
   ```

4. **Run the Script**
   Open your terminal, navigate to this folder, and run:
   ```bash
   python3 generate_guide.py
   ```

5. **Done!**
   The script will extract all mapped keybindings from your XML file and automatically inject them into `RenoiseKeys.html`. Open the HTML file to see your personalized shortcuts.

---

## 🤝 Contributions
Pull requests are welcome! If you want to improve the HTML/CSS styling or optimize the Python parsing, feel free to fork and submit a PR.
