import openai
import json

openai.api_key = "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"

model = 'text-davinci-003'

class Humanizer:
    @staticmethod
    def humanize(message):
        prompt = f'When it comes to writing content, two factors are crucial, "perplexity" and "burstiness". ' \
                 f'Perplexity measures the complexity of text. Separately, burstiness compares the variations of ' \
                 f'sentences. Humans tend to write with greater burstiness, for example, with some longer or complex ' \
                 f'sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing ' \
                 f'the following content, I am going to ask you to create, I need it to have a good amount of ' \
                 f'perplexity and burstiness. Do you understand?\n\nPrompt 3: Using the concepts written previously, ' \
                 f'rewrite this text with a high degree of perplexity and burstiness: {message} '

        response = openai.Completion.create(
            prompt=prompt,
            model=model,
            max_tokens=1024,
            temperature=0.9
        )

        for result in response.choices:
            return result.text



