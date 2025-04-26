import pandas as pd
import json
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from .api_integrations import APIIntegrations

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", cache_embeddings: bool = True):
        """Initialize RAG pipeline with specified embedding model"""
        try:
            self.model = SentenceTransformer(embedding_model)
            self.api = APIIntegrations()
            self.cache_embeddings = cache_embeddings
            self._embedding_cache = {}
            logger.info(f"Initialized RAGPipeline with model: {embedding_model}")
        except Exception as e:
            logger.error(f"Failed to initialize RAGPipeline: {e}")
            raise

    def semantic_search(self, 
                       query: str, 
                       data_source: str, 
                       top_k: int = 3, 
                       filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Perform semantic search on the specified data source with optional filters"""
        try:
            data, descriptions = self._get_data_and_descriptions(data_source, filters)
            if not descriptions:
                logger.warning(f"No descriptions found for data source: {data_source}")
                return []
            
            matches = self._get_top_matches(query, descriptions, data, top_k)
            logger.info(f"Found {len(matches)} matches for query in {data_source}")
            return matches
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []

    def _get_data_and_descriptions(self, 
                                 data_source: str, 
                                 filters: Optional[Dict]) -> Tuple[List[Dict], List[str]]:
        """Get data and descriptions for the specified source"""
        if data_source == "jobs":
            data = self.api.fetch_job_listings(filters=filters)
            descriptions = [
                f"{item['job_title']} at {item['company']} in {item['location']} ({item['industry']})"
                for item in data if self._validate_job_item(item)
            ]
        elif data_source == "sessions":
            data = self.api.fetch_events()
            descriptions = [
                f"{item['title']} - {item['description']}"
                for item in data if self._validate_session_item(item)
            ]
        elif data_source == "mentorship":
            data = self.api.fetch_mentorship_programs(filters=filters)
            descriptions = [
                f"{item['title']} - {item['description']}"
                for item in data if self._validate_mentorship_item(item)
            ]
        else:
            raise ValueError(f"Unknown data source: {data_source}")
            
        return data, descriptions

    def _validate_job_item(self, item: Dict) -> bool:
        """Validate job listing item"""
        required_fields = ['job_title', 'company', 'location', 'industry']
        return all(item.get(field) for field in required_fields)

    def _validate_session_item(self, item: Dict) -> bool:
        """Validate session item"""
        return item.get('title') and item.get('description')

    def _validate_mentorship_item(self, item: Dict) -> bool:
        """Validate mentorship program item"""
        return item.get('title') and item.get('description')

    def _get_top_matches(self, 
                        query: str, 
                        descriptions: List[str], 
                        data: Any, 
                        top_k: int) -> List[Dict[str, Any]]:
        """Get top matching results based on semantic similarity"""
        try:
            # Get or compute query embedding
            cache_key = f"query_{hash(query)}"
            query_embedding = (self._embedding_cache.get(cache_key) if self.cache_embeddings 
                            else self.model.encode(query, convert_to_tensor=True))
            
            if self.cache_embeddings and cache_key not in self._embedding_cache:
                self._embedding_cache[cache_key] = query_embedding

            # Get or compute corpus embeddings
            corpus_key = f"corpus_{hash(str(descriptions))}"
            corpus_embeddings = (self._embedding_cache.get(corpus_key) if self.cache_embeddings 
                               else self.model.encode(descriptions, convert_to_tensor=True))
            
            if self.cache_embeddings and corpus_key not in self._embedding_cache:
                self._embedding_cache[corpus_key] = corpus_embeddings

            # Calculate similarities and get top matches
            similarities = np.inner(query_embedding, corpus_embeddings)
            top_k = min(top_k, len(descriptions))
            top_indices = similarities.argsort()[-top_k:][::-1]

            # Return results based on data type
            if isinstance(data, pd.DataFrame):
                return [data.iloc[i].to_dict() for i in top_indices]
            return [data[i] for i in top_indices]

        except Exception as e:
            logger.error(f"Error in getting top matches: {e}")
            return []

    def retrieve_information(self, query: str, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Main method to retrieve information based on user query"""
        try:
            query = query.lower()
            keywords = {
                "jobs": ["job", "career", "position", "work", "employment", "hiring"],
                "sessions": ["session", "workshop", "training", "event", "webinar"],
                "mentorship": ["mentor", "guidance", "program", "coaching", "advice"]
            }

            # Try to find best matching source
            for source, terms in keywords.items():
                if any(term in query for term in terms):
                    result = self.semantic_search(query, source, filters=filters)
                    if result:
                        return {"source": source, "data": result}

            # Return combined results if no specific match
            logger.info("No specific source match found, returning combined results")
            return {
                "source": "combined",
                "data": {
                    "jobs": self.semantic_search(query, "jobs", top_k=1, filters=filters),
                    "sessions": self.semantic_search(query, "sessions", top_k=1),
                    "mentorship": self.semantic_search(query, "mentorship", top_k=1, filters=filters)
                }
            }

        except Exception as e:
            logger.error(f"Error in retrieve_information: {e}")
            return {"source": "error", "data": []}