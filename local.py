from transformers import pipeline

pipe = pipeline("text-generation", model="DiscoResearch/DiscoLM_German_7b_v1")
pipe.save_pretrained("./models/")
