from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
import src.addphoto as addphoto
import re
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import random
import re
import requests
import io


def create_ppt(text_file, design_number, ppt_name, author):
    prs = Presentation(f"Designs/Design-{design_number}.pptx")
    slide_master = prs.slide_masters[0]
    slide_count = 0
    header = ""
    content = ""
    last_slide_layout_index = -1
    firsttime = True
    with open(text_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
                            
            if line.startswith('#Title:'):
                header = line.replace('#Title:', '').strip()
                slide = prs.slides.add_slide(prs.slide_layouts[0])
                title = slide.shapes.title
                title.text = header
                subtitle = slide.placeholders[1]
                subtitle.text = author
                body_shape = slide.shapes.placeholders[1]
                continue
            elif line.startswith('#Slide:'):
                if slide_count > 0:
                    slide = prs.slides.add_slide(prs.slide_layouts[slide_layout_index])
                    title = slide.shapes.title
                    title.text = header
                    body_shape = slide.shapes.placeholders[slide_placeholder_index]
                    tf = body_shape.text_frame
                    tf.text = content
                    if slide_layout_index == 8:
                        placeholder = slide.placeholders[1]
                        query = f'{ppt_name} {header}'
                        picture = placeholder.insert_picture("images/"+addphoto.get_images(query,1)[0])
                        addphoto.empty_images()
                        # image_url = addphoto.search_pexels_images(ppt_name)
                        # if image_url is not None:
                        #     # download the image
                        #     image_data = requests.get(image_url).content
                        #     # load image into BytesIO object
                        #     image_stream = io.BytesIO(image_data)
                        #     picture = placeholder.insert_picture(image_stream)
                    # if slide_layout_index == 7:
                    #     placeholder = slide.placeholders[1]
                    #     picture = placeholder.insert_picture('Sample.png')
                    

                content = "" 
                slide_count += 1
                slide_layout_index = last_slide_layout_index
                layout_indices = [1, 7, 8] 
                while slide_layout_index == last_slide_layout_index:
                    if firsttime == True:
                        slide_layout_index = 1
                        slide_placeholder_index = 1
                        firsttime = False
                        break
                    slide_layout_index = random.choice(layout_indices) # Select random slide index
                    if slide_layout_index == 8:
                        slide_placeholder_index = 2
                    else:
                        slide_placeholder_index = 1

                last_slide_layout_index = slide_layout_index
                continue

            elif line.startswith('#Header:'):
                header = line.replace('#Header:', '').strip()
                
                continue

            elif line.startswith('#Content:'):
                content = line.replace('#Content:', '').strip()
                next_line = f.readline().strip()
                while next_line and not next_line.startswith('#'):
                    content += '\n' + next_line
                    next_line = f.readline().strip()
                continue
                

    prs.save(f'GeneratedPresentations/{ppt_name}.pptx')
    
