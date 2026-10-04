from datasets import load_dataset
import pandas as pd


ds = load_dataset("dair-ai/emotion", "unsplit")

# print(ds)
# print(ds["train"][:5])
# print(ds["train"].features["label"].names)

train_df = ds["train"].to_pandas()
# print(train_df.head())
# print(train_df["label"].value_counts())
# 0-sadness; 1-joy; 2-love; 3-anger; 4-fear; 5-surprise


# sample 10 cases for each emotion to set up a dataset 
sampled_emotion = []
for label in range(6):
    emotion = train_df[train_df["label"] == label].sample(n=10, random_state=8)
    sampled_emotion.append(emotion)

sampled_df = pd.concat(sampled_emotion)
# print(sampled_df["label"].value_counts())

label_names = ["sadness", "joy", "love", "anger", "fear", "surprise"]
sampled_df["emotion"] = sampled_df["label"].apply(lambda x: label_names[x])

sampled_df = sampled_df.reset_index(drop=True)
sampled_df["tweet_id"] = sampled_df.index + 1

sampled_df = sampled_df[
    ["tweet_id", "text", "label", "emotion"]
]
print(sampled_df.head())

sampled_df.to_csv("emotion_sample.csv", index=False)