from core.loader import DataLoader
from core.cleaner import DataCleaner
from core.mapper import DataMapper
from core.deduplicator import Deduplicator
from core.merger import Merger
from services.report import ReportService
import pandas as pd

class Pipeline:

    def __init__(self):
        self.loader = DataLoader()
        self.cleaner = DataCleaner()
        self.mapper = DataMapper()
        self.deduper = Deduplicator()
        self.merger = Merger()
        self.report = ReportService()

    def run(self, files, mapping):
        df = self.loader.load(files)
        df_clean = self.cleaner.clean(df)

        df_mapped = self.mapper.apply(df_clean, mapping)

        groups = self.deduper.group(df_mapped)

        merged = [self.merger.merge_group(g) for g in groups]

        result_df = pd.DataFrame(merged)

        result_df = result_df.dropna(how="all")

        report = self.report.generate(df_mapped, result_df)

        return df_mapped, result_df, report, groups