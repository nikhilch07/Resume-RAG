from documents import chunk_text
from embeddings import search_similar

def analyze_gaps(jd_text: str, distance_threshold: float = 0.65) -> list[dict]:
    jd_chunks = chunk_text(jd_text, chunk_size=50)   # smaller chunks = more specific requirements per chunk
    
    gap_report = []
    for jd_chunk in jd_chunks:
        best_matches = search_similar(jd_chunk, top_n=1, source_filter="resume")
        
        if not best_matches:
            gap_report.append({"jd_requirement": jd_chunk, "status": "MISSING", "distance": None})
            continue
        
        best_distance = best_matches[0]["distance"]
        status = "GAP" if best_distance > distance_threshold else "COVERED"
        
        gap_report.append({
            "jd_requirement": jd_chunk,
            "status": status,
            "distance": best_distance
        })
    
    return gap_report