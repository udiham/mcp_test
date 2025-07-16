from PIL import Image, ImageDraw, ImageFont
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JPEG_server")

# Initialize FastMCP server
mcp = FastMCP("JPEG_server",port=10000)

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

@mcp.tool()
def text_to_jpeg(text, filename='output.jpg', width=1280, height=720, font_size=30):
    """
    takes text string and converts it to a JPEG image

    Args:
        text: the contents of the text

    Returns:
        a jpeg image containing the text
    """
    # Create a blank image with white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position
    #text_width, text_height = draw.textsize(text, font=font)
    text_width, text_height = textsize(text, font=font)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw the text on the image
    draw.text((text_x, text_y), text, fill='black', font=font)

    # Save the image as JPEG
    image.save(filename, 'JPEG')
    return image

if __name__ == "__main__":
    #mcp.run()
    mcp.run(transport='sse')