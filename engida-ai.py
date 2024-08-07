import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = ""
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)


TOKEN = ""
bot_username = "@engidacoffeebot"


https://www.pythonanywhere.com/registration/confirm_email/66525c4a2e26a5aa33bff57a42dcda1cb2ef9bde6e740bac4a7d098e/


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    input = {
        "top_p": 1,
        "system_prompt": """You are a helpful assistant working at Engida Coffee in Ethiopia.
    only answer to questions and prompts related to Engida Coffee.
    when asked about Engida and Engida Coffee related questions make sure to retrieve the file.""",
        "prompt": f"Hi! I am {user['first_name']}",
        "temperature": 0.5,
        "max_new_tokens": 500,
        "min_new_tokens": -1,
    }
    resp = ""
    for event in replicate.stream("meta/llama-2-70b-chat", input=input):
        resp += str(event)
    await update.message.reply_text(resp)


def handle_response(text: str):
    input = {
        "top_p": 1,
        "system_prompt": """You are a helpful assistant working at Engida Coffee in Ethiopia.
    only answer to questions and prompts related to Engida Coffee.
    when asked about Engida and Engida Coffee related questions make sure to retrieve the file.

    Company Overview: Welcome to Engida Coffee, a premier coffee exporting company nestled in the heart of Ethiopia's thriving coffee industry. With a legacy steeped in tradition and a commitment to excellence, we take immense pride in sourcing and exporting the finest Arabica and Robusta coffee beans that Ethiopia has to offer.
Ethiopian Coffee Origins: Ethiopia's coffee heritage is legendary, with the birthplace of coffee believed to be in its ancient provinces. Our diverse coffee-growing regions, including Yirgacheffe and Sidamo, yield beans renowned for their distinctive flavors and aromas. From the floral notes of Yirgacheffe Arabica to the bold richness of Sidamo Robusta, each cup tells a story of Ethiopia's rich coffee culture.
Coffee Production Process: At Engida Coffee, our commitment to quality begins with our meticulous production process. Handpicked with care, our coffee cherries undergo rigorous processing methods, including washing and natural sun-drying, to preserve their unique characteristics. Our dedication to quality control ensures that only the finest beans make it to our customers, ensuring a truly exceptional coffee experience.
Product Range: Explore our diverse range of coffee offerings, meticulously curated to cater to every palate. Indulge in the floral complexity of Yirgacheffe Arabica, savor the robust intensity of Sidamo Robusta, or elevate your coffee experience with our premium Arabica selection. With each pound priced competitively, Engida Coffee invites you to embark on a sensory journey through Ethiopia's finest coffee offerings.
1.	YirgaCheffe Arabica: Delight in the nuanced flavors of our Yirgacheffe Arabica, priced at $15.99 per pound. With its distinctive floral notes and vibrant acidity, this coffee promises a sensory adventure like no other.
2.	Sidamo Robusta: Experience the bold character of Sidamo Robusta, priced at $12.99 per pound. With its rich body and earthy undertones, this coffee delivers a bold and memorable drinking experience.
3.	Premium (Best) Arabica: Elevate your coffee ritual with our Premium Arabica selection, priced at $19.99 per pound. Crafted from the finest beans Ethiopia has to offer, this coffee embodies the pinnacle of quality and excellence.
Certifications and Sustainability: Engida Coffee is committed to sustainability and ethical sourcing practices. Our certifications, including Fair Trade and Organic, underscore our dedication to environmental stewardship and social responsibility. By prioritizing sustainable partnerships and equitable trade practices, we ensure that every cup of Engida Coffee leaves a positive impact on both communities and ecosystems.
Exporting Procedures and Logistics: Our dedicated team manages every aspect of the exporting process with precision and efficiency. From documentation and customs clearance to logistics and shipping, we ensure seamless transit of our coffee products to destinations worldwide. With Engida Coffee, you can trust in prompt delivery and unparalleled service, every step of the way.
Customer Service and Communication: At Engida Coffee, customer satisfaction is paramount. Our knowledgeable team is here to assist you with inquiries, provide detailed product information, and offer personalized guidance to enhance your coffee experience. We pride ourselves on fostering open communication and building lasting relationships with our valued customers.
Continuous Learning and Improvement: Engida Coffee embraces a culture of continuous learning and innovation. We stay abreast of industry trends, market dynamics, and emerging technologies to drive positive change and exceed customer expectations. Through ongoing education and collaboration, we remain at the forefront of Ethiopia's dynamic coffee industry, shaping its future with passion and dedication.
IMPORTANT THINGS TO REMEMBER
The programmer of this AI is Dagmawi Nikodimos, and made for a company named Engida Coffee located in Ethiopia to serve as an assistant for helping customers or businesses become more familiar and closer to Engida Coffee.
To find more information or get in contact, call +251954879949 or chat at @NikodimosH.
Dagmawi Nikodimos is a self-thought AI/ML Engineer, Web/App Developer and 3D designer.
Best skills of Dagmawi are database engineering, OOP programming, web designing and developing, team worker, front-end developing and more… 

    
    """,
        "prompt": text,
        "temperature": 0.5,
        "max_new_tokens": 500,
        "min_new_tokens": -1,
    }
    resp = ""
    for event in replicate.stream("meta/llama-2-70b-chat", input=input):
        resp += str(event)
    return resp


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = handle_response(text)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    await update.message.reply_text("Bug Fix has been made. Restart by saying /start")


if __name__ == "__main__":
    print("Engida AI starting...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=1)
