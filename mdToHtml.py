import os
import markdown
import re
import shutil

ANKI_MEDIA = "/home/alderson/.local/share/Anki2/main/collection.media/"
IMAGES_PATH = "/home/alderson/Apps/obsidian/main/3. Resources/_Images"

def process_brackets(text):
  hr_pattern = re.compile(r'^(?P<hr>\*{3,})$', re.MULTILINE)
  hr_lines = hr_pattern.findall(text)
  text = hr_pattern.sub('-HRLINE-', text)
  bracket_pattern = re.compile(r'\[\[([^\]]+)\]\]')
  parts = text.split('**')

  def replace_inside(match):
    content = match.group(1)
    if '|' in content:
      return content.split('|', 1)[1]
    else:
      return content

  def replace_outside(match):
    content = match.group(1)
    if '|' in content:
      return f"**{content.split('|', 1)[1]}**"
    else:
      return f"**{content}**"

  for i in range(len(parts)):
    if i % 2 == 1:
      # Inside bold
      parts[i] = bracket_pattern.sub(replace_inside, parts[i])
    else:
      # Outside bold
      parts[i] = bracket_pattern.sub(replace_outside, parts[i])

  result = '**'.join(parts)

  for hr in hr_lines:
    result = result.replace('-HRLINE-', hr, 1)

  return result

def convert_obsidian_links(md_content):
  obsidian_image_pattern = r"!\[\[([^\]]+)\]\]"

  def replacement(match):
    content = match.group(1)
    parts = content.split('|', 1)
    image_name = parts[0].strip()

    if image_name.lower().endswith('.excalidraw'):
      return ''

    full_image_path = os.path.join(IMAGES_PATH, image_name)
    no_spaces_name = re.sub(r"\s", "_", image_name)

    try:
        shutil.copy(full_image_path, os.path.join(ANKI_MEDIA, no_spaces_name))
    except Exception as _:
        return ''

    return f'\n ![{no_spaces_name}]({no_spaces_name})'

  return re.sub(obsidian_image_pattern, replacement, md_content)

def replace_latex_syntax(md_content):
    block_math_pattern = r"\$\$(.*?)\$\$"
    md_content = re.sub(block_math_pattern, r"\\\\[\1\\\\]", md_content, flags=re.DOTALL)

    inline_math_pattern = r"\$(.*?)\$"
    md_content = re.sub(inline_math_pattern, r"\\\\(\1\\\\)", md_content)

    return md_content


def convert_to_html(fullPath):
    with open(fullPath, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    md_content = convert_obsidian_links(md_content)
    md_content = process_brackets(md_content)
    md_content = replace_latex_syntax(md_content)

    md_content = md_content.split("---")[2]

    html_content = markdown.markdown(md_content)

    return html_content
