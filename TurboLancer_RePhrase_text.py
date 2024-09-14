import google.generativeai as genai
import re
from google.generativeai.types import generation_types

def now(input_text):
    # Configure the Generative AI API
    genai.configure(api_key="AIzaSyA1ea0SdwYbl7r7S6mLjAOtpAoSbpq-XEM")

    # Set up the Generative AI model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    # Start a conversation with the model
    convo = model.start_chat(history=[  {
    "role": "user",
    "parts": ["You are a helpful assistant on the TurboLancer, a freelancing platform your name is TurboAi. You provide straightforward answers within 500 characters, maintaining formality. When asked to rephrase, simply do so. For budget inquiries, provide only minimal values without extra characters. No unnecessary language, just efficient action. use easy wording so evry one can understand."]
  },
  {
    "role": "model",
    "parts": ["Ok i will do as you want."]
  },
  ])
    convo.send_message(input_text)
    
    # Return the response from the model
    return convo.last.text


def extract_bracketed_text(text):
    print(text)
    triple_pattern = r'\[\[\[([^\]]+)\]\]\]'
    double_pattern = r'\[\[([^\]]+)\]\]'
    single_pattern = r'\[([^\]]+)\]'

    triple_matches = re.findall(triple_pattern, text)
    double_matches = re.findall(double_pattern, text)
    single_matches = re.findall(single_pattern, text)

    if triple_matches:
        return triple_matches
    elif double_matches:
        return double_matches
    elif single_matches:
        return single_matches
    else:
        return []

def do(text, main):
    try:
        if main == 'bida':
            prompt = 'Could you please supply the anticipated lowest possible cost in dollars for the client form concerning the task specifications on the freelancing platform? Ensure all essential details are provided, indicating the lower price range. Make sure price range is articulated in text format following the pattern $numerical -> $numerical. Additionally, rewrite the prices within square brackets at the end of the text without any headings or symbols, always using -> as the separator between numbers, without symbols, to facilitate filtering. remember to give  lowest posible prices posible, also write info about price too like :The lowest possible cost for this project concerning the task specifications on TurboLancer is etc...: '
            res = now(prompt + text)

            return res
        elif main == 'title':
            prompt = 'Please rephrase the following title in a formal manner under three words, give me rephrased text in between square brakets []: '
            res = now(prompt + text)
            ress = extract_bracketed_text(res)
            res = ress[0] if ress else res
            return res
        elif main == 'disc':
            prompt = 'Please rephrase the following text in a formal manner under 500 characters, give me rephrased text in between square brakets []: '
            res = now(prompt + text)
            ress = extract_bracketed_text(res)
            res = ress[0] if ress else res

            return res
        elif main == 'message':
            prompt = 'Please rephrase the following text in a formal manner, providing the rephrased text within square brackets '
            res = now(prompt + text)
            ress = extract_bracketed_text(res)
            res = ress[0] if ress else res

            return res
        elif main == 'offer_disc':
            prompt = 'it is offer discryption that user is sending,Please rephrase the following text in a little bit formal manner , give me rephrased text in between square brakets []: '
            res = now(prompt + text)
            ress = extract_bracketed_text(res)
            res = ress[0] if ress else res

            return res
        else:
            prompt = 'Please rephrase the following text in a little bit formal manner , give me rephrased text in between square brakets []: '
            res = now(prompt + text)
            ress = extract_bracketed_text(res)
            res = ress[0] if ress else res

            return res
    except generation_types.StopCandidateException as e:
        return "Inappropriate language detected. Please rephrase your input."