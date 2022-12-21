from pptx import Presentation
#import aspose.slides as slides

file_path = "230 - O Little Town of Bethlehem.pptx"
save_file = "hold.pptx"

# p = slides.Presentation(file_path)
verse_set = [str(i) for i in range(1, 10, 1)]

"""
# Instantiate a Presentation object that represents a PPTX file
pres = slides.Presentation(file_path)
# Saving the PPTX presentation to PPTX format
pres.save(save_file, slides.export.SaveFormat.PPTX)
"""

prs = Presentation(file_path)

# text_runs will be populated with a list of strings,
# one for each text run in presentation
text_runs = []

for slide in prs.slides:
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                text_runs.append(run.text)

line = ""
for t in text_runs:
    if t[0] in verse_set and t[1] == '.':
        print(line)
        print("[===]")
        line = t[3:]
    elif line == "":
        line = t
    else:
        line = line + " " + t
print(line)