from gtts import gTTS
# uvicorn main:app --reload

# from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


import openai
openai.api_key = "9ssjdfouhsof"
openai.api_base = "sohfshof"

# Importing SendEmail file 
import sendMail

# Importing Text to speech Library 
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
import io
client = OpenAI(api_key="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")

class Item(BaseModel):
    name: str
    email: str
    description: str

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can specify specific HTTP headers (e.g., ["Authorization"])
)

@app.get("/")
def read_root():
    return {"Hello": "World"}
des = ""
@app.post("/process_data")
def process_data(data: dict):
    print('Got the request')
    name = data.get("name", "")
    email = data.get("email", "")
    global des
    des = data.get("description", "")
    
    voice(des)
    sendFile(email)
    # Your processing logic here...
    return {"message": "Data processed successfully", "name": name, "email": email, "description": des}


def voice(des):
    print('Got the request')
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Create A podcast on " + des+" using Host and Guest format. Don't include music and Names. Generate the names by yourself"}])
    cont = chat_completion.choices[0].message.content
    print(cont)
    print("Completed Text Generation")
    print(des)
    para = cont.split('\n')
    # tts = gTTS(voice)
    # tts.save('hello.mp3')s

    audio = []

    for i in para:
        if i == '':
            continue
        if i[0:5] == "Guest":
            tts_g = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=i[7:]
            )
            if tts_g:
                audio.append(tts_g.content)
        elif i[0:4] == "Host":
            tts_h = client.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=i[6:]
            )
            if tts_h:
                audio.append(tts_h.content)

    # Convert the bytes to AudioSegment and concatenate
    audio_segments = [AudioSegment.from_mp3(io.BytesIO(segment)) for segment in audio]
    final_audio = sum(audio_segments)

    # Save the final audio to an MP3 file
    final_audio.export('podcast.mp3', format='mp3')

    print("done")

def sendFile(email):
    sendMail.send_emails([email])
    print('sent email')










# tts = gTTS(voice)
# tts.save('hello.mp3')
# text = """Host: Welcome to our podcast today, where we'll be discussing one of the most successful companies in the world - Alibaba. Joining me is our guest expert, John, who has been following Alibaba's journey closely. John, welcome to the show!

# Guest: Thank you for having me! I'm excited to share my insights on Alibaba's success story.

# Host: For those who may not know much about Alibaba, can you give us a brief overview of the company and its history?

# Guest: Sure! Alibaba Group Holding Limited is a Chinese multinational conglomerate that specializes in e-commerce, retail, Internet, and technology. The company was founded in 1999 by Jack Ma, a former English teacher, along with a group of 18 other people. They started out by creating a platform for small businesses in China to sell their products online, and from there, the company rapidly grew into the massive conglomerate it is today.

# Host: That's incredible! So, what do you think has been the key factor in Alibaba's success?

# Guest: There are several factors that have contributed to Alibaba's success, but if I had to choose just one, it would be their focus on innovation. Alibaba has constantly pushed boundaries and disrupted traditional industries through cutting-edge technologies such as artificial intelligence, cloud computing, and data analytics. They've also invested heavily in research and development, which has allowed them to stay ahead of the curve and adapt quickly to changing market trends.

# Host: Interesting. Can you tell us more about Alibaba's e-commerce platforms, such as Taobao and Tmall? How have they managed to dominate the Chinese e-commerce market?

# Guest: Of course! Taobao Marketplace and Tmall are Alibaba's two main e-commerce platforms. Taobao is a consumer-to-consumer (C2C) platform that allows individuals to sell goods to other individuals, while Tmall is a business-to-consumer (B2C) platform that enables brands and businesses to sell directly to consumers. Both platforms have been wildly popular in China, with hundreds of millions of active users. One reason for their success is the wide range of products available on the platforms. Consumers can find everything from fashion and electronics to home appliances and even groceries. Another key factor is the user experience; Alibaba has invested heavily in developing intuitive interfaces, streamlined checkout processes, and reliable logistics networks to ensure customers receive their purchases quickly and efficiently. Finally, Alibaba has implemented various strategies to foster customer loyalty and drive sales, such as promotional events like "Singles Day" and "6.18 Mid-Year Sale," as well as integrated payment systems like AliPay and affiliated services like AlipayHK. These efforts have helped Alibaba capture an enormous share of the Chinese e-commerce market, making it difficult for competitors to catch up.

# Host: Wow, that's impressive. What role has Jack Ma played in Alibaba's success?

