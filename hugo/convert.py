import re
import os
import sys

old_dir = sys.argv[1]
new_dir = sys.argv[2]

files = os.listdir(old_dir)

for f in files:
    if f.endswith('.md'):
        finished_header = False
        m = re.match("(\d{4}-\d{2}-\d{2})-(.*)", f)
        if m is not None:
            extracted_date = m.group(1)
            out_file = m.group(2)
        else: out_file = f
        date_written = False

        with open(old_dir+f, 'r') as in_f:
            with open(new_dir + out_file, 'w') as out_f:
                out_f.write('+++\n')
                lines = in_f.readlines()
                for line in lines:
                    if finished_header:
                        #m = re.match("\{\%\s*githubrepo\s+([a-zA-Z\/]+)\s*\%\}")
                        #if ()
                        # replace "{% speakerdeck 82b209c0f181013106da6eb14261a8ef %}"
                        # with    "{{< speakerdeck 82b209c0f181013106da6eb14261a8ef >}}"
                        def liquid_to_shortcode(m):
                            name = m.group(1)
                            args = m.group(2)
                            if name == "githubrepo":
                                return "[" + args + "](http://github.com/" + args + ")"
                            if name == "vimeo":
                                args = args.split(" ")
                                args[0] = "id=\"" + args[0] + "\""
                                args = " ".join(args)
                            return "{{< " + name + " " + args + ">}}"

                        out_f.write(re.sub(r"\{\%\s+([a-zA-z]+)\s+(.*)\%\}", liquid_to_shortcode, line))
                    elif line.startswith('title: '):
                        _, title = line.split(':', 1)
                        title = title.strip()
                        title = title.replace('"', "'")
                        out_f.write('title = "'+title+'"\n')
                    elif line.startswith('date: '):
                        _, date = line.split(':', 1)
                        date = date.strip()
                        date = date.replace(" ", "T")
                        date = date[:16]
                        out_f.write('date = '+date+'\n')
                        date_written = True
                    elif line.startswith('author: '):
                        continue
                    elif line.startswith('summary: '):
                        continue
                    elif line.startswith('layout: '):
                        continue
                    elif line.startswith('status: '):
                        continue
                    elif line.startswith('slug: '):
                        _, slug = line.split(':', 1)
                        slug = slug.strip()
                        out_f.write('slug = "'+slug+'"\n')
                    elif line.startswith('category: '):
                        _, tags = line.split(':', 1)
                        tags = tags.strip().split(',')
                        tags = ['"'+tag.strip()+'"' for tag in tags]
                        tags = ', '.join(tags)
                        out_f.write('categories = ['+tags+']\n')
                    elif line.startswith('tags: '):
                        out_f.write('type = "post"\n')
                    elif line.strip() == "":
                        if not date_written: out_f.write('date = ' + extracted_date + '\n')
                        out_f.write('draft = "False"\n')
                        out_f.write('+++\n')
                        finished_header = True
                    else:
                        out_f.write(line)

