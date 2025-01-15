from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from textwrap import wrap
import requests
import logging
import base64

app = FastAPI()
def draw_text_lines(startX, startY, endX, endY, lines, font, image):
    draw = ImageDraw.Draw(image)
    y_position = startY
    max_width = endX - startX
    wrapped_lines = wrap(lines, width=80)  # Adjust width as needed

    for line in wrapped_lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        if text_width > max_width:
            sub_lines = wrap(line, width=int(max_width / (text_width / len(line))))
            for sub_line in sub_lines:
                sub_text_bbox = draw.textbbox((0, 0), sub_line, font=font)
                sub_text_width = sub_text_bbox[2] - sub_text_bbox[0]
                x_position = startX + (max_width - sub_text_width) // 2
                draw.text((x_position, y_position), sub_line, fill="#FFFFFF", font=font)
                y_position += text_height + 10
        else:
            x_position = startX + (max_width - text_width) // 2
            draw.text((x_position, y_position), line, fill="#FFFFFF", font=font)
            y_position += text_height + 10

        if y_position > endY:
            break

    return y_position

app.mount("/imgs", StaticFiles(directory="imgs"), name='images')

@app.get("/", response_class=HTMLResponse)
def serve():
    logging.basicConfig(level=logging.INFO)
    img = Image.open('./imgs/images.png')
    I1 = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Regular.ttf", 200)
    I1.text((28, 36), "nice Car", fill=(0, 0, 0), font=font)
    img.save('./imgs/edited_image.png')
    img = Image.open('./imgs/edited_image.png')
    img.show()

