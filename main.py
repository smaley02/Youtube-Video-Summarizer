import openai
from youtube_transcript_api import YouTubeTranscriptApi

# enter API key here
openai.api_key = ''


def main():
    # get key from youtube video
    # video from: https://www.youtube.com/watch?v=DuDz6B4cqVc
    video_id = 'DuDz6B4cqVc'

    # extract transcript form youtube video
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    input_text = ''
    for transcript in transcript_list:
        input_text += transcript.get('text') + " "

    # count number of input tokens, be sure to leave room for response tokens
    total_tokens = 0
    num_completions = 0
    tokens = 0
    temp = ''
    summaries = []
    for i in input_text:
        total_tokens += 1
        tokens += 1
        temp += i
        if tokens >= 15000 and i == ' ':
            # run a completion call for part of the transcript
            num_completions += 1
            print(f"\n\nCompletion number #{num_completions}:")
            print("\nInput tokens: ", end="")
            print(tokens / 4)
            print("\nTemp input: ")
            print(temp)
            # call to chatgpt api
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system",
                           "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as "
                                      "possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
                          {"role": "user", "content": "Summarize this youtube video" + temp}, ]
            )
            # print response
            print("\nResponse:")
            print(completion.choices[0].message.content)
            total_tokens += completion.usage.completion_tokens
            summaries.append(completion.choices[0].message.content)
            temp = ''
            tokens = 0

    num_completions += 1
    print(f"\n\nCompletion number #{num_completions}")
    print("\nInput tokens: ", end="")
    print(tokens / 4)
    print("\nTemp input: ")
    print(temp)
    # call to chatgpt api
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system",
                   "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as "
                              "possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
                  {"role": "user", "content": "Summarize this youtube video" + temp}, ]
    )
    # print response
    total_tokens += completion.usage.completion_tokens
    print("\nResponse:\n")
    print(completion.choices[0].message.content)
    summaries.append(completion.choices[0].message.content)

    print(f"\nTotal tokens: " + str(total_tokens / 4) + "\n")

    # summarize the summaries
    final_input = ''
    sum_num = 1
    for s in summaries:
        final_input += "Summary #" + str(sum_num) + "\n"
        # print(s)
        final_input += s + "\n"
        sum_num += 1
    print(final_input)

    # create final summary that summarizes the other summaries and makes a list of key terms
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system",
                   "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as "
                              "possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
                  {"role": "user", "content": "Summarize these summaries about a youtube video into one, 300 word "
                                              "summary that explains the key ideas from the video and gives a "
                                              "list of top 2 key terms in the format \"Keyterms: keyterm1, keyterm2\"\n"
                                              + final_input}, ]
    )
    print("\nFinal Response:\n")
    final = completion.choices[0].message.content
    print(final)


if __name__ == '__main__':
    main()

