from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd
import numpy as np
import faiss

pd.set_option("display.max_colwidth", 1000)


tokenizer = AutoTokenizer.from_pretrained('facebook/contriever-msmarco')
contriever = AutoModel.from_pretrained('facebook/contriever-msmarco')


def cos_sim_2d(x, y):
    norm_x = x / np.linalg.norm(x, axis=1, keepdims=True)
    norm_y = y / np.linalg.norm(y, axis=1, keepdims=True)
    return np.matmul(norm_x, norm_y.T)


# Mean pooling
def mean_pooling(token_embeddings, mask):
    token_embeddings = token_embeddings.masked_fill(
        ~mask[..., None].bool(), 0.)
    sentence_embeddings = token_embeddings.sum(
        dim=1) / mask.sum(dim=1)[..., None]
    return sentence_embeddings


def get_text(
    query: str,
    device: str = None,
    wiki_sentence_path: str = "wikipedia-en-sentences.parquet",
    indexpath: str = 'knn.index',
    k=5
) -> str:

    output = []

    if device is not None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    contriever.to(device)
    my_index = faiss.read_index(
        indexpath, faiss.IO_FLAG_MMAP | faiss.IO_FLAG_READ_ONLY)
    df_sententces = pd.read_parquet(wiki_sentence_path, engine='fastparquet')
    my_index = faiss.read_index(
        indexpath, faiss.IO_FLAG_MMAP | faiss.IO_FLAG_READ_ONLY)
    inputs = tokenizer([query], padding=True, truncation=True,
                       return_tensors="pt").to(device)

    outputs = contriever(**inputs)
    embeddings = mean_pooling(outputs[0], inputs['attention_mask'])

    query_vector = np.asarray(
        embeddings .cpu().detach().numpy()).reshape(1, 768)

    # print(query_vector.shape)

    distances, indices = my_index.search(query_vector, k)

    for i, (dist, indice) in enumerate(zip(distances[0], indices[0])):

        text = str(df_sententces.iloc[[indice]]['text_snippet'])
        # get embedding of neighboring 3-sentence segments
        try:
            inputs = tokenizer([str(df_sententces.iloc[[indice-1]]['text_snippet']), str(df_sententces.iloc[[indice]]['text_snippet']), str(
                df_sententces.iloc[[indice+1]]['text_snippet'])], padding=True, truncation=True, return_tensors="pt").to(device)
            outputs = contriever(**inputs)
            embeddings = mean_pooling(outputs[0], inputs['attention_mask'])
            embeddings = np.asarray(embeddings .cpu().detach().numpy())

            if cos_sim_2d(embeddings[0].reshape(1, 768), embeddings[1].reshape(1, 768)) > 0.7:
                text = str(df_sententces.iloc[[indice-1]]['text_snippet']) + \
                    " " + str(df_sententces.iloc[[indice]]['text_snippet'])

            if cos_sim_2d(embeddings[0].reshape(1, 768), embeddings[1].reshape(1, 768)) > 0.7:
                text += str(df_sententces.iloc[[indice+1]]['text_snippet'])
            out = {
                'i': i,
                'text': text
            }
            output.append(out)

        except:
            pass

    return output
