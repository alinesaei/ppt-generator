
import time

def process(difficulty, language):
    prompt = """Write a presentation/powerpoint about the user's topic. You only answer with the presentation. Follow the structure of the example.
            Notice
            -You do all the presentation text for the user.
            -You write the texts no longer than 250 characters!
            -You make very short titles!
            -You make the presentation easy to understand.
            -The presentation has a table of contents.
            -The presentation has a summary.
            -At least 8 slides.

            Example! - Stick to this formatting exactly!
            #Title: TITLE OF THE PRESENTATION

            #Slide: 1
            #Header: table of contents
            #Content: 1. CONTENT OF THIS POWERPOINT
            2. CONTENTS OF THIS POWERPOINT
            3. CONTENT OF THIS POWERPOINT
            ...

            #Slide: 2
            #Header: TITLE OF SLIDE
            #Content: CONTENT OF THE SLIDE

            #Slide: 3
            #Header: TITLE OF SLIDE
            #Content: CONTENT OF THE SLIDE

            #Slide: 4
            #Header: TITLE OF SLIDE
            #Content: CONTENT OF THE SLIDE

            #Slide: 5
            #Headers: summary
            #Content: CONTENT OF THE SUMMARY

            #Slide: END"""
    if difficulty == "easy":
            prompt += " Please provide a simple and basic overview.Use simple vocabulary."
    elif difficulty == "medium":
            prompt += " Please provide a detailed overview including key facts and concepts."
    elif difficulty == "hard":
            prompt += " Please provide an in-depth analysis including advantages, disadvantages, and examples with use academic lexical resource."

    if language == 'farsi' : 
            prompt += " language of the content should be farsi"

    return prompt