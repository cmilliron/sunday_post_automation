from pptx import Presentation

file_path = "resources/powerpoints/218 - It Came upon the Midnight Clear.pptx"
verse_set = [str(i) for i in range(1, 10, 1)]

# save_file = "hold.pptx"
# p = slides.Presentation(file_path)
# text_runs will be populated with a list of strings,
# one for each text run in presentation


def slides_to_test(presentation):
    text_runs = []
    for slide in presentation.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    print(run.text)
                    text_runs.append(run.text)
    return text_runs


def text_to_openlp(text):
    line = ""
    for t in text:
        if t[0] in verse_set and t[1] == '.':
            print(line)
            print("[===]")
            line = t[3:]
        elif line == "":
            line = t
        else:
            line = line + " " + t
    return line


if __name__ == "__main__":
    prs = Presentation(file_path)
    prs_text = slides_to_test(prs)
    print(text_to_openlp(prs_text))