@app.get("/trends", response_class=HTMLResponse)
async def overlay_image(request: Request):
    try:
        logging.basicConfig(level=logging.INFO)
        
        y_position = 0
        text = request.query_params.get('text', 'New AI Breakthrough')
        subtext = request.query_params.get('subtext', 'Researchers achieve significant progress in natural language processing')
        funding_amount = request.query_params.get('funding_amount', '')
        website_url = request.query_params.get('website_url', '')
        logo_url = request.query_params.get('logo_url', '')
        
       # image_url = "https://iili.io/2470hrl.png"
        image_url = "https://iili.io/26V1t8G.png"
        
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image = image.convert('RGB')
        draw = ImageDraw.Draw(image)
        
        
        
        heading='Understanding Global Warming: Causes, Effects, and Future Projections'
        SubHeading1=' Primary Causes of Global Warming'
        Desription1= 'Global warming is primarily driven by human activities, namely the burning of fossil fuels, deforestation, and certain agricultural practices. These activities release greenhouse gases like carbon dioxide, methane, and nitrous oxide into the atmosphere, which trap heat and lead to an increase in Earth s average surface temperature.'
        SubHeading2= 'Current and Projected Temperature Increases'
        Description2= 'Since the pre-industrial period, Earth s average temperature has risen by approximately 1 degree Celsius. Currently, the temperature is increasing at a rate of more than 0.2 degrees Celsius per decade. The World Meteorological Organization predicts an 80% chance that global temperatures will surpass 1.5 °C for at least one year between 2024 and 2028.'
        SubHeading3= 'Impacts of Global Warming'
        Descrption3= 'The effects of global warming include significant phenomena such as sea ice loss, melting glaciers, rising sea levels, and extreme weather events like heat waves, droughts, and wildfires. Future scenarios under high emission conditions predict even more severe weather patterns and substantial changes to land surfaces, including desertification and loss of agricultural land.'
        SubHeading4=' Mitigation and Long-term Consequences'
        Descrption4= 'To limit global warming to 1.5°C, it is essential to halve greenhouse gas emissions by 2030 and achieve net-zero emissions by 2050. Even with successful mitigation efforts, some effects, like ocean heating and acidification, will persist for centuries, emphasizing the need for immediate global action to ensure a sustainable future.'
        
    #Loading Fonts
        try:
            headingFont = ImageFont.truetype('WorkSans-Bold.ttf', 50)
            SubHeadingFont=ImageFont.truetype('WorkSans-Bold.ttf', 24)
            descriptionFont=ImageFont.truetype('WorkSans-Regular.ttf',14)
            comfortaa_font_small = ImageFont.truetype('WorkSans-Regular.ttf', 32)
        except IOError:
            logging.warning("Failed to load custom fonts, using default font.")
            headingFont = ImageFont.load_default()
            SubHeadingFont = ImageFont.load_default()
            descriptionFont = ImageFont.load_default()
            comfortaa_font_small = ImageFont.load_default()

        
        # draw.text((28, 36), heading, fill=(0, 0, 0), font=comfortaa_font_large)
        
          # Coordinates of the blue boxes
       # Coordinates of the corners of the rectangular box
        top_left = (1.33*144, 1.31*345)
        top_right = (1.33*473, 1.31*345)
        bottom_left = (1.33*144, 1.31*510)
        bottom_right = (1.33*473, 1.31*510)
         # Calculate the center of the rectangular box
        center_x = (top_left[0] + top_right[0] + bottom_left[0] + bottom_right[0]) // 4
        center_y = (top_left[1] + top_right[1] + bottom_left[1] + bottom_right[1]) // 4
        
        # main_lines = wrap(heading, width=30)
        #Main Lines
        draw_text_lines(50,50,image.size[0]-30,image.size[0]-50,heading,headingFont,image)
        
        # # Calculate the width of the rectangular box
        startX = top_left[0]
        startY = top_left[1]
        endX = top_right[0]
        endY = top_right[1]
        # box_height = bottom_left[1] - top_left[1]
        # box_width = (top_right[0] + top_left[0]) // 2
        
        
        #SubHeading1
        passingY=draw_text_lines(startX+70,startY-10,endX,endY,SubHeading1,SubHeadingFont,image)
        draw_text_lines(startX+70,passingY+20,endX,endY,Desription1,descriptionFont,image)
        
        
        
        
        
        #SubHeading2
        passingY=draw_text_lines(startX+70,startY+360,endX,endY+340,SubHeading2,SubHeadingFont,image)
        draw_text_lines(startX+70,passingY+20,endX,endY,Description2,descriptionFont,image)
       
        
       #SubHeading3
        passingY=draw_text_lines(startX+70,startY+720,endX,endY+720,SubHeading3,SubHeadingFont,image)
        draw_text_lines(startX+70,passingY+20,endX,endY,Descrption3,descriptionFont,image)

        #SubHeading4
        passingY=draw_text_lines(startX+70,startY+1090,endX,endY+1090,SubHeading4,SubHeadingFont,image)
        draw_text_lines(startX+70,passingY+20,endX,endY,Descrption4,descriptionFont,image)
          
        
        image.save('./imgs/edited_image.png')
        image = Image.open('./imgs/edited_image.png')
        image.show()

        # if website_url:
        #     website_text = website_url
        #     text_width, text_height = draw.textsize(website_text, font=comfortaa_font_small)
        #     x_position = (image.size[0] - text_width) // 2
        #     draw.text((x_position, y_position), website_text, fill="#FFFFFF", font=comfortaa_font_small)

        # if funding_amount:
        #     funding_text = "Funding: $ " + funding_amount
        #     amount_y_position = image.size[1] - 300
        #     text_width, text_height = draw.textsize(funding_text, font=comfortaa_font_large)
        #     x_position = (image.size[0] - text_width) // 2
        #     draw.text((x_position, amount_y_position), funding_text, fill="#FFFFFF", font=comfortaa_font_large)

        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        FREEIMAGE_UPLOAD_URL = "https://api.imgbb.com/1/upload"
        params = {
            "key": "daeb1bf2967b2875450375e2ee699c88",
            "image": img_base64
        }
        
        response = requests.post(FREEIMAGE_UPLOAD_URL, data=params)

        if response.status_code == 200:
            link = response.json()["data"]["url"]
            logging.info(f"Image uploaded successfully: {link}")
            image_url = link
        else:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            logging.error(f"Failed to upload image. Error: {error_message}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

#     return f"""
#     <html>
#     <head>
#         <title>Image with Text</title>
#     </head>
#     <body>
#         <h1>Hello World</h1>
#         <img src="{image_url}" alt="Edited Image" style="max-width: 100%; height: 50%;">
#     </body>
# </html>
#     """