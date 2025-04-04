from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import time

class SearchEngine:
    def __init__(self):
        self.model = SentenceTransformer("ml/model")
        self.sentences = np.load("encode/sentences.npy")
        self.index = faiss.read_index("encode/faiss_index.bin")

        # ค่า Top 1
        self.k = 1

    def l2_to_cosine_similarity(self, l2):
        return 1 / (1 + l2)

    def vector_search(self, text_seach):
        start_time = time.time()
        query = self.model.encode([text_seach])
        print("Time to encode:", time.time() - start_time)
        return np.array(query).astype("float32")

    
    def search_model(self, text_search):
        start_time = time.time()
        # ค่าความคล้ายที่สุด
        threshold = 0.9
        best_match = None
        best_similarity = 0

        query = self.vector_search(text_search)
        distances, indices = self.index.search(query, self.k)     # ค้นหา

        # Loop ผลลัพธ์
        for i, dist in zip(indices[0].tolist(), distances[0].tolist()):
            similarity = self.l2_to_cosine_similarity(dist)
            if similarity > threshold and similarity > best_similarity:
                best_match = self.sentences[i]
                best_similarity = similarity

        print("Time to search model:", time.time() - start_time)
        # print("Best Match:", best_match)
        return best_match, best_similarity
    
    def search_contain(self, text_seach, df):
        start_time = time.time()
        match_sn = [sn for sn in df['SerialNumber'] if text_seach in sn]
        print("Time to search contain:", time.time() - start_time)
        return match_sn
    
    # def search_result(self, best_match, best_similarity, df, text_seach):
    #     start_time = time.time()
    #     if best_match:
    #         matched_data = df[df["SerialNumber"] == best_match].to_dict(orient="records")
    #         res = {
    #             "best_similarity": best_similarity,
    #             "detail": matched_data,
    #             "process": "model"
    #         }
    #         print(res)
    #     else:
    #         matched_sn = self.search_contain(text_seach, df)

    #         if matched_sn:
    #             matched_data = df[df["SerialNumber"].isin(matched_sn)].to_dict(orient="records")

    #             if matched_data:
    #                 res = {
    #                     "best_similarity": best_similarity,
    #                     "detail": matched_data,
    #                     "process": "contain"
    #                 }
    #                 print(res)
    #             else:
    #                 print("serial number not found in contain search")
    #         else:
    #             print("serial number not found in model search")
    #     print("Time to search :", time.time() - start_time)
    #     return res

