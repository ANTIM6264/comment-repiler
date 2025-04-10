import openai
import googleapiclient.discovery

openai.api_key = "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"
YOUTUBE_API_KEY = "AIzaSyA-2lu0dNXRbIfPCSTptQuU2TVruM-Dnd8"

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    return None

def fetch_comments(video_id, max_results=5):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    response = request.execute()

    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)
    return comments

def generate_reply(comment):
    prompt = f"Reply politely to this YouTube comment: \"{comment}\""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60
    )
    return response.choices[0].message.content.strip()