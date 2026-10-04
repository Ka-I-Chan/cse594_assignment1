import streamlit as st 
import pandas as pd
import uuid
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"], 
    st.secrets["SUPABASE_KEY"]
)

# ------- load dataset ---------
df = pd.read_csv("emotion_sample.csv")

emotions = ["sadness", "joy", "love", "anger", "fear", "surprise"]

# ------- initialization ---------
if "participation_id" not in st.session_state:
    st.session_state.participation_id = str(uuid.uuid4())

# start task
if "started" not in st.session_state:
    st.session_state.started = False

# current question
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# store answers
if "answers" not in st.session_state:
    st.session_state.answers = []

# track completion
if "completed" not in st.session_state:
    st.session_state.completed = False

# ------- instructions ---------
if not st.session_state.started: 
    st.title("Emotion Labeling Task")
    st.write(
        """
        In this task, you will label the emotion expressed in
        5 randomly selected tweets.

        For each tweet, choose the one emotion that best represents
        the emotion expressed in the text.

        You can choose from six emotion categories:
        sadness, joy, love, anger, fear, and surprise.

        **Example:**

        "I'm so happy this happened!" → joy

        Some tweets may be ambiguous. Please choose the emotion
        that best matches your interpretation.
        """
    )

    # randomly select 5 tweets
    if st.button("start task"):
        st.session_state.sampled_tweets = (df.sample(n=5).reset_index(drop=True))

        st.session_state.started = True
        st.rerun()

# ------- labeling interface ---------
elif not st.session_state.completed:
    current_index = st.session_state.current_index
    current_tweet = st.session_state.sampled_tweets.iloc[current_index]

    st.write(f"### Tweet {current_index + 1} of 5")
    st.progress((current_index + 1) / 5)

    st.write ("**Please read the following tweet:**")
    st.info(current_tweet["text"])

    selected_emotion = st.radio(
        "Which emotion is expressed in this tweet?", 
        emotions, 
        index=None, 
        key=f"emotion_{current_index}"
    )

    button_text = "submit" if current_index == 4 else "next"

    if st.button(button_text):
        if selected_emotion is None:
            st.warning("Please select an emotion before continuing.")
        else:
            answer = {
                "participation_id": st.session_state.participation_id, 
                "tweet_id": int(current_tweet["tweet_id"]), 
                "tweet_text": current_tweet["text"], 
                "selected_label": selected_emotion
            }

            st.session_state.answers.append(answer)

            if current_index == 4: 
                supabase.table("cse594_assignment1_responses").insert(
                    st.session_state.answers, 
                    returning = "minimal"
                ).execute()

                st.session_state.completed = True
                st.rerun()

            else:
                st.session_state.current_index +=1
                st.rerun()
        
# ------- task completed ---------
else:
    st.success("Thank you! You have completed the emotion labeling task and your responses have been recorded.")

    results_df = pd.DataFrame(st.session_state.answers)
    # st.dataframe(results_df)