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
    wrapped_lines = wrap(lines, width=80)

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
                draw.text((x_position, y_position), sub_line, fill="#000000", font=font)
                y_position += text_height + 10
        else:
            x_position = startX + (max_width - text_width) // 2
            draw.text((x_position, y_position), line, fill="#000000", font=font)
            y_position += text_height + 10

        if y_position > endY:
            break

    return y_position


@app.get("/trends", response_class=HTMLResponse)
async def overlay_image_1(request: Request):
    try:
        heading = request.query_params.get('heading', 'Understanding Global Warming: Causes, Effects, and Future Projections')
        SubHeading1 = request.query_params.get('SubHeading1', 'Researchers achieve significant progress in natural language processing')
        Desription1 = request.query_params.get('Desription1', 'Global warming is primarily driven by human activities, namely the burning of fossil fuels, deforestation, and certain agricultural practices. These activities release greenhouse gases like carbon dioxide, methane, and nitrous oxide into the atmosphere, which trap heat and lead to an increase in Earth s average surface temperature.')
        SubHeading2 = request.query_params.get('SubHeading2', 'Current and Projected Temperature Increases')
        Desription2 = request.query_params.get('Desription2', 'Since the pre-industrial period, Earth s average temperature has risen by approximately 1 degree Celsius. Currently, the temperature is increasing at a rate of more than 0.2 degrees Celsius per decade. The World Meteorological Organization predicts an 80% chance that global temperatures will surpass 1.5 °C for at least one year between 2024 and 2028.')
        SubHeading3 = request.query_params.get('SubHeading3', 'Impacts of Global Warming')
        Desription3 = request.query_params.get('Desription3', 'The effects of global warming include significant phenomena such as sea ice loss, melting glaciers, rising sea levels, and extreme weather events like heat waves, droughts, and wildfires. Future scenarios under high emission conditions predict even more severe weather patterns and substantial changes to land surfaces, including desertification and loss of agricultural land.')
        SubHeading4 = request.query_params.get('SubHeading4', 'Mitigation and Long-term Consequences')
        Desription4 = request.query_params.get('Desription4', 'To limit global warming to 1.5°C, it is essential to halve greenhouse gas emissions by 2030 and achieve net-zero emissions by 2050. Even with successful mitigation efforts, some effects, like ocean heating and acidification, will persist for centuries, emphasizing the need for immediate global action to ensure a sustainable future.')
        #SubHeading5 = request.query_params.get('SubHeading5', 'Researchers achieve significant progress in natural language processing')
        #Desription5 = request.query_params.get('Desription5', '')
        heading_color = request.query_params.get('heading_color', 150)
        sub_heading_color = request.query_params.get('sub_heading_color', 80)
        description_color = request.query_params.get('description_color', 50)
        image_url = request.query_params.get('image_url', 'imgs/temp_5_steps_litz.jpg')
        
        if image_url.startswith("http"):
            # If the image URL is an HTTP link, download it
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
        else:
            # Otherwise, treat it as a local file path
            image = Image.open(image_url)

        image = image.convert('RGB')

        try:
            headingFont = ImageFont.truetype('fonts/Acme.woff2', heading_color)
            SubHeadingFont=ImageFont.truetype('fonts/Acme.woff2', sub_heading_color)
            descriptionFont=ImageFont.truetype('fonts/Acme.woff2',description_color)
        except IOError:
            headingFont = ImageFont.load_default()
            SubHeadingFont = ImageFont.load_default()
            descriptionFont = ImageFont.load_default()


        top_left = (1.33*144, 1.31*345)
        top_right = (5*473, 6*1000)
        #bottom_left = (1.33*144, 1.31*510)
        #bottom_right = (1.33*473, 1.31*510)
         # Calculate the center of the rectangular box
        #center_x = (top_left[0] + top_right[0] + bottom_left[0] + bottom_right[0]) // 4
        #center_y = (top_left[1] + top_right[1] + bottom_left[1] + bottom_right[1]) // 4
        
        # main_lines = wrap(heading, width=30)
        #Main Lines
        draw_text_lines(200,200,image.size[0]-200,image.size[0]-200,heading,headingFont,image)
        
        # # Calculate the width of the rectangular box
        startX = 0#top_left[0]
        startY = 0#top_left[1]
        endX = 2500#top_right[0]
        endY = 6000#top_right[1]
                
        #SubHeading1
        passingY=draw_text_lines(startX+500,startY+1500,endX-300,endY+1000,SubHeading1,SubHeadingFont,image)
        draw_text_lines(startX+500,passingY+100,endX-300,endY,Desription1,descriptionFont,image)
        
        
        #SubHeading2
        passingY=draw_text_lines(startX+70,startY+2500,endX-600,endY,SubHeading2,SubHeadingFont,image)
        draw_text_lines(startX+70,passingY+100,endX-600,endY,Desription2,descriptionFont,image)
       
        
        #SubHeading3
        passingY=draw_text_lines(startX+500,startY+3500,endX-300,endY,SubHeading3,SubHeadingFont,image)
        draw_text_lines(startX+500,passingY+100,endX-300,endY,Desription3,descriptionFont,image)

        #SubHeading4
        passingY=draw_text_lines(startX+70,startY+4500,endX-600,endY,SubHeading4,SubHeadingFont,image)
        draw_text_lines(startX+70,passingY+100,endX-600,endY,Desription4,descriptionFont,image)
        
        #SubHeading5
        passingY=draw_text_lines(startX+500,startY+5500,endX-300,endY,SubHeading3,SubHeadingFont,image)
        draw_text_lines(startX+500,passingY+100,endX-300,endY,Desription3,descriptionFont,image)

        
        image.save('./imgs/edited_image.png')
        image = Image.open('./imgs/edited_image.png')
        image.show()
        return 
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        print("Test")
        FREEIMAGE_UPLOAD_URL = "https://api.imgbb.com/1/upload"
        params = {
            "key": "11b1e818e3238dc36d4cc8e769e75da9",
            "image": img_base64
        }
        
        response = requests.post(FREEIMAGE_UPLOAD_URL, data=params)

        if response.status_code == 200:
            link = response.json()["data"]["url"]
            logging.info(f"Image uploaded successfully: {link}")
            image_url = link
            return image_url
        else:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            logging.error(f"Failed to upload image. Error: {error_message}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5005)