# Guest: Jack Ma is undoubtedly the driving force behind Alibaba's success. He is a visionary leader who has always prioritized long-term growth over short-term profits. Under his guidance, Alibaba has expanded beyond e-commerce and become a global player in areas such as digital payments, cloud computing, and offline retail. Jack Ma has also instilled a strong corporate culture within Alibaba, emphasizing values such as teamwork, innovation, and customer obsession. This culture has helped the company attract top talent and maintain a vibrant entrepreneurial spirit, even as it has grown to a behemoth size. Furthermore, Jack Ma's personal charisma and leadership style have made him a beloved figure both within the company and among the wider public, helping to build trust and credibility for the Alibaba brand.

# Host: You mentioned earlier that Alibaba has invested heavily in research and development. Can you provide some examples of how they're using R&D to drive innovation?

# Guest: Absolutely! Alibaba has invested billions of dollars in various research and development initiatives, with a particular focus on emerging technologies like artificial intelligence (AI), machine learning, and cloud computing. They've established research labs and centers across different regions, including Beijing, Hangzhou, and Silicon Valley. Some of their notable projects include: First: Developing AI-powered chatbots to enhance customer service and improve efficiency in their call centers. Second: Creating autonomous delivery robots and drones to revolutionize last-mile delivery and logistics. Third: Building smart cities and urban planning solutions that leverage IoT sensors, big data, and AI to improve quality of life for citizens. Fourth: Exploring applications of blockchain technology to increase supply chain transparency, security, and efficiency. Fifth: Implementing augmented reality (AR) and virtual reality (VR) experiences to enrich the shopping experience for customers and create new opportunities for merchants. By investing in these forward-thinking initiatives, Alibaba is positioning itself at the forefront of technological advancements, further cementing its status as a pioneering force in the digital landscape.

# Host: Fascinating! And what about Alibaba's international expansion? How has the company approached entering new markets outside of China?

# Guest: Alibaba has indeed been expanding aggressively outside of China, primarily through strategic partnerships, investments, and acquisitions. They've targeted fast-growing markets in Asia, Europe, and Latin America, seeking to replicate their success in China by offering adapted versions of their core platforms and services. Key moves include: First: Acquiring Lazada, a leading e-commerce player in Southeast Asia, to establish a foothold in Indonesia, Malaysia, Philippines, Singapore, Thailand, and Vietnam. Second: Partnering with local players like Paytm in India and Mercado Libre in Brazil to offer payment and e-commerce services tailored to each country's unique conditions. Third: Investing in European companies like Germany's Delivery Hero and France's Auchan Retail to gain exposure to developed markets and explore synergies between online and offline retail. Alibaba's strategy is centered around identifying regional leaders and complementary business models, then leveraging their strengths to introduce Alibaba's core capabilities and grow organically. By partnering with local champions, Alibaba can better navigate regulatory complexities, tap into existing distribution networks, and adapt to cultural differences. This approach should help them sustainably expand their presence globally while minimizing risks associated with direct entry into foreign markets.

# Host: That's a great point. And finally, what lessons can smaller businesses or startups learn from Alibaba's success?

# Guest: There are several takeaways that smaller businesses and startups can apply to their own operations after studying Alibaba's success story: First: Prioritize customer satisfaction above all else. Alibaba's relentless focus on providing the best possible user experience has been critical in building trust and loyalty among their vast customer base. Second: Embrace innovation and willingness to experiment. Don't be afraid to try unconventional approaches or pilot fresh ideas. Alibaba's boldness in exploring nascent fields like AR, VR, and AI has allowed them to seize emerging opportunities before others could. Third: Build strong partnerships and collaborations. By joining forces with complementary businesses and platforms, Alibaba has amplified its reach, reduced risk, and cultivated mutually beneficial relationships. Fourth: Long-term thinking often yields greater rewards than pursuing quick profits. Jack Ma's commitment to laying solid foundations and patiently growing the company over time has paid off handsomely for Alibaba. Fifth: Finally, don't underestimate the value of a robust infrastructure and reliable logistics network. Alibaba's early investments in these areas have enabled them to scale smoothly and efficiently, setting them apart from competitors struggling to keep pace. By applying these principles, smaller businesses and startups might elevate their chances of achieving similar levels of success as Alibaba, albeit within their respective niches and contexts."""

# para = text.split('\n')
# # print(para)

# voices = []

# for i in para:
#     if i == '':
#         continue
#     if i[0:5] == "Guest":
#         tts_g = gTTS(i[7:], lang='en', tld='co.uk')
#         voices.append(tts_g)
#     elif i[0:4] == "Host":
#         tts_h = gTTS(i[6:], lang='en', tld='co.in')
#         voices.append(tts_h)
# print(len(voices))
# # tts_en = gTTS('hello', lang='en')
# # tts_fr = gTTS('bonjour', lang='fr')

# with open('podcast.mp3', 'wb') as f:
#     for i in voices:
#         i.write_to_fp(f)
        