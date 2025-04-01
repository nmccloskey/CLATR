import os
import logging
logger = logging.getLogger("CustomLogger")
from utils.OutputManager import OutputManager
from data.preprocessing import preprocess_text
from analyses.graphemes import analyze_graphemes
from analyses.lexicon import analyze_lexicon
from analyses.morphology import analyze_morphology
from analyses.syntax import analyze_syntax
from analyses.phonology import analyze_phonology
from analyses.semantics import analyze_semantics
from analyses.mechanics import analyze_mechanics


# Section configuration: mapping section name to analysis function + raw table structure
SECTION_CONFIG = {

    "preprocessing": (
        preprocess_text,
        {
            "preprocessed": [
                "sample_data", "sample_text"
            ]
        }
    ),

    "graphemes": (
        analyze_graphemes,
        {
            "grapheme_stats": [
                "grapheme_basic_specs", "grapheme_counts", "grapheme_props",
                "grapheme_modes", "word_counts", "word_props"
            ]
        }
    ),
    
    "lexicon": (
        analyze_lexicon, 
        {
            "lex_measures": [
                "freqs_cleaned", "freqs_tokenized", "richness_cleaned",
                "richness_tokenized", "named_entities"
            ]
        }
    ),
    
    "morphology": (
        analyze_morphology,
        {
            "morph_stats": [
                "morpheme_basic_specs", "morph_tag_counts", "morph_tag_props", "morph_tags_commonest",
                 "morph_tag_sets_commonest", "pos_tag_counts", "pos_tag_props", "pos_tags_commonest"
            ]
        }
    ),
    
    "syntax": (
        analyze_syntax,
        {
            "syntax_measures": [
                "syn_trees", "dep_tag_counts", "dep_tag_props", "dep_tags_commonest", "tree_comp"
            ]
        }
    ),
    
    "phonology": (
        analyze_phonology,
        {
            "phoneme_stats": [
                "syllable_stats", "phoneme_basic_specs", "phoneme_counts", "phoneme_props", "phoneme_commonest",
                "phon_feature_counts", "phon_feature_props", "word_lens_counts", "word_lens_props"
            ]
        }
    ),
    
    "semantics": (
        analyze_semantics,
        {
            "semantic_data": [
                "unit_sim", "NRCLex", "VADER", "TextBlob", "Afinn", "topics"
            ]
        }
    ),
    
    "mechanics": (
        analyze_mechanics,
        {
            "errors": [
                "lg_tool"
            ]
        }
    )
}


class PipelineManager:
    """
    Manages initialization of analysis sections and their configuration.
    """
    def __init__(self, OM: OutputManager):
        self.om = OM
        self.sentence_level = OM.config.get("sentence_level", False)
        self.visualize = OM.visualize
        self.dep_trees = OM.config.get("dep_trees", False)
        self.granularities = ["doc", "sent"] if self.om.config.get("sentence_level", False) else ["doc"]
        self.sections = {}  # section_name: Analysis instance
        self._init_analyses(SECTION_CONFIG)
        self.analyses = {k for k in self.sections if self.om.sections.get(k, False)}

    def _init_analyses(self, section_dict):
        for section, (func, table_structure) in section_dict.items():
            if section == "preprocessing" or self.om.sections.get(section, False):
                analysis = Analysis(self.om, section, self.granularities)
                analysis.func = func
                analysis.table_bases = table_structure
                self.sections[section] = analysis
    
    def run_preprocessing(self):
        return self.sections["preprocessing"].func(self)

    def run_section(self, section, sample_data):
        # self.sections[section].create_raw_data_tables()
        return self.sections[section].func(self, sample_data)

    def get_fact_table_name(self):
        return "sample_text_sent" if self.sentence_level else "sample_text_doc"

    def get_sample_data(self, doc_id):
        fact_table = self.get_fact_table_name()
        sample_data = self.om.tables[fact_table].get_data(filters={"doc_id":doc_id})
        if self.sentence_level: # and section != "mechanics":
            sample_data = sample_data.sort_values(by='sent_id').to_dict(orient="records")
        else:
            sample_data = sample_data.to_dict(orient="records")[0]
        return sample_data


class Analysis:
    """
    Represents a single analysis section (e.g., graphemes), with associated functions and table schemas.
    """
    def __init__(self, OM: OutputManager, name: str, granularities: list):
        self.om = OM
        self.name = name
        self.func = None
        self.granularities = granularities
        self.table_bases = {}  # file_name_base: [table_name_bases]

    def create_raw_data_tables(self, tags=["raw"]):
        """
        Creates OutputManager tables for raw data per granularity.

        Args:
            tags (list): Tags to attach to each table.
        """
        pks = {"doc": ["doc_id"], "sent": ["doc_id", "sent_id"]}

        for file_base, table_list in self.table_bases.items():
            for gran in self.granularities:
                for table in table_list:
                    table_name = f"{table}_{gran}"
                    file_name = f"{file_base}_{gran}.xlsx"
                    self.om.create_table(
                        name=table_name,
                        sheet_name=table,
                        section=self.name,
                        subdir=self.name,
                        file_name=file_name,
                        primary_keys=pks[gran]
                    )
                    t = self.om.tables[table_name]
                    t.granularity = gran
                    t.family = file_base
                    t.source_fn = self.func.__name__
                    t.granularity = gran
                    if table in ["sample_text", "sample_data"]:
                        if table == "sample_text":
                            t.fact = True
                        if table == "sample_data":
                            t.tags.append("grouping")
                    else:
                        t.tags = tags
                        t.fact_table = f"sample_text_{gran}"
                        t.grouping_table = f"sample_data_{gran}"
                    if self.name not in ["preprocessing", "mechanics"]:
                        t.file_path = os.path.join(t.file_path, gran)
                        t.subdir = os.path.join(t.subdir, gran)

    def init_results_dict(self):
        """
        Builds initial result structure for all raw tables, keyed by granularity.

        Returns:
            dict: {table_name: [] or {}} based on granularity
        """
        results = {}
        for table_names in self.table_bases.values():
            for gran in self.granularities:
                for table in table_names:
                    key = f"{table}_{gran}"
                    results[key] = [] if gran == "sent" else {}
        return results
