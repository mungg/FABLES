import json

with open("data/FABLES.json", "r") as f:
    data = json.load(f)

# get FABLE data
data = data['FABLES']

# change this or select from data.keys()
book_key = "Flawless"
book_key_list = data.keys()

# getting model list for a given book
model_key = "GPT-4"
model_key_list = data[book_key].keys()

# getting summary data generated by 'GPT-4' for a given book
summary = data[book_key][model_key]["summary"]

# getting general comments of human annotations for a given book and model
general_comment = data[book_key][model_key]['general_comment']

# getting human annotations of each claim given book and model
claims = data[book_key][model_key]['claims']
for idx, claim_data in claims.items():
    print("Claim: ", claim_data['claim'])   # Claim generated from summary
    print("Is it faithful?: ", claim_data['label']) # Label of faithfulness
    print("Evidence: ", claim_data['evidence']) # Evidence that either support or contradict claim
    print("Reason: ", claim_data['reason']) # Reason of label
