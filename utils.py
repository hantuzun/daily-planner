import unicode_tex

def escape_for_tex(chars):
	escaped = ''.join(list(map(lambda x : unicode_tex.unicode_to_tex_map.get(x, x), chars)))
	return escaped.replace('\space', ' ')
