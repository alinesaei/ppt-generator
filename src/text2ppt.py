from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
import src.addphoto as addphoto
import re
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN


#Create a new PowerPoint presentation
def presentate(defined_list, save_as, color,  title, author):
    prs = Presentation()

    def add_slide(prs, layout, title, subtitle):
        slide = prs.slides.add_slide(layout)
        slide.shapes.title.text = title.strip()
        slide.placeholders[1].text=subtitle
        font = slide.shapes.title.text_frame.paragraphs[0].font
        font.name = 'Arial'
        font.size = Pt(30)
        font.bold = True
        font.italic = False
        for x in  slide.placeholders[1].text_frame.paragraphs:
            font1= x.font
            font1.name = 'Arial'
            font1.size = Pt(16)
            font1.bold = False
            font1.italic = False
        return slide
    
    def add_slide1(prs, layout, title, subtitle):
        slide = prs.slides.add_slide(layout)
        slide.shapes.title.text = title.strip()
        slide.placeholders[1].text=subtitle
        font = slide.shapes.title.text_frame.paragraphs[0].font
        font.name = 'Arial'
        font.size = Pt(30)
        font.bold = True
        font.italic = False
        for x in  slide.placeholders[1].text_frame.paragraphs:
            font1= x.font
            font1.name = 'Arial'
            font1.size = Pt(16)
            font1.bold = False
            font1.italic = False
        return slide

    def add_slide_img(prs, layout, img_path):
        slide = prs.slides.add_slide(layout)
        img_path =  ""+img_path
        left =  Inches(1.10)
        top = Inches(0.7)
        width = Inches(8)
        height = Inches(6)
        pic = slide.shapes.add_picture(img_path, left, top, width, height)

    def add_title_slide(prs, prs_title, author):
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)

        title = slide.shapes.title
        title.text = prs_title
        title.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER  # Center align the title

        # Modify the font properties for the title
        title_font = title.text_frame.paragraphs[0].runs[0].font
        title_font.bold = True
        title_font.name = 'Arial'
        title_font.size = Pt(40)  # Adjust the font size as desired

        subtitle = slide.placeholders[1]
        subtitle.text = author

        # Modify the font properties for the author name
        author_font = subtitle.text_frame.paragraphs[0].runs[0].font
        author_font.color.rgb = RGBColor(0, 0, 0)  # Set the author name color (black in this case)
        author_font.bold = False
        author_font.name = 'Arial'
        author_font.size = Pt(20)  # Adjust the font size as desired

    def add_two_content_slide(prs, title, content_text, picture_path):
        slide_layout = prs.slide_layouts[3]  # Use layout number 3 (Two Content)
        slide = prs.slides.add_slide(slide_layout)

        shapes = slide.shapes
        title_shape = shapes.title
        content_shape = shapes.placeholders[1]
        picture_placeholder = shapes.placeholders[2]

        title_shape.text = title
        content_shape.text = content_text

        # Set the position and size of the picture placeholder
        left = Inches(5)  # Adjust the position as desired
        top = Inches(1)  # Adjust the position as desired
        width = Inches(4)  # Adjust the size as desired
        height = Inches(5)  # Adjust the size as desired
        picture = picture_placeholder.insert_picture(picture_path)
        picture.left = left
        picture.top = top
        picture.width = width
        picture.height = height
        

    title_slide_layout = prs.slide_layouts[1]
    title_slide_layimg=prs.slide_layouts[6]

    for d in defined_list:
        d["Summary"] = [re.sub(r'\d+\.\s+', '', item).strip() for item in d["Summary"] if re.sub(r'\d+\.\s+', '', item).strip()]

    for i in range (0,len(defined_list)):
        add_title_slide(prs, title, author)
        slide = add_slide(prs, title_slide_layout, defined_list[i]["Topic"],"\n".join(defined_list[i]["Summary"][0:len(defined_list[i]["Summary"])//2]))
        slide = add_slide(prs, title_slide_layout, defined_list[i]["Topic"],"\n".join(defined_list[i]["Summary"][len(defined_list[i]["Summary"])//2:]))
        #slide = add_slide1(prs, title_slide_layout, "Code Snippet For "+defined_list[i]["Topic"],defined_list[i]["Code"])
        try:
            slide2 = add_slide_img(prs,title_slide_layimg,"images/"+addphoto.get_images(defined_list[i]["Topic"],1)[0])
        except:
            slide2 = add_slide_img(prs,title_slide_layimg,"images/"+addphoto.get_images(defined_list[i]["Topic"],1)[1])
        addphoto.empty_images()

    rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    background_color = RGBColor(rgb_color[0], rgb_color[1], rgb_color[2])
    
    for slide in prs.slides:
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = background_color

    prs.save(f"{save_as}.pptx